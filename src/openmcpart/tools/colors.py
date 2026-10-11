"""
Color-related tools
"""
from typing import Dict, Any
from ..utils.color_utils import (
    hex_to_rgb,
    rgb_to_hex,
    rgb_to_hsl,
    contrast_ratio,
    wcag_level,
    generate_harmony,
    generate_palette_from_mood,
    simulate_color_blindness,
    hsl_to_hex,
)

def tool_generate_color_palette(
    base_color: str = None,
    mood: str = None,
    harmony: str = "complementary",
    count: int = 5,
) -> Dict[str, Any]:
    """Generate a deterministic palette with exactly ``count`` selected colors."""
    if not 2 <= count <= 10:
        return {"error": "count must be between 2 and 10"}

    valid_harmonies = {"complementary", "analogous", "triadic", "tetradic", "split", "split-complementary", "monochromatic"}
    if harmony.lower() not in valid_harmonies:
        return {"error": f"Unsupported harmony: {harmony}. Choose from {sorted(valid_harmonies)}"}

    if base_color:
        try:
            red, green, blue = hex_to_rgb(base_color)
            hue, saturation, lightness = rgb_to_hsl(red, green, blue)
        except (AttributeError, TypeError, ValueError) as exc:
            return {"error": f"Invalid base_color {base_color}: {exc}"}

        base = rgb_to_hex(red, green, blue)
        harmonies = list(dict.fromkeys([base] + generate_harmony(base, harmony)))
        tints = [hsl_to_hex(hue, saturation, min(95, lightness + step * 12)) for step in range(1, 4)]
        shades = [hsl_to_hex(hue, saturation, max(8, lightness - step * 12)) for step in range(1, 4)]
        candidates = list(dict.fromkeys(harmonies + tints + shades))
        for candidate_lightness in range(8, 96, 7):
            candidate = hsl_to_hex(hue, saturation, candidate_lightness)
            if candidate not in candidates:
                candidates.append(candidate)
            if len(candidates) >= count:
                break
        selected = candidates[:count]
        result = {
            "base_color": base,
            "harmony_type": harmony.lower(),
            "harmony_colors": harmonies,
            "tints": tints,
            "shades": shades,
            "full_palette": selected,
            "usage": {
                "primary": base,
                "secondary": selected[1],
                "accent": selected[2] if len(selected) > 2 else selected[-1],
                "background": "#ffffff",
                "surface": tints[-1] if tints else "#f5f5f5",
                "text": shades[-1] if shades else "#111111",
            },
            "css_variables": "\n".join(
                f"  --color-{index + 1}: {color};" for index, color in enumerate(selected)
            ),
        }
    else:
        default_mood_used = not bool(mood)
        result = generate_palette_from_mood(mood or "tech")
        mood_base = result["primary"]
        red, green, blue = hex_to_rgb(mood_base)
        hue, saturation, lightness = rgb_to_hsl(red, green, blue)
        harmonies = list(dict.fromkeys([mood_base] + generate_harmony(mood_base, harmony)))
        tints = [hsl_to_hex(hue, saturation, min(95, lightness + step * 12)) for step in range(1, 4)]
        shades = [hsl_to_hex(hue, saturation, max(8, lightness - step * 12)) for step in range(1, 4)]
        candidates = list(dict.fromkeys(harmonies + tints + shades))
        for candidate_lightness in range(8, 96, 7):
            candidate = hsl_to_hex(hue, saturation, candidate_lightness)
            if candidate not in candidates:
                candidates.append(candidate)
            if len(candidates) >= count:
                break
        result.update(
            {
                "harmony_type": harmony.lower(),
                "harmony_colors": harmonies,
                "tints": tints,
                "shades": shades,
                "full_palette": candidates[:count],
                "secondary": candidates[1],
                "accent": candidates[2] if count > 2 else candidates[1],
                "usage": {
                    "primary": mood_base,
                    "secondary": candidates[1],
                    "accent": candidates[2] if count > 2 else candidates[1],
                    "background": "#ffffff",
                    "surface": result["neutrals"]["100"],
                    "text": result["neutrals"]["900"],
                },
                "default_mood_used": default_mood_used,
            }
        )
        result["css_variables"] = "\n".join(
            f"  --color-{index + 1}: {color};"
            for index, color in enumerate(result["full_palette"])
        )

    result["count"] = len(result["full_palette"])
    result["requested_count"] = count
    return result

def tool_check_color_contrast(foreground: str, background: str) -> Dict[str, Any]:
    try:
        fg = rgb_to_hex(*hex_to_rgb(foreground))
        bg = rgb_to_hex(*hex_to_rgb(background))
        ratio = contrast_ratio(fg, bg)
        levels = wcag_level(ratio)
        cb_sims = {}
        for deficiency in ("deuteranopia", "protanopia", "tritanopia"):
            simulated_fg = simulate_color_blindness(fg, deficiency)
            simulated_bg = simulate_color_blindness(bg, deficiency)
            cb_sims[deficiency] = {
                "fg": simulated_fg,
                "bg": simulated_bg,
                "ratio": round(contrast_ratio(simulated_fg, simulated_bg), 2),
            }

        recommendation = (
            "Excellent contrast" if ratio >= 7 else "Good contrast" if ratio >= 4.5 else "Poor contrast - consider adjusting"
        )
        if ratio < 3:
            recommendation += ". Fails AA for all text sizes. Increase contrast."
        elif ratio < 4.5:
            recommendation += ". Passes AA for large text only. For body text, increase contrast."

        accessible_pairs = []
        candidates = [("#000000", bg), ("#ffffff", bg), (fg, "#ffffff"), (fg, "#000000")]
        seen_pairs = set()
        for candidate_fg, candidate_bg in candidates:
            pair = (candidate_fg, candidate_bg)
            candidate_ratio = contrast_ratio(candidate_fg, candidate_bg)
            if candidate_ratio >= 4.5 and pair not in seen_pairs:
                accessible_pairs.append(
                    {
                        "foreground": candidate_fg,
                        "background": candidate_bg,
                        "ratio": round(candidate_ratio, 2),
                        "wcag_aa_normal_text": True,
                    }
                )
                seen_pairs.add(pair)

        return {
            "foreground": fg,
            "background": bg,
            "ratio": round(ratio, 2),
            "wcag": levels,
            "thresholds": {"AA_normal": 4.5, "AA_large": 3.0, "AAA_normal": 7.0, "AAA_large": 4.5},
            "recommendation": recommendation,
            "color_blindness_simulation": cb_sims,
            "suggestions": {
                "if_fails": "Adjust foreground or background lightness, then verify the final rendered colors.",
                "accessible_pairs": accessible_pairs,
                "note": "Suggested pairs meet the numeric 4.5:1 AA threshold for normal text; verify actual use and color management.",
            },
        }
    except (AttributeError, TypeError, ValueError) as exc:
        return {"error": str(exc)}

def tool_generate_gradient(from_color: str, to_color: str, style: str = "linear", angle: int = 135) -> Dict[str, Any]:
    try:
        if not isinstance(angle, int) or isinstance(angle, bool) or not 0 <= angle <= 360:
            return {"error": "angle must be an integer between 0 and 360"}
        style = style.lower()
        if style not in {"linear", "radial", "conic"}:
            return {"error": "style must be linear, radial, or conic"}

        r1, g1, b1 = hex_to_rgb(from_color)
        r2, g2, b2 = hex_to_rgb(to_color)
        from_color = rgb_to_hex(r1, g1, b1)
        to_color = rgb_to_hex(r2, g2, b2)
        mid_color = rgb_to_hex((r1 + r2) // 2, (g1 + g2) // 2, (b1 + b2) // 2)

        if style == "linear":
            css = f"linear-gradient({angle}deg, {from_color}, {to_color})"
            css_with_mid = f"linear-gradient({angle}deg, {from_color}, {mid_color}, {to_color})"
            tailwind = f"bg-gradient-to-br from-[{from_color}] to-[{to_color}]"
        elif style == "radial":
            css = f"radial-gradient(circle, {from_color}, {to_color})"
            css_with_mid = f"radial-gradient(circle, {from_color}, {mid_color}, {to_color})"
            tailwind = f"bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-[{from_color}] to-[{to_color}]"
        else:
            css = f"conic-gradient(from {angle}deg, {from_color}, {to_color})"
            css_with_mid = f"conic-gradient(from {angle}deg, {from_color}, {mid_color}, {to_color})"
            tailwind = f"bg-[conic-gradient(from_{angle}deg_at_50%_50%,{from_color},{to_color})]"

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
                "The intermediate color can also be used for hover states",
            ],
        }
    except (AttributeError, TypeError, ValueError) as exc:
        return {"error": str(exc)}
