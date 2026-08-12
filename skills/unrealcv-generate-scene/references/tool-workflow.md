# Scene Generation Tool Workflow

## Tool contracts

Call tools with:

```powershell
python ../../examples/runtime_mcp_client.py call TOOL --arguments 'JSON'
```

Treat the live `tools` result as authoritative. Expected mature-route tools:

| Tool | Purpose | Important arguments |
| --- | --- | --- |
| `perception.snapshot` | Native, non-visual scene state | `radius_cm`, `max_objects` <= 64, `max_rays` <= 16 |
| `scene.raycast_down` | Find the first blocking ground surface | `x`, `y`, `z`, optional `trace_length_cm` |
| `scene.check_region` | Preflight an axis-aligned placement region | `center_x/y/z`, `extent_x/y/z` |
| `camera.get_pose` | Read the main view | none |
| `camera.set_view_preset` | Place and aim the main camera | `target`, `preset`, `distance_cm` |
| `camera.frame_bounds` | Frame one actor outside its bounds | `actor`, `preset`, `margin` |
| `assets.search` | Bounded spawnable asset discovery | `path`, `search_spec`, `offset`, `limit` <= 30 |
| `assets.get_bounds` | Load native or measured asset bounds | `asset_path` |
| `spawn.from_asset` | Spawn, settle, annotate, and overlap-check | `asset_path`, `location`, optional `rotation`, `name`, `settle` |
| `spawn.validate_placement` | Verify overlap and ground contact | `actor` |
| `spawn.get_overlaps` | Diagnose an invalid placement | `actor` |
| `spawn.destroy` | Roll back a workflow actor | `actor` |
| `scene.capture_view` | Return an MCP image | `camera_id`, `mode=lit` |

The raw compatibility commands include:

```text
vget /scene/perception [radius_cm] [max_objects] [max_rays]
vget /scene/raycast_down [x] [y] [z] [trace_length]
vget /objects/scan_assets [path] [search_spec]
```

Prefer the structured MCP tools over parsing raw command text.

`top_down` and `z_positive` are aliases, as are `bottom_up` and `z_negative`.

## Planning

Convert the description into an ordered manifest. For each object record:

- semantic role and requested count;
- likely asset search terms and acceptable substitutes;
- approximate width, depth, and height in centimeters;
- preferred yaw and relation to the scene anchor or another object;
- required clearance and whether exact identity is mandatory.

Use `top_down` as the default planning view. A passenger car commonly needs a
camera distance of at least 300 cm; increase the distance using the largest
planned diagonal and scene footprint.

## Ground and region gate

1. Trace down from the input coordinate.
2. Require `hit=true`; prefer `walkable=true` for ordinary props and vehicles.
3. Build a candidate box from the asset bounds and intended transform.
4. Call `scene.check_region` before spawning.
5. Offset candidates on a deterministic expanding grid around the anchor. Try
   at most three candidates per object.
6. Treat intersections with workflow-generated actors as hard conflicts.
   Existing floors and terrain may intersect the candidate vertically at the
   contact plane; the post-spawn ground-contact check decides validity.

## Asset selection

Search with `limit=30`. Use pagination only when the first page contains no
reasonable candidate. Prefer native StaticMesh or SkeletalMesh bounds; accept a
transient measured Blueprint bound when native bounds are unavailable. Reject
assets with zero or implausible bounds. Compare aspect ratio and scale to the
description before spawning.

Do not scale an asset merely to disguise a category mismatch. Choose another
asset or fail with the candidates considered.

## Spawn transaction

For each object:

1. Add a pending manifest entry.
2. Call `spawn.from_asset` with `settle="bounds"` by default and
   `reject_overlaps=1`.
3. Record the returned actor name immediately.
4. Call `spawn.validate_placement`.
5. On failure, optionally call `spawn.get_overlaps` for diagnosis, then destroy
   only that actor and mark the attempt rolled back.
6. On success, append the actor, transform, bounds, asset path, and validation
   result to the committed manifest.

Do not proceed to the next object while the current placement is unresolved.

## Six-view evaluation

Return exactly these six final views:

1. `top_down`
2. `x_positive_down_45`
3. `x_negative_down_45`
4. `y_positive_down_45`
5. `y_negative_down_45`
6. `hero_view`

Use `camera.set_view_preset` for the first five. For `hero_view`, frame the main
subject with `camera.frame_bounds` using the most informative diagonal preset,
then adjust distance if needed. Capture each with `scene.capture_view` in `lit`
mode.

For every image check:

- at least one intended object is visible;
- the camera is not inside an object;
- framing contains the relevant scene footprint;
- no major object-object penetration is visible;
- no object is clearly floating or deeply buried.

Move outward and retry a failed view at most three times. Keep the last valid
image content for each named view.

## Final result

Return a compact structured summary followed by the six image contents:

```json
{
  "status": "success|error",
  "anchor": {"x": 0, "y": 0, "z": 0},
  "generation_route": "asset_spawn|generative",
  "actors": [
    {
      "actor": "name",
      "asset_path": "/Game/...",
      "transform": {},
      "bounds": {},
      "placement_valid": true
    }
  ],
  "rolled_back": [],
  "evaluation": {
    "object_count_ok": true,
    "overlap_ok": true,
    "grounding_ok": true,
    "six_views_ok": true
  },
  "views": [
    "top_down",
    "x_positive_down_45",
    "x_negative_down_45",
    "y_positive_down_45",
    "y_negative_down_45",
    "hero_view"
  ]
}
```

When returning an error, preserve successful committed actors unless the user
requested all-or-nothing behavior. State which requirement failed, attempts
made, actors left in the scene, and actors rolled back.
