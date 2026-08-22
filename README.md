# UnrealCV Runtime MCP

Public client examples and agent skills for the Runtime MCP service in
**UnrealCV Dev For UnrealZoo**.

The Runtime MCP server is currently distributed with supported UnrealZoo
environments and is tested there first. This repository does not contain the
server's Unreal Engine C++ implementation.

## Examples
### Complex Scene Navigation

### Scene Captioning

### Blueprint Function Calling (Change Character Appearance)

## Get Started

### Universal configuration
Add the following configuration to a local `.mcp.json` file or to your coding agent's MCP configuration file:

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

### Codex configuration
Add the following configuration to `~/.codex/config.toml`:
```toml
[mcp_servers.unrealcv]
url = "http://127.0.0.1:29998/mcp"
enabled = true
```

## Supported Protocols

| Layer                   | Current Support                                |
| ----------------------- | ---------------------------------------------- |
| Application Protocol    | Model Context Protocol (MCP)                   |
| MCP Versions            | 2025-11-25, 2025-06-18, 2025-03-26, 2024-11-05 |
| RPC                     | JSON-RPC 2.0                                   |
| Transport               | Streamable HTTP                                |
| Standard Responses      | `application/json`                             |
| Streaming Responses     | `text/event-stream` using SSE `message` events |
| Session Management      | `Mcp-Session-Id`                               |
| Protocol Version Header | `Mcp-Protocol-Version`                         |
| Default Endpoint        | `http://127.0.0.1:29998/mcp`                   |



## Availability

- Open-source UnrealCV commands: <https://docs.unrealcv.org/en/latest/reference/commands.html>
- UnrealCV Dev For UnrealZoo documentation: <https://docs.unrealcv.org/en/latest/unrealcv_plus/index.html>
- UnrealZoo environments: <https://unrealzoo.github.io/>

## License

MIT. See [LICENSE](LICENSE).
