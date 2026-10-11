"""Read-only project inspection for lightweight design and accessibility audits.

The scanner deliberately uses only the Python standard library. It never executes
project code, follows symlinks, makes network requests, or writes into the target
project. Findings are heuristics, not a substitute for browser or assistive
technology testing.
"""

from __future__ import annotations

import os
import re
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

from ..utils.color_utils import contrast_ratio, hex_to_rgb, rgb_to_hex

SUPPORTED_EXTENSIONS = {".css", ".html", ".htm", ".vue", ".svelte"}
HTML_EXTENSIONS = {".html", ".htm"}
IGNORED_DIRECTORIES = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "vendor",
    "dist",
    "build",
    "coverage",
    "out",
    "target",
    "storybook-static",
    "storybook-build",
    "playwright-report",
    "test-results",
    ".next",
    ".nuxt",
    ".output",
    ".svelte-kit",
    "__pycache__",
}
MAX_FILE_BYTES = 1_000_000
MAX_TOTAL_BYTES = 20_000_000
MAX_FINDINGS = 200
MAX_RETURNED_CUSTOM_PROPERTIES = 500
MAX_RETURNED_COLOR_TOKENS = 200
MAX_TOKEN_VALUE_CHARS = 500
HEX_RE = re.compile(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b")
RGB_RE = re.compile(
    r"rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})(?:\s*,\s*([\d.]+))?\s*\)",
    re.IGNORECASE,
)
CSS_RULE_RE = re.compile(r"([^{}]+)\{([^{}]*)\}", re.DOTALL)
CSS_VAR_RE = re.compile(r"(--[\w-]+)\s*:\s*([^;{}]+)")
CSS_COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)


def _strip_css_comments(source: str) -> str:
    """Replace comments with whitespace while preserving source line numbers."""
    return CSS_COMMENT_RE.sub(
        lambda match: "".join("\n" if character == "\n" else " " for character in match.group()),
        source,
    )


class _MarkupParser(HTMLParser):
    """Collect a small, useful subset of HTML semantics without a DOM dependency."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.images: List[Dict[str, Any]] = []
        self.controls: List[Dict[str, Any]] = []
        self.interactive: List[Dict[str, Any]] = []
        self.labels_for: set[str] = set()
        self.ids: set[str] = set()
        self.duplicate_ids: List[Tuple[str, int]] = []
        self.nested_label_controls: set[int] = set()
        self.headings: List[Tuple[int, int]] = []
        self.has_main = False
        self.has_html_root = False
        self.has_document_title = False
        self.has_document_language = False
        self._inside_head = False
        self._inside_title = False
        self._active_text: List[Dict[str, Any]] = []
        self._label_stack: List[Dict[str, Any]] = []

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        attrs_map = {name.lower(): (value or "") for name, value in attrs}
        line = self.getpos()[0]
        element_id = attrs_map.get("id", "")
        if element_id:
            if element_id in self.ids:
                self.duplicate_ids.append((element_id, line))
            self.ids.add(element_id)

        if tag == "main":
            self.has_main = True
        if tag == "html":
            self.has_html_root = True
            self.has_document_language = self.has_document_language or bool(attrs_map.get("lang", "").strip())
        if tag == "head":
            self._inside_head = True
        if tag == "title" and self._inside_head:
            self._inside_title = True
        if re.fullmatch(r"h[1-6]", tag):
            self.headings.append((int(tag[1]), line))
        if tag == "img":
            self.images.append({"attrs": attrs_map, "line": line})
            alt_text = attrs_map.get("alt", "").strip()
            if alt_text:
                for item in self._active_text:
                    item["text"] += f" {alt_text}"

        if tag == "label":
            label = {"for": attrs_map.get("for", ""), "text": ""}
            self._label_stack.append(label)
            if label["for"]:
                self.labels_for.add(label["for"])

        if tag in {"input", "select", "textarea"}:
            if not (tag == "input" and attrs_map.get("type", "").lower() == "hidden"):
                control = {
                    "tag": tag,
                    "attrs": attrs_map,
                    "line": line,
                    "label_index": len(self.controls),
                }
                self.controls.append(control)
                if self._label_stack:
                    self.nested_label_controls.add(control["label_index"])

        if tag in {"button", "a"}:
            interactive = {"tag": tag, "attrs": attrs_map, "line": line, "text": ""}
            self.interactive.append(interactive)
            self._active_text.append(interactive)

    def handle_startendtag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_data(self, data: str) -> None:
        if self._inside_title and data.strip():
            self.has_document_title = True
        text = data.strip()
        if not text:
            return
        for item in self._active_text:
            item["text"] += f" {text}"
        for label in self._label_stack:
            label["text"] += f" {text}"

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._inside_title = False
        if tag == "head":
            self._inside_head = False
        if tag in {"button", "a"}:
            for index in range(len(self._active_text) - 1, -1, -1):
                if self._active_text[index]["tag"] == tag:
                    self._active_text.pop(index)
                    break
        if tag == "label" and self._label_stack:
            self._label_stack.pop()

    def close(self) -> None:
        super().close()


def _finding(
    code: str,
    category: str,
    severity: str,
    confidence: str,
    message: str,
    recommendation: str,
    path: str,
    line: Optional[int] = None,
    evidence: Optional[str] = None,
    criterion: Optional[str] = None,
) -> Dict[str, Any]:
    result: Dict[str, Any] = {
        "code": code,
        "category": category,
        "severity": severity,
        "confidence": confidence,
        "message": message,
        "recommendation": recommendation,
        "source": {"path": path, "line": line},
    }
    if evidence:
        result["evidence"] = evidence[:300]
    if criterion:
        result["wcag_criterion"] = criterion
    return result


def _read_project_files(root: Path, max_files: int) -> Tuple[List[Tuple[Path, str]], Dict[str, int]]:
    files: List[Tuple[Path, str]] = []
    skipped_large = 0
    skipped_unreadable = 0
    skipped_symlink = 0
    truncated = False
    byte_limit_reached = False
    total_bytes_read = 0

    for current, directories, filenames in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        directories[:] = sorted(
            name
            for name in directories
            if name not in IGNORED_DIRECTORIES
            and not name.startswith(".")
            and not (current_path / name).is_symlink()
        )
        for filename in sorted(filenames):
            path = current_path / filename
            if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue
            if path.is_symlink():
                skipped_symlink += 1
                continue
            if len(files) >= max_files:
                truncated = True
                break
            try:
                file_size = path.stat().st_size
                if file_size > MAX_FILE_BYTES:
                    skipped_large += 1
                    continue
                remaining_bytes = MAX_TOTAL_BYTES - total_bytes_read
                if file_size > remaining_bytes:
                    byte_limit_reached = True
                    break
                with path.open("rb") as file_handle:
                    contents = file_handle.read(min(MAX_FILE_BYTES, remaining_bytes) + 1)
                if len(contents) > MAX_FILE_BYTES:
                    skipped_large += 1
                    continue
                if len(contents) > remaining_bytes:
                    byte_limit_reached = True
                    break
                source = contents.decode("utf-8-sig", errors="replace")
            except OSError:
                skipped_unreadable += 1
                continue
            files.append((path, source))
            total_bytes_read += len(contents)
        if truncated or byte_limit_reached:
            break

    return files, {
        "skipped_large_files": skipped_large,
        "skipped_unreadable_files": skipped_unreadable,
        "skipped_symlinks": skipped_symlink,
        "file_limit_reached": int(truncated),
        "byte_limit_reached": int(byte_limit_reached),
        "total_bytes_read": total_bytes_read,
    }


def _parse_declarations(body: str) -> Dict[str, str]:
    declarations: Dict[str, str] = {}
    for declaration in body.split(";"):
        if ":" not in declaration:
            continue
        name, value = declaration.split(":", 1)
        name = name.strip().lower()
        value = value.strip()
        if name and value:
            declarations[name] = value
    return declarations


def _extract_css_rules(source: str) -> List[Dict[str, Any]]:
    without_comments = _strip_css_comments(source)
    rules: List[Dict[str, Any]] = []
    previous_end = 0
    current_line = 1
    for match in CSS_RULE_RE.finditer(without_comments):
        current_line += without_comments.count("\n", previous_end, match.start())
        raw_selector = match.group(1)
        leading_whitespace = len(raw_selector) - len(raw_selector.lstrip())
        line = current_line + raw_selector[:leading_whitespace].count("\n")
        current_line += without_comments.count("\n", match.start(), match.end())
        previous_end = match.end()
        selector = raw_selector.strip()
        if selector.startswith("@"):
            continue
        rules.append(
            {
                "selector": selector,
                "declarations": _parse_declarations(match.group(2)),
                "line": line,
            }
        )
    return rules


def _resolve_css_vars(value: str, variables: Dict[str, str]) -> str:
    resolved = value
    for _ in range(6):
        match = re.search(r"var\(\s*(--[\w-]+)\s*(?:,\s*([^)]*))?\)", resolved)
        if not match:
            break
        replacement = variables.get(match.group(1), match.group(2) or "")
        resolved = resolved[: match.start()] + replacement + resolved[match.end() :]
    return resolved.strip()


def _css_color_to_hex(value: str, variables: Dict[str, str]) -> Optional[str]:
    resolved = _resolve_css_vars(value.strip(), variables)
    resolved = re.sub(r"\s*!important\s*$", "", resolved, flags=re.IGNORECASE).strip()
    if re.search(r"(?:gradient|url)\s*\(", resolved, re.IGNORECASE):
        return None
    if re.search(r"\b(?:transparent|currentcolor|inherit|initial|unset)\b", resolved, re.IGNORECASE):
        return None

    hex_match = HEX_RE.fullmatch(resolved)
    if hex_match:
        try:
            red, green, blue = hex_to_rgb(hex_match.group(0))
        except ValueError:
            return None
        return rgb_to_hex(red, green, blue)

    rgb_match = RGB_RE.fullmatch(resolved)
    if rgb_match:
        channels = [int(channel) for channel in rgb_match.groups()[:3]]
        alpha_value = rgb_match.group(4)
        try:
            alpha = float(alpha_value) if alpha_value is not None else 1.0
        except ValueError:
            return None
        if all(0 <= channel <= 255 for channel in channels) and alpha >= 1:
            return rgb_to_hex(*channels)
        return None

    named = {"black": "#000000", "white": "#ffffff"}
    return named.get(resolved.lower())


def _truncate_token_value(value: str) -> str:
    if len(value) <= MAX_TOKEN_VALUE_CHARS:
        return value
    return value[: MAX_TOKEN_VALUE_CHARS - 3] + "..."


def _extract_tokens(css_sources: Sequence[Tuple[str, str]]) -> Dict[str, Any]:
    variables: Dict[str, str] = {}
    colors: Counter[str] = Counter()
    font_families: Counter[str] = Counter()
    spacing: Counter[str] = Counter()
    radii: Counter[str] = Counter()
    shadows: Counter[str] = Counter()
    token_sources: Dict[str, str] = {}

    for relative_path, source in css_sources:
        clean = _strip_css_comments(source)
        for match in CSS_VAR_RE.finditer(clean):
            name, value = match.group(1).strip(), match.group(2).strip()
            if name.startswith("--") and value:
                variables[name] = value
                token_sources[name] = relative_path
        for rule in _extract_css_rules(source):
            declarations = rule["declarations"]
            for key in ("color", "background", "background-color", "border-color", "outline-color", "fill", "stroke"):
                value = declarations.get(key)
                if value:
                    color = _css_color_to_hex(value, variables)
                    if color:
                        colors[color] += 1
            family = declarations.get("font-family")
            if family:
                font_families[family.strip()] += 1
            for key in ("margin", "margin-top", "margin-right", "margin-bottom", "margin-left", "padding", "padding-top", "padding-right", "padding-bottom", "padding-left", "gap", "row-gap", "column-gap"):
                value = declarations.get(key)
                if value:
                    spacing[value.strip()] += 1
            radius = declarations.get("border-radius")
            if radius:
                radii[radius.strip()] += 1
            shadow = declarations.get("box-shadow")
            if shadow and shadow.lower() != "none":
                shadows[shadow.strip()] += 1

    sorted_variables = sorted(variables.items())
    color_token_items = [
        (name, value)
        for name, value in sorted_variables
        if any(key in name.lower() for key in ("color", "bg", "background", "surface", "text", "border", "accent", "primary", "secondary"))
    ]
    custom_properties = {
        name: _truncate_token_value(value)
        for name, value in sorted_variables[:MAX_RETURNED_CUSTOM_PROPERTIES]
    }
    color_tokens = {
        name: {
            "value": _truncate_token_value(value),
            "source": token_sources.get(name),
            "resolved_color": _css_color_to_hex(value, variables),
        }
        for name, value in color_token_items[:MAX_RETURNED_COLOR_TOKENS]
    }
    return {
        "custom_properties": custom_properties,
        "custom_properties_total": len(sorted_variables),
        "custom_properties_truncated": len(sorted_variables) > MAX_RETURNED_CUSTOM_PROPERTIES,
        "color_tokens": color_tokens,
        "color_tokens_total": len(color_token_items),
        "color_tokens_truncated": len(color_token_items) > MAX_RETURNED_COLOR_TOKENS,
        "repeated_colors": [
            {"value": value, "occurrences": count}
            for value, count in colors.most_common(20)
            if count > 1
        ],
        "font_families": [
            {"value": value, "occurrences": count} for value, count in font_families.most_common(20)
        ],
        "spacing_values": [
            {"value": value, "occurrences": count} for value, count in spacing.most_common(30)
        ],
        "border_radii": [
            {"value": value, "occurrences": count} for value, count in radii.most_common(20)
        ],
        "box_shadows": [
            {"value": value, "occurrences": count} for value, count in shadows.most_common(20)
        ],
    }


def _extract_style_sources(files: Sequence[Tuple[Path, str]], root: Path) -> List[Tuple[str, str]]:
    styles: List[Tuple[str, str]] = []
    for path, source in files:
        relative = path.relative_to(root).as_posix()
        if path.suffix.lower() == ".css":
            styles.append((relative, source))
        elif path.suffix.lower() in {".vue", ".svelte"}:
            for match in re.finditer(r"<style\b[^>]*>(.*?)</style\s*>", source, re.IGNORECASE | re.DOTALL):
                start_line = source.count("\n", 0, match.start(1))
                styles.append((relative, "\n" * start_line + match.group(1)))
    return styles


def _analyze_markup(path: str, source: str, findings: List[Dict[str, Any]]) -> Dict[str, Any]:
    parser = _MarkupParser()
    try:
        parser.feed(source)
        parser.close()
    except Exception:
        return {"images": 0, "controls": 0, "interactive": 0, "headings": 0}

    if parser.has_html_root and not parser.has_document_language:
        findings.append(
            _finding(
                "document-language-missing",
                "accessibility",
                "high",
                "high",
                "html要素にページの主言語を示すlang属性がありません。",
                "html要素に適切なBCP 47言語タグを設定してください (例: lang=\"ja\" または lang=\"en\")。",
                path,
                criterion="WCAG 3.1.1",
            )
        )
    if parser.has_html_root and not parser.has_document_title:
        findings.append(
            _finding(
                "document-title-missing",
                "accessibility",
                "high",
                "high",
                "HTML文書に空でないtitle要素を検出できません。",
                "ページの主題を簡潔に説明するtitle要素をhead内に追加してください。",
                path,
                criterion="WCAG 2.4.2",
            )
        )

    for duplicate_id, line in parser.duplicate_ids:
        findings.append(
            _finding(
                "duplicate-id",
                "semantics",
                "medium",
                "high",
                f"id属性 {duplicate_id!r} が同じHTML文書内で重複しています。",
                "各要素に一意のidを付け、labelやARIA参照先が意図した要素を指すようにしてください。",
                path,
                line,
                evidence=f"id={duplicate_id}",
            )
        )

    for image in parser.images:
        attrs = image["attrs"]
        if "alt" not in attrs:
            findings.append(
                _finding(
                    "image-alt-missing",
                    "accessibility",
                    "high",
                    "high",
                    "画像にalt属性がありません。",
                    "画像の目的を伝えるaltを追加してください。装飾画像ならalt=\"\"を指定してください。",
                    path,
                    image["line"],
                    criterion="WCAG 1.1.1",
                )
            )

    for item in parser.interactive:
        attrs = item["attrs"]
        labelled_by = attrs.get("aria-labelledby", "").split()
        missing_references = [reference for reference in labelled_by if reference not in parser.ids]
        if missing_references:
            findings.append(
                _finding(
                    "aria-labelledby-target-missing",
                    "accessibility",
                    "medium",
                    "high",
                    "aria-labelledbyが参照するidが見つかりません: " + ", ".join(missing_references),
                    "同じHTML文書内に参照先のidを追加するか、正しいidへ更新してください。",
                    path,
                    item["line"],
                    criterion="WCAG 4.1.2",
                )
            )
        has_name = bool(
            item["text"].strip()
            or attrs.get("aria-label", "").strip()
            or attrs.get("aria-labelledby", "").strip()
            or attrs.get("title", "").strip()
            or attrs.get("value", "").strip()
        )
        if not has_name:
            findings.append(
                _finding(
                    f"{item['tag']}-name-missing",
                    "accessibility",
                    "high",
                    "medium",
                    f"名前を判定できない{item['tag']}要素があります。",
                    "表示テキストか、適切なaria-label / aria-labelledbyを追加してください。アイコンだけの場合も操作内容を伝えてください。",
                    path,
                    item["line"],
                    criterion="WCAG 4.1.2",
                )
            )

    for index, control in enumerate(parser.controls):
        attrs = control["attrs"]
        labelled_by = attrs.get("aria-labelledby", "").split()
        missing_references = [reference for reference in labelled_by if reference not in parser.ids]
        if missing_references:
            findings.append(
                _finding(
                    "aria-labelledby-target-missing",
                    "accessibility",
                    "medium",
                    "high",
                    "aria-labelledbyが参照するidが見つかりません: " + ", ".join(missing_references),
                    "同じHTML文書内に参照先のidを追加するか、正しいidへ更新してください。",
                    path,
                    control["line"],
                    criterion="WCAG 4.1.2",
                )
            )
        control_type = attrs.get("type", "").lower()
        if control_type in {"submit", "button", "reset"} and attrs.get("value", "").strip():
            continue
        has_programmatic_name = bool(
            attrs.get("aria-label", "").strip() or attrs.get("aria-labelledby", "").strip()
        )
        has_label = bool(
            attrs.get("id", "") in parser.labels_for
            or index in parser.nested_label_controls
            or has_programmatic_name
        )
        if not has_label:
            findings.append(
                _finding(
                    "form-control-label-missing",
                    "accessibility",
                    "high",
                    "medium",
                    f"{control['tag']}にプログラムから判定できるラベルが見つかりません。",
                    "label要素を関連付けるか、aria-label / aria-labelledbyで目的を説明してください。placeholderだけをラベルの代わりにしないでください。",
                    path,
                    control["line"],
                    criterion="WCAG 1.3.1, 3.3.2, 4.1.2",
                )
            )

    previous_level: Optional[int] = None
    for level, line in parser.headings:
        if previous_level is not None and level > previous_level + 1:
            findings.append(
                _finding(
                    "heading-level-skipped",
                    "semantics",
                    "medium",
                    "medium",
                    f"見出しレベルがh{previous_level}からh{level}へ飛んでいます。",
                    "見た目の大きさではなく、文書構造に沿った見出しレベルを使ってください。",
                    path,
                    line,
                    criterion="WCAG 1.3.1",
                )
            )
        previous_level = level

    return {
        "images": len(parser.images),
        "controls": len(parser.controls),
        "interactive": len(parser.interactive),
        "headings": len(parser.headings),
        "duplicate_ids": len(parser.duplicate_ids),
        "has_main": parser.has_main,
        "has_html_root": parser.has_html_root,
        "has_document_language": parser.has_document_language,
        "has_document_title": parser.has_document_title,
    }


def _analyze_css(
    css_sources: Sequence[Tuple[str, str]], findings: List[Dict[str, Any]]
) -> Dict[str, Any]:
    all_css = "\n".join(_strip_css_comments(source) for _, source in css_sources)
    variables: Dict[str, str] = {}
    for _, source in css_sources:
        variables.update({match.group(1): match.group(2).strip() for match in CSS_VAR_RE.finditer(_strip_css_comments(source))})

    contrast_pairs_seen: set[Tuple[str, str, str, int]] = set()
    rule_count = 0
    contrast_checks = 0
    reduced_motion = bool(re.search(r"prefers-reduced-motion\s*:\s*reduce", all_css, re.IGNORECASE))
    focus_disabled = False
    focus_replacement_selectors: set[str] = set()
    focus_indicator_properties = {
        "outline",
        "outline-color",
        "outline-style",
        "outline-width",
        "box-shadow",
        "border",
        "border-color",
        "background",
        "background-color",
    }
    for _, source in css_sources:
        for rule in _extract_css_rules(source):
            selector = rule["selector"]
            if not re.search(r":focus(?:-visible)?\b", selector, re.IGNORECASE):
                continue
            declarations = rule["declarations"]
            has_visible_indicator = any(
                declarations.get(property_name, "").strip().lower() not in {"", "none", "0", "transparent"}
                for property_name in focus_indicator_properties
            )
            if has_visible_indicator:
                selector_without_focus = re.sub(r":focus(?:-visible)?\b", "", selector, flags=re.IGNORECASE)
                focus_replacement_selectors.update(
                    part.strip() for part in selector_without_focus.split(",")
                )
    has_motion = bool(re.search(r"\b(?:transition|animation)\s*:", all_css, re.IGNORECASE))

    for path, source in css_sources:
        for rule in _extract_css_rules(source):
            rule_count += 1
            declarations = rule["declarations"]
            selector = rule["selector"]
            foreground_value = declarations.get("color")
            background_value = declarations.get("background-color") or declarations.get("background")
            if foreground_value and background_value:
                foreground = _css_color_to_hex(foreground_value, variables)
                background = _css_color_to_hex(background_value, variables)
                if foreground and background:
                    try:
                        ratio = contrast_ratio(foreground, background)
                    except ValueError:
                        ratio = 0
                    contrast_checks += 1
                    font_size_match = re.search(r"([\d.]+)\s*(px|rem|em|pt)", declarations.get("font-size", ""), re.IGNORECASE)
                    font_size_px = None
                    if font_size_match:
                        font_size_px = float(font_size_match.group(1))
                        unit = font_size_match.group(2).lower()
                        if unit in {"rem", "em"}:
                            font_size_px *= 16
                        elif unit == "pt":
                            font_size_px *= 4 / 3
                    is_bold = declarations.get("font-weight", "").lower() in {"bold", "600", "700", "800", "900"}
                    is_large = font_size_px is not None and (font_size_px >= 24 or (is_bold and font_size_px >= 18.66))
                    threshold = 3.0 if is_large else 4.5
                    key = (path, selector, foreground, rule["line"])
                    if ratio < threshold and key not in contrast_pairs_seen:
                        contrast_pairs_seen.add(key)
                        findings.append(
                            _finding(
                                "text-contrast-low",
                                "accessibility",
                                "high" if ratio < 3 else "medium",
                                "medium",
                                f"このCSSルールの文字色と背景色のコントラストは{ratio:.2f}:1です（目安: {threshold:.1f}:1以上）。",
                                "実際の重なり・継承・透明度をブラウザで確認したうえで、文字色または背景色を調整してください。",
                                path,
                                rule["line"],
                                evidence=f"{selector}: color {foreground}; background {background}",
                                criterion="WCAG 1.4.3",
                            )
                        )

            if re.search(
                r"(?:^|[^\w-])(?:button|input|select|textarea|\.btn[\w-]*|\.button[\w-]*)(?=$|[^\w-])",
                selector,
                re.IGNORECASE,
            ):
                outline = declarations.get("outline", "").lower().replace(" ", "")
                if outline in {"none", "0", "0none"} or declarations.get("outline-style", "").lower() == "none":
                    disabled_selectors = [part.strip() for part in selector.split(",")]
                    has_focus_replacement = "" in focus_replacement_selectors or "*" in focus_replacement_selectors or any(
                        part in focus_replacement_selectors for part in disabled_selectors
                    )
                    if not has_focus_replacement:
                        focus_disabled = True
                        findings.append(
                            _finding(
                                "focus-indicator-removed",
                                "accessibility",
                                "high",
                                "medium",
                                "操作要素のアウトラインを消していますが、代替フォーカス表示を検出できません。",
                                ":focus-visibleで十分なコントラストのフォーカスリングを定義してください。",
                                path,
                                rule["line"],
                                evidence=f"{selector}: outline {declarations.get('outline', declarations.get('outline-style', 'none'))}",
                                criterion="WCAG 2.4.7, 2.4.11",
                            )
                        )

    if has_motion and not reduced_motion:
        findings.append(
            _finding(
                "reduced-motion-not-detected",
                "accessibility",
                "low",
                "low",
                "アニメーションまたはtransitionがありますが、prefers-reduced-motionの対応を検出できませんでした。",
                "動きが重要でない場合は、prefers-reduced-motion: reduceで抑制できるようにしてください。",
                css_sources[0][0] if css_sources else "",
                None,
                criterion="WCAG 2.3.3 (AAA) / user preference",
            )
        )

    return {
        "stylesheets": len(css_sources),
        "css_rules": rule_count,
        "static_contrast_pairs_checked": contrast_checks,
        "has_motion_rules": has_motion,
        "reduced_motion_rule_detected": reduced_motion,
        "focus_indicators_removed_without_replacement": focus_disabled,
    }


def _severity_rank(value: str) -> int:
    return {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}.get(value, 5)


def _markdown_report(result: Dict[str, Any]) -> str:
    summary = result["summary"]
    lines = [
        f"# openmcpart audit — {result['project_name']}",
        "",
        f"Scanned {summary['files_scanned']} source files; found {summary['findings_total']} potential issue(s).",
        "",
        "> Static, read-only heuristics. Confirm findings in a browser and with assistive technology; this is not a WCAG conformance certificate.",
        "",
    ]
    if not result["findings"]:
        lines.extend(["## Findings", "", "No issues were detected by the available static checks.", ""])
    else:
        lines.extend(["## Findings", ""])
        for finding in result["findings"]:
            source = finding["source"]
            location = source["path"]
            if source.get("line"):
                location += f":{source['line']}"
            lines.extend(
                [
                    f"### [{finding['severity'].upper()}] {finding['code']}",
                    "",
                    finding["message"],
                    "",
                    f"- **Source:** `{location}`",
                    f"- **Confidence:** {finding['confidence']}",
                    f"- **Fix:** {finding['recommendation']}",
                ]
            )
            if finding.get("wcag_criterion"):
                lines.append(f"- **Reference:** {finding['wcag_criterion']}")
            if finding.get("evidence"):
                lines.append(f"- **Evidence:** `{finding['evidence']}`")
            lines.append("")
    lines.extend(
        [
            "## Design tokens discovered",
            "",
            f"- CSS custom properties: {len(result['design_tokens']['custom_properties'])} returned of {result['design_tokens']['custom_properties_total']}",
            f"- Color tokens: {len(result['design_tokens']['color_tokens'])} returned of {result['design_tokens']['color_tokens_total']}",
            f"- Repeated color values: {len(result['design_tokens']['repeated_colors'])}",
            f"- Font-family declarations: {len(result['design_tokens']['font_families'])}",
            "",
        ]
    )
    return "\n".join(lines)


def tool_audit_project(project_path: str = ".", max_files: int = 500) -> Dict[str, Any]:
    """Read a local frontend project and report static accessibility/design signals.

    The scanner reads only supported text files under ``project_path``. It skips
    hidden and generated directories, symlinks, and files larger than 1 MB. It
    never executes code, accesses the network, or modifies files.
    """
    if max_files < 1 or max_files > 5000:
        return {"error": "max_files must be between 1 and 5000"}
    if not isinstance(project_path, str) or not project_path.strip():
        return {"error": "project_path must be a non-empty directory path"}
    try:
        root = Path(project_path).expanduser().resolve(strict=True)
    except (OSError, RuntimeError, ValueError) as exc:
        return {"error": f"Project path cannot be opened: {exc}"}
    if not root.is_dir():
        return {"error": "project_path must point to a directory"}

    files, skipped = _read_project_files(root, max_files)
    findings: List[Dict[str, Any]] = []
    markup_stats: Counter[str] = Counter()
    files_by_extension = Counter(path.suffix.lower() for path, _ in files)

    for path, source in files:
        if path.suffix.lower() in HTML_EXTENSIONS:
            relative = path.relative_to(root).as_posix()
            markup_stats.update(_analyze_markup(relative, source, findings))

    css_sources = _extract_style_sources(files, root)
    css_stats = _analyze_css(css_sources, findings)
    design_tokens = _extract_tokens(css_sources)

    findings.sort(
        key=lambda item: (
            _severity_rank(item["severity"]),
            item["source"]["path"],
            item["source"]["line"] or 0,
            item["code"],
        )
    )
    findings_total = len(findings)
    returned_findings = findings[:MAX_FINDINGS]
    severity_counts = Counter(item["severity"] for item in findings)
    code_counts = Counter(item["code"] for item in findings)

    result: Dict[str, Any] = {
        "project_name": root.name or str(root),
        "scan_scope": {
            "extensions": sorted(SUPPORTED_EXTENSIONS),
            "max_file_bytes": MAX_FILE_BYTES,
            "max_total_bytes": MAX_TOTAL_BYTES,
            "max_files": max_files,
            "read_only": True,
            "code_executed": False,
            "network_used": False,
        },
        "summary": {
            "files_scanned": len(files),
            "files_by_extension": dict(sorted(files_by_extension.items())),
            "findings_total": findings_total,
            "findings_returned": len(returned_findings),
            "findings_truncated": findings_total > len(returned_findings),
            "by_severity": dict(sorted(severity_counts.items())),
            "by_code": dict(sorted(code_counts.items())),
            "markup_elements": dict(sorted(markup_stats.items())),
            "css": css_stats,
            **skipped,
        },
        "findings": returned_findings,
        "design_tokens": design_tokens,
        "limitations": [
            "Markup semantics are parsed only from .html and .htm files; framework templates are not fully parsed.",
            "CSS contrast pairs are checked only when foreground and background colors are statically declared in the same rule.",
            "Computed styles, inheritance, opacity, images, browser layout, and runtime-generated markup are not evaluated.",
            "An absence of findings is not proof of accessibility or WCAG conformance; verify manually and with browser-based tools.",
        ],
    }
    result["markdown_report"] = _markdown_report(result)
    return result


def tool_extract_project_tokens(project_path: str = ".", max_files: int = 500) -> Dict[str, Any]:
    """Extract CSS custom properties and repeated design values from a project."""
    audit = tool_audit_project(project_path=project_path, max_files=max_files)
    if "error" in audit:
        return audit
    return {
        "project_name": audit["project_name"],
        "files_scanned": audit["summary"]["files_scanned"],
        "design_tokens": audit["design_tokens"],
        "read_only": True,
        "limitations": [
            "Values are heuristically extracted from CSS and component style blocks; this is not a complete CSS parser.",
            "Only text source files up to 1 MB each, 20 MB total, and the requested file limit are scanned.",
            "Returned custom-property and color-token lists are capped; check truncation flags and total counts."
        ],
    }
