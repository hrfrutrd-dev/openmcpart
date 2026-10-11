"""
Accessibility and critique tools
"""
import re
from typing import Any, Dict

from ..utils.color_utils import contrast_ratio, wcag_level

def tool_check_accessibility(
    description: str = "",
    foreground: str = None,
    background: str = None,
    font_size: str = "16px",
    interactive: bool = False
) -> Dict[str, Any]:
    """
    Comprehensive accessibility check
    """
    checks = []
    
    # Color contrast check if colors provided
    if foreground and background:
        try:
            ratio = contrast_ratio(foreground, background)
            levels = wcag_level(ratio)
            checks.append({
                "category": "Color Contrast",
                "check": f"{foreground} on {background}",
                "ratio": round(ratio, 2),
                "wcag": levels,
                "status": "PASS" if levels["AA_normal"] else "FAIL",
                "fix": "コントラスト比を4.5:1以上に。暗い色をより暗く、明るい色をより明るく。" if not levels["AA_normal"] else "OK"
            })
        except Exception as e:
            checks.append({"category": "Color Contrast", "error": str(e), "status": "ERROR"})
    
    # General checklist based on description
    general_checks = [
        {
            "category": "Perceivable",
            "item": "代替テキスト",
            "question": "すべての画像に適切なalt属性があるか？",
            "importance": "高",
            "how_to_check": "画像が情報を伝える場合は具体的に、装飾の場合はalt=\"\"",
        },
        {
            "category": "Perceivable",
            "item": "色だけに依存しない",
            "question": "色だけで情報を伝えていないか？",
            "importance": "高",
            "how_to_check": "エラーは色+アイコン+テキストで伝える。リンクは色+下線など。",
        },
        {
            "category": "Operable",
            "item": "キーボード操作",
            "question": "すべての機能をキーボードで操作可能か？",
            "importance": "高",
            "how_to_check": "Tab, Enter, Space, Esc, 矢印キーで操作確認。フォーカス順序が論理的か。",
        },
        {
            "category": "Operable",
            "item": "フォーカス表示",
            "question": "フォーカス状態が視覚的に明確か？",
            "importance": "高",
            "how_to_check": "outline: 2px solid など、2px以上のコントラストあるフォーカスリング",
        },
        {
            "category": "Operable",
            "item": "タッチターゲット",
            "question": "タッチターゲットは44x44px以上か？",
            "importance": "中",
            "how_to_check": "ボタン、リンクは最低44px。間隔は8px以上。",
        },
        {
            "category": "Understandable",
            "item": "ラベルとエラーメッセージ",
            "question": "フォームに適切なラベルとエラーメッセージがあるか？",
            "importance": "高",
            "how_to_check": "label要素とinputの紐付け、エラーは具体的に修正方法を示す",
        },
        {
            "category": "Robust",
            "item": "セマンティックHTML",
            "question": "適切なHTML要素を使用しているか？",
            "importance": "中",
            "how_to_check": "buttonは<button>, 見出しはh1-h6, nav, main, landmarkを適切に",
        },
    ]
    
    # Add interactive specific checks
    if interactive:
        general_checks.extend([
            {
                "category": "Operable",
                "item": "モーション",
                "question": "動きの激しいアニメーションに配慮があるか？",
                "importance": "中",
                "how_to_check": "prefers-reduced-motionでアニメーションを無効化できるように",
            },
            {
                "category": "Understandable",
                "item": "一貫性",
                "question": "ナビゲーションや操作は一貫しているか？",
                "importance": "中",
                "how_to_check": "同じ機能は同じ位置、同じ見た目で",
            }
        ])
    
    # Font-size heuristic. This does not determine whether a real page is readable.
    size_match = re.fullmatch(r"\s*(\d+(?:\.\d+)?)\s*(px|rem|em|pt)?\s*", font_size.lower())
    if size_match:
        size_num = float(size_match.group(1))
        unit = size_match.group(2) or "px"
        if unit in {"rem", "em"}:
            size_num *= 16
        elif unit == "pt":
            size_num *= 4 / 3
        checks.append(
            {
                "category": "Perceivable",
                "item": "テキストサイズ",
                "current": font_size,
                "estimated_px": round(size_num, 2),
                "recommended": "本文は16px程度以上を検討。ユーザーの拡大を妨げないこと。",
                "status": "PASS" if size_num >= 16 else "WARN" if size_num >= 12 else "FAIL",
                "note": "一つの指定値だけを確認する簡易ヒューリスティックです。ページ全体の可読性判定ではありません。",
            }
        )
    else:
        checks.append(
            {
                "category": "Perceivable",
                "item": "テキストサイズ",
                "current": font_size,
                "status": "UNKNOWN",
                "note": "px, rem, em, pt形式の単一サイズとして解釈できませんでした。",
            }
        )

    # Avoid implying conformance through a synthetic percentage score.
    fail_count = sum(1 for c in checks if c.get("status") == "FAIL")
    total = len(checks) + len(general_checks)
    
    return {
        "description": description,
        "specific_checks": checks,
        "general_checklist": general_checks,
        "summary": {
            "total_checks": total,
            "automated_checks": len(checks),
            "manual_checks": len(general_checks),
            "failures": fail_count,
            "automated_status": "FAIL" if fail_count else "NO_AUTOMATED_FAILURES",
            "note": "手動チェック項目は未判定です。この結果はWCAG適合証明や総合スコアではありません。",
        },
        "quick_wins": [
            "1. すべての画像にaltを追加",
            "2. コントラスト比を4.5:1以上に",
            "3. フォーカスリングを明確に (2px solid)",
            "4. ボタンは44px以上に",
            "5. 見出し階層を正しく (h1→h2→h3)",
        ],
        "tools": [
            "axe DevTools (Chrome拡張)",
            "WAVE (WebAIM)",
            "Lighthouse Accessibility Audit",
            "Color Contrast Analyzer"
        ]
    }

def tool_critique_design(design_description: str, focus: str = "all") -> Dict[str, Any]:
    """Offer text-based review prompts and flag only explicitly described concerns."""
    if not isinstance(design_description, str) or not design_description.strip():
        return {"error": "design_description must not be empty"}
    if not isinstance(focus, str):
        return {"error": "focus must be a string"}

    focus_aliases = {
        "all": ("all", "すべて", "全て"),
        "hierarchy": ("hierarchy", "visual hierarchy", "visual_hierarchy", "階層", "視覚的階層"),
        "consistency": ("consistency", "一貫性"),
        "proximity": ("proximity", "近接"),
        "alignment": ("alignment", "整列"),
        "contrast": ("contrast", "コントラスト"),
        "repetition": ("repetition", "反復"),
        "whitespace": ("whitespace", "white space", "spacing", "余白", "スペーシング"),
        "accessibility": ("accessibility", "a11y", "アクセシビリティ"),
    }
    requested_focus = focus.strip().casefold()
    matched_focus = next(
        (name for name, aliases in focus_aliases.items() if requested_focus in aliases),
        None,
    )
    if matched_focus is None:
        choices = ", ".join(focus_aliases)
        return {"error": f"Unsupported focus: {focus}. Choose from: {choices}"}

    heuristics = [
        {
            "principle": "視覚的階層 (Visual Hierarchy)",
            "question": "最重要の情報と次の行動が、意図した順序で伝わるか？",
            "checklist": ["見出しと本文の差", "CTAの優先度", "余白によるグルーピング"],
        },
        {
            "principle": "一貫性 (Consistency)",
            "question": "同じ役割の要素に一貫性があり、意図的な差分が分かるか？",
            "checklist": ["色・タイポグラフィ", "間隔とコンポーネント", "操作後の状態"],
        },
        {
            "principle": "近接 (Proximity)",
            "question": "関連する情報がまとまり、異なるグループと区別されているか？",
            "checklist": ["関連要素の距離", "グループ間の余白", "画面幅に応じた再配置"],
        },
        {
            "principle": "整列 (Alignment)",
            "question": "整列がコンテンツとブランドの意図に沿っているか？",
            "checklist": ["グリッドやエッジ", "左右・中央揃えの使い分け", "小さい画面での崩れ"],
        },
        {
            "principle": "コントラスト (Contrast)",
            "question": "文字や操作要素が十分に識別できるか？",
            "checklist": ["色を指定した場合は実際の比率を測定", "色だけに情報を依存しない", "文字サイズに合う基準を使用"],
        },
        {
            "principle": "反復 (Repetition)",
            "question": "繰り返しが予測可能性を高め、ブランドに合っているか？",
            "checklist": ["再利用可能なコンポーネント", "必要な色・フォントだけを使う", "例外が意図的か"],
        },
        {
            "principle": "余白 (White Space)",
            "question": "情報密度と余白のバランスが用途に合っているか？",
            "checklist": ["読みやすい行長", "情報グループの距離", "画面サイズに応じた余白"],
        },
        {
            "principle": "アクセシビリティ (Accessibility)",
            "question": "キーボード・支援技術・異なる表示条件で使えるか？",
            "checklist": ["コントラストと色以外の手がかり", "キーボードとフォーカス", "画像の代替テキストとフォームラベル"],
        },
    ]
    if matched_focus != "all":
        focus_term = {
            "hierarchy": "hierarchy",
            "consistency": "consistency",
            "proximity": "proximity",
            "alignment": "alignment",
            "contrast": "contrast",
            "repetition": "repetition",
            "whitespace": "white space",
            "accessibility": "accessibility",
        }[matched_focus]
        heuristics = [item for item in heuristics if focus_term in item["principle"].casefold()]

    description = design_description.casefold()
    concern_rules = [
        {
            "issue": "Information density concern",
            "triggers": ("ごちゃ", "詰め込み", "clutter", "busy", "overcrowded", "too many elements"),
            "next_step": "Prioritize the key user task, then review which content can be grouped, deferred, or removed.",
        },
        {
            "issue": "Text contrast concern",
            "triggers": ("低コントラスト", "コントラストが低", "low contrast", "poor contrast", "hard to read"),
            "next_step": "Measure the actual foreground/background pair at the applicable text-size threshold, then verify rendered states.",
        },
        {
            "issue": "Typography readability concern",
            "triggers": ("文字が小", "文字が読みにく", "small text", "tiny text", "font too small"),
            "next_step": "Check zoom, line length, line height, and content hierarchy with representative users.",
        },
        {
            "issue": "Primary action discoverability concern",
            "triggers": ("ctaが目立たない", "cta not visible", "weak cta", "button is hard to find", "ボタンが見つからない"),
            "next_step": "Test whether users can identify the primary action and understand its label without relying on color alone.",
        },
        {
            "issue": "Color-palette complexity concern",
            "triggers": ("色が多すぎ", "色が多い", "too many colors", "palette is too broad"),
            "next_step": "Group colors by semantic role and remove only values that do not serve a clear purpose.",
        },
    ]
    critique = []
    for rule in concern_rules:
        evidence = next((token for token in rule["triggers"] if token in description), None)
        if evidence:
            critique.append(
                {
                    "issue": rule["issue"],
                    "evidence": evidence,
                    "next_step": rule["next_step"],
                    "confidence": "keyword_heuristic",
                    "status": "review_requested_by_description",
                }
            )

    return {
        "design_description": design_description,
        "focus": matched_focus,
        "analysis_type": "keyword_heuristic",
        "heuristics": heuristics,
        "critique": critique,
        "review_prompts": {
            "visual_hierarchy": "最重要の情報、主要タスク、次の行動が明確かを実画面で確認してください。",
            "consistency": "同じ役割の要素が一貫し、例外が意図的かを確認してください。",
            "accessibility": "コントラスト計算に加え、キーボードと支援技術でも確認してください。",
        },
        "action_plan": {
            "immediate": ["説明に現れた懸念を、画面・実データ・利用者で確認する"],
            "short_term": ["確認できた課題だけを優先し、デザインシステムやテストに反映する"],
            "long_term": ["代表的な利用者と支援技術を含むユーザーテストを行う"],
        },
        "limitations": [
            "テキスト説明だけをキーワードで確認し、画像・DOM・実際の画面は解析しません。",
            "懸念語が見つからなくても、デザイン品質やアクセシビリティの保証にはなりません。",
            "余白・角丸・色数などの好みは普遍的な品質基準として扱いません。",
        ],
        "resources": [
            "Refactoring UI - Adam Wathan & Steve Schoger",
            "Laws of UX - Jon Yablonski",
            "Gestalt Principles",
            "Material Design 3 / Human Interface Guidelines",
        ],
    }

def tool_suggest_component_variants(component: str, style: str = "modern", count: int = 3) -> Dict[str, Any]:
    if not isinstance(component, str) or not component.strip():
        return {"error": "component must not be empty"}
    if not isinstance(count, int) or isinstance(count, bool) or not 1 <= count <= 5:
        return {"error": "count must be an integer between 1 and 5"}
    if not isinstance(style, str) or style.lower() not in {"modern", "playful", "elegant", "minimal"}:
        return {"error": "style must be modern, playful, elegant, or minimal"}
    component = component.lower().strip()
    style = style.lower()
    
    components = {
        "button": {
            "variants": [
                {"name": "Primary", "style": "bg-primary text-white hover:bg-primary-600", "usage": "主要アクション、1画面1つ"},
                {"name": "Secondary", "style": "bg-white border border-gray-300 text-gray-700 hover:bg-gray-50", "usage": "次要アクション"},
                {"name": "Ghost", "style": "bg-transparent text-gray-600 hover:bg-gray-100", "usage": "控えめなアクション"},
                {"name": "Destructive", "style": "bg-red-600 text-white hover:bg-red-700", "usage": "削除など危険な操作"},
                {"name": "Link", "style": "text-primary underline hover:text-primary-700", "usage": "テキストリンクとして"},
            ],
            "sizes": {
                "sm": "h-8 px-3 text-sm",
                "md": "h-10 px-4 text-base",
                "lg": "h-12 px-6 text-lg",
            },
            "states": ["default", "hover", "active", "focus (ring)", "disabled", "loading"],
            "a11y": "44px以上、フォーカスリング2px、disabledはaria-disabled"
        },
        "card": {
            "variants": [
                {"name": "Elevated", "style": "bg-white rounded-xl shadow-md p-6", "usage": "標準、ダッシュボード"},
                {"name": "Outlined", "style": "bg-white rounded-xl border p-6", "usage": "控えめ、リスト"},
                {"name": "Filled", "style": "bg-gray-50 rounded-xl p-6", "usage": "背景と区別、サブセクション"},
                {"name": "Interactive", "style": "bg-white rounded-xl border p-6 hover:shadow-lg transition", "usage": "クリック可能なカード"},
            ],
            "anatomy": ["Header (title, action)", "Body (content)", "Footer (actions, meta)"],
            "a11y": "インタラクティブなカードはボタンまたはリンクとしてマークアップ"
        },
        "input": {
            "variants": [
                {"name": "Default", "style": "border border-gray-300 rounded-lg px-3 h-10 focus:ring-2 focus:ring-primary", "usage": "標準入力"},
                {"name": "Filled", "style": "bg-gray-100 border-transparent rounded-lg px-3 h-10 focus:bg-white focus:border-primary", "usage": "密なフォーム"},
                {"name": "Flushed", "style": "border-b border-gray-300 rounded-none px-0 focus:border-primary", "usage": "ミニマル"},
            ],
            "states": ["default", "focus", "error (red border + message)", "disabled", "with icon"],
            "a11y": "label必須、エラーはaria-describedbyで関連付け"
        }
    }
    
    # Default if not found
    if component not in components:
        # Try fuzzy
        for key in components:
            if key in component or component in key:
                component = key
                break
        else:
            # generic
            return {
                "component": component,
                "message": f"{component} の一般的なバリエーション提案",
                "variants": [
                    {"name": "Default", "description": "標準スタイル"},
                    {"name": "Primary", "description": "強調スタイル"},
                    {"name": "Subtle", "description": "控えめスタイル"},
                ],
                "principles": [
                    "一貫性: 同じコンポーネントは同じ見た目",
                    "階層: Primaryは1画面1つ",
                    "状態: hover, focus, disabledを必ず定義",
                    "アクセシビリティ: コントラスト、44px、キーボード操作"
                ],
                "available_components": list(components.keys())
            }
    
    data = components[component]
    # Limit count
    if "variants" in data:
        data["variants"] = data["variants"][:count]
    
    # Style adjustments
    style_tweaks = {
        "modern": "角丸8px, subtle shadow, Interフォント",
        "playful": "角丸16px, 柔らかい影, Poppinsフォント, 明るい色",
        "elegant": "角丸4px, 細いボーダー, Playfair Display, 落ち着いた色",
        "minimal": "角丸0-4px, ボーダーのみ, モノクロ",
    }
    
    data["style_tweak"] = style_tweaks.get(style, style_tweaks["modern"])
    data["component"] = component
    data["requested_style"] = style
    
    # Add code examples
    if component == "button":
        data["code"] = {
            "html": '<button class="h-10 px-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:ring-2">Button</button>',
            "react": 'function Button({children, variant="primary"}) { return <button className={`btn btn-${variant}`}>{children}</button> }'
        }
    
    return data
