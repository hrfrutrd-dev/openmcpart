# openmcpart - Universal Design Specialist MCP Server
### どんなAgentでも使えるデザイン専門MCPサーバー — AIっぽくない、洗練されたUI

[![MCP](https://img.shields.io/badge/MCP-Compatible-blue)](https://modelcontextprotocol.io)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Sophisticated](https://img.shields.io/badge/UI-Paper%20%26%20Ink%20No%20AI%20Tropes-black)](./web/)

**Claude Desktop, Cursor, VS Code, ChatGPT, どんなMCP対応Agentでも使えるデザイン専門サーバー**

プロのデザイナーが持つ知識を、AI Agentが使える16のツールとしてパッケージ化。
**AIっぽくない、洗練されたUI**のための2つの新ツールを含む: `generate_sophisticated_ui`, `critique_ai_look`

> 紙とインク。0.5pxの線で区切る。紫グラデも、24px角丸も、影も、✨も使わない。

- **Web Demo**: `web/index.html` - 洗練されたUIのライブデモ (Paper #fdfcfa / Ink #121212 / Hairline 0.5px / Radius 0px)
- **Playground**: `web/playground.html` - 16ツールをブラウザで試す

---

## ✨ 特徴

- **Universal**: MCP標準準拠 - 1回実装で全Agent対応
- **Sophisticated**: AIっぽくない洗練UI - Paper & Ink, hairline, serif, 非対称, 160px余白
- **Professional**: 8pt Grid, WCAG, 60-30-10ルールなどプロのベストプラクティス
- **Practical**: CSS / Tailwind / Figmaでそのまま使えるコードを出力
- **Japanese First**: 日本語フォント、日本語UXにも完全対応
- **No API Key**: 外部API不要、ローカル完結

---

## 🎨 AIっぽくない洗練されたUIとは？

### AI定番 (避ける) → 洗練 (こちら)

| AIっぽい (Generic) | 洗練された (Sophisticated) |
|-------------------|---------------------------|
| Purple → Blue gradient | 単色 + 紙の質感 #fdfcfa |
| Rounded 24px everywhere | 0-4px, sharpが洗練 |
| Shadow-lg, 浮かせる | Hairline 0.5pxで区切る |
| Centered hero + blob | 左寄せ、右に大きく余白 |
| 3-col icon grid | 1列 + 詳細、線で描く |
| Inter only, no personality | Instrument Serif + Inter Tight |
| ✨ Magic, Supercharge | 具体的な動詞: 組む、編む、削る |
| Bouncy scale hover | Opacity 0.85, 150ms |
| 詰め込み 80px余白 | 160-240px、余白を恐れない |

**新ツール:**
- `generate_sophisticated_ui` - AIっぽくないUI仕様生成 (Paper & Ink, Clay & Moss, Editorial Noir, Atelier)
- `critique_ai_look` - AIっぽいデザインを検出し、洗練された代替案を提示 (Before/After)

詳細: `web/` フォルダのデモサイトがそのままベストプラクティス。

---

## 🛠️ 提供ツール (16 tools)

### 🎨 Color カラー
| Tool | 説明 |
|------|------|
| `generate_color_palette` | ベースカラー/ムードから調和の取れたパレット生成。complementary, analogous, triadic等 |
| `check_color_contrast` | WCAG準拠コントラストチェック + 色覚多様性シミュレーション |
| `generate_gradient` | グラデーション生成 (linear/radial/conic) CSS & Tailwind出力 |

### ✍️ Typography タイポグラフィ
| Tool | 説明 |
|------|------|
| `suggest_typography_pairing` | 業界・ムード・言語からフォントペアリング提案 (日本語対応) |
| `generate_type_scale` | タイプスケール生成 (minor_second〜golden_ratio) |

### 📐 Layout レイアウト
| Tool | 説明 |
|------|------|
| `suggest_layout` | コンテンツタイプ別レイアウトパターン (SaaS, Dashboard, EC, Blog等) |
| `generate_spacing_system` | 8ptグリッド準拠スペーシングシステム生成 |

### 🧩 Design Tokens デザインシステム
| Tool | 説明 |
|------|------|
| `generate_design_tokens` | 完全なデザイントークン生成 (色, タイポ, 余白, 角丸, 影) |
| `generate_tailwind_config` | Tailwind設定ファイル生成 |

### ♿ Accessibility & Critique
| Tool | 説明 |
|------|------|
| `check_accessibility` | WCAGチェックリスト + 自動チェック |
| `critique_design` | 8原則ヒューリスティック評価 + アクションプラン |
| `suggest_component_variants` | UIコンポーネントバリエーション (Button, Card, Input等) |

### 🏷️ Branding ブランディング
| Tool | 説明 |
|------|------|
| `extract_design_principles` | ブランドキーワードからアーキタイプ・原則・パレット抽出 |
| `generate_moodboard_brief` | ムードボードブリーフ生成 (minimal, brutalism, glassmorphism, japanese等) |

### ✨ Sophisticated UI — AIっぽくない洗練 (NEW)
| Tool | 説明 |
|------|------|
| `generate_sophisticated_ui` | AIっぽくないUI仕様生成。Paper & Ink, Clay & Moss, Editorial Noir, Atelierの4 aesthetic。0px角丸、hairline、セリフ体、非対称、160px余白 |
| `critique_ai_look` | AIっぽいデザインを批評。紫グラデ、24px角丸、影、✨等を検出し、Before/Afterで洗練された代替案を提示 |

### 📚 Resources & Prompts
- `design://tokens/template` - トークンテンプレート
- `design://guidelines/8pt-grid` - 8ptグリッドガイドライン
- `design://guidelines/wcag` - WCAGクイックリファレンス
- `design://checklist/design-review` - デザインレビューチェックリスト
- Prompts: `design_critique_prompt`, `branding_workshop_prompt`, `component_design_prompt`

---

## 🚀 インストール

### 1. pipでインストール (推奨)

```bash
pip install openmcpart
# または
uv pip install openmcpart
```

### 2. ソースから

```bash
git clone https://github.com/hrfrutrd-dev/openmcpart
cd openmcpart
pip install -e .
```

### 3. 動作確認

```bash
openmcpart --help
# または
design-mcp
```

---

## ⚙️ 各Agentでの設定

### Claude Desktop

`~/Library/Application Support/Claude/claude_desktop_config.json` (Mac) または
`%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "openmcpart-design": {
      "command": "openmcpart",
      "args": [],
      "env": {}
    }
  }
}
```

uvを使う場合:
```json
{
  "mcpServers": {
    "openmcpart-design": {
      "command": "uvx",
      "args": ["openmcpart"],
      "env": {}
    }
  }
}
```

### Cursor

`.cursor/mcp.json` または Cursor Settings > MCP:

```json
{
  "mcpServers": {
    "openmcpart-design": {
      "command": "openmcpart",
      "args": []
    }
  }
}
```

### VS Code (Copilot)

`.vscode/mcp.json`:

```json
{
  "servers": {
    "openmcpart-design": {
      "type": "stdio",
      "command": "openmcpart",
      "args": []
    }
  }
}
```

### ChatGPT / OpenAI

MCP対応クライアント経由で接続。stdio transportを使用。

### 汎用 (任意のMCPクライアント)

```bash
# stdio transport (標準)
openmcpart

# 環境変数で設定可能
MCP_TRANSPORT=stdio openmcpart
```

---

## 💡 使用例

### Agentへのプロンプト例

```
「#3b82f6をベースに、SaaS向けのカラーパレットを作って」
→ generate_color_palette(base_color="#3b82f6", harmony="analogous")

「この配色のコントラストはWCAG AAに通る？」
→ check_color_contrast(foreground="#ffffff", background="#3b82f6")

「テック系スタートアップのフォントペアリングを提案して、日本語対応も」
→ suggest_typography_pairing(mood="tech_trust", industry="tech", language="ja")

「ダッシュボードのレイアウトを考えて、モバイル対応も」
→ suggest_layout(content_type="dashboard", target="mobile", style="minimal")

「ブランドキーワード: 信頼,革新,シンプル からデザイン原則を抽出して」
→ extract_design_principles(brand_keywords="信頼,革新,シンプル", industry="SaaS")

「このランディングページのデザインを批評して」
→ critique_design(design_description="SaaSランディング、CTAが目立たない、情報が多い", focus="all")

「ボタンコンポーネントのバリエーションをTailwindで」
→ suggest_component_variants(component="button", style="modern", count=5)

「デザイントークンを生成して、Tailwind設定も」
→ generate_design_tokens(primary_color="#3b82f6", brand_name="MySaaS")
→ generate_tailwind_config(primary="#3b82f6", style="modern")
```

### 出力例

`generate_color_palette(mood="calm")`:

```json
{
  "mood": "calm",
  "description": "穏やか・安心 - ブルー系",
  "primary": "#5ba4cf",
  "secondary": "#6b8fc2",
  "accent": "#cf8a5b",
  "css_variables": "--color-primary: #5ba4cf; ..."
}
```

---

## 🏗️ アーキテクチャ

```
src/openmcpart/
├── server.py          # FastMCPサーバー本体 (13 tools + 4 resources + 3 prompts)
├── tools/
│   ├── colors.py      # カラー関連 (3 tools)
│   ├── typography.py  # タイポグラフィ (2 tools)
│   ├── layout.py      # レイアウト (2 tools)
│   ├── tokens.py      # デザイントークン (2 tools)
│   ├── accessibility.py # アクセシビリティ & 批評 (3 tools)
│   └── branding.py    # ブランディング (2 tools)
└── utils/
    └── color_utils.py # 色変換・コントラスト計算
```

- **Transport**: stdio (標準) - 全MCPクライアント対応
- **Dependencies**: `mcp>=1.20.0`, `pydantic>=2.0.0` のみ - 軽量
- **No External API**: 完全ローカル動作

---

## 🎯 デザイン原則 (このMCPが準拠する原則)

このMCP自体が以下の原則に従って設計されています:

1. **8pt Grid**: すべての余白は8の倍数
2. **60-30-10 Rule**: 60% neutral, 30% primary, 10% accent
3. **WCAG AA**: コントラスト 4.5:1以上
4. **2 Fonts, 3 Weights**: フォントは2種類、ウェイトは3つまで
5. **Less is More**: 必要最低限のツールで最大の価値

---

## 🧪 テスト

```bash
pip install pytest
pytest tests/ -v

# MCP Inspectorでテスト
npx @modelcontextprotocol/inspector openmcpart
```

---

## 📖 ドキュメント

- [MCP公式ドキュメント](https://modelcontextprotocol.io)
- [examples/](./examples) - 設定例と使用例
- [docs/](./docs) - 詳細ドキュメント

---

## 🤝 コントリビュート

1. Fork
2. Feature branch (`git checkout -b feature/amazing`)
3. Commit (`git commit -m 'Add amazing feature'`)
4. Push (`git push origin feature/amazing`)
5. Pull Request

---

## 📄 ライセンス

MIT License - 詳細は [LICENSE](LICENSE) を参照

---

## 🙏 謝辞

- [Model Context Protocol](https://modelcontextprotocol.io) - 標準化されたAgent接続
- [Refactoring UI](https://www.refactoringui.com/) - デザイン原則
- [WCAG](https://www.w3.org/WAI/standards-guidelines/wcag/) - アクセシビリティ基準

---

**Made with ❤️ for all Agents - どんなAgentでも使えるデザインMCP**

> "Good design is as little design as possible" - Dieter Rams
