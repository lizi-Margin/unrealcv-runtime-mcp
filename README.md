# UnrealCV Runtime MCP

Public client examples and agent skills for the Runtime MCP service in
**UnrealCV Dev For UnrealZoo**.

The Runtime MCP server is currently distributed with supported UnrealZoo
environments and is tested there first. This repository does not contain the
server's Unreal Engine C++ implementation.

## Examples

### Complex Scene Navigation

The agent spawns a character, switches to first-person view, finds two sakura
trees, approaches the second tree to within 0.5 meters, and captures a final
third-person composition.

[<img src="examples/complex_scene_navigation/MCP_Scene_Nav_480x270.gif" width="480" alt="Complex scene navigation with UnrealCV Runtime MCP">](examples/complex_scene_navigation/MCP_Scene_Nav_1080x576.gif)

| 1. Initial First Person View | 2. First Sakura Reached | 3. Second Sakura Reached |
|:---:|:---:|:---:|
| <img src="examples/complex_scene_navigation/01_initial_first_person_sakura_spotted.png" width="100%" alt="Try to find the sakura tree"> | <img src="examples/complex_scene_navigation/02_first_sakura_reached.png" width="100%" alt="Character reaches the first sakura tree"> | <img src="examples/complex_scene_navigation/03_second_sakura_close_range.png" width="100%" alt="Character reaches the second sakura tree at close range"> |
| Try to find the sakura tree | The character navigates to the first sakura | The character approaches the second sakura to within 0.5 m |

| 4. Front Framing | 5. Left Framing | 6. Right Framing | 7. Final Capture |
|:---:|:---:|:---:|:---:|
| <img src="examples/complex_scene_navigation/04_detached_camera_front_framing.png" width="100%" alt="Detached camera testing a front framing"> | <img src="examples/complex_scene_navigation/05_detached_camera_left_framing.png" width="100%" alt="Detached camera testing a left framing"> | <img src="examples/complex_scene_navigation/06_detached_camera_right_framing.png" width="100%" alt="Detached camera testing a right framing"> | <img src="examples/complex_scene_navigation/07_final_character_and_sakura.png" width="100%" alt="Final capture containing the character and sakura tree"> |
| Camera detached and moved to the front | Composition evaluated from the left | Composition evaluated from the right | Character and sakura framed together |

**Prompt:** [View the original prompt](examples/complex_scene_navigation/prompt.md) &middot;
**Workflow:** [View the execution details](examples/complex_scene_navigation/procedure.md)

### Scene Captioning

The agent uses UnrealCV Runtime MCP tools to perceive the scene, rotate the
camera, and capture views in six directions. The six images below are the
resulting north, east, south, west, upward, and downward observations used to
produce a caption of the complete environment.

[<img src="examples/scene_caption/MCP_Scene_Caption_480x270.gif" width="480" alt="Multi-direction scene captioning with UnrealCV Runtime MCP">](examples/scene_caption/MCP_Scene_Caption_1080x576.gif)

| North | East | South |
|:---:|:---:|:---:|
| <img src="examples/scene_caption/north.png" width="100%" alt="Scene captured while looking north"> | <img src="examples/scene_caption/east.png" width="100%" alt="Scene captured while looking east"> | <img src="examples/scene_caption/south.png" width="100%" alt="Scene captured while looking south"> |

| West | Up | Down |
|:---:|:---:|:---:|
| <img src="examples/scene_caption/west.png" width="100%" alt="Scene captured while looking west"> | <img src="examples/scene_caption/up.png" width="100%" alt="Scene captured while looking upward"> | <img src="examples/scene_caption/down.png" width="100%" alt="Scene captured while looking downward"> |

> A vibrant, compact stylized Tokyo district of dense mid-rise buildings,
> neon signage, elevated structures, narrow streets and sidewalks, all
> threaded with abundant pink cherry blossoms beneath a bright blue sky.

**Prompt:** [View the original prompt](examples/scene_caption/prompt.md) &middot;
**Workflow:** [View the captioning process](examples/scene_caption/procedure.md) &middot;
**Result:** [View the caption](examples/scene_caption/result.md)

### Blueprint Function Calling (Change Character Appearance)

The agent uses UnrealCV Runtime MCP tools to discover the character's Blueprint API, call `set_app(NewParam)` to switch its appearance,
and photograph each result. The ten images below were captured by the agent
after applying the ten appearance variants.

[<img src="examples/change_character_appearance/MCP_set_app_480x270.gif" width="480" alt="Changing character appearances through a Blueprint function">](examples/change_character_appearance/MCP_set_app_1080x576.gif)

<table>
  <tr>
    <td width="25%"><img src="examples/change_character_appearance/scene_capture_camera0_02361BD7497A7A2B.png" width="100%" alt="Captured character appearance 1"></td>
    <td width="25%"><img src="examples/change_character_appearance/scene_capture_camera0_0AFAD5F74A646BBB.png" width="100%" alt="Captured character appearance 2"></td>
    <td width="25%"><img src="examples/change_character_appearance/scene_capture_camera0_1770029B466F96B5.png" width="100%" alt="Captured character appearance 3"></td>
    <td width="25%"><img src="examples/change_character_appearance/scene_capture_camera0_220DDDD84A4CE6B4.png" width="100%" alt="Captured character appearance 4"></td>
  </tr>
  <tr>
    <td><img src="examples/change_character_appearance/scene_capture_camera0_2666930E4792C594.png" width="100%" alt="Captured character appearance 5"></td>
    <td><img src="examples/change_character_appearance/scene_capture_camera0_288557AF4FE4C721.png" width="100%" alt="Captured character appearance 6"></td>
    <td><img src="examples/change_character_appearance/scene_capture_camera0_752B949D4BE1825E.png" width="100%" alt="Captured character appearance 7"></td>
    <td><img src="examples/change_character_appearance/scene_capture_camera0_91C39BDB47E3D6B2.png" width="100%" alt="Captured character appearance 8"></td>
  </tr>
  <tr>
    <td colspan="2" align="center"><img src="examples/change_character_appearance/scene_capture_camera0_BD21E84447B2618F.png" width="50%" alt="Captured character appearance 9"></td>
    <td colspan="2" align="center"><img src="examples/change_character_appearance/scene_capture_camera0_EDE9EA1E4A5D8B99.png" width="50%" alt="Captured character appearance 10"></td>
  </tr>
</table>

**Prompt:** [View the original prompt](examples/change_character_appearance/prompt.md) &middot;
**Workflow:** [View the execution details](examples/change_character_appearance/procedure.md)

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
```

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
