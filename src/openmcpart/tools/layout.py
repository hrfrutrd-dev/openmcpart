"""
Layout and spacing tools
"""
from typing import Dict, Any, List

LAYOUT_PATTERNS = {
    "landing_saas": {
        "name": "SaaSランディング",
        "sections": ["Header (logo, nav, CTA)", "Hero (headline, sub, CTA, visual)", "Social proof (logos)", "Features (3col grid)", "How it works (steps)", "Testimonials", "Pricing", "FAQ", "Final CTA", "Footer"],
        "grid": "12 column, max-w 1280px, gutter 24px",
        "spacing": "セクション間 96-128px, 要素間 24-32px",
        "tips": ["HeroはAbove the foldに収める", "CTAは3回以上繰り返す", "Social proofはHero直後に配置"]
    },
    "dashboard": {
        "name": "ダッシュボード",
        "sections": ["Sidebar (240px)", "Topbar (64px)", "Main content (cards, charts, tables)", "Right drawer (optional)"],
        "grid": "Sidebar fixed, main fluid, card grid 12col",
        "spacing": "カード間 16-24px, セクション間 32px, コンテンツパディング 24px",
        "tips": ["情報の優先度でサイズと位置を決める", "カードは8px radius, subtle shadow", "データ密度は高めだが余白で呼吸させる"]
    },
    "ecommerce": {
        "name": "EC商品ページ",
        "sections": ["Header", "Breadcrumb", "Product gallery (left 60%)", "Product info (right 40% - title, price, variants, CTA)", "Tabs (description, specs, reviews)", "Related products (4col)", "Footer"],
        "grid": "2col for product, 4col for related",
        "spacing": "ギャラリー間 8px, 情報間 16px, セクション間 64px",
        "tips": ["CTAはスクロール追従", "画像は正方形、ホバーでズーム", "レビューは星評価を目立たせる"]
    },
    "blog": {
        "name": "ブログ・メディア",
        "sections": ["Header", "Article header (title, meta, cover)", "TOC (sticky left)", "Article body (max 720px)", "Author bio", "Related articles", "Newsletter CTA", "Footer"],
        "grid": "Single column 720px centered, TOC 240px sticky",
        "spacing": "段落間 24px, 見出し前 48px, 見出し後 16px",
        "tips": ["行間 1.8, 1行 35-40文字", "見出しにアンカーリンク", "目次はスクロール追従"]
    },
    "portfolio": {
        "name": "ポートフォリオ",
        "sections": ["Minimal header", "Hero intro (large type)", "Selected works (masonry or 2col)", "About", "Contact", "Footer"],
        "grid": "Masonry or 2col, generous whitespace",
        "spacing": "作品間 48-80px, セクション間 120px+",
        "tips": ["余白を大胆に使う", "作品が主役、UIは控えめに", "タイポグラフィで個性を出す"]
    },
    "mobile_app": {
        "name": "モバイルアプリ",
        "sections": ["Status bar", "App bar (56px)", "Content (16px padding)", "Bottom nav (80px) or FAB", "Bottom sheet"],
        "grid": "4px base, 16px margins, single column",
        "spacing": "要素間 8-16px, セクション間 24px",
        "tips": ["親指の届く範囲に主要アクション", "Bottom navは3-5項目", "ジェスチャーも考慮"]
    }
}

SPACING_SYSTEM = {
    "base": 4,
    "scale": [0, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128, 160, 192, 256],
    "semantic": {
        "xs": "4px - アイコン内余白、ボーダー",
        "sm": "8px - タイトな要素間、ボタンパディングY",
        "md": "16px - 標準要素間、カードパディング",
        "lg": "24px - セクション内グループ間",
        "xl": "32px - カード間、コンポーネント間",
        "2xl": "48px - セクション内大グループ間",
        "3xl": "64px - セクション間 (小)",
        "4xl": "96px - セクション間 (中)",
        "5xl": "128px - セクション間 (大)、ページ間",
    }
}

def tool_suggest_layout(content_type: str, target: str = "desktop", style: str = "minimal") -> Dict[str, Any]:
    content_type = content_type.lower()
    matched = None
    for key, pattern in LAYOUT_PATTERNS.items():
        if content_type in key or key in content_type:
            matched = pattern
            matched_key = key
            break
        # fuzzy
        if "saas" in content_type and "saas" in key:
            matched = pattern
            matched_key = key
            break
        if "shop" in content_type and "ecommerce" in key:
            matched = pattern
            matched_key = key
            break
    
    if not matched:
        # default mapping
        if "dashboard" in content_type or "admin" in content_type:
            matched = LAYOUT_PATTERNS["dashboard"]
            matched_key = "dashboard"
        elif "landing" in content_type:
            matched = LAYOUT_PATTERNS["landing_saas"]
            matched_key = "landing_saas"
        else:
            matched = LAYOUT_PATTERNS["landing_saas"]
            matched_key = "landing_saas"
    
    # Responsive adjustments
    responsive = {}
    if target == "mobile":
        responsive = {
            "grid": "4 columns, margin 16px, gutter 16px",
            "breakpoint": "< 768px",
            "adjustments": ["12col -> 4col", "Sidebar -> Drawer", "3col cards -> 1col stack", "Hover -> Tap"]
        }
    elif target == "tablet":
        responsive = {
            "grid": "8 columns, margin 24px, gutter 24px",
            "breakpoint": "768px - 1024px",
            "adjustments": ["12col -> 8col", "2col maintained", "Font size -10%"]
        }
    else:
        responsive = {
            "grid": "12 columns, max-width 1280px, gutter 24px, margin 32px",
            "breakpoint": "> 1024px",
            "adjustments": ["Full 12col grid", "Sidebar visible", "Hover states enabled"]
        }
    
    # Style variations
    style_details = {}
    if style == "minimal":
        style_details = {"radius": "8px", "shadow": "0 1px 3px rgba(0,0,0,0.08)", "border": "1px solid #eee", "density": "余白多め、要素少なめ"}
    elif style == "bold":
        style_details = {"radius": "16px", "shadow": "0 8px 32px rgba(0,0,0,0.12)", "border": "2px solid #111", "density": "コントラスト強め、大きなタイポ"}
    elif style == "soft":
        style_details = {"radius": "24px", "shadow": "0 4px 24px rgba(0,0,0,0.06)", "border": "none", "density": "柔らかい影、パステル、丸み"}
    else:
        style_details = {"radius": "12px", "shadow": "0 2px 8px rgba(0,0,0,0.08)", "border": "1px solid #e5e7eb", "density": "バランス型"}
    
    return {
        "content_type": content_type,
        "matched_pattern": matched_key,
        "layout": matched,
        "responsive": responsive,
        "style": style_details,
        "spacing_system": SPACING_SYSTEM,
        "8pt_grid_rule": "すべての余白・サイズは8の倍数を基本に (4は例外的に密な箇所で許容)。 8pt gridで一貫性と開発効率を向上。",
        "implementation": {
            "css": f"/* {matched['name']} */\n.container {{ max-width: 1280px; margin: 0 auto; padding: 0 32px; }}\n.section {{ padding: {SPACING_SYSTEM['scale'][12]}px 0; }}\n.card {{ border-radius: {style_details['radius']}; box-shadow: {style_details['shadow']}; }}",
            "tailwind": f"max-w-7xl mx-auto px-8 py-24 grid grid-cols-12 gap-6"
        }
    }

def tool_generate_spacing_system(base: int = 8, max_scale: int = 10) -> Dict[str, Any]:
    scale = [base * i for i in range(0, max_scale+1)]
    # also include 4pt half steps for first few
    detailed = {}
    names = ["0", "xs", "sm", "md", "lg", "xl", "2xl", "3xl", "4xl", "5xl", "6xl"]
    for idx, val in enumerate(scale):
        if idx < len(names):
            detailed[names[idx]] = f"{val}px"
    
    return {
        "base_unit": base,
        "scale": scale,
        "semantic_tokens": detailed,
        "usage_guide": {
            "4px": "アイコン、ボーダー、微調整",
            "8px": "関連要素間、ボタン内余白",
            "16px": "標準余白、カード内パディング",
            "24px": "コンポーネント間",
            "32px+": "セクション間"
        },
        "css_variables": "\n".join([f"  --space-{name}: {val};" for name, val in detailed.items()]),
        "tailwind_extend": "spacing: { '18': '4.5rem', '22': '5.5rem', '30': '7.5rem' } // 8pt準拠を追加",
        "rule": "8ptグリッド: デザインの一貫性のため、余白は8の倍数を原則とする。4ptは密なUIでのみ例外的に使用。"
    }
