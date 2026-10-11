import json
from pathlib import Path

from openmcpart.server import main
import openmcpart.tools.project_audit as project_audit
from openmcpart.tools.project_audit import (
    tool_audit_project,
    tool_extract_project_tokens,
)


def _sample_project(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    (root / "index.html").write_text(
        """<!doctype html>
<html><body>
<main>
  <h1>Welcome</h1>
  <h3>Skipped heading</h3>
  <img src="hero.png">
  <button></button>
  <button aria-labelledby="missing-label"></button>
  <a href="/icon"><img src="icon.svg" alt="Open settings"></a>
  <input id="email">
  <label for="search">Search</label><input id="search">
  <div id="duplicate"></div><span id="duplicate"></span>
</main>
</body></html>
""",
        encoding="utf-8",
    )
    (root / "styles.css").write_text(
        """:root {
  --color-primary: #334455;
  --space-md: 16px;
}
/* Keep this comment on its own lines so source locations remain testable.
   It spans a second line. */
.btn {
  color: #888888;
  background-color: #ffffff;
  outline: none;
  transition: color 0.2s;
  font-family: Inter, sans-serif;
  border-radius: 8px;
}
.safe { outline: none; }
.safe:focus-visible { outline: 2px solid #000000; }
.btn:hover { color: #111111; background-color: #ffffff; }
""",
        encoding="utf-8",
    )
    (root / "README.md").write_text("not scanned", encoding="utf-8")
    (root / "node_modules").mkdir()
    (root / "node_modules" / "vendor.css").write_text(".x { color: #000; }", encoding="utf-8")
    return root


def test_project_audit_reports_static_findings_and_limits(tmp_path):
    project = _sample_project(tmp_path / "sample-app")

    result = tool_audit_project(str(project))

    codes = {finding["code"] for finding in result["findings"]}
    assert "image-alt-missing" in codes
    assert "button-name-missing" in codes
    assert "form-control-label-missing" in codes
    assert "heading-level-skipped" in codes
    assert "document-language-missing" in codes
    assert "document-title-missing" in codes
    assert "aria-labelledby-target-missing" in codes
    assert "text-contrast-low" in codes
    assert "focus-indicator-removed" in codes
    assert "duplicate-id" in codes
    assert "a-name-missing" not in codes
    assert "reduced-motion-not-detected" in codes
    focus_findings = [finding for finding in result["findings"] if finding["code"] == "focus-indicator-removed"]
    assert any(".btn" in finding.get("evidence", "") for finding in focus_findings)
    assert all(".safe" not in finding.get("evidence", "") for finding in focus_findings)
    assert result["summary"]["files_scanned"] == 2
    assert result["summary"]["css"]["static_contrast_pairs_checked"] >= 1
    assert result["scan_scope"]["read_only"] is True
    assert result["scan_scope"]["code_executed"] is False
    assert "not a WCAG conformance certificate" in result["markdown_report"]


def test_document_title_and_language_are_recognized_when_present():
    findings = []
    source = '<!doctype html><html lang="ja"><head><title>サービス案内</title></head><body><main></main></body></html>'

    stats = project_audit._analyze_markup("index.html", source, findings)

    assert stats["has_document_language"] is True
    assert stats["has_document_title"] is True
    assert "document-language-missing" not in {finding["code"] for finding in findings}
    assert "document-title-missing" not in {finding["code"] for finding in findings}


def test_svg_title_does_not_count_as_document_title():
    findings = []
    source = '<html lang="en"><head></head><body><svg><title>Chart icon</title></svg></body></html>'

    stats = project_audit._analyze_markup("index.html", source, findings)

    assert stats["has_document_title"] is False
    assert "document-title-missing" in {finding["code"] for finding in findings}


def test_project_audit_extracts_design_tokens(tmp_path):
    project = _sample_project(tmp_path / "sample-app")

    result = tool_extract_project_tokens(str(project))

    tokens = result["design_tokens"]
    assert tokens["custom_properties"]["--color-primary"] == "#334455"
    assert tokens["color_tokens"]["--color-primary"]["resolved_color"] == "#334455"
    assert {item["value"] for item in tokens["font_families"]} >= {"Inter, sans-serif"}
    assert {item["value"] for item in tokens["border_radii"]} >= {"8px"}
    assert result["read_only"] is True


def test_project_audit_rejects_invalid_paths_and_limits(tmp_path):
    missing = tool_audit_project(str(tmp_path / "missing"))
    not_directory = tmp_path / "file.txt"
    not_directory.write_text("x", encoding="utf-8")
    file_result = tool_audit_project(str(not_directory))
    invalid_limit = tool_audit_project(str(tmp_path), max_files=0)
    empty_path = tool_audit_project("")

    assert "error" in empty_path
    assert "error" in missing
    assert "directory" in file_result["error"]
    assert "max_files" in invalid_limit["error"]


def test_project_audit_skips_symlinked_files(tmp_path):
    project = tmp_path / "app"
    project.mkdir()
    outside = tmp_path / "outside.css"
    outside.write_text(".x { color: #000000; }", encoding="utf-8")
    (project / "linked.css").symlink_to(outside)

    result = tool_audit_project(str(project))

    assert result["summary"]["files_scanned"] == 0
    assert result["summary"]["skipped_symlinks"] == 1


def test_project_audit_honors_file_limit(tmp_path):
    project = tmp_path / "many-files"
    project.mkdir()
    (project / "a.css").write_text(".a { color: #111; }", encoding="utf-8")
    (project / "b.html").write_text("<main></main>", encoding="utf-8")

    result = tool_audit_project(str(project), max_files=1)

    assert result["summary"]["files_scanned"] == 1
    assert result["summary"]["file_limit_reached"] == 1


def test_project_audit_obeys_total_byte_budget(tmp_path, monkeypatch):
    project = tmp_path / "large-app"
    project.mkdir()
    (project / "a.css").write_text("a" * 40, encoding="utf-8")
    (project / "b.css").write_text("b" * 20, encoding="utf-8")
    monkeypatch.setattr(project_audit, "MAX_TOTAL_BYTES", 48)

    result = tool_audit_project(str(project))

    assert result["summary"]["total_bytes_read"] == 40
    assert result["summary"]["byte_limit_reached"] == 1


def test_css_comment_removal_preserves_line_numbers_and_style_block_offsets(tmp_path):
    css_rules = project_audit._extract_css_rules(
        """/* first line
second line */
.btn { outline: none; }"""
    )
    root = tmp_path / "vue-app"
    root.mkdir()
    component = root / "App.vue"
    component.write_text(
        """<template>
<div />
</template>
<style>
.btn {
  outline: none;
}
</style>""",
        encoding="utf-8",
    )
    style_sources = project_audit._extract_style_sources([(component, component.read_text())], root)

    assert css_rules[0]["line"] == 3
    assert project_audit._extract_css_rules(style_sources[0][1])[0]["line"] == 5


def test_token_output_is_bounded_and_reports_truncation(monkeypatch):
    monkeypatch.setattr(project_audit, "MAX_RETURNED_CUSTOM_PROPERTIES", 2)
    monkeypatch.setattr(project_audit, "MAX_RETURNED_COLOR_TOKENS", 1)
    monkeypatch.setattr(project_audit, "MAX_TOKEN_VALUE_CHARS", 8)
    source = ":root { --color-a: " + "x" * 40 + "; --color-b: #445566; --spacing-large: " + "y" * 40 + "; }"

    tokens = project_audit._extract_tokens([("tokens.css", source)])

    assert len(tokens["custom_properties"]) == 2
    assert tokens["custom_properties_total"] == 3
    assert tokens["custom_properties_truncated"] is True
    assert len(tokens["color_tokens"]) == 1
    assert tokens["color_tokens_total"] == 2
    assert tokens["color_tokens_truncated"] is True
    assert len(tokens["custom_properties"]["--color-a"]) <= 8


def test_static_contrast_skips_gradients_and_translucent_colors():
    assert project_audit._css_color_to_hex("linear-gradient(#000, #fff)", {}) is None
    assert project_audit._css_color_to_hex("rgba(0, 0, 0, 0.5)", {}) is None
    assert project_audit._css_color_to_hex("rgba(0, 0, 0, 1)", {}) == "#000000"


def test_cli_audit_emits_json(tmp_path, capsys):
    project = _sample_project(tmp_path / "sample-app")

    exit_code = main(["audit", str(project), "--format", "json"])

    output = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert output["project_name"] == "sample-app"


def test_cli_can_fail_on_accessibility_findings(tmp_path, capsys):
    project = _sample_project(tmp_path / "sample-app")

    exit_code = main(["audit", str(project), "--fail-on", "high"])

    assert exit_code == 1
    assert "image-alt-missing" in capsys.readouterr().out


def test_cli_returns_nonzero_for_missing_project(tmp_path, capsys):
    exit_code = main(["audit", str(tmp_path / "missing")])

    assert exit_code == 2
    assert "cannot be opened" in capsys.readouterr().err.lower()
