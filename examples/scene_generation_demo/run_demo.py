#!/usr/bin/env python3
"""Generate the audited Tokyo street-rest scene through Runtime MCP."""

from __future__ import annotations

import base64
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "examples"))
from runtime_mcp_client import RuntimeMCPClient  # noqa: E402


DEMO_DIR = Path(__file__).resolve().parent
IMAGE_DIR = DEMO_DIR / "images"
REQUESTS = DEMO_DIR / "requests.jsonl"
RESPONSES = DEMO_DIR / "responses.jsonl"
ANCHOR = {"x": -4500.0, "y": -500.0, "z": 2000.0}
SCENE_DESCRIPTION = (
    "Create a small Tokyo street-side rest point with one bench, one table, "
    "and one traffic cone, all grounded and mutually non-overlapping."
)
ASSETS = [
    {
        "role": "bench",
        "asset_path": "/Game/TokyoStylizedEnvironment/Meshes/Unique_Props/SM_Bench.SM_Bench",
        "name": "MCPDemo_Bench",
        "location": {"x": -4620.0, "y": -500.0, "z": 232.2836},
        "rotation": {"x": 0.0, "y": 0.0, "z": 0.0},
    },
    {
        "role": "table",
        "asset_path": "/Game/RoofProps/Geometry/Props/SM_table.SM_table",
        "name": "MCPDemo_Table",
        "location": {"x": -4400.0, "y": -500.0, "z": 232.2836},
        "rotation": {"x": 0.0, "y": 0.0, "z": 0.0},
    },
    {
        "role": "traffic_cone",
        "asset_path": "/Game/TokyoStylizedEnvironment/Meshes/Road_Barriers/SM_Cone01.SM_Cone01",
        "name": "MCPDemo_Cone",
        "location": {"x": -4450.0, "y": -350.0, "z": 232.2836},
        "rotation": {"x": 0.0, "y": 20.0, "z": 0.0},
    },
]
VIEWS = [
    ("01_top_down", "top_down", 600.0),
    ("02_x_positive_down_45", "x_positive_down_45", 650.0),
    ("03_x_negative_down_45", "x_negative_down_45", 650.0),
    ("04_y_positive_down_45", "y_positive_down_45", 650.0),
    ("05_y_negative_down_45", "y_negative_down_45", 650.0),
    ("06_hero_view", "x_negative_down_45", 650.0),
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_jsonl(path: Path, value: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n")


def git_head(path: Path) -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=path, text=True).strip()


def main() -> int:
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    REQUESTS.write_text("", encoding="utf-8")
    RESPONSES.write_text("", encoding="utf-8")
    sequence = 0
    audit: list[dict[str, Any]] = []
    actors: list[dict[str, Any]] = []
    views: list[dict[str, Any]] = []

    with RuntimeMCPClient(timeout=180.0) as client:
        # A prior interrupted run can leave only these explicitly named demo actors.
        for planned in ASSETS:
            client.call_tool("spawn.destroy", {"actor": planned["name"]})

        def call(tool: str, arguments: dict[str, Any] | None = None, image_name: str | None = None) -> dict[str, Any]:
            nonlocal sequence
            sequence += 1
            arguments = arguments or {}
            requested_at = now()
            write_jsonl(REQUESTS, {"sequence": sequence, "timestamp": requested_at, "tool": tool, "arguments": arguments})
            result = client.call_tool(tool, arguments)
            response = json.loads(json.dumps(result))
            if image_name:
                content = response.get("content", [])
                if content and content[0].get("type") == "image":
                    data = base64.b64decode(content[0].pop("data"))
                    image_path = IMAGE_DIR / f"{image_name}.png"
                    image_path.write_bytes(data)
                    digest = hashlib.sha256(data).hexdigest()
                    content[0]["file"] = str(image_path.relative_to(DEMO_DIR)).replace("\\", "/")
                    content[0]["sha256"] = digest
                    content[0]["bytes"] = len(data)
            completed_at = now()
            write_jsonl(RESPONSES, {"sequence": sequence, "timestamp": completed_at, "tool": tool, "result": response})
            audit.append({"sequence": sequence, "tool": tool, "requested_at": requested_at, "completed_at": completed_at})
            if result.get("isError"):
                raise RuntimeError(f"{tool} failed: {response}")
            return response

        tools = client.list_tools()
        (DEMO_DIR / "tools.json").write_text(json.dumps(tools, ensure_ascii=False, indent=2), encoding="utf-8")
        pose_before = call("camera.get_pose").get("structuredContent", {})
        perception_before = call("perception.snapshot", {"radius_cm": 2500, "max_objects": 24, "max_rays": 8}).get("structuredContent", {})
        ground = call("scene.raycast_down", {**ANCHOR, "trace_length_cm": 5000}).get("structuredContent", {})
        call("camera.set_view_preset", {"target": ground["location"], "preset": "top_down", "distance_cm": 600})
        preflight = call("scene.check_region", {
            "center_x": -4510, "center_y": -450, "center_z": ground["location"]["z"] + 55,
            "extent_x": 220, "extent_y": 180, "extent_z": 55,
        }).get("structuredContent", {})
        pre_image = call("scene.capture_view", {"camera_id": 0, "source": "mqrc", "width": 640, "height": 360}, "00_pre_generation_top_down")

        searches = {}
        for spec in ("bench", "table", "cone"):
            searches[spec] = call("assets.search", {"path": "/Game", "search_spec": spec, "limit": 30}).get("structuredContent", {})

        for planned in ASSETS:
            bounds = call("assets.get_bounds", {"asset_path": planned["asset_path"]}).get("structuredContent", {})
            spawned = call("spawn.from_asset", {
                "asset_path": planned["asset_path"],
                "location": planned["location"],
                "rotation": planned["rotation"],
                "name": planned["name"],
                "settle": "bounds",
                "reject_overlaps": 1,
            }).get("structuredContent", {})
            validation = call("spawn.validate_placement", {"actor": spawned["actor"]}).get("structuredContent", {})
            actors.append({**planned, "asset_bounds": bounds, "spawn_result": spawned, "validation": validation})

        target = {"x": -4510.0, "y": -450.0, "z": ground["location"]["z"] + 55.0}
        for image_name, preset, distance in VIEWS:
            call("camera.set_view_preset", {"target": target, "preset": preset, "distance_cm": distance})
            capture = call("scene.capture_view", {"camera_id": 0, "source": "mqrc", "width": 640, "height": 360}, image_name)
            metadata = capture.get("structuredContent", {})
            if metadata.get("render_source") != "mqrc" or metadata.get("uses_base_camera_sensor") is not False:
                raise RuntimeError(f"invalid capture provenance for {image_name}: {metadata}")
            views.append({"name": image_name, "preset": preset, "distance_cm": distance, "metadata": metadata})

        perception_after = call("perception.snapshot", {"radius_cm": 1200, "max_objects": 32, "max_rays": 8}).get("structuredContent", {})

    checksums = []
    for image_path in sorted(IMAGE_DIR.glob("*.png")):
        digest = hashlib.sha256(image_path.read_bytes()).hexdigest()
        checksums.append(f"{digest}  images/{image_path.name}")
    (DEMO_DIR / "checksums.sha256").write_text("\n".join(checksums) + "\n", encoding="ascii")
    manifest = {
        "schema_version": "unrealcv.scene_generation_audit.v1",
        "status": "success",
        "created_at": now(),
        "scene_description": SCENE_DESCRIPTION,
        "input_coordinate_cm": ANCHOR,
        "world": {"name": perception_before.get("world_name"), "path": perception_before.get("world_path")},
        "generation_route": "asset_spawn",
        "capture_policy": {"allowed": ["mqrc", "main_viewport_backbuffer"], "used": "mqrc", "uses_base_camera_sensor": False, "resolution": [640, 360], "max_resolution": [1280, 720]},
        "runtime_tool_count": len(tools),
        "camera_pose_before": pose_before,
        "ground": ground,
        "preflight": preflight,
        "pre_generation_capture": pre_image.get("structuredContent", {}),
        "asset_searches": searches,
        "actors": actors,
        "views": views,
        "evaluation": {"object_count_ok": len(actors) == 3, "overlap_ok": all(a["validation"].get("overlap_count") == 0 for a in actors), "grounding_ok": all(a["validation"].get("ground_contact") for a in actors), "six_views_ok": len(views) == 6},
        "perception_after": perception_after,
        "cleanup": {"performed": False, "reason": "Generated actors intentionally remain in the running demo scene until the process exits."},
        "audit_events": audit,
        "build_identity": {"closed_repo_head_before_changes": git_head(Path(r"C:\Users\hulc\Desktop\UE_Projects\HUAWEI_Project\Plugins\unrealcv")), "public_repo_head_before_changes": git_head(ROOT)},
    }
    (DEMO_DIR / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
