---
name: unrealcv-generate-scene
description: Generate and validate an Unreal Engine runtime scene from a natural-language description and a world coordinate through UnrealCV Runtime MCP. Use when Codex needs to find the ground below a coordinate, inspect the scene without vision, select bounded asset search results, place and settle non-overlapping actors, or return a human-visible six-view evaluation of a generated scene.
---

# UnrealCV Generate Scene

Use `../../examples/runtime_mcp_client.py` for every Runtime MCP call. Read
[`references/tool-workflow.md`](references/tool-workflow.md) before generating a
scene; it defines the tool contracts, placement gates, retries, rollback rules,
and required final result.

## Workflow

1. Run `tools` and verify the connected runtime exposes `perception.snapshot`,
   `scene.raycast_down`, `camera.set_view_preset`, `assets.search`,
   `assets.get_bounds`, `spawn.from_asset`, `spawn.validate_placement`, and
   `scene.capture_view`. Stop with a missing-capability error otherwise.
2. Parse the description into an ordered object plan with count, approximate
   size, asset search terms, rotations, and spatial relationships. Use the
   mature asset-spawn route unless the runtime exposes a suitable generative
   ToolSet and it is materially better for the requested object.
3. Call `scene.raycast_down` from the supplied coordinate. Reject a miss or an
   unsuitable surface. Use the hit point as the local scene anchor.
4. Move to a `top_down` view at a distance derived from the largest planned
   object. Call `perception.snapshot`, `scene.check_region`, and one top-down
   capture before changing the scene. Reject a blocked region that cannot be
   resolved within three candidate offsets.
5. For each planned object, search assets with `limit` at most 30, inspect
   candidate bounds, choose a placement that preserves clearance from all
   previously generated actors, call `spawn.from_asset`, and immediately call
   `spawn.validate_placement`.
6. Roll back the current actor with `spawn.destroy` when spawn, settle, overlap,
   or validation fails. Try at most three placements or asset candidates per
   object. Do not remove actors that predated this workflow.
7. After all objects exist, capture the six required views. Reframe and recapture
   when the camera is inside geometry, the target is absent, or framing is not
   useful. Allow at most three capture attempts per view.
8. Inspect all six images plus structured placement results. Report failure for
   missing actors, wrong count, major penetration, floating or buried objects,
   or unresolved camera clipping.
9. Return the final actor manifest, transforms, bounds, validation findings, and
   all six MCP image contents so they remain visible to the human.

## Guardrails

- Treat centimeters as Unreal world units and rotations as degrees.
- Keep a workflow-owned actor list and rollback list after every state change.
- Never accept an overlap with another workflow-generated actor.
- Never claim success from a command response alone; validate placement and the
  six final images.
- Keep searches and perception results bounded. Do not dump unlimited assets or
  scene actors into context.
- Stop with an actionable error after bounded retries instead of silently
  changing the requested object count or scene semantics.
