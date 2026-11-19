# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A ROS 2 (Humble, Python 3.10) colcon workspace for a Hello Robot Stretch that will detect and handle a Rubik's cube. The git root is the workspace (`~/ament_ws`). Only two packages under `src/` are project code:

- `src/cube_vision/`: plain Python vision library (OpenCV + NumPy) that finds a cube face's 3x3 sticker grid.
- `src/stretch_joint_reader/`: an `ament_python` ROS 2 package with robot-side scripts.

Everything else in `src/` (`stretch_ros2`, `realsense-ros`, `rosbridge_suite`, `stretch_tutorials`, `stretch_web_teleop`, `audio_common`, `respeaker_ros2`, `ros2_numpy`, `sllidar_ros2`, `tf2_web_republisher_py`) is a third-party dependency repo that the root `.gitignore` excludes. Don't edit them. `build/`, `install/` and `log/` are colcon output.

## Commands

```bash
# Build (from ~/ament_ws), then source the overlay
colcon build --packages-select stretch_joint_reader
source install/setup.bash

# Run the motion script (needs the Stretch driver running)
ros2 run stretch_joint_reader run

# Live cube detector on a camera topic. It is not a console_scripts entry, so run the file directly.
# If the OpenCV window fails under a snap/VS Code terminal, `unset GTK_PATH` first.
python3 src/stretch_joint_reader/stretch_joint_reader/cube_contour.py [TOPIC] [--no-gui]
#   default TOPIC: /gripper_camera/color/image_rect_raw; also publishes /cube_detection/image

# cube_vision tests (run from src/cube_vision so the package is importable).
# PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 is required: a user-installed anyio pytest plugin
# breaks the system pytest with "No module named '_pytest.scope'".
cd src/cube_vision
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest -q test
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest -q test/test_sticker_detector.py::test_rotated_20_degrees

# Annotate still images with the detected grid (writes <name>_grid.png / <name>_mask.png)
python3 scripts/draw_grid.py IMG [IMG ...] --out debug_out [--max-dim 1000] [--sticker-px PX]
```

`stretch_joint_reader` has the stock ament linters (`test_flake8.py`, `test_pep257.py`, `test_copyright.py`). Run them with `colcon test --packages-select stretch_joint_reader && colcon test-result --verbose`.

## Robot and environment gotchas

- Every terminal needs `source /opt/ros/humble/setup.bash` and `source ~/ament_ws/install/setup.bash`.
- Driver: `ros2 launch stretch_core stretch_driver.launch.py`. Home the robot first, with `stretch_robot_home.py` (driver off) or `ros2 service call /home_the_robot std_srvs/srv/Trigger` (driver on). An unhomed robot or a wrong joint name is silently ignored.
- Gripper camera (D405): `ros2 launch stretch_core d405_basic.launch.py`, which publishes `/gripper_camera/color/image_rect_raw`. Its color/exposure parameters are under `depth_module.*`. If the feed freezes or drops frames, launch with `pointcloud.enable:=false align_depth.enable:=false` and run one camera at a time.
- GUI tools (OpenCV windows) fail in VS Code's snap terminal with a libpthread error: `unset GTK_PATH` or use a regular terminal.
- `run.py`: `wrist_extension` has no `joint_` prefix, unlike the other joints. `main()` must end with `rclpy.shutdown()` and `node.new_thread.join()`, or the process core-dumps.
- `cv_bridge.cv2_to_imgmsg` raises `KeyError: 16` because pip OpenCV in `~/.local` conflicts with the system one. `cube_contour.py` therefore builds the `Image` message by hand; keep it that way.

## Cube detection status (as of 2026-11-19)

The camera must work in dim light, so don't rely on adding light. Tuned on 50 dim frames in `cube_dataset/` (gitignored; collect more with `collect_frames.py --tag <name>`), `cube_contour.py` matches 5+ of 9 stickers in 32 of them. The gains came from `auto_gain()` (a brightness stretch); loosening the color thresholds did not help. Those numbers are tuned on the same frames, not held out.

`cube_scanner.py` scans the six faces (SPACE per face, order F R B L U D) and shows the unfolded cube. It labels each sticker by the nearest face-center chromaticity (brightness-independent), so it needs no fixed color thresholds, and outputs a 54-letter URFDLB facelet string. Tested on synthetic cubes only. The grid orientation is only resolved within +/-45 degrees, so hold faces roughly upright. Planned: a labeled held-out set, a learned detector if the geometric one stays unreliable, and the solver.

## Architecture notes

**`cube_vision` is not a ROS package.** It has no `package.xml` or `setup.py`, so colcon ignores it and nothing on the robot side imports it yet. Tests and `scripts/draw_grid.py` find it through the cwd or `sys.path`. `color_classifier.py`, `facelet.py`, `test_detector.py` and `test_facelet.py` are empty placeholders for the planned color-classification and facelet stages.

**`sticker_detector.find_stickers` pipeline** (takes an RGB image, returns a `StickerGrid` or `None`):
1. `_sticker_mask`: HSV threshold for saturated pixels OR bright low-saturation pixels (white stickers).
2. `_square_candidates`: square-ish contours, as `[cx, cy, side]`, sized relative to the image's shorter side.
3. `_pick_size_cluster`: keep the largest group of similar-sized squares. If `expected_sticker_px` is given (e.g. from depth and intrinsics), first filter to within ±40% of it.
4. `_lattice_params`: pitch and rotation from nearest-neighbor vectors. The angle is averaged as 4θ because a square grid has 90° symmetry, so rotation is only resolved within ±45°.
5. `_fit_lattice`: try every point as the center sticker and keep the 3x3 lattice that matches the most points.

`centers[row, col] = (x, y)` follows image orientation, with NaN for missing stickers. A grid needs at least `min_stickers` (6) matches. Tests build synthetic faces with `make_face(angle, clutter, hide)` in `test_sticker_detector.py` and check center positions to within 3 px.

**Two separate detectors exist.** `stretch_joint_reader/cube_contour.py` is a standalone ROS node with its own `find_stickers`, which works differently: it runs CLAHE, then Canny edges, then solid-color square regions on **BGR** frames, and falls back to a "color blob" mask. It draws a rotated box around the face and does not use `cube_vision`. `cube_vision` expects **RGB**, so convert ROS/cv2 BGR frames before calling it. The head camera (`/camera/color/image_raw`) is mounted sideways, so `cube_contour.py` rotates any non-gripper topic 90° clockwise.

**`run.py`** subclasses `hello_helpers.hello_misc.HelloNode` (from `stretch_ros2`). It switches the robot to position mode and then runs a hard-coded sequence of blocking `move_to_pose` calls (lift, wrist extension, wrist yaw/pitch/roll, gripper). Joint names follow the Stretch driver's conventions (`joint_lift`, `wrist_extension`, `joint_wrist_*`, `joint_gripper_finger_left`).
