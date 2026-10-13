# openmcpart — Design Tools & Local Audit MCP Server
### MCP対応Agentで使うデザイン支援サーバー — スタイル提案とローカル静的監査

[![PyPI](https://img.shields.io/badge/PyPI-openmcpart-3775A9)](https://pypi.org/project/openmcpart/)
[![MCP](https://img.shields.io/badge/MCP-Compatible-blue)](https://modelcontextprotocol.io)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](https://github.com/hrfrutrd-dev/openmcpart/blob/main/LICENSE)
[![Paper & Ink](https://img.shields.io/badge/UI-Optional%20Paper%20%26%20Ink-black)](https://github.com/hrfrutrd-dev/openmcpart/tree/main/web)

**Claude Desktop、Cursor、VS CodeなどのMCP対応クライアントで利用できるデザイン支援サーバー**

対応するTransportやResourcesの範囲はクライアントごとに異なります。

デザイン支援・トークン生成・静的UI監査を、AI Agentが使える18のMCPツールとして提供します。
Paper & Inkなどの美的方向性は**選択可能なスタイルプリセット**であり、普遍的な品質基準として強制しません。

新しいローカル監査ツール: `audit_project`, `extract_project_tokens`

> Paper & Inkは選択可能な美的方向性のひとつ。紫、角丸、影、グラデーションを一律に禁止せず、ブランドと用途に合わせて選びます。

- **Web Demo**: `web/index.html` - スタイルプリセットのデモ
- **Playground**: `web/playground.html` - ブラウザ内の5つのサンプル体験。全MCPツールの動作はローカルサーバーまたはCLIで確認してください。
- **Project Audit**: HTML/CSSの静的監査とトークン抽出。MCPツールでは対象パスが必須です。CLIは`openmcpart audit .`のように指定したローカルパスを読み取り、コード実行・ネットワーク通信・書き込みは行いません。
- **GitHub Action**: リポジトリ内で`uses: ./`として実行できるComposite Action。Markdownサマリーと重大度しきい値を提供します（GitHub上での実実行は未確認）。

---

## ✨ 特徴

- **MCP-compatible**: MCPを使うクライアントから接続可能。対応する機能・Transportはクライアントごとに確認
- **Flexible**: Paper & Inkなど複数のスタイル方向を提供。好みはブランドと用途に合わせて選択
- **Practical**: CSS / Tailwind / JSON形式の実装可能な出力。DTCG-style JSONも生成
- **Project-aware (static)**: 指定したローカルHTML/CSSのアクセシビリティ候補と既存トークンを検査
- **Japanese First**: 日本語フォント、日本語UXを考慮した提案
- **Local-first**: 外部AI APIキー不要。プロジェクト監査は読み取り専用でネットワークを使わない

---

## 🎨 スタイルプリセットの例: Paper & Ink

「AIっぽくない」は本プロジェクトの一つの美的方向性です。以下はPaper & Inkプリセットの例であり、すべてのブランドで避けるべきルールではありません。グラデーション、角丸、影などは目的に合えば使えます。

### Paper & Inkの方向性の例

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

## 🛠️ 提供ツール (18 tools)

### 🎨 Color カラー
| Tool | 説明 |
|------|------|
| `generate_color_palette` | ベースカラー/ムードから調和の取れたパレット生成。complementary, analogous, triadic等 |
| `check_color_contrast` | WCAGコントラスト比と閾値の参考評価 + 色覚多様性シミュレーション |
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
| `generate_design_tokens` | 解決済みHEXカラーを含むデザイントークン生成 (色, タイポ, 余白, 角丸, 影)。CSS / Tailwind / JSON / DTCG-style JSON |
| `generate_tailwind_config` | 検証済みの色スケールを含むTailwind設定ファイル生成 |
| `extract_project_tokens` | 明示したローカルプロジェクトからCSS変数、色、フォント、余白、角丸、影を読み取り専用で抽出 |

### ♿ Accessibility & Critique
| Tool | 説明 |
|------|------|
| `check_accessibility` | コントラスト・サイズ候補 + 手動チェックリスト。適合スコアは出さない |
| `audit_project` | 指定したローカルHTML/CSSプロジェクトを読み取り専用で静的監査。根拠・WCAG参考・制約を含む |
| `critique_design` | 説明文の明示的な懸念をキーワード検出し、8原則の手動レビュー項目を提示（画面画像やDOMは解析しません） |
| `suggest_component_variants` | UIコンポーネントバリエーション (Button, Card, Input等) |

### 🏷️ Branding ブランディング
| Tool | 説明 |
|------|------|
| `extract_design_principles` | ブランドキーワードからアーキタイプ・原則・パレット抽出 |
| `generate_moodboard_brief` | ムードボードブリーフ生成 (minimal, brutalism, glassmorphism, japanese等) |

### ✨ Sophisticated UI — AIっぽくない洗練 (NEW)
| Tool | 説明 |
|------|------|
| `generate_sophisticated_ui` | Paper & Ink, Clay & Moss, Editorial Noir, Atelierのスタイル仕様を生成。選んだ美的方向の例として利用 |
| `critique_ai_look` | 説明文に明示されたスタイルパターンだけをヒューリスティックに検出。美的好みを普遍的な不具合とは扱わない |

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
# MCPサーバーを起動
design-mcp
```

### ローカルプロジェクトを監査する

```bash
# HTML/CSSの静的アクセシビリティ候補をMarkdownで確認
openmcpart audit ./my-app

# CI向け: high以上の検出があれば終了コード1
openmcpart audit ./my-app --fail-on high

# JSONレポートを出力
openmcpart audit ./my-app --format json

# 既存デザイントークン候補を抽出
openmcpart tokens ./my-app --format json
```

走査は指定したディレクトリ内の対応テキストファイルのみを読み取ります。コード実行・ネットワークアクセス・ファイル書き込みは行いません。デフォルトで隠しフォルダ、依存関係フォルダ、生成物、1MBを超えるファイルを除外し、1回の走査は合計20MBまでです。検査結果は静的な候補であり、ブラウザや支援技術による確認の代替ではありません。

GitHub Actionsでは、このリポジトリのルート`action.yml`を使えます。公開タグを利用する際は、利用するリリースのタグまたはcommit SHAに固定してください:

```yaml
- uses: hrfrutrd-dev/openmcpart@main
  with:
    project-path: .
    fail-on: high
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
  "primary": "#70b8db",
  "secondary": "#db9370",
  "accent": "#a1d0e7",
  "css_variables": "--color-1: #70b8db; ..."
}
```

---

## 🏗️ アーキテクチャ

現在は **18 tools / 4 resources / 3 prompts**。構成・Transport・監査の制約は[Architecture](https://github.com/hrfrutrd-dev/openmcpart/blob/main/docs/ARCHITECTURE.md)を参照してください。

- stdioを標準Transportとして使用。SSE／streamable HTTPも実装
- ランタイム依存はMCP SDKとPydantic。監査ロジックは標準ライブラリ
- MCPツールとCLIはローカル計算。監査対象のコードを実行しない

---

## 🎯 デザイン原則

8ptグリッド、60-30-10、フォント数の制限などは**出発点となるヒューリスティック**です。ブランドやユーザーの要件に応じて調整してください。コントラスト基準も対象テキストの大きさ・用途に合わせて判定します。静的監査の結果だけでWCAG適合を保証することはありません。

---

## 🧪 テストとLint

```bash
pip install -e '.[dev]'
ruff check src tests
pytest -q

# MCP Inspectorでテスト
npx @modelcontextprotocol/inspector openmcpart
```

GitHub ActionsではPython 3.10–3.13のテスト、Lint、CLI smoke testを実行します。
GitHub Releaseを公開すると `.github/workflows/publish.yml` がPyPIへ配布します(Trusted Publishing、トークン不要)。手順は [docs/PUBLISHING_JA.md](https://github.com/hrfrutrd-dev/openmcpart/blob/main/docs/PUBLISHING_JA.md) を参照してください。

---

## 📖 ドキュメント

- [MCP公式ドキュメント](https://modelcontextprotocol.io)
- [examples/](https://github.com/hrfrutrd-dev/openmcpart/tree/main/examples) - 設定例と使用例
- [docs/USAGE_JA.md](https://github.com/hrfrutrd-dev/openmcpart/blob/main/docs/USAGE_JA.md) - MCP設定・CLI利用ガイド
- [docs/ARCHITECTURE.md](https://github.com/hrfrutrd-dev/openmcpart/blob/main/docs/ARCHITECTURE.md) - 構成・監査の範囲・安全性
- [docs/PUBLISHING_JA.md](https://github.com/hrfrutrd-dev/openmcpart/blob/main/docs/PUBLISHING_JA.md) - PyPI公開手順(Trusted Publishing / 手動アップロード)

---

## 🤝 コントリビュート

1. Fork
2. Feature branch (`git checkout -b feature/amazing`)
3. Commit (`git commit -m 'Add amazing feature'`)
4. Push (`git push origin feature/amazing`)
5. Pull Request

---

## 📄 ライセンス

MIT License - 詳細は [LICENSE](https://github.com/hrfrutrd-dev/openmcpart/blob/main/LICENSE) を参照

---

## 🙏 謝辞

- [Model Context Protocol](https://modelcontextprotocol.io) - 標準化されたAgent接続
- [Refactoring UI](https://www.refactoringui.com/) - デザイン原則
- [WCAG](https://www.w3.org/WAI/standards-guidelines/wcag/) - アクセシビリティ基準

---

**Made with ❤️ for MCP-compatible clients and local-first design workflows**

> "Good design is as little design as possible" - Dieter Rams
