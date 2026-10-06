"""
Sophisticated UI Generator - AIっぽくない洗練されたUIを生成

Avoids common AI tropes:
- No purple/blue gradients
- No excessive rounded corners
- No generic card shadows
- No sparkles/ai magic copy
- No centered blob hero

Instead:
- Editorial, asymmetrical, intentional whitespace
- Serif + Sans pairing with character
- Hairline borders, sharp edges
- Earthy, paper-based palette
- Real content, not lorem ipsum
"""

from typing import Dict, Any, List

SOPHISTICATED_PALETTES = {
    "paper_ink": {
        "name": "Paper & Ink",
        "description": "紙とインク - 最も洗練された基本。Aesop, Muji的",
        "colors": {
            "paper": "#fdfcfa",
            "paper_dark": "#f5f3ef",
            "ink": "#121212",
            "ink_light": "#6b6b6b",
            "hairline": "#e8e3dc",
            "accent": "#c45a3c",  # terracotta, not purple
        },
        "usage": "60% paper, 30% ink, 10% terracotta. 影は使わずhairlineで区切る"
    },
    "clay_moss": {
        "name": "Clay & Moss",
        "description": "土と苔 - 日本的、工芸的",
        "colors": {
            "paper": "#faf8f5",
            "clay": "#c4a484",
            "moss": "#5a6b5d",
            "ink": "#1a1a18",
            "stone": "#e8e0d5",
            "accent": "#8b7355",
        },
        "usage": "工芸、和ブランド、建築に。彩度低く、質感で語る"
    },
    "editorial": {
        "name": "Editorial Noir",
        "description": "編集的ノワール - Linear, Stripeの抑制",
        "colors": {
            "paper": "#ffffff",
            "ink": "#0a0a0a",
            "gray_100": "#f5f5f3",
            "gray_300": "#d4d4d0",
            "gray_600": "#6b6b68",
            "accent": "#ff3b30",  # single vivid, not gradient
        },
        "usage": "モノクロ基調に1色だけ vivid。情報設計で勝負"
    },
    "atelier": {
        "name": "Atelier",
        "description": "アトリエ - 制作現場の美しさ",
        "colors": {
            "canvas": "#f0ede8",
            "charcoal": "#2b2b2b",
            "chalk": "#ffffff",
            "rust": "#a0522d",
            "paper": "#e8e2d9",
            "line": "#2b2b2b",
        },
        "usage": "手作業、素材感、未完成の美。罫線は手描き風ではなく正確なhairline"
    }
}

SOPHISTICATED_TYPOGRAPHY = {
    "editorial": {
        "heading": "Instrument Serif / Newsreader / Fraunces",
        "body": "Suisse Int'l / Inter Tight / IBM Plex Sans",
        "mono": "IBM Plex Mono / Fragment Mono",
        "pairing_reason": "セリフの個性 + サンセリフの中立。AIっぽい幾何学サンセリフだけを避ける",
        "scale": "見出しは大きく (48-72px), 行間タイト (1.05), 本文は小さく読みやすく (15px, 1.7)",
        "details": "見出しは -0.02em tracking, 本文は 0。見出しはfont-weight 400で十分、太くしない"
    },
    "japanese_refined": {
        "heading": "Shippori Mincho / Zen Old Mincho",
        "body": "Noto Sans JP / Zen Kaku Gothic",
        "mono": "IBM Plex Mono",
        "pairing_reason": "明朝の品格。ゴシックだけの無難さを避け、明朝で差別化",
        "scale": "日本語は欧文より1.1倍大きく。行間 1.8-2.0で余裕を",
        "details": "約物は半角ではなく全角、字間は詰めすぎない"
    },
    "grotesk_sharp": {
        "heading": "Neue Haas Grotesk / Helvetica Now",
        "body": "Neue Haas Grotesk",
        "mono": "Mono",
        "pairing_reason": "同一ファミリーでウェイトとサイズで階層。フォントを増やさない潔さ",
        "scale": "全て同じフォント、サイズとウェイトで語る。最も洗練された方法",
        "details": "ウェイトは2つまで (400, 500)。Boldは使わない"
    }
}

AI_TROPES_TO_AVOID = [
    {"trope": "Purple → Blue gradient", "why": "2023-24年のAIジェネリック", "instead": "単色 + 紙の質感、または同系色の微グラデ (5%差)"},
    {"trope": "Rounded 24px cards everywhere", "why": "AIが好む安全な丸み", "instead": "0-4px、または1つだけ16pxをアクセントに。基本はsharp"},
    {"trope": "Soft large shadows (0 8px 32px)", "why": "浮かせれば良いと思っているAI", "instead": "影なし + hairline border (0.5px)。または1px solid"},
    {"trope": "Sparkles ✨ Magic AI copy", "why": "AIがAIを語る自己言及", "instead": "具体的な動詞。'生成'ではなく'組む、編む、削る'"},
    {"trope": "Centered hero + blob background", "why": "全てのAI LPが同じ", "instead": "Asymmetrical, 左に寄せ、右に大きく余白。背景は紙色のみ"},
    {"trope": "3-col feature grid with icons in circles", "why": "最も思考停止なレイアウト", "instead": "1列 + 横に長い説明、または2列で片方を大きく。アイコンは線で描く、または使わない"},
    {"trope": "Inter everywhere, no personality", "why": "安全すぎる", "instead": "セリフを1つ入れるだけで脱AI。Instrument Serif, Newsreader等"},
    {"trope": "Bouncy scale hover", "why": "安っぽい", "instead": "Underline, またはopacity 0.6。動きは150ms、ease-out"},
    {"trope": "Neon, high saturation", "why": "デジタルすぎる", "instead": "彩度30-50%、紙に印刷しても美しい色"},
]

def tool_generate_sophisticated_ui(
    purpose: str = "landing page",
    aesthetic: str = "paper_ink",
    industry: str = "",
    avoid_ai_tropes: bool = True
) -> Dict[str, Any]:
    """
    AIっぽくない洗練されたUIの設計仕様を生成
    """
    palette = SOPHISTICATED_PALETTES.get(aesthetic, SOPHISTICATED_PALETTES["paper_ink"])
    
    # Select typography based on aesthetic
    if "japanese" in aesthetic or "japan" in purpose.lower():
        typo = SOPHISTICATED_TYPOGRAPHY["japanese_refined"]
    elif "editorial" in aesthetic or "paper" in aesthetic:
        typo = SOPHISTICATED_TYPOGRAPHY["editorial"]
    else:
        typo = SOPHISTICATED_TYPOGRAPHY["grotesk_sharp"]
    
    # Layout principles for non-AI look
    layout_principles = {
        "grid": "12colだが、常に非対称に使う。例: 左5colにタイトル、右7colは空け、コンテンツは左6colに",
        "whitespace": "セクション間 160-240px。AIは80pxで詰めがち。余白を恐れないのが洗練",
        "alignment": "左揃え基本。中央揃えは1ページに1回まで。右揃えを1箇所入れると緊張感",
        "borders": "0.5px hairline (#e8e3dc)で区切る。影は使わない。線は情報",
        "radius": "基本0px。どうしても必要な箇所だけ4px。24pxは使わない",
        "density": "要素を50%減らす。1画面に1メッセージ。AIは詰め込みがち",
    }
    
    # Component specs that avoid AI look
    components = {
        "button": {
            "primary": "bg-ink text-paper, radius 0, height 44px, padding 0 24px, font-size 14px, letter-spacing 0.02em, uppercase or normal, hover: opacity 0.85, no scale",
            "secondary": "bg-transparent border 1px solid hairline, text-ink, same size, hover: bg-paper_dark",
            "avoid": "gradient, shadow, rounded-full, scale-105, sparkles",
            "example_css": "button.primary { background: #121212; color: #fdfcfa; border: 0; border-radius: 0; height: 44px; padding: 0 24px; font-size: 14px; letter-spacing: 0.02em; transition: opacity 150ms; } button.primary:hover { opacity: 0.85; }"
        },
        "card": {
            "style": "bg-paper, border 0.5px solid hairline, radius 0, padding 32px, no shadow",
            "hover": "border-color: ink (0.5px -> 1px), no shadow, no lift",
            "avoid": "shadow-lg, rounded-2xl, gradient border",
            "example_css": ".card { background: #fdfcfa; border: 0.5px solid #e8e3dc; border-radius: 0; padding: 32px; } .card:hover { border-color: #121212; }"
        },
        "input": {
            "style": "bg-transparent, border-bottom 1px solid hairline, radius 0, height 48px, focus: border-bottom 1px solid ink",
            "avoid": "full border, rounded, shadow, floating label with bg",
            "example_css": "input { background: transparent; border: 0; border-bottom: 1px solid #e8e3dc; border-radius: 0; height: 48px; } input:focus { border-bottom-color: #121212; outline: 0; }"
        }
    }
    
    # Page structure example for landing
    if "landing" in purpose.lower():
        structure = [
            {"section": "Header", "spec": "height 72px, border-bottom 0.5px, logo left (serif 20px), nav right (14px, 24px gap), no shadow, no CTA in header (洗練はCTAを急がない)"},
            {"section": "Hero", "spec": "padding 120px 0 80px, 左6col: 見出し 64px serif, line-height 0.95, -0.02em tracking, 右6col: 空白または小さな注釈 (14px mono)。CTAは1つだけ、heroの下部に置く、目立たせすぎない"},
            {"section": "Manifesto / Statement", "spec": "1文を大きく (32px serif)、左に寄せ、右は空ける。AIは3つの特徴を並べるが、洗練は1つの強い主張"},
            {"section": "Work / Product", "spec": "1列、大きな余白、各項目はhairlineで区切る、画像はフルブリードまたは左に寄せ、説明は小さく (14px)"},
            {"section": "Footer", "spec": "border-top 0.5px, padding 48px 0, 小さく (13px), mono, 3列だが情報は少なく"},
        ]
    elif "dashboard" in purpose.lower():
        structure = [
            {"section": "Sidebar", "spec": "width 240px, bg-paper_dark, border-right 0.5px, navは14px, 32px gap, activeはbg-ink text-paper, radius 0"},
            {"section": "Main", "spec": "padding 32px, cardsはhairline border, no shadow, dataはmono 13px, 大きな数字はserif 48px"},
        ]
    else:
        structure = [
            {"section": "General", "spec": "Asymmetrical grid, huge whitespace, hairline borders, 0 radius, serif headings"},
        ]
    
    # Copywriting that avoids AI cliches
    copy_guide = {
        "avoid": ["AI-powered", "Magical", "Supercharge", "Unleash", "Elevate", "Revolutionary", "Next-gen", "✨"],
        "instead": ["具体的な動詞を使う: 組む、編む、削る、整える、並べる", "数字で語る: 0.5px, 160px, 1つの主張", "否定で語る: 何をしないかを言う (影を使わない、丸めない)"],
        "example_headline": {
            "ai_like": "AI-Powered Design Magic ✨ Supercharge Your Workflow",
            "sophisticated": "紙とインク。0.5pxの線で区切る。"
        }
    }
    
    return {
        "purpose": purpose,
        "aesthetic": aesthetic,
        "palette": palette,
        "typography": typo,
        "layout_principles": layout_principles,
        "components": components,
        "page_structure": structure,
        "copy_guide": copy_guide,
        "ai_tropes_to_avoid": AI_TROPES_TO_AVOID if avoid_ai_tropes else [],
        "css_variables": f"""
:root {{
  --paper: {palette['colors'].get('paper', '#fdfcfa')};
  --paper-dark: {palette['colors'].get('paper_dark', palette['colors'].get('stone', '#f5f3ef'))};
  --ink: {palette['colors'].get('ink', '#121212')};
  --ink-light: {palette['colors'].get('ink_light', '#6b6b6b')};
  --hairline: {palette['colors'].get('hairline', '#e8e3dc')};
  --accent: {palette['colors'].get('accent', '#c45a3c')};
  --font-serif: 'Instrument Serif', 'Newsreader', Georgia, serif;
  --font-sans: 'Suisse Int\\'l', 'Inter Tight', system-ui, sans-serif;
  --font-mono: 'Fragment Mono', 'IBM Plex Mono', monospace;
  --radius-none: 0px;
  --radius-sm: 2px;
  --hairline: 0.5px solid var(--hairline);
}}
* {{ border-radius: 0; }}
body {{ background: var(--paper); color: var(--ink); font-family: var(--font-sans); }}
h1,h2 {{ font-family: var(--font-serif); font-weight: 400; letter-spacing: -0.02em; line-height: 0.95; }}
""",
        "tailwind_config": f"""
// tailwind.config.js - Sophisticated, non-AI
module.exports = {{
  theme: {{
    extend: {{
      colors: {{
        paper: '{palette['colors'].get('paper', '#fdfcfa')}',
        ink: '{palette['colors'].get('ink', '#121212')}',
        hairline: '{palette['colors'].get('hairline', '#e8e3dc')}',
        accent: '{palette['colors'].get('accent', '#c45a3c')}',
      }},
      fontFamily: {{
        serif: ['Instrument Serif', 'Newsreader', 'serif'],
        sans: ['Suisse Int\\'l', 'Inter Tight', 'sans-serif'],
        mono: ['Fragment Mono', 'monospace'],
      }},
      borderRadius: {{ NONE: '0', sm: '2px' }}, // No 2xl
      boxShadow: {{ none: 'none' }}, // No shadows
    }}
  }}
}}
""",
        "checklist": [
            "影を使っていないか？ → hairlineに",
            "角丸が24pxになっていないか？ → 0-4pxに",
            "紫→青グラデを使っていないか？ → 単色に",
            "中央揃えばかりでないか？ → 左揃え基本に",
            "余白が80pxで詰めていないか？ → 160pxに",
            "Interだけでないか？ → セリフを1つ入れる",
            "✨やMagicという言葉を使っていないか？ → 具体的な動詞に",
            "3列アイコン並びでないか？ → 1列 + 詳細に",
        ]
    }

def tool_critique_ai_look(design_description: str) -> Dict[str, Any]:
    """
    AIっぽいデザインを批評し、洗練された代替案を提示
    """
    desc_lower = design_description.lower()
    
    detected_tropes = []
    for trope in AI_TROPES_TO_AVOID:
        # Simple keyword matching
        if any(keyword in desc_lower for keyword in trope["trope"].lower().split()):
            detected_tropes.append(trope)
        # Check for common AI words
        if "gradient" in desc_lower and "gradient" in trope["trope"].lower():
            if trope not in detected_tropes:
                detected_tropes.append(trope)
        if "rounded" in desc_lower and "rounded" in trope["trope"].lower():
            if trope not in detected_tropes:
                detected_tropes.append(trope)
    
    # If no specific detection, give general critique
    if not detected_tropes:
        detected_tropes = AI_TROPES_TO_AVOID[:3]
    
    suggestions = []
    for trope in detected_tropes:
        suggestions.append({
            "issue": trope["trope"],
            "why_ai": trope["why"],
            "fix": trope["instead"],
            "severity": "高" if "gradient" in trope["trope"].lower() or "rounded" in trope["trope"].lower() else "中"
        })
    
    return {
        "input": design_description,
        "detected_ai_tropes": detected_tropes,
        "suggestions": suggestions,
        "sophisticated_alternative": {
            "palette": SOPHISTICATED_PALETTES["paper_ink"],
            "typography": SOPHISTICATED_TYPOGRAPHY["editorial"],
            "quick_fixes": [
                "背景を #fdfcfa (紙色) に",
                "角丸を 0px に",
                "影を消して 0.5px border に",
                "見出しをセリフ体 (Instrument Serif) に",
                "セクション間を 160px に",
                "CTAを1つに減らし、左に寄せる",
                "中央揃えを左揃えに",
            ]
        },
        "before_after": {
            "before": "紫グラデ背景 + 丸いカード + 影 + Inter + 中央揃え + ✨",
            "after": "紙色背景 + 0px角 + hairline + セリフ見出し + 左揃え + 160px余白"
        }
    }
