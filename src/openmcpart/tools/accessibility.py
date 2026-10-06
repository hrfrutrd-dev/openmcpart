"""
Accessibility and critique tools
"""
from typing import Dict, Any, List
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
    
    # Font size check
    try:
        size_num = int(font_size.replace("px", "").replace("rem", "").strip())
        if "rem" in font_size:
            size_num = size_num * 16
        font_check = {
            "category": "Perceivable",
            "item": "テキストサイズ",
            "current": font_size,
            "recommended": "本文16px以上、最小12px",
            "status": "PASS" if size_num >= 16 else "WARN" if size_num >= 12 else "FAIL"
        }
        checks.append(font_check)
    except:
        pass
    
    # Calculate score
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
            "score": f"{max(0, 100 - fail_count*15)}/100 (推定)",
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
    """
    Heuristic evaluation of design
    """
    heuristics = [
        {
            "principle": "視覚的階層 (Visual Hierarchy)",
            "question": "最も重要な要素が最も目立っているか？",
            "checklist": ["サイズのコントラスト", "色・重さのコントラスト", "配置 (F/Zパターン)", "余白によるグルーピング"],
        },
        {
            "principle": "一貫性 (Consistency)",
            "question": "同様の要素は同様に見えるか？",
            "checklist": ["色の一貫性", "タイポグラフィの一貫性", "間隔の一貫性 (8pt grid)", "インタラクションの一貫性"],
        },
        {
            "principle": "近接 (Proximity)",
            "question": "関連する要素は近くに配置されているか？",
            "checklist": ["ゲシュタルトの近接の法則", "グループ間は24px+, 要素間は8-16px", "セクション間は64px+"],
        },
        {
            "principle": "整列 (Alignment)",
            "question": "要素は意図的に整列されているか？",
            "checklist": ["グリッドに沿っているか", "中央揃えの乱用を避け左揃え基本", "エッジを揃える"],
        },
        {
            "principle": "コントラスト (Contrast)",
            "question": "重要な違いは明確に区別されているか？",
            "checklist": ["テキストコントラスト 4.5:1以上", "サイズコントラスト (1.25倍以上)", "色だけでなく形でも区別"],
        },
        {
            "principle": "反復 (Repetition)",
            "question": "パターンが繰り返され予測可能か？",
            "checklist": ["同じスタイルの繰り返し", "コンポーネントの再利用", "色・フォントの制限 (3色, 2フォント)"],
        },
        {
            "principle": "余白 (White Space)",
            "question": "余白は十分かつ意図的か？",
            "checklist": ["詰め込みすぎていないか", "余白は8の倍数か", "呼吸感があるか"],
        },
        {
            "principle": "アクセシビリティ (Accessibility)",
            "question": "誰でも使えるか？",
            "checklist": ["コントラスト", "タッチターゲット44px", "キーボード操作", "代替テキスト"],
        },
    ]
    
    # Filter by focus
    if focus != "all":
        focus = focus.lower()
        heuristics = [h for h in heuristics if focus in h["principle"].lower() or focus in h["question"].lower()] or heuristics
    
    # Generate critique based on description keywords
    critique_points = []
    desc_lower = design_description.lower()
    
    if "ごちゃ" in design_description or "clutter" in desc_lower or "busy" in desc_lower:
        critique_points.append({"issue": "情報過多", "severity": "高", "suggestion": "要素を50%削減、余白を2倍に。優先度付けを明確に。"})
    if "色" in design_description or "color" in desc_lower:
        critique_points.append({"issue": "色の使用", "severity": "中", "suggestion": "3色パレットに制限 (60-30-10ルール: 60% neutral, 30% primary, 10% accent)"})
    if "文字" in design_description or "text" in desc_lower or "font" in desc_lower:
        critique_points.append({"issue": "タイポグラフィ", "severity": "中", "suggestion": "フォントは2種類まで、ウェイトは3つまで。行間1.5-1.7、1行35-45文字。"})
    if "ボタン" in design_description or "button" in desc_lower or "cta" in desc_lower:
        critique_points.append({"issue": "CTA", "severity": "高", "suggestion": "主要CTAは1画面1つ。色で目立たせ、周囲に余白を。44px以上の高さ。"})
    
    # If no specific keywords, give general critique framework
    if not critique_points:
        critique_points = [
            {"issue": "全体の印象", "severity": "要確認", "suggestion": "5秒テスト: 5秒見て何のサイトか、次に何をすべきか分かるか？"},
            {"issue": "視線の流れ", "severity": "要確認", "suggestion": "Fパターン/Zパターンに沿っているか？重要→詳細の順に視線が流れるか？"},
            {"issue": "余白", "severity": "中", "suggestion": "要素間に十分な余白があるか？詰め込みすぎていないか？8pt grid準拠か？"},
        ]
    
    return {
        "design_description": design_description,
        "focus": focus,
        "heuristics": heuristics,
        "critique": critique_points,
        "action_plan": {
            "immediate": ["コントラストチェック", "余白を1.5倍に", "CTAを明確化"],
            "short_term": ["8ptグリッド導入", "タイポグラフィ整理 (2フォント, 3ウェイト)", "色を3色に制限"],
            "long_term": ["デザインシステム構築", "コンポーネント化", "ユーザーテスト"]
        },
        "scores": {
            "visual_hierarchy": "要レビュー - 最重要要素が最も目立つか？",
            "consistency": "要レビュー - 同じ要素は同じ見た目か？",
            "accessibility": "要レビュー - WCAG AA準拠か？",
        },
        "resources": [
            "Refactoring UI - Adam Wathan & Steve Schoger",
            "Laws of UX - Jon Yablonski",
            "Gestalt Principles",
            "Material Design 3 / Human Interface Guidelines"
        ]
    }

def tool_suggest_component_variants(component: str, style: str = "modern", count: int = 3) -> Dict[str, Any]:
    component = component.lower()
    
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
