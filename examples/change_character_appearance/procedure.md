## Character Appearance Control Workflow

1. Inspect the camera
    - Called camera_get_pose to obtain the camera position, rotation, forward vector, and FOV.

2. Find a valid placement surface
    - Calculated a point in front of and below the camera.
    - Called scene_raycast_down to locate a walkable ground surface without using a settle tool.

3. Spawn the character
    - Called character_spawn_ready to create AppearanceCharacter at the detected ground position.

4. Aim the camera
    - Called camera_look_at to center the character in the camera view.

5. Discover the Blueprint interface
    - Called blueprint_inspect_api and identified set_app(NewParam) as the character appearance function.

6. Switch and capture appearances
    - Repeatedly called blueprint_call with set_app values 1–10.
    - After each appearance change, called scene_capture_view with the mvrc source to save a PNG screenshot.

7. Process the outputs
    - Copied all captured images into examples/ change_character_appearance.

    - Used Python and OpenCV (cv2) to convert every image to BGRA and set the complete alpha channel to 255.

    - Verified all 11 generated images had four channels and fully opaque alpha values.