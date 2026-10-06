"""
Design tokens tools
"""
from typing import Dict, Any, List
import json

def tool_generate_design_tokens(
    primary_color: str = "#3b82f6",
    secondary_color: str = "#8b5cf6",
    neutral_color: str = "#6b7280",
    font_heading: str = "Inter",
    font_body: str = "Inter",
    radius: str = "medium",
    brand_name: str = "MyBrand"
) -> Dict[str, Any]:
    
    radius_map = {
        "none": {"sm": "0px", "md": "0px", "lg": "0px", "full": "9999px"},
        "small": {"sm": "4px", "md": "6px", "lg": "8px", "full": "9999px"},
        "medium": {"sm": "6px", "md": "8px", "lg": "12px", "full": "9999px"},
        "large": {"sm": "8px", "md": "12px", "lg": "16px", "full": "9999px"},
        "full": {"sm": "12px", "md": "16px", "lg": "24px", "full": "9999px"},
    }
    radii = radius_map.get(radius, radius_map["medium"])
    
    tokens = {
        "brand": brand_name,
        "color": {
            "primary": {
                "50": f"color-mix(in srgb, {primary_color} 10%, white)",
                "100": f"color-mix(in srgb, {primary_color} 20%, white)",
                "200": f"color-mix(in srgb, {primary_color} 40%, white)",
                "300": f"color-mix(in srgb, {primary_color} 60%, white)",
                "400": f"color-mix(in srgb, {primary_color} 80%, white)",
                "500": primary_color,
                "600": f"color-mix(in srgb, {primary_color} 80%, black)",
                "700": f"color-mix(in srgb, {primary_color} 60%, black)",
                "800": f"color-mix(in srgb, {primary_color} 40%, black)",
                "900": f"color-mix(in srgb, {primary_color} 20%, black)",
            },
            "secondary": {
                "500": secondary_color,
            },
            "neutral": {
                "50": "#f9fafb",
                "100": "#f3f4f6",
                "200": "#e5e7eb",
                "300": "#d1d5db",
                "400": "#9ca3af",
                "500": neutral_color,
                "600": "#4b5563",
                "700": "#374151",
                "800": "#1f2937",
                "900": "#111827",
            },
            "semantic": {
                "background": "#ffffff",
                "surface": "#f9fafb",
                "text": "#111827",
                "textSecondary": "#6b7280",
                "border": "#e5e7eb",
                "success": "#10b981",
                "warning": "#f59e0b",
                "error": "#ef4444",
                "info": "#3b82f6",
            }
        },
        "typography": {
            "fontFamily": {
                "heading": font_heading,
                "body": font_body,
                "mono": "JetBrains Mono, monospace"
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
                "5xl": "3rem"
            },
            "fontWeight": {
                "regular": 400,
                "medium": 500,
                "semibold": 600,
                "bold": 700
            },
            "lineHeight": {
                "tight": 1.1,
                "snug": 1.2,
                "normal": 1.5,
                "relaxed": 1.625,
                "loose": 2
            }
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
            "32": "128px"
        },
        "radius": radii,
        "shadow": {
            "xs": "0 1px 2px rgba(0,0,0,0.05)",
            "sm": "0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06)",
            "md": "0 4px 6px rgba(0,0,0,0.07), 0 2px 4px rgba(0,0,0,0.06)",
            "lg": "0 10px 15px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.05)",
            "xl": "0 20px 25px rgba(0,0,0,0.1), 0 10px 10px rgba(0,0,0,0.04)",
            "inner": "inset 0 2px 4px rgba(0,0,0,0.06)"
        },
        "breakpoint": {
            "sm": "640px",
            "md": "768px",
            "lg": "1024px",
            "xl": "1280px",
            "2xl": "1536px"
        }
    }
    
    # Generate outputs
    css_vars = []
    css_vars.append(":root {")
    css_vars.append(f"  /* Brand: {brand_name} */")
    css_vars.append(f"  --color-primary: {primary_color};")
    css_vars.append(f"  --color-secondary: {secondary_color};")
    css_vars.append(f"  --color-neutral-500: {neutral_color};")
    for name, value in radii.items():
        css_vars.append(f"  --radius-{name}: {value};")
    css_vars.append(f"  --font-heading: '{font_heading}', sans-serif;")
    css_vars.append(f"  --font-body: '{font_body}', sans-serif;")
    css_vars.append("}")
    
    tailwind_config = {
        "theme": {
            "extend": {
                "colors": {
                    "primary": {
                        "DEFAULT": primary_color,
                        "50": tokens["color"]["primary"]["50"],
                    },
                    "secondary": secondary_color,
                },
                "fontFamily": {
                    "heading": [font_heading],
                    "body": [font_body],
                },
                "borderRadius": radii,
            }
        }
    }
    
    return {
        "tokens": tokens,
        "css_variables": "\n".join(css_vars),
        "tailwind_config_js": f"// tailwind.config.js\nmodule.exports = {json.dumps(tailwind_config, indent=2, ensure_ascii=False)}",
        "json": json.dumps(tokens, indent=2, ensure_ascii=False),
        "usage": {
            "figma": "Figma TokensプラグインでJSONをインポート可能",
            "style_dictionary": "Style Dictionaryで各プラットフォーム向けに変換可能",
            "css": "CSS変数としてそのまま利用可能"
        }
    }

def tool_generate_tailwind_config(primary: str = "#3b82f6", style: str = "modern") -> Dict[str, Any]:
    configs = {
        "modern": {
            "borderRadius": {"DEFAULT": "0.5rem", "lg": "0.75rem", "full": "9999px"},
            "boxShadow": {"soft": "0 2px 10px rgba(0,0,0,0.05)", "medium": "0 4px 20px rgba(0,0,0,0.08)"},
            "fontFamily": {"sans": ["Inter", "sans-serif"]}
        },
        "playful": {
            "borderRadius": {"DEFAULT": "1rem", "lg": "1.5rem", "full": "9999px"},
            "boxShadow": {"soft": "0 4px 20px rgba(0,0,0,0.08)", "medium": "0 8px 30px rgba(0,0,0,0.12)"},
            "fontFamily": {"sans": ["Poppins", "sans-serif"]}
        },
        "elegant": {
            "borderRadius": {"DEFAULT": "0.25rem", "lg": "0.5rem", "full": "9999px"},
            "boxShadow": {"soft": "0 1px 3px rgba(0,0,0,0.1)", "medium": "0 4px 12px rgba(0,0,0,0.08)"},
            "fontFamily": {"sans": ["Playfair Display", "serif"]}
        }
    }
    chosen = configs.get(style, configs["modern"])
    
    config_str = f"""
/** @type {{import('tailwindcss').Config}} */
module.exports = {{
  content: ["./src/**/*{{{{js,ts,jsx,tsx}}}}"],
  theme: {{
    extend: {{
      colors: {{
        primary: {{
          50: 'color-mix(in srgb, {primary} 10%, white)',
          100: 'color-mix(in srgb, {primary} 20%, white)',
          500: '{primary}',
          600: 'color-mix(in srgb, {primary} 80%, black)',
          900: 'color-mix(in srgb, {primary} 20%, black)',
        }}
      }},
      borderRadius: {json.dumps(chosen['borderRadius'], indent=8)},
      boxShadow: {json.dumps(chosen['boxShadow'], indent=8)},
      fontFamily: {json.dumps(chosen['fontFamily'], indent=8)},
      spacing: {{
        '18': '4.5rem',
        '22': '5.5rem',
      }},
      animation: {{
        'fade-in': 'fadeIn 0.5s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
      }}
    }}
  }},
  plugins: [],
}}
"""
    return {
        "primary": primary,
        "style": style,
        "config": config_str.strip(),
        "install": "npm install -D tailwindcss postcss autoprefixer && npx tailwindcss init -p",
        "tips": [
            "primary色はcolor-mixで自動的に濃淡生成",
            "8ptグリッド準拠のspacing拡張を含める",
            "アニメーションは控えめに、150-300msが目安"
        ]
    }
