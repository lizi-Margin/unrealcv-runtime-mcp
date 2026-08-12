---
name: unrealcv-runtime-mcp
description: Inspect and control a running UnrealZoo environment through UnrealCV Runtime MCP. Use when Codex needs to list Runtime MCP tools, inspect nearby scene actors, capture a runtime view, or execute an UnrealCV command against an UnrealCV Dev For UnrealZoo build on TCP port 29998.
---

# UnrealCV Runtime MCP

Use `../../examples/runtime_mcp_client.py` as the transport client. The server is
available only in supported UnrealCV Dev For UnrealZoo environments; do not
assume the open-source UnrealCV plugin includes it.

## Workflow

1. Confirm the UnrealZoo environment is running and port `29998` is reachable.
2. Run `python ../../examples/runtime_mcp_client.py tools` and treat the returned
   tool list as authoritative for the connected build.
3. Prefer compact agent tools:
   - Call `scene.overview` before inspecting individual actors.
   - Call `scene.inspect_actor` only for actors selected from the overview.
   - Call `scene.capture_view` only when structured scene data is insufficient.
4. Use `unrealcv.describe_command` before an unfamiliar raw command.
5. Use `unrealcv.exec` only after confirming the command exists with
   `unrealcv.list_cmd` or the open-source command reference.
6. Report the host, port, tool called, important structured result, and any MCP
   or UnrealCV error. Do not claim a state change without reading the response.

## Commands

```powershell
python ../../examples/runtime_mcp_client.py ping
python ../../examples/runtime_mcp_client.py tools
python ../../examples/runtime_mcp_client.py call scene.overview --arguments '{"radius":2500,"max_actors":20}'
python ../../examples/runtime_mcp_client.py call scene.inspect_actor --arguments '{"actor":"ActorName"}'
python ../../examples/runtime_mcp_client.py exec "vget /unrealcv/status"
```

Pass `--host`, `--port`, or `--timeout` before the subcommand when the runtime
does not use the defaults.

## Guardrails

- Treat the runtime as trusted-network software; do not expose port `29998` to
  untrusted networks.
- Ask before destructive or broad state-changing commands.
- Do not invent unavailable tools or arguments. Re-run `tools` after changing
  environments or builds.
- Keep responses compact. Prefer structured fields over screenshots or large
  raw command dumps.
