"""
Color-related tools
"""
from typing import List, Dict, Any
from ..utils.color_utils import (
    hex_to_rgb,
    rgb_to_hex,
    rgb_to_hsl,
    hsl_to_rgb,
    contrast_ratio,
    wcag_level,
    generate_harmony,
    generate_palette_from_mood,
    simulate_color_blindness,
    hsl_to_hex,
)

def tool_generate_color_palette(base_color: str = None, mood: str = None, harmony: str = "complementary", count: int = 5) -> Dict[str, Any]:
    """
    Generate color palette from base color or mood.
    """
    result = {}
    if base_color:
        try:
            r, g, b = hex_to_rgb(base_color)
            h, s, l = rgb_to_hsl(r, g, b)
        except Exception as e:
            return {"error": f"Invalid base_color {base_color}: {e}"}
        
        harmonies = generate_harmony(base_color, harmony)
        
        # Generate tints/shades for depth
        tints = [hsl_to_hex(h, s, min(95, l + i*12)) for i in range(1, 4)]
        shades = [hsl_to_hex(h, s, max(8, l - i*12)) for i in range(1, 4)]
        
        result = {
            "base_color": base_color,
            "harmony_type": harmony,
            "harmony_colors": harmonies,
            "tints": tints,
            "shades": shades,
            "full_palette": list(dict.fromkeys(harmonies + tints + shades)),  # dedup preserve order
            "usage": {
                "primary": harmonies[0] if harmonies else base_color,
                "secondary": harmonies[1] if len(harmonies) > 1 else tints[0],
                "accent": harmonies[-1] if len(harmonies) > 2 else shades[0],
                "background": "#ffffff",
                "surface": tints[-1] if tints else "#f5f5f5",
                "text": shades[-1] if shades else "#111111"
            },
            "css_variables": "\n".join([f"  --color-{i}: {c};" for i, c in enumerate(harmonies + tints[:2] + shades[:2])])
        }
    elif mood:
        palette = generate_palette_from_mood(mood)
        result = palette
        result["css_variables"] = f"""
  --color-primary: {palette['primary']};
  --color-secondary: {palette['secondary']};
  --color-accent: {palette['accent']};
  --color-neutral-900: {palette['neutrals']['900']};
  --color-neutral-100: {palette['neutrals']['100']};
"""
    else:
        return {"error": "Either base_color or mood must be provided"}
    
    result["count"] = len(result.get("full_palette", []))
    return result

def tool_check_color_contrast(foreground: str, background: str) -> Dict[str, Any]:
    try:
        ratio = contrast_ratio(foreground, background)
        levels = wcag_level(ratio)
        # color blindness simulation
        cb_sims = {
            "deuteranopia": {
                "fg": simulate_color_blindness(foreground, "deuteranopia"),
                "bg": simulate_color_blindness(background, "deuteranopia"),
                "ratio": contrast_ratio(simulate_color_blindness(foreground, "deuteranopia"), simulate_color_blindness(background, "deuteranopia"))
            },
            "protanopia": {
                "fg": simulate_color_blindness(foreground, "protanopia"),
                "bg": simulate_color_blindness(background, "protanopia"),
                "ratio": contrast_ratio(simulate_color_blindness(foreground, "protanopia"), simulate_color_blindness(background, "protanopia"))
            },
            "tritanopia": {
                "fg": simulate_color_blindness(foreground, "tritanopia"),
                "bg": simulate_color_blindness(background, "tritanopia"),
                "ratio": contrast_ratio(simulate_color_blindness(foreground, "tritanopia"), simulate_color_blindness(background, "tritanopia"))
            }
        }
        
        recommendation = "Excellent contrast" if ratio >= 7 else "Good contrast" if ratio >= 4.5 else "Poor contrast - consider adjusting"
        if ratio < 3:
            recommendation += ". Fails AA for all text sizes. Increase contrast."
        elif ratio < 4.5:
            recommendation += ". Passes AA for large text only. For body text, increase contrast."
        
        return {
            "foreground": foreground,
            "background": background,
            "ratio": round(ratio, 2),
            "wcag": levels,
            "recommendation": recommendation,
            "color_blindness_simulation": cb_sims,
            "suggestions": {
                "if_fails": "Try darkening the darker color or lightening the lighter color. Adjust lightness by 10-15%.",
                "accessible_pairs": [
                    f"{foreground} on #ffffff: {round(contrast_ratio(foreground, '#ffffff'), 2)}",
                    f"{foreground} on #000000: {round(contrast_ratio(foreground, '#000000'), 2)}",
                ]
            }
        }
    except Exception as e:
        return {"error": str(e)}

def tool_generate_gradient(from_color: str, to_color: str, style: str = "linear", angle: int = 135) -> Dict[str, Any]:
    try:
        # Validate colors
        hex_to_rgb(from_color)
        hex_to_rgb(to_color)
        
        if style == "linear":
            css = f"linear-gradient({angle}deg, {from_color}, {to_color})"
            tailwind = f"bg-gradient-to-br from-[{from_color}] to-[{to_color}]"
        elif style == "radial":
            css = f"radial-gradient(circle, {from_color}, {to_color})"
            tailwind = f"bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-[{from_color}] to-[{to_color}]"
        elif style == "conic":
            css = f"conic-gradient(from {angle}deg, {from_color}, {to_color})"
            tailwind = f"bg-[conic-gradient(from_{angle}deg_at_50%_50%,{from_color},{to_color})]"
        else:
            css = f"linear-gradient({angle}deg, {from_color}, {to_color})"
            tailwind = f"bg-gradient-to-br from-[{from_color}] to-[{to_color}]"
        
        # Generate intermediate stops
        r1, g1, b1 = hex_to_rgb(from_color)
        r2, g2, b2 = hex_to_rgb(to_color)
        mid_r = (r1 + r2) // 2
        mid_g = (g1 + g2) // 2
        mid_b = (b1 + b2) // 2
        mid_color = rgb_to_hex(mid_r, mid_g, mid_b)
        
        css_with_mid = f"linear-gradient({angle}deg, {from_color}, {mid_color}, {to_color})"
        
        return {
            "from": from_color,
            "to": to_color,
            "mid": mid_color,
            "style": style,
            "angle": angle,
            "css": {
                "simple": css,
                "with_mid": css_with_mid,
                "as_background": f"background: {css};",
            },
            "tailwind": tailwind,
            "usage_tips": [
                "Use gradients sparingly for CTAs and hero sections",
                "Ensure text over gradient has sufficient contrast (add overlay if needed)",
                "Mid color can be used for hover states"
            ]
        }
    except Exception as e:
        return {"error": str(e)}
