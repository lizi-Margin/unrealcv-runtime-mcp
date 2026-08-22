### Captioning Process

1. Scene Perception — scene_perceive
   Inspected the map structure, nearby objects, visibility, and spatial layout.

2. Camera Orientation — camera_set_pose
   Rotated the camera toward east, north, west, south, up, and down.

3. Directional Capture — scene_capture_view
   Captured a visual reference for each direction.

4. Visual Inspection — view_image
   Reviewed all six captured images for landmarks and environmental details.

5. Caption Synthesis
   Combined the structured perception data and visual observations into one concise caption.