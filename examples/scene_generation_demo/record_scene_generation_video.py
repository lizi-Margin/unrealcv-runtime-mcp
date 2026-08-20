"""Record the Runtime MCP scene-generation and guided-agent demo."""

from __future__ import annotations

import base64
import io
import subprocess
import tempfile
import time
from pathlib import Path
import sys

import cv2
import numpy as np
from imageio_ffmpeg import get_ffmpeg_exe
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "examples"))
from runtime_mcp_client import RuntimeMCPClient  # noqa: E402


def capture(client: RuntimeMCPClient, path: Path, caption: str) -> None:
    result = client.call_tool("scene.capture_view", {"source": "mqrc", "width": 960, "height": 540})
    image = next(item for item in result["content"] if item.get("type") == "image")
    frame = Image.open(io.BytesIO(base64.b64decode(image["data"]))).convert("RGB")
    draw = ImageDraw.Draw(frame)
    draw.rectangle((0, 0, frame.width, 74), fill=(12, 18, 28))
    draw.text((24, 14), "UnrealCV Runtime MCP", fill=(245, 248, 255))
    draw.text((24, 42), caption, fill=(172, 205, 230))
    frame.save(path)


def warmup(client: RuntimeMCPClient, frames: int = 8) -> None:
    for _ in range(frames):
        client.call_tool("scene.capture_view", {"source": "mqrc", "width": 960, "height": 540})
        time.sleep(0.08)


def call(client: RuntimeMCPClient, name: str, arguments: dict) -> dict:
    result = client.call_tool(name, arguments)
    if result.get("isError"):
        raise RuntimeError(f"{name} failed: {result}")
    return result.get("structuredContent", {})


def main() -> int:
    output = Path("artifacts/runtime_mcp_scene_generation.mp4").resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="runtime_mcp_video_") as temp:
        frame_dir = Path(temp)
        with RuntimeMCPClient() as client:
            ground = call(client, "scene.raycast_down", {"x": -4500, "y": -500, "z": 2000})
            ground_z = float(ground["location"]["z"])
            target = {"x": -4510.0, "y": -500.0, "z": ground_z + 120.0}
            call(client, "camera.set_view_preset", {"target": target, "preset": "top_down", "distance_cm": 760})
            warmup(client)
            capture(client, frame_dir / "frame_00000.png", "Natural-language instruction: create a street-side rest point")

            planned = [
                ("bench", "/Game/TokyoStylizedEnvironment/Meshes/Unique_Props/SM_Bench.SM_Bench", {"x": -4700, "y": -500, "z": ground_z + 160}),
                ("table", "/Game/RoofProps/Geometry/Props/SM_table.SM_table", {"x": -4400, "y": -500, "z": ground_z + 160}),
                ("character", "/Game/Characters/BP_Character.BP_Character", {"x": -5000, "y": -700, "z": ground_z + 100}),
            ]
            for role, asset_path, location in planned:
                actor_name = f"MCPVideo_{role}"
                call(client, "spawn.from_asset", {"asset_path": asset_path, "location": location, "name": actor_name, "settle": "bounds", "reject_overlaps": 0})
                call(client, "spawn.validate_placement", {"actor": actor_name})
                warmup(client, 4)
                capture(client, frame_dir / f"frame_{len(list(frame_dir.glob('*.png'))):05d}.png", f"MCP tool call: spawn and validate {role}")

            call(client, "camera.set_view_preset", {"target": target, "preset": "x_positive_down_45", "distance_cm": 920})
            for index in range(12):
                progress = index / 11.0
                x = -4800 + 180 * progress
                y = -700 + 200 * progress
                command = f"vset /object/MCPVideo_character/location {x:.2f} {y:.2f} {ground_z + 80:.2f}"
                client.call_tool("unrealcv.exec", {"command": command})
                capture(client, frame_dir / f"frame_{len(list(frame_dir.glob('*.png'))):05d}.png", "Natural-language instruction: move the character to the bench")
                warmup(client, 2)

            for actor in ("MCPVideo_character", "MCPVideo_table", "MCPVideo_bench"):
                call(client, "spawn.destroy", {"actor": actor})

        command = [get_ffmpeg_exe(), "-y", "-framerate", "3", "-i", str(frame_dir / "frame_%05d.png"), "-vf", "format=yuv420p", "-c:v", "libx264", "-crf", "19", "-movflags", "+faststart", str(output)]
        subprocess.run(command, check=True)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
