"""
Typography tools
"""
from typing import Dict, Any, List

FONT_PAIRINGS = {
    "modern_minimal": {
        "heading": "Inter",
        "body": "Inter",
        "accent": "JetBrains Mono",
        "description": "モダンでミニマル - スタートアップ、SaaSに最適",
        "google_fonts_url": "https://fonts.google.com/specimen/Inter",
        "pairing_reason": "同一ファミリーで統一感、ウェイトで階層を表現"
    },
    "elegant_luxury": {
        "heading": "Playfair Display",
        "body": "Lora",
        "accent": "Montserrat",
        "description": "エレガント・高級感 - ファッション、ジュエリー、高級ブランド",
        "google_fonts_url": "https://fonts.google.com/specimen/Playfair+Display",
        "pairing_reason": "セリフの気品とサンセリフの読みやすさの対比"
    },
    "tech_trust": {
        "heading": "Space Grotesk",
        "body": "IBM Plex Sans",
        "accent": "IBM Plex Mono",
        "description": "テクノロジー・信頼 - B2B, フィンテック",
        "google_fonts_url": "https://fonts.google.com/specimen/Space+Grotesk",
        "pairing_reason": "幾何学的で未来的、かつ高い可読性"
    },
    "friendly_warm": {
        "heading": "Poppins",
        "body": "Nunito Sans",
        "accent": "Poppins",
        "description": "フレンドリー・親しみ - 教育、ヘルスケア、コミュニティ",
        "google_fonts_url": "https://fonts.google.com/specimen/Poppins",
        "pairing_reason": "丸みを帯びた親しみやすさ"
    },
    "editorial": {
        "heading": "Merriweather",
        "body": "Source Serif Pro",
        "accent": "Source Sans Pro",
        "description": "エディトリアル・知的 - メディア、出版、ブログ",
        "google_fonts_url": "https://fonts.google.com/specimen/Merriweather",
        "pairing_reason": "長文読書に最適化されたセリフ組み合わせ"
    },
    "bold_impact": {
        "heading": "Bebas Neue",
        "body": "Roboto",
        "accent": "Oswald",
        "description": "大胆・インパクト - イベント、エンタメ、スポーツ",
        "google_fonts_url": "https://fonts.google.com/specimen/Bebas+Neue",
        "pairing_reason": "強い見出しとニュートラルな本文の対比で視線を誘導"
    },
    "japanese_modern": {
        "heading": "Noto Sans JP",
        "body": "Noto Sans JP",
        "accent": "Zen Kaku Gothic New",
        "description": "日本語モダン - 日本語サイト全般",
        "google_fonts_url": "https://fonts.google.com/specimen/Noto+Sans+JP",
        "pairing_reason": "日本語の可読性と美しさを両立"
    },
    "japanese_elegant": {
        "heading": "Shippori Mincho",
        "body": "Noto Serif JP",
        "accent": "Zen Old Mincho",
        "description": "日本語エレガント - 和ブランド、高級料亭、伝統工芸",
        "google_fonts_url": "https://fonts.google.com/specimen/Shippori+Mincho",
        "pairing_reason": "明朝体の品格と情緒"
    }
}

TYPE_SCALES = {
    "minor_second": 1.067,
    "major_second": 1.125,
    "minor_third": 1.2,
    "major_third": 1.25,
    "perfect_fourth": 1.333,
    "augmented_fourth": 1.414,
    "perfect_fifth": 1.5,
    "golden_ratio": 1.618
}

def tool_suggest_typography_pairing(mood: str = "modern_minimal", industry: str = None, language: str = "en") -> Dict[str, Any]:
    mood = mood.lower()
    # fuzzy matching
    best_match = None
    for key in FONT_PAIRINGS:
        if mood in key or key in mood:
            best_match = key
            break
    
    # industry mapping
    if not best_match and industry:
        industry = industry.lower()
        mapping = {
            "tech": "tech_trust",
            "saas": "modern_minimal",
            "fashion": "elegant_luxury",
            "luxury": "elegant_luxury",
            "finance": "tech_trust",
            "education": "friendly_warm",
            "health": "friendly_warm",
            "media": "editorial",
            "blog": "editorial",
            "event": "bold_impact",
            "sport": "bold_impact",
            "japan": "japanese_modern",
            "japanese": "japanese_modern",
        }
        for k, v in mapping.items():
            if k in industry:
                best_match = v
                break
    
    if language and "ja" in language.lower() or "japanese" in language.lower():
        if "elegant" in mood or "luxury" in mood:
            best_match = "japanese_elegant"
        else:
            best_match = "japanese_modern"
    
    if not best_match:
        best_match = "modern_minimal"
    
    pairing = FONT_PAIRINGS[best_match]
    
    # Generate type scale
    base_size = 16
    scale_ratio = TYPE_SCALES["major_third"] if "minimal" in best_match else TYPE_SCALES["perfect_fourth"]
    
    scale = {}
    sizes = ["xs", "sm", "base", "lg", "xl", "2xl", "3xl", "4xl", "5xl"]
    # base is 16px
    current = base_size / (scale_ratio * scale_ratio)  # start smaller
    for size_name in sizes:
        scale[size_name] = f"{round(current)}px / {round(current*1.5)}px"
        current *= scale_ratio
        if size_name == "base":
            current = base_size * scale_ratio
    
    # More precise scale
    detailed_scale = {
        "xs": {"fontSize": "12px", "lineHeight": "16px", "usage": "キャプション、ラベル"},
        "sm": {"fontSize": "14px", "lineHeight": "20px", "usage": "補助テキスト、メタ情報"},
        "base": {"fontSize": "16px", "lineHeight": "24px", "usage": "本文、標準"},
        "lg": {"fontSize": "18px", "lineHeight": "28px", "usage": "リード文、強調"},
        "xl": {"fontSize": "20px", "lineHeight": "28px", "usage": "小見出し"},
        "2xl": {"fontSize": "24px", "lineHeight": "32px", "usage": "セクション見出し"},
        "3xl": {"fontSize": "30px", "lineHeight": "36px", "usage": "ページ見出し"},
        "4xl": {"fontSize": "36px", "lineHeight": "40px", "usage": "ヒーロー見出し"},
        "5xl": {"fontSize": "48px", "lineHeight": "48px", "usage": "特大見出し、ランディング"},
    }
    
    return {
        "requested_mood": mood,
        "matched_style": best_match,
        "pairing": pairing,
        "type_scale": detailed_scale,
        "scale_ratio": scale_ratio,
        "scale_name": [k for k, v in TYPE_SCALES.items() if v == scale_ratio][0] if scale_ratio in TYPE_SCALES.values() else "custom",
        "recommendations": {
            "line_height": "本文 1.5-1.7, 見出し 1.1-1.3",
            "letter_spacing": "見出し -0.02em, 本文 0, 大文字 0.05em",
            "max_line_length": "45-75文字 (日本語 35-45文字)",
            "font_weights": "400 regular, 500 medium, 700 bold の3ウェイトに絞る",
        },
        "css_import": f"@import url('https://fonts.googleapis.com/css2?family={pairing['heading'].replace(' ', '+')}:wght@400;500;700&family={pairing['body'].replace(' ', '+')}:wght@400;500&display=swap');",
        "tailwind_config": f"""
fontFamily: {{
  heading: ['{pairing['heading']}', 'sans-serif'],
  body: ['{pairing['body']}', 'sans-serif'],
  mono: ['{pairing['accent']}', 'monospace'],
}}
"""
    }

def tool_generate_type_scale(base_size: int = 16, ratio: str = "major_third",) -> Dict[str, Any]:
    ratio_value = TYPE_SCALES.get(ratio, TYPE_SCALES["major_third"])
    
    # Generate scale both up and down
    scale_steps = [
        ("xs", -2),
        ("sm", -1),
        ("base", 0),
        ("lg", 1),
        ("xl", 2),
        ("2xl", 3),
        ("3xl", 4),
        ("4xl", 5),
        ("5xl", 6),
        ("6xl", 7),
    ]
    
    result = {}
    for name, step in scale_steps:
        size = base_size * (ratio_value ** step)
        # line height heuristic
        if size < 18:
            lh = 1.6
        elif size < 24:
            lh = 1.5
        elif size < 36:
            lh = 1.3
        else:
            lh = 1.1
        result[name] = {
            "fontSize": f"{round(size, 1)}px",
            "fontSizeRem": f"{round(size/16, 3)}rem",
            "lineHeight": f"{round(size*lh)}px",
            "lineHeightRatio": lh,
        }
    
    return {
        "base_size": base_size,
        "ratio_name": ratio,
        "ratio_value": ratio_value,
        "scale": result,
        "css_variables": "\n".join([f"  --text-{k}: {v['fontSizeRem']};" for k, v in result.items()]),
        "available_ratios": TYPE_SCALES,
    }
