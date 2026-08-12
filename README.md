# UnrealCV Runtime MCP

Public client examples and agent skills for the Runtime MCP service in
**UnrealCV Dev For UnrealZoo**.

The Runtime MCP server is currently distributed with supported UnrealZoo
environments and is tested there first. This repository does not contain the
server's Unreal Engine C++ implementation.

## Quick start

Start an UnrealZoo environment that provides Runtime MCP, then run:

```powershell
python .\examples\runtime_mcp_client.py --host 127.0.0.1 --port 29998 tools
python .\examples\runtime_mcp_client.py call scene.overview --arguments '{"radius":2500,"max_actors":20}'
python .\examples\runtime_mcp_client.py exec "vget /unrealcv/status"
```

The client uses only the Python standard library. It implements the framed TCP
transport used by UnrealCV and the Runtime MCP JSON-RPC methods `initialize`,
`ping`, `tools/list`, and `tools/call`.

## Agent skill

The reusable Codex skill is in
[`skills/unrealcv-runtime-mcp`](skills/unrealcv-runtime-mcp/SKILL.md). Install
that directory in your Codex skills folder, then invoke
`$unrealcv-runtime-mcp` for runtime inspection and command execution.

## Availability

- Open-source UnrealCV commands: <https://docs.unrealcv.org/en/latest/reference/commands.html>
- UnrealCV Dev For UnrealZoo documentation: <https://docs.unrealcv.org/en/latest/unrealcv_plus/index.html>
- UnrealZoo environments: <https://unrealzoo.github.io/>

Before relying on a command or MCP tool, list the capabilities exposed by the
connected runtime. Development builds can differ.

## License

MIT. See [LICENSE](LICENSE).
