# UnrealCV Runtime MCP

Public client examples and agent skills for the Runtime MCP service in
**UnrealCV Dev For UnrealZoo**.

The Runtime MCP server is currently distributed with supported UnrealZoo
environments and is tested there first. This repository does not contain the
server's Unreal Engine C++ implementation.

## Examples


## Get Started

Universal configuration
write this to a .mcp.json local file or your coding agent's config file.
```json
{
  "mcpServers": {
    "unrealcv": {
      "type": "http",
      "url": "http://127.0.0.1:29998/mcp",
      "disabled": false
    }
  }
}
```

Codex configuration
write this to ~/.codex/config.toml
```toml
[mcp_servers.unrealcv]
url = "http://127.0.0.1:29998/mcp"
enabled = true
```

## 支持的协议

 层级            当前支持
━━━━━━━━━━━━━━  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 应用协议        Model Context Protocol（MCP）
──────────────  ────────────────────────────────────────────────
 MCP 版本        2025-11-25、2025-06-18、2025-03-26、2024-11-05
──────────────  ────────────────────────────────────────────────
 RPC             JSON-RPC 2.0
──────────────  ────────────────────────────────────────────────
 传输            Streamable HTTP 风格
──────────────  ────────────────────────────────────────────────
 普通响应        application/json
──────────────  ────────────────────────────────────────────────
 流式响应格式    text/event-stream，SSE message event
──────────────  ────────────────────────────────────────────────
 会话            Mcp-Session-Id
──────────────  ────────────────────────────────────────────────
 版本请求头      Mcp-Protocol-Version
──────────────  ────────────────────────────────────────────────
 默认端点        http://127.0.0.1:29998/mcp


## Availability

- Open-source UnrealCV commands: <https://docs.unrealcv.org/en/latest/reference/commands.html>
- UnrealCV Dev For UnrealZoo documentation: <https://docs.unrealcv.org/en/latest/unrealcv_plus/index.html>
- UnrealZoo environments: <https://unrealzoo.github.io/>

Before relying on a command or MCP tool, list the capabilities exposed by the
connected runtime. Development builds can differ.

## License

MIT. See [LICENSE](LICENSE).
