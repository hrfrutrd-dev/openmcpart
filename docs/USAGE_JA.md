# MCP対応Agentでの利用ガイド

openmcpartはMCPサーバーです。利用できるTransportや設定形式はクライアントのバージョンにより異なるため、各Agentの最新ドキュメントも確認してください。サーバーには18 tools / 4 resources / 3 promptsがあります。

## クライアント設定例

このリポジトリには次の設定例があります。クライアントのMCPサポート、設定形式、Transportはリリースにより変わることがあるため、利用中のバージョンの公式手順を優先してください。

| クライアント | サンプル | 備考 |
|---|---|---|
| Claude Desktop | [`examples/claude_desktop_config.json`](../examples/claude_desktop_config.json) | stdio起動例 |
| Cursor | [`examples/cursor_mcp.json`](../examples/cursor_mcp.json) | MCPサーバー設定例 |
| VS Code | [`examples/vscode_mcp.json`](../examples/vscode_mcp.json) | サーバー設定例 |
| その他のMCPクライアント | 設定なし | クライアントが対応するTransport・設定形式を確認 |
| Pythonクライアント | [`examples/client_example.py`](../examples/client_example.py) | MCP Python SDKのstdio例 |

## MCPクライアントとの接続

### 1. MCPプロトコル

MCP対応クライアントから利用できます。クライアント側のTransport、設定形式、利用できるResources／Promptsは各クライアントで異なる場合があります。

```
Agent (Client) <--MCP--> Server (このMCP)
     |                        |
     |  tools/list            |  18 tools
     |  tools/call            |  4 resources
     |  resources/read        |  3 prompts
     |  prompts/get           |
```

### 2. stdio Transport

ローカルのMCPクライアントで使う標準的な構成例です。対応状況や設定形式は各クライアントで確認してください。

```json
{
  "command": "openmcpart",
  "args": []
}
```

これはstdio接続の基本形です。実際の設定キーや対応Transportは、利用するクライアントのドキュメントも確認してください。

### 3. 実行モードと通信

- 外部AI APIキーは不要です。
- stdioとCLIはローカル実行です。プロジェクト監査は明示されたフォルダを読み取り専用で検査します。
- SSE / streamable HTTPを選んだ場合はHTTPサーバーを起動します。既定は`127.0.0.1`だけにbindします。コンテナ内では`MCP_HOST=0.0.0.0`を設定し、ポート公開を必要な範囲に制限してください。
- HTTPサーバーを公開ネットワークへ置く場合は、MCPサーバー単体に認証を任せず、認証・アクセス制御を別途設計してください。
- ランタイム依存はMCP SDKとPydanticです。

## 各Agentでの使い方

### Claude Desktop

1. 設定ファイルを開く:
   - Mac: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. 追加:

```json
{
  "mcpServers": {
    "openmcpart-design": {
      "command": "uvx",
      "args": ["openmcpart"]
    }
  }
}
```

3. Claude Desktop再起動

4. 使う:

```
あなた: このサイトの配色を考えて、信頼感のある青系で
Claude: [generate_color_paletteを呼び出し] 信頼感のある青系パレットを生成しました...
```

### Cursor

1. `.cursor/mcp.json`作成:

```json
{
  "mcpServers": {
    "openmcpart-design": {
      "command": "openmcpart"
    }
  }
}
```

2. Cursor再起動

3. Agent Chatで:

```
@openmcpart-design ボタンコンポーネントのバリエーションを教えて
```

### VS Code

1. `.vscode/mcp.json`:

```json
{
  "servers": {
    "openmcpart-design": {
      "type": "stdio",
      "command": "openmcpart"
    }
  }
}
```

2. Copilot Chatで `@workspace` や `#tool` 経由で呼び出し

### 自作Python Agent

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    params = StdioServerParameters(command="openmcpart", args=[])
    async with stdio_client(params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            tools = await session.list_tools()
            print(tools)
            result = await session.call_tool(
                "generate_color_palette", {"mood": "calm", "count": 5}
            )
            print(result)

asyncio.run(main())
```

### 自作TypeScript Agent

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const transport = new StdioClientTransport({
  command: "openmcpart"
});

const client = new Client({ name: "my-agent", version: "1.0" });
await client.connect(transport);

const result = await client.callTool({
  name: "generate_color_palette",
  arguments: { mood: "calm" }
});
```

### HTTP経由 (streamable HTTP)

```bash
openmcpart --transport streamable-http --host 127.0.0.1 --port 8000
```

別プロセスのPythonクライアントから接続する例:

```python
import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

async def main():
    async with streamable_http_client("http://127.0.0.1:8000/mcp") as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.call_tool(
                "check_color_contrast",
                {"foreground": "#ffffff", "background": "#000000"},
            )
            print(result)

asyncio.run(main())
```

HTTP transportをインターネットに公開する場合、MCPサーバー単体に認証を任せず、信頼できるネットワーク境界・認証プロキシなどを用意してください。

## ローカルプロジェクト監査 (CLI)

```bash
# 読み取り専用のHTML/CSS静的監査
openmcpart audit ./my-app

# high以上の候補が見つかったらCIを失敗させる
openmcpart audit ./my-app --fail-on high

# JSON形式の結果
openmcpart audit ./my-app --format json

# CSSトークン候補を抽出
openmcpart tokens ./my-app --format json
```

監査は指定ディレクトリ内の対応テキストファイルを読むだけで、コード実行、ネットワーク通信、書き込みはしません。CSSの継承、動的な画面、スクリーンリーダー動作などは評価できません。結果をWCAG適合証明として扱わず、実ブラウザ・支援技術でも確認してください。詳しくは[Architecture](./ARCHITECTURE.md)を参照。

## ツールの呼び出し方 (自然言語)

Agentに自然言語で指示するだけで、裏側で適切なツールが呼ばれます。

| あなたの指示 | 呼ばれるツール |
|--------------|---------------|
| 「青系のパレット作って」 | `generate_color_palette` |
| 「この配色、コントラスト大丈夫？」 | `check_color_contrast` |
| 「グラデーション作って」 | `generate_gradient` |
| 「フォントペアリング提案して」 | `suggest_typography_pairing` |
| 「文字サイズのスケール作って」 | `generate_type_scale` |
| 「ダッシュボードのレイアウト考えて」 | `suggest_layout` |
| 「余白のルール教えて」 | `generate_spacing_system` |
| 「デザインシステム作って」 | `generate_design_tokens` |
| 「Tailwind設定作って」 | `generate_tailwind_config` |
| 「アクセシビリティチェックして」 | `check_accessibility` |
| 「デザイン批評して」 | `critique_design` |
| 「ボタンのバリエーション教えて」 | `suggest_component_variants` |
| 「ブランドからデザイン原則出して」 | `extract_design_principles` |
| 「ムードボード作って」 | `generate_moodboard_brief` |
| 「指定したHTML/CSSを静的監査して」 | `audit_project` |
| 「既存CSSのデザイントークン候補を抽出して」 | `extract_project_tokens` |

## ベストプラクティス

### 1. ワークフロー化

```
ブランディング → カラー → タイポ → トークン → レイアウト → コンポーネント → チェック
```

MCPツール呼び出しに対応するAgentであれば、たとえば「SaaSのランディングページをゼロからデザインして」と依頼して関連ツールを活用できます。どのツールを呼び出すかはAgentとクライアントの挙動によります。

### 2. 日本語対応

- 「日本語サイト向けに」「Noto Sans JPで」など日本語で指示
- `language: ja` パラメータが自動で使われる

### 3. 実装可能な出力

出力形式はツールごとに異なります。トークン生成ツールはCSS変数・Tailwind config・JSON・DTCG-style JSONを出力しますが、Figma向けの直接連携はなく、プラグイン互換性は利用先で確認してください。

## トラブルシューティング

### ツールが表示されない

- MCPクライアントを再起動
- `openmcpart` がPATHにあるか確認: `which openmcpart`
- ログ確認: Claude Desktopなら `~/Library/Logs/Claude/mcp*.log`

### 色がおかしい

- hexは `#3b82f6` 形式で
- moodは英語推奨: calm, energetic, luxury等 (日本語も一部対応)

### 日本語フォントが提案されない

- `language: ja` または `language: japanese` を明示
- moodに `japanese` を含める

## まとめ

- MCP対応クライアント向けのstdio設定例
- 自然言語からMCPツールを呼び出す利用方法
- CSS / Tailwind / JSON / DTCG-style JSONの出力
- 日本語フォントや日本語UXを考慮した提案
- 外部AI APIキー不要。ローカルソース監査は読み取り専用

MCPクライアントでデザイン支援を使い、必要に応じてCLIでローカルソースを静的監査できます。
