"""
Color utilities for design MCP server.
"""
import colorsys
import math
import re
from typing import Tuple, List, Dict


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    hex_color = hex_color.strip().lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])
    if len(hex_color) != 6:
        raise ValueError(f"Invalid hex color: {hex_color}")
    return (
        int(hex_color[0:2], 16),
        int(hex_color[2:4], 16),
        int(hex_color[4:6], 16),
    )

def rgb_to_hex(r: int, g: int, b: int) -> str:
    return f"#{r:02x}{g:02x}{b:02x}"

def rgb_to_hsl(r: int, g: int, b: int) -> Tuple[float, float, float]:
    r_, g_, b_ = r/255.0, g/255.0, b/255.0
    h, l, s = colorsys.rgb_to_hls(r_, g_, b_)
    # colorsys uses HLS, convert to HSL: H is same, L is same, S is same but HLS order is different
    return (h*360, s*100, l*100)

def hsl_to_rgb(h: float, s: float, l: float) -> Tuple[int, int, int]:
    h_ = (h % 360) / 360.0
    s_ = max(0, min(100, s)) / 100.0
    l_ = max(0, min(100, l)) / 100.0
    r_, g_, b_ = colorsys.hls_to_rgb(h_, l_, s_)
    return (int(round(r_*255)), int(round(g_*255)), int(round(b_*255)))

def hsl_to_hex(h: float, s: float, l: float) -> str:
    r, g, b = hsl_to_rgb(h, s, l)
    return rgb_to_hex(r, g, b)

def relative_luminance(r: int, g: int, b: int) -> float:
    def linearize(c):
        c = c / 255.0
        return c/12.92 if c <= 0.04045 else ((c+0.055)/1.055) ** 2.4
    return 0.2126*linearize(r) + 0.7152*linearize(g) + 0.0722*linearize(b)

def contrast_ratio(hex1: str, hex2: str) -> float:
    r1, g1, b1 = hex_to_rgb(hex1)
    r2, g2, b2 = hex_to_rgb(hex2)
    l1 = relative_luminance(r1, g1, b1)
    l2 = relative_luminance(r2, g2, b2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)

def wcag_level(ratio: float) -> Dict[str, bool]:
    return {
        "AA_normal": ratio >= 4.5,
        "AA_large": ratio >= 3.0,
        "AAA_normal": ratio >= 7.0,
        "AAA_large": ratio >= 4.5,
    }

def generate_harmony(base_hex: str, harmony_type: str) -> List[str]:
    """
    harmony_type: complementary, analogous, triadic, tetradic, split, monochromatic
    """
    r, g, b = hex_to_rgb(base_hex)
    h, s, l = rgb_to_hsl(r, g, b)
    palettes = []
    harmony_type = harmony_type.lower()
    
    if harmony_type == "complementary":
        palettes = [h, (h+180)%360]
    elif harmony_type == "analogous":
        palettes = [(h-30)%360, h, (h+30)%360]
    elif harmony_type == "triadic":
        palettes = [h, (h+120)%360, (h+240)%360]
    elif harmony_type == "tetradic":
        palettes = [h, (h+90)%360, (h+180)%360, (h+270)%360]
    elif harmony_type in ("split", "split-complementary"):
        palettes = [h, (h+150)%360, (h+210)%360]
    elif harmony_type == "monochromatic":
        # vary lightness
        return [
            hsl_to_hex(h, s, max(10, l-30)),
            hsl_to_hex(h, s, max(10, l-15)),
            hsl_to_hex(h, s, l),
            hsl_to_hex(h, s, min(90, l+15)),
            hsl_to_hex(h, s, min(95, l+30)),
        ]
    else:
        # default complementary
        palettes = [h, (h+180)%360]
    
    result = []
    for hue in palettes:
        result.append(hsl_to_hex(hue, s, l))
    return result

def generate_palette_from_mood(mood: str) -> Dict:
    """
    Map mood keywords to base hue ranges and generate palette.
    """
    mood = mood.lower()
    mood_map = {
        "energetic": {"hue": 15, "s": 90, "l": 60, "desc": "情熱的・活動的 - 赤オレンジ系"},
        "calm": {"hue": 200, "s": 60, "l": 65, "desc": "穏やか・安心 - ブルー系"},
        "luxury": {"hue": 280, "s": 40, "l": 25, "desc": "高級・洗練 - 深いパープル"},
        "natural": {"hue": 120, "s": 35, "l": 55, "desc": "自然・オーガニック - グリーン系"},
        "playful": {"hue": 50, "s": 95, "l": 65, "desc": "楽しい・遊び心 - イエロー系"},
        "minimal": {"hue": 0, "s": 0, "l": 90, "desc": "ミニマル・清潔 - ニュートラル"},
        "tech": {"hue": 220, "s": 80, "l": 55, "desc": "テクノロジー・信頼 - インディゴ"},
        "warm": {"hue": 30, "s": 80, "l": 60, "desc": "暖かみ・親しみ - オレンジ系"},
        "cool": {"hue": 180, "s": 50, "l": 60, "desc": "クール・知的 - ティール"},
        "elegant": {"hue": 340, "s": 30, "l": 30, "desc": "エレガント・上品 - ローズウッド"},
        "vibrant": {"hue": 320, "s": 85, "l": 60, "desc": "鮮やか・大胆 - マゼンタ"},
        "earthy": {"hue": 25, "s": 45, "l": 45, "desc": "アーシー・温もり - ブラウン系"},
    }
    # fuzzy match
    base = None
    for key, val in mood_map.items():
        if key in mood or mood in key:
            base = val
            break
    if not base:
        # default to tech
        base = mood_map["tech"]
    
    h, s, l = base["hue"], base["s"], base["l"]
    # generate full palette
    primary = hsl_to_hex(h, s, l)
    secondary = hsl_to_hex((h+30)%360, s*0.8, l)
    accent = hsl_to_hex((h+180)%360, min(100, s*1.1), l)
    neutral_dark = hsl_to_hex(h, 10, 20)
    neutral_light = hsl_to_hex(h, 10, 95)
    neutral_mid = hsl_to_hex(h, 8, 70)
    
    # tints and shades
    tints = [hsl_to_hex(h, s, min(95, l + i*10)) for i in range(1, 4)]
    shades = [hsl_to_hex(h, s, max(10, l - i*12)) for i in range(1, 4)]
    
    return {
        "mood": mood,
        "description": base["desc"],
        "primary": primary,
        "secondary": secondary,
        "accent": accent,
        "neutrals": {
            "900": neutral_dark,
            "500": neutral_mid,
            "100": neutral_light,
            "white": "#ffffff",
            "black": "#111111"
        },
        "tints": tints,
        "shades": shades,
        "full_palette": [primary, secondary, accent] + tints + shades + [neutral_dark, neutral_mid, neutral_light]
    }

def simulate_color_blindness(hex_color: str, cb_type: str = "deuteranopia") -> str:
    """
    Simple matrix approximation for color blindness simulation.
    """
    r, g, b = hex_to_rgb(hex_color)
    r_f, g_f, b_f = r/255.0, g/255.0, b/255.0
    
    # Simplified matrices
    if cb_type == "deuteranopia":  # green weak
        r2 = 0.625*r_f + 0.375*g_f
        g2 = 0.7*r_f + 0.3*g_f
        b2 = 0.3*g_f + 0.7*b_f
    elif cb_type == "protanopia":  # red weak
        r2 = 0.567*r_f + 0.433*g_f
        g2 = 0.558*r_f + 0.442*g_f
        b2 = 0.242*g_f + 0.758*b_f
    elif cb_type == "tritanopia":  # blue weak
        r2 = 0.95*r_f + 0.05*g_f
        g2 = 0.0*r_f + 0.433*g_f + 0.567*b_f
        b2 = 0.0*r_f + 0.475*g_f + 0.525*b_f
    else:
        r2, g2, b2 = r_f, g_f, b_f
    
    r2 = max(0, min(1, r2))
    g2 = max(0, min(1, g2))
    b2 = max(0, min(1, b2))
    return rgb_to_hex(int(r2*255), int(g2*255), int(b2*255))
