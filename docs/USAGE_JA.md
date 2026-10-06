# どんなAgentでも使える - 完全ガイド

このMCPサーバーは **MCP標準準拠** なので、1回実装すれば全Agentで使えます。

## 対応Agent一覧

| Agent / ツール | 対応 | 設定ファイル | Transport |
|----------------|------|--------------|-----------|
| Claude Desktop | ✅ | `claude_desktop_config.json` | stdio |
| Cursor | ✅ | `.cursor/mcp.json` | stdio |
| VS Code Copilot | ✅ | `.vscode/mcp.json` | stdio |
| Windsurf | ✅ | `mcp_config.json` | stdio |
| Cline | ✅ | `cline_mcp_settings.json` | stdio |
| ChatGPT (MCP対応) | ✅ | 環境による | stdio / sse |
| 自作Agent (Python) | ✅ | コードで指定 | stdio / http |
| 自作Agent (TS) | ✅ | コードで指定 | stdio / http |
| n8n, Make等 | ✅ | HTTP経由 | sse / streamable-http |

## なぜ「どんなAgentでも」使えるのか？

### 1. MCP標準準拠

Model Context ProtocolはAnthropicが提唱し、OpenAI, Google, Microsoftも採用するオープンスタンダード。

```
Agent (Client) <--MCP--> Server (このMCP)
     |                        |
     |  tools/list            |  13 tools
     |  tools/call            |  4 resources
     |  resources/read        |  3 prompts
     |  prompts/get           |
```

### 2. stdio Transport

最も互換性が高いstdioを使用。すべてのMCPクライアントが対応。

```json
{
  "command": "openmcpart",
  "args": []
}
```

これだけで動く。

### 3. 外部依存なし

- APIキー不要
- ネットワーク不要 (ローカル完結)
- 軽量 (依存はmcpとpydanticのみ)

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
from mcp import Client
from mcp.client.stdio import StdioServerParameters

async def main():
    params = StdioServerParameters(command="openmcpart")
    async with Client(params) as client:
        # ツール一覧
        tools = await client.list_tools()
        print(tools)
        
        # カラーパレット生成
        result = await client.call_tool("generate_color_palette", {
            "mood": "calm"
        })
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

### HTTP経由 (n8n, Zapier, Web)

```bash
# SSE transportで起動
MCP_TRANSPORT=sse MCP_PORT=8000 openmcpart
# または
openmcpart --transport sse --port 8000
```

その後、HTTPクライアントから:

```python
from mcp import Client

async with Client("http://localhost:8000/sse") as client:
    result = await client.call_tool("check_color_contrast", {
        "foreground": "#ffffff",
        "background": "#000000"
    })
```

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

## ベストプラクティス

### 1. ワークフロー化

```
ブランディング → カラー → タイポ → トークン → レイアウト → コンポーネント → チェック
```

Agentに「SaaSのランディングページをゼロからデザインして」と言えば、このフローで全ツールを使ってくれます。

### 2. 日本語対応

- 「日本語サイト向けに」「Noto Sans JPで」など日本語で指示
- `language: ja` パラメータが自動で使われる

### 3. 実装可能な出力

すべてのツールはCSS/Tailwind/Figmaで使える形式を出力。Agentはそのままコードを生成できます。

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

- **1回設定で全Agent対応**
- **自然言語でデザイン指示**
- **プロの出力 (CSS/Tailwind/Figma)**
- **日本語完全対応**
- **外部API不要**

これが「どんなAgentでも使える」デザインMCPサーバーです。
