## UnrealCV Navigation Workflow

1. Spawned the character under the active camera
    - Read camera transform with camera_get_pose.
    - Located the ground using scene_raycast_down.
    - Spawned FirstPersonCharacter with character_spawn_ready.

2. Enabled first-person view
    - Attached the active view to the character’s FPS Camera using camera_follow_actor.

3. Located the sakura trees
    - Searched runtime actors with scene_list_actors.
    - Inspected candidates using scene_inspect_actor.
    - Confirmed targets visually through scene_capture_view and local image inspection.

4. Navigated through the complex scene
    - Added an AI controller with character_ensure_ai_controller.
    - Configured the navigation bounds using character_nav_area.
    - Sent reachable goals with character_navigate.
    - Monitored position, velocity, and arrival using character_movement_state.

    - Adjusted the destination to account for trunk collision and reached the second visible sakura within 0.5 m of its surface.

5. Captured the final photo
    - Detached first-person view using camera_detach.
    - Tested several framing angles with camera_set_view_preset.
    - Captured the character and sakura together using scene_capture_view.