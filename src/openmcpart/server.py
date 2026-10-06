"""
openmcpart - Universal Design Specialist MCP Server
どんなAgentでも使えるデザイン専門MCPサーバー

This MCP server provides comprehensive design tools that any AI agent can use:
- Color palette generation & contrast checking
- Typography pairing & type scale
- Layout & spacing systems
- Design tokens & Tailwind config
- Accessibility auditing
- Design critique & heuristics
- Component variants
- Branding & moodboard

Compatible with:
- Claude Desktop
- Cursor
- VS Code (Copilot)
- ChatGPT (with MCP)
- Any MCP-compliant client
"""

from typing import Annotated, Optional

try:
    # MCP v2.x - FastMCP renamed to MCPServer
    from mcp.server import MCPServer as FastMCP
except ImportError:
    try:
        from mcp.server.mcpserver import MCPServer as FastMCP
    except ImportError:
        # Fallback to v1.x
        from mcp.server.fastmcp import FastMCP

from pydantic import Field

from .tools.colors import (
    tool_generate_color_palette,
    tool_check_color_contrast,
    tool_generate_gradient,
)
from .tools.typography import (
    tool_suggest_typography_pairing,
    tool_generate_type_scale,
)
from .tools.layout import (
    tool_suggest_layout,
    tool_generate_spacing_system,
)
from .tools.tokens import (
    tool_generate_design_tokens,
    tool_generate_tailwind_config,
)
from .tools.accessibility import (
    tool_check_accessibility,
    tool_critique_design,
    tool_suggest_component_variants,
)
from .tools.branding import (
    tool_extract_design_principles,
    tool_generate_moodboard_brief,
)
from .tools.ui_generator import (
    tool_generate_sophisticated_ui,
    tool_critique_ai_look,
)

# Initialize FastMCP server
mcp = FastMCP(
    "openmcpart-design",
    instructions="""
    あなたはプロのデザイナーです。以下のツールを使って、UI/UXデザインを支援します。
    
    対応領域:
    - カラー: パレット生成、コントラストチェック、グラデーション
    - タイポグラフィ: フォントペアリング、タイプスケール
    - レイアウト: レイアウトパターン、スペーシングシステム (8pt grid)
    - デザイントークン: トークン生成、Tailwind設定
    - アクセシビリティ: WCAGチェック、改善提案
    - デザインレビュー: ヒューリスティック評価、改善案
    - コンポーネント: ボタン、カード等のバリエーション
    - ブランディング: ブランドアーキタイプ、ムードボード
    - 洗練UI: AIっぽくない、編集的、紙とインク、hairline、非対称、巨大余白
    
    重要: AIっぽいデザイン (紫グラデ、24px角丸、影、✨、中央揃え、3列アイコン) は避け、洗練された代替を提示してください。
    
    どんなAgentでも使えるように、出力は具体的で実装可能な形で提供してください。
    CSS, Tailwind, Figmaで使える形式を常に含めてください。
    """,
)

# ========== COLOR TOOLS ==========

@mcp.tool()
def generate_color_palette(
    base_color: Annotated[Optional[str], Field(description="ベースカラー (hex, 例: #3b82f6). 指定しない場合はmoodから生成")] = None,
    mood: Annotated[Optional[str], Field(description="ムード・雰囲気 (例: calm, energetic, luxury, natural, tech, warm, minimal, vibrant, elegant, earthy)")] = None,
    harmony: Annotated[str, Field(description="配色調和の種類")] = "complementary",
    count: Annotated[int, Field(description="生成する色数 (参考値)", ge=2, le=10)] = 5,
) -> dict:
    """
    カラーパレットを生成する。ベースカラーまたはムードから、調和の取れたパレットを作成。
    harmony: complementary, analogous, triadic, tetradic, split, monochromatic
    
    出力はCSS変数、Tailwind、Figmaで使える形式。
    """
    return tool_generate_color_palette(base_color=base_color, mood=mood, harmony=harmony, count=count)


@mcp.tool()
def check_color_contrast(
    foreground: Annotated[str, Field(description="前景色 (テキスト色) hex, 例: #ffffff")],
    background: Annotated[str, Field(description="背景色 hex, 例: #000000")],
) -> dict:
    """
    2色間のコントラスト比をWCAG基準でチェック。AA/AAA合否、色覚多様性シミュレーションも含む。
    アクセシビリティ対応に必須。
    """
    return tool_check_color_contrast(foreground=foreground, background=background)


@mcp.tool()
def generate_gradient(
    from_color: Annotated[str, Field(description="開始色 hex")],
    to_color: Annotated[str, Field(description="終了色 hex")],
    style: Annotated[str, Field(description="グラデーションスタイル: linear, radial, conic")] = "linear",
    angle: Annotated[int, Field(description="角度 (linear/conic用) 0-360", ge=0, le=360)] = 135,
) -> dict:
    """
    グラデーションを生成。CSSとTailwind形式で出力。中間色も自動生成。
    """
    return tool_generate_gradient(from_color=from_color, to_color=to_color, style=style, angle=angle)


# ========== TYPOGRAPHY TOOLS ==========

@mcp.tool()
def suggest_typography_pairing(
    mood: Annotated[str, Field(description="ムード・スタイル: modern_minimal, elegant_luxury, tech_trust, friendly_warm, editorial, bold_impact, japanese_modern, japanese_elegant")] = "modern_minimal",
    industry: Annotated[Optional[str], Field(description="業界 (例: tech, fashion, finance, education, health, media)")] = None,
    language: Annotated[str, Field(description="言語: en, ja, japanese")] = "en",
) -> dict:
    """
    タイポグラフィのペアリングを提案。見出し・本文・アクセントフォント、タイプスケール、行間、文字間まで含む。
    Google Fonts対応、日本語フォントも対応。
    """
    return tool_suggest_typography_pairing(mood=mood, industry=industry, language=language)


@mcp.tool()
def generate_type_scale(
    base_size: Annotated[int, Field(description="ベースフォントサイズ px", ge=10, le=24)] = 16,
    ratio: Annotated[str, Field(description="スケール比率: minor_second, major_second, minor_third, major_third, perfect_fourth, augmented_fourth, perfect_fifth, golden_ratio")] = "major_third",
) -> dict:
    """
    タイプスケールを生成。ベースサイズと比率から、xs〜6xlまでのスケールを作成。
    CSS変数も出力。
    """
    return tool_generate_type_scale(base_size=base_size, ratio=ratio)


# ========== LAYOUT TOOLS ==========

@mcp.tool()
def suggest_layout(
    content_type: Annotated[str, Field(description="コンテンツタイプ: landing_saas, dashboard, ecommerce, blog, portfolio, mobile_app")],
    target: Annotated[str, Field(description="ターゲットデバイス: desktop, tablet, mobile")] = "desktop",
    style: Annotated[str, Field(description="スタイル: minimal, bold, soft, balanced")] = "minimal",
) -> dict:
    """
    レイアウトパターンを提案。グリッド、セクション構成、スペーシング、レスポンシブ対応まで。
    8ptグリッド準拠。
    """
    return tool_suggest_layout(content_type=content_type, target=target, style=style)


@mcp.tool()
def generate_spacing_system(
    base: Annotated[int, Field(description="ベース単位 px (通常 4 or 8)", ge=2, le=16)] = 8,
    max_scale: Annotated[int, Field(description="最大スケール数", ge=5, le=20)] = 10,
) -> dict:
    """
    スペーシングシステム (8ptグリッド) を生成。セマンティックトークン、CSS変数、Tailwind拡張を含む。
    """
    return tool_generate_spacing_system(base=base, max_scale=max_scale)


# ========== DESIGN TOKENS TOOLS ==========

@mcp.tool()
def generate_design_tokens(
    primary_color: Annotated[str, Field(description="プライマリカラー hex")] = "#3b82f6",
    secondary_color: Annotated[str, Field(description="セカンダリカラー hex")] = "#8b5cf6",
    neutral_color: Annotated[str, Field(description="ニュートラルカラー hex")] = "#6b7280",
    font_heading: Annotated[str, Field(description="見出しフォント")] = "Inter",
    font_body: Annotated[str, Field(description="本文フォント")] = "Inter",
    radius: Annotated[str, Field(description="角丸スタイル: none, small, medium, large, full")] = "medium",
    brand_name: Annotated[str, Field(description="ブランド名")] = "MyBrand",
) -> dict:
    """
    デザイントークンを生成。色、タイポグラフィ、スペーシング、角丸、影、ブレークポイントを含む完全なトークンセット。
    CSS変数、Tailwind config、JSON形式で出力。Figma Tokens対応。
    """
    return tool_generate_design_tokens(
        primary_color=primary_color,
        secondary_color=secondary_color,
        neutral_color=neutral_color,
        font_heading=font_heading,
        font_body=font_body,
        radius=radius,
        brand_name=brand_name,
    )


@mcp.tool()
def generate_tailwind_config(
    primary: Annotated[str, Field(description="プライマリカラー hex")] = "#3b82f6",
    style: Annotated[str, Field(description="スタイル: modern, playful, elegant")] = "modern",
) -> dict:
    """
    Tailwind CSS設定を生成。カラー、角丸、影、フォント、アニメーションを含む。
    """
    return tool_generate_tailwind_config(primary=primary, style=style)


# ========== ACCESSIBILITY & CRITIQUE TOOLS ==========

@mcp.tool()
def check_accessibility(
    description: Annotated[str, Field(description="チェック対象の説明 (例: ランディングページのヒーローセクション)")] = "",
    foreground: Annotated[Optional[str], Field(description="前景色 hex (任意)")] = None,
    background: Annotated[Optional[str], Field(description="背景色 hex (任意)")] = None,
    font_size: Annotated[str, Field(description="フォントサイズ (例: 16px)")] = "16px",
    interactive: Annotated[bool, Field(description="インタラクティブ要素を含むか")] = False,
) -> dict:
    """
    アクセシビリティチェック。WCAG基準、色コントラスト、キーボード操作、タッチターゲット等のチェックリストを提供。
    """
    return tool_check_accessibility(
        description=description,
        foreground=foreground,
        background=background,
        font_size=font_size,
        interactive=interactive,
    )


@mcp.tool()
def critique_design(
    design_description: Annotated[str, Field(description="デザインの説明。例: SaaSのダッシュボード、情報が多くごちゃごちゃしている、CTAが目立たない")],
    focus: Annotated[str, Field(description="フォーカス領域: all, hierarchy, consistency, contrast, accessibility, whitespace など")] = "all",
) -> dict:
    """
    デザインをヒューリスティック評価。視覚的階層、一貫性、近接、整列、コントラスト、反復、余白、アクセシビリティの8原則でレビュー。
    具体的な改善アクションプランも提供。
    """
    return tool_critique_design(design_description=design_description, focus=focus)


@mcp.tool()
def suggest_component_variants(
    component: Annotated[str, Field(description="コンポーネント名: button, card, input, modal, navbar, etc")],
    style: Annotated[str, Field(description="スタイル: modern, playful, elegant, minimal")] = "modern",
    count: Annotated[int, Field(description="バリエーション数", ge=1, le=5)] = 3,
) -> dict:
    """
    UIコンポーネントのバリエーションを提案。スタイル、サイズ、状態、アクセシビリティ考慮事項、コード例を含む。
    """
    return tool_suggest_component_variants(component=component, style=style, count=count)


# ========== BRANDING TOOLS ==========

@mcp.tool()
def extract_design_principles(
    brand_keywords: Annotated[str, Field(description="ブランドキーワード (カンマ区切り, 例: 信頼,革新,シンプル,温かみ)")],
    industry: Annotated[str, Field(description="業界")] = "",
    audience: Annotated[str, Field(description="ターゲットオーディエンス")] = "",
) -> dict:
    """
    ブランドキーワードからデザイン原則を抽出。ブランドアーキタイプ、カラー心理学、タイポグラフィ方向性、イメージ方向性を提供。
    """
    return tool_extract_design_principles(brand_keywords=brand_keywords, industry=industry, audience=audience)


@mcp.tool()
def generate_moodboard_brief(
    theme: Annotated[str, Field(description="テーマ: minimal, brutalism, glassmorphism, neomorphism, japanese, y2k など")],
    keywords: Annotated[str, Field(description="追加キーワード")] = "",
) -> dict:
    """
    ムードボードのブリーフを生成。カラー、フォント、イメージ、テクスチャ、参考ブランド、Do's and Don'tsを含む。
    """
    return tool_generate_moodboard_brief(theme=theme, keywords=keywords)


# ========== SOPHISTICATED UI TOOLS (AIっぽくない) ==========

@mcp.tool()
def generate_sophisticated_ui(
    purpose: Annotated[str, Field(description="用途: landing page, dashboard, portfolio, editorial, ecommerce など")] = "landing page",
    aesthetic: Annotated[str, Field(description="美的方向性: paper_ink, clay_moss, editorial, atelier")] = "paper_ink",
    industry: Annotated[str, Field(description="業界 (任意)")] = "",
    avoid_ai_tropes: Annotated[bool, Field(description="AIっぽい定番を避けるか")] = True,
) -> dict:
    """
    AIっぽくない洗練されたUIの設計仕様を生成。紫グラデ、過剰な角丸、影、✨を避け、紙とインク、hairline、セリフ体、非対称、巨大な余白で洗練を表現。
    """
    return tool_generate_sophisticated_ui(purpose=purpose, aesthetic=aesthetic, industry=industry, avoid_ai_tropes=avoid_ai_tropes)


@mcp.tool()
def critique_ai_look(
    design_description: Annotated[str, Field(description="批評したいデザインの説明。例: 紫グラデ背景に丸いカードが並ぶAIっぽいLP")],
) -> dict:
    """
    AIっぽいデザインを批評し、洗練された代替案を提示。AI定番 (紫グラデ、24px角丸、影、中央揃え、✨) を検出し、具体的な修正方法を提案。
    """
    return tool_critique_ai_look(design_description=design_description)


# ========== RESOURCES ==========

@mcp.resource("design://tokens/template")
def design_tokens_template() -> str:
    """デザインシステムのトークンテンプレート (JSON)"""
    return """{
  "color": {
    "primary": { "500": "#3b82f6" },
    "secondary": { "500": "#8b5cf6" },
    "neutral": { "50": "#f9fafb", "900": "#111827" }
  },
  "typography": {
    "fontFamily": { "heading": "Inter", "body": "Inter" },
    "fontSize": { "base": "1rem", "2xl": "1.5rem" }
  },
  "spacing": { "4": "16px", "8": "32px" },
  "radius": { "md": "8px", "full": "9999px" },
  "shadow": { "md": "0 4px 6px rgba(0,0,0,0.07)" }
}"""

@mcp.resource("design://guidelines/8pt-grid")
def guideline_8pt() -> str:
    """8ptグリッドガイドライン"""
    return """
# 8pt Grid System

## 基本原則
- すべての余白、サイズは8の倍数を基本
- 4ptは例外的に密なUIでのみ使用
- 一貫性と開発効率向上

## スケール
0, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128, 160, 192, 256

## セマンティック
- xs: 4px - アイコン内余白
- sm: 8px - タイトな要素間
- md: 16px - 標準要素間
- lg: 24px - グループ間
- xl: 32px - コンポーネント間
- 2xl: 48px - 大グループ間
- 3xl: 64px - セクション間 (小)
- 4xl: 96px - セクション間 (中)
- 5xl: 128px - セクション間 (大)

## 実装
CSS: --space-md: 16px
Tailwind: p-4 (16px), m-8 (32px), gap-6 (24px)
"""

@mcp.resource("design://guidelines/wcag")
def guideline_wcag() -> str:
    """WCAGクイックリファレンス"""
    return """
# WCAG 2.2 Quick Reference

## コントラスト
- 通常テキスト: 4.5:1以上 (AA), 7:1以上 (AAA)
- 大きなテキスト (18pt+ or 14pt bold+): 3:1以上 (AA), 4.5:1以上 (AAA)
- 非テキスト (アイコン、グラフ): 3:1以上

## タッチターゲット
- 最小 24x24px (AA), 推奨 44x44px (AAA)
- 間隔 8px以上

## フォーカス
- 2px以上のコントラストあるリング
- フォーカス順序は論理的に

## テキスト
- 本文 16px以上推奨
- 行間 1.5以上
- 1行 45-75文字 (日本語 35-45文字)

## ツール
- axe DevTools
- WAVE
- Lighthouse
- Color Contrast Analyzer
"""

@mcp.resource("design://checklist/design-review")
def checklist_review() -> str:
    """デザイン review checklist"""
    return """
# Design Review Checklist

## Visual Hierarchy
- [ ] 最重要要素が最も目立つか？
- [ ] サイズ、色、配置で階層を表現しているか？
- [ ] F/Zパターンに沿っているか？

## Consistency
- [ ] 色は3色以内か？ (60-30-10ルール)
- [ ] フォントは2種類以内か？
- [ ] 間隔は8pt grid準拠か？

## Accessibility
- [ ] コントラスト 4.5:1以上か？
- [ ] タッチターゲット 44px以上か？
- [ ] フォーカスリングは明確か？
- [ ] altテキストは適切か？

## Usability
- [ ] 5秒テスト: 何のサイトか、次に何をすべきか分かるか？
- [ ] CTAは1画面1つで明確か？
- [ ] エラー時は具体的な修正方法を示しているか？

## Polish
- [ ] 余白は十分か？ (詰め込みすぎていないか)
- [ ] 整列は意図的か？ (グリッドに沿っているか)
- [ ] 状態 (hover, focus, disabled) は定義されているか？
"""

# ========== PROMPTS ==========

@mcp.prompt()
def design_critique_prompt(design_type: str = "landing page") -> str:
    """デザイン批評用のプロンプト"""
    return f"""
あなたはシニアプロダクトデザイナーです。以下の観点で{design_type}のデザインを批評してください:

1. 視覚的階層: 最も重要な要素が最も目立っているか？
2. 一貫性: 色、タイポグラフィ、間隔は一貫しているか？
3. アクセシビリティ: WCAG AA準拠か？コントラスト、タッチターゲットは？
4. 余白: 詰め込みすぎていないか？8pt grid準拠か？
5. CTA: 明確で目立つか？1画面1つか？

各項目について:
- 良い点
- 改善点
- 具体的な修正案 (CSS/Tailwindコード付き)

最後に、優先度付きアクションプラン (Immediate / Short-term / Long-term) を作成してください。
"""

@mcp.prompt()
def branding_workshop_prompt(brand_name: str = "MyBrand") -> str:
    """ブランディングワークショップ用プロンプト"""
    return f"""
{brand_name}のブランディングワークショップを行います。

以下の質問に答えて、デザイン方向性を明確にしましょう:

1. ブランドを3つのキーワードで表すと？
2. 競合と差別化するポイントは？
3. ターゲットユーザーは誰？ (年齢、職業、価値観)
4. ブランドに例えるなら、人、動物、場所は？
5. 避けたいイメージは？

回答を元に:
- ブランドアーキタイプを特定
- カラーパレット (3色) を提案
- タイポグラフィ (2フォント) を提案
- ムードボードの方向性を提示

ツール `extract_design_principles` と `generate_moodboard_brief` を使って具体化してください。
"""

@mcp.prompt()
def component_design_prompt(component: str = "button") -> str:
    """コンポーネントデザイン用プロンプト"""
    return f"""
{component}コンポーネントをデザインシステムとして設計します。

以下を定義してください:

1. バリエーション: Primary, Secondary, Ghost, Destructiveなど
2. サイズ: sm, md, lg
3. 状態: default, hover, active, focus, disabled, loading
4. アクセシビリティ: コントラスト、44px、キーボード、ARIA
5. コード: HTML, Tailwind, React例

ツール `suggest_component_variants` を使って開始し、必要に応じて `generate_design_tokens` でトークンを定義してください。

出力は開発者がそのまま実装できる具体的なコードを含めてください。
"""

def main():
    """Entry point for the MCP server
    
    Supports multiple transports for universal agent compatibility:
    - stdio (default): Claude Desktop, Cursor, VS Code, any MCP client
    - sse: HTTP SSE for web-based clients
    - streamable-http: Modern HTTP transport
    
    Env vars:
    - MCP_TRANSPORT: stdio, sse, streamable-http (default: stdio)
    - MCP_PORT: port for http transports (default: 8000)
    - MCP_HOST: host for http transports (default: 0.0.0.0)
    """
    import os
    import argparse
    
    parser = argparse.ArgumentParser(description="openmcpart - Universal Design MCP Server")
    parser.add_argument("--transport", choices=["stdio", "sse", "streamable-http"], 
                        default=os.getenv("MCP_TRANSPORT", "stdio"),
                        help="Transport protocol")
    parser.add_argument("--port", type=int, default=int(os.getenv("MCP_PORT", "8000")),
                        help="Port for HTTP transports")
    parser.add_argument("--host", default=os.getenv("MCP_HOST", "0.0.0.0"),
                        help="Host for HTTP transports")
    
    args = parser.parse_args()
    
    print(f"Starting openmcpart design MCP server...", file=os.sys.stderr)
    print(f"Transport: {args.transport}", file=os.sys.stderr)
    print(f"Tools: 14 | Resources: 4 | Prompts: 3", file=os.sys.stderr)
    print(f"Universal - Works with any MCP agent", file=os.sys.stderr)
    
    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        mcp.run(transport="streamable-http", host=args.host, port=args.port)

if __name__ == "__main__":
    main()
