# Audited Scene Generation Demo

This directory is a complete Runtime MCP trace for one generated Tokyo street
scene. The scene contains a bench, table, and traffic cone placed on the first
walkable surface below the supplied coordinate.

All evaluation images are real 1920x1080 PNG files read from the main viewport
backbuffer. Every capture response records `uses_base_camera_sensor: false`;
no `UBaseCameraSensor` subclass was used.

Evidence:

- `manifest.json`: input, world, ground hit, assets, transforms, validation,
  capture provenance, evaluation, and cleanup state.
- `requests.jsonl` and `responses.jsonl`: ordered MCP audit trail. Image base64
  is replaced with a local file path and SHA-256.
- `tools.json`: exact Runtime MCP tool snapshot.
- `images/`: pre-generation image plus six final evaluation views.
- `checksums.sha256`: SHA-256 for every PNG.
