# Architecture

## 概要

openmcpartは、MCP (Model Context Protocol) 標準に準拠したデザイン専門サーバーです。
FastMCP (Python SDK) を使用して実装されています。

## 構成

```
openmcpart/
├── src/openmcpart/
│   ├── __init__.py
│   ├── server.py          # FastMCPインスタンス、13 tools, 4 resources, 3 prompts
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── colors.py      # generate_color_palette, check_color_contrast, generate_gradient
│   │   ├── typography.py  # suggest_typography_pairing, generate_type_scale
│   │   ├── layout.py      # suggest_layout, generate_spacing_system
│   │   ├── tokens.py      # generate_design_tokens, generate_tailwind_config
│   │   ├── accessibility.py # check_accessibility, critique_design, suggest_component_variants
│   │   └── branding.py    # extract_design_principles, generate_moodboard_brief
│   └── utils/
│       ├── __init__.py
│       └── color_utils.py # 色変換、コントラスト、調和、色覚シミュレーション
```

## Transport

- **stdio**: デフォルト、全MCPクライアント対応
- 将来的にSSE/HTTPも対応可能 (FastMCPがサポート)

## Tool設計原則

1. **入力はシンプルに**: 必須パラメータ最小限、オプションで詳細化
2. **出力は実装可能に**: CSS, Tailwind, Figmaで使える形式を必ず含む
3. **日本語対応**: フォント、ブランディングで日本語を考慮
4. **アクセシビリティ内蔵**: コントラスト、色覚多様性を常に含める
5. **外部依存なし**: 計算はローカルで完結、APIキー不要

## 依存関係

- `mcp>=1.20.0` - MCP Python SDK
- `pydantic>=2.0.0` - バリデーション

のみ。軽量。

## 拡張方法

新しいツールを追加する場合:

1. `src/openmcpart/tools/` に新しいモジュール作成
2. 関数を定義 (型ヒントとdocstring必須)
3. `tools/__init__.py` でエクスポート
4. `server.py` で `@mcp.tool()` デコレータで登録

例:

```python
# tools/my_new_tool.py
def tool_my_new_feature(param: str) -> dict:
    return {"result": "..."}

# server.py
from .tools.my_new_tool import tool_my_new_feature

@mcp.tool()
def my_new_feature(param: Annotated[str, Field(description="...")]) -> dict:
    \"\"\"説明\"\"\"
    return tool_my_new_feature(param)
```

## テスト

- `pytest` でユニットテスト
- `npx @modelcontextprotocol/inspector openmcpart` でMCP Inspectorテスト
- 各ツールの入出力をJSON Schemaで検証

## セキュリティ

- 外部API呼び出しなし
- ファイルシステムアクセスなし (resourcesはメモリ内のテンプレートのみ)
- 入力はPydanticでバリデーション
- 色コードは正規表現でサニタイズ

## パフォーマンス

- すべての計算はO(1)〜O(n)で軽量
- 色変換、コントラスト計算は数ms
- パレット生成も10色程度で即時
- メモリ使用量 < 50MB
