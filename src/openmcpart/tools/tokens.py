"""Design-token generation with portable, resolved color values."""

import json
from typing import Any, Dict

from ..utils.color_utils import hex_to_rgb, rgb_to_hex

COLOR_STEPS = ("50", "100", "200", "300", "400", "500", "600", "700", "800", "900")
WHITE_MIX = {"50": 0.94, "100": 0.88, "200": 0.76, "300": 0.60, "400": 0.35}
BLACK_MIX = {"600": 0.15, "700": 0.30, "800": 0.45, "900": 0.60}


def _normalize_hex(value: str, field_name: str) -> str:
    try:
        red, green, blue = hex_to_rgb(value)
    except (AttributeError, TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be a 3- or 6-digit hex color: {exc}") from exc
    return rgb_to_hex(red, green, blue)


def _mix_with(hex_color: str, target: str, amount: float) -> str:
    source_rgb = hex_to_rgb(hex_color)
    target_rgb = hex_to_rgb(target)
    channels = [
        round(start * (1 - amount) + end * amount)
        for start, end in zip(source_rgb, target_rgb)
    ]
    return rgb_to_hex(*channels)


def _color_ramp(base: str) -> Dict[str, str]:
    ramp = {step: _mix_with(base, "#ffffff", amount) for step, amount in WHITE_MIX.items()}
    ramp["500"] = base
    ramp.update({step: _mix_with(base, "#000000", amount) for step, amount in BLACK_MIX.items()})
    return {step: ramp[step] for step in COLOR_STEPS}


def _css_font_family(value: str) -> str:
    """Escape user-supplied font names before embedding them in a CSS string."""
    cleaned = " ".join(value.replace("\r", " ").replace("\n", " ").split())
    return cleaned.replace("\\", "\\\\").replace("'", "\\'")


def _dtcg_color_group(group: Dict[str, str]) -> Dict[str, Dict[str, str]]:
    return {name: {"$type": "color", "$value": value} for name, value in group.items()}


def tool_generate_design_tokens(
    primary_color: str = "#3b82f6",
    secondary_color: str = "#8b5cf6",
    neutral_color: str = "#6b7280",
    font_heading: str = "Inter",
    font_body: str = "Inter",
    radius: str = "medium",
    brand_name: str = "MyBrand",
) -> Dict[str, Any]:
    """Generate CSS, Tailwind, JSON, and DTCG-style token representations."""
    radius_map = {
        "none": {"sm": "0px", "md": "0px", "lg": "0px", "full": "9999px"},
        "small": {"sm": "4px", "md": "6px", "lg": "8px", "full": "9999px"},
        "medium": {"sm": "6px", "md": "8px", "lg": "12px", "full": "9999px"},
        "large": {"sm": "8px", "md": "12px", "lg": "16px", "full": "9999px"},
        "full": {"sm": "12px", "md": "16px", "lg": "24px", "full": "9999px"},
    }
    if radius not in radius_map:
        return {"error": f"Unsupported radius: {radius}. Choose from {sorted(radius_map)}"}
    if not font_heading.strip() or not font_body.strip():
        return {"error": "font_heading and font_body must not be empty"}

    try:
        primary = _normalize_hex(primary_color, "primary_color")
        secondary = _normalize_hex(secondary_color, "secondary_color")
        neutral = _normalize_hex(neutral_color, "neutral_color")
    except ValueError as exc:
        return {"error": str(exc)}

    colors = {
        "primary": _color_ramp(primary),
        "secondary": _color_ramp(secondary),
        "neutral": _color_ramp(neutral),
        "semantic": {
            "background": "#ffffff",
            "surface": _color_ramp(neutral)["50"],
            "text": _color_ramp(neutral)["900"],
            "textSecondary": _color_ramp(neutral)["600"],
            "border": _color_ramp(neutral)["200"],
            "success": "#10b981",
            "warning": "#f59e0b",
            "error": "#ef4444",
            "info": primary,
        },
    }
    radii = radius_map[radius]
    safe_heading = _css_font_family(font_heading)
    safe_body = _css_font_family(font_body)
    safe_brand = " ".join(brand_name.replace("\r", " ").replace("\n", " ").split()).replace("*/", "* /")

    tokens: Dict[str, Any] = {
        "brand": safe_brand,
        "color": colors,
        "typography": {
            "fontFamily": {
                "heading": font_heading,
                "body": font_body,
                "mono": "JetBrains Mono, monospace",
            },
            "fontSize": {
                "xs": "0.75rem",
                "sm": "0.875rem",
                "base": "1rem",
                "lg": "1.125rem",
                "xl": "1.25rem",
                "2xl": "1.5rem",
                "3xl": "1.875rem",
                "4xl": "2.25rem",
                "5xl": "3rem",
            },
            "fontWeight": {"regular": 400, "medium": 500, "semibold": 600, "bold": 700},
            "lineHeight": {"tight": 1.1, "snug": 1.2, "normal": 1.5, "relaxed": 1.625, "loose": 2},
        },
        "spacing": {
            "0": "0px",
            "1": "4px",
            "2": "8px",
            "3": "12px",
            "4": "16px",
            "5": "20px",
            "6": "24px",
            "8": "32px",
            "10": "40px",
            "12": "48px",
            "16": "64px",
            "20": "80px",
            "24": "96px",
            "32": "128px",
        },
        "radius": radii,
        "shadow": {
            "none": "none",
            "xs": "0 1px 2px rgba(0,0,0,0.05)",
            "sm": "0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06)",
            "md": "0 4px 6px rgba(0,0,0,0.07), 0 2px 4px rgba(0,0,0,0.06)",
            "lg": "0 10px 15px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.05)",
            "xl": "0 20px 25px rgba(0,0,0,0.1), 0 10px 10px rgba(0,0,0,0.04)",
            "inner": "inset 0 2px 4px rgba(0,0,0,0.06)",
        },
        "breakpoint": {"sm": "640px", "md": "768px", "lg": "1024px", "xl": "1280px", "2xl": "1536px"},
    }

    css_vars = [":root {", f"  /* Brand: {safe_brand} */"]
    for group_name in ("primary", "secondary", "neutral"):
        for step, value in colors[group_name].items():
            css_vars.append(f"  --color-{group_name}-{step}: {value};")
    for name, value in colors["semantic"].items():
        css_vars.append(f"  --color-{name}: {value};")
    for name, value in radii.items():
        css_vars.append(f"  --radius-{name}: {value};")
    css_vars.extend(
        [
            f"  --font-heading: '{safe_heading}', sans-serif;",
            f"  --font-body: '{safe_body}', sans-serif;",
            "}",
        ]
    )

    tailwind_config = {
        "theme": {
            "extend": {
                "colors": {
                    "primary": colors["primary"],
                    "secondary": colors["secondary"],
                    "neutral": colors["neutral"],
                    **colors["semantic"],
                },
                "fontFamily": {"heading": [font_heading], "body": [font_body]},
                "borderRadius": radii,
            }
        }
    }
    dtcg = {
        "$schema": "https://design-tokens.github.io/community-group/format/",
        "color": {
            "primary": _dtcg_color_group(colors["primary"]),
            "secondary": _dtcg_color_group(colors["secondary"]),
            "neutral": _dtcg_color_group(colors["neutral"]),
            "semantic": _dtcg_color_group(colors["semantic"]),
        },
        "radius": {name: {"$type": "dimension", "$value": value} for name, value in radii.items()},
        "spacing": {
            name: {"$type": "dimension", "$value": value}
            for name, value in tokens["spacing"].items()
        },
        "typography": {
            "fontFamily": {
                "heading": {"$type": "fontFamily", "$value": [font_heading]},
                "body": {"$type": "fontFamily", "$value": [font_body]},
            },
            "fontSize": {
                name: {"$type": "dimension", "$value": value}
                for name, value in tokens["typography"]["fontSize"].items()
            },
            "fontWeight": {
                name: {"$type": "fontWeight", "$value": value}
                for name, value in tokens["typography"]["fontWeight"].items()
            },
            "lineHeight": {
                name: {"$type": "number", "$value": value}
                for name, value in tokens["typography"]["lineHeight"].items()
            },
        },
        "breakpoint": {
            name: {"$type": "dimension", "$value": value}
            for name, value in tokens["breakpoint"].items()
        },
    }

    return {
        "tokens": tokens,
        "css_variables": "\n".join(css_vars),
        "tailwind_config_js": f"// tailwind.config.js\nmodule.exports = {json.dumps(tailwind_config, indent=2, ensure_ascii=False)}",
        "json": json.dumps(tokens, indent=2, ensure_ascii=False),
        "dtcg_json": json.dumps(dtcg, indent=2, ensure_ascii=False),
        "usage": {
            "figma": "DTCG-style JSONを出力します。インポート前に利用するFigmaプラグインの対応形式を確認してください。",
            "style_dictionary": "CSS変数またはDTCG-style JSONを入力として利用できます。",
            "css": "CSS変数としてそのまま利用可能です。",
            "tailwind": "tailwind_config_jsはTailwind config向けのJavaScriptオブジェクトを含みます。",
        },
    }


def tool_generate_tailwind_config(primary: str = "#3b82f6", style: str = "modern") -> Dict[str, Any]:
    """Generate a Tailwind CSS config fragment with validated brand color."""
    configs = {
        "modern": {
            "borderRadius": {"DEFAULT": "0.5rem", "lg": "0.75rem", "full": "9999px"},
            "boxShadow": {"soft": "0 2px 10px rgba(0,0,0,0.05)", "medium": "0 4px 20px rgba(0,0,0,0.08)"},
            "fontFamily": {"sans": ["Inter", "sans-serif"]},
        },
        "playful": {
            "borderRadius": {"DEFAULT": "1rem", "lg": "1.5rem", "full": "9999px"},
            "boxShadow": {"soft": "0 4px 20px rgba(0,0,0,0.08)", "medium": "0 8px 30px rgba(0,0,0,0.12)"},
            "fontFamily": {"sans": ["Poppins", "sans-serif"]},
        },
        "elegant": {
            "borderRadius": {"DEFAULT": "0.25rem", "lg": "0.5rem", "full": "9999px"},
            "boxShadow": {"soft": "0 1px 3px rgba(0,0,0,0.1)", "medium": "0 4px 12px rgba(0,0,0,0.08)"},
            "fontFamily": {"sans": ["Playfair Display", "serif"]},
        },
    }
    if style not in configs:
        return {"error": f"Unsupported style: {style}. Choose from {sorted(configs)}"}
    try:
        primary = _normalize_hex(primary, "primary")
    except ValueError as exc:
        return {"error": str(exc)}

    chosen = configs[style]
    config = {
        "content": ["./src/**/*.{js,ts,jsx,tsx}"],
        "theme": {
            "extend": {
                "colors": {"primary": _color_ramp(primary)},
                "borderRadius": chosen["borderRadius"],
                "boxShadow": chosen["boxShadow"],
                "fontFamily": chosen["fontFamily"],
                "spacing": {"18": "4.5rem", "22": "5.5rem"},
                "animation": {"fade-in": "fadeIn 0.5s ease-out", "slide-up": "slideUp 0.3s ease-out"},
            }
        },
        "plugins": [],
    }
    config_str = "/** @type {import('tailwindcss').Config} */\nmodule.exports = " + json.dumps(config, indent=2)
    return {
        "primary": primary,
        "style": style,
        "config": config_str,
        "install": "npm install -D tailwindcss postcss autoprefixer && npx tailwindcss init -p",
        "tips": [
            "パレットは実際のHEX値として出力され、color-mixに依存しません。",
            "スタイルに応じた角丸・影・フォントを生成します。",
            "出力configは利用中のTailwindメジャーバージョンで確認してください。",
        ],
    }
