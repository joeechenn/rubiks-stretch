#!/usr/bin/env python3
"""Keep the Stretch gripper camera centered over a Rubik's cube (visual servoing).

Usage (driver + gripper camera must be running; run from a regular terminal for --gui):
    python3 cube_track.py                       # track (moves the arm)
    python3 cube_track.py --dry-run             # print the moves, don't send them
    python3 cube_track.py --no-gui              # headless (window is shown by default)

What it does:
  1. Puts the arm in a "look straight down" pose (also the cube-scanning pose): lift to the
     top, wrist straightened along the arm, then pitched down, gripper open.
  2. Loop forever: grab the newest gripper-camera frame, find the cube face with
     cube_contour.find_face, measure how far the face center is from the target pixel
     (image center + offset) and nudge wrist_extension to cancel the error along the
     arm's axis. The drive base never moves, so the error across the arm's axis is
     only shown (move the cube or the robot to fix it).
     The pixel error becomes meters through the sticker pitch (a cube sticker pitch is
     ~19 mm, so pitch_px tells the scale without depth or intrinsics).
  3. If the cube is not seen (hidden, out of frame, moved too fast) the robot HOLDS STILL
     and keeps polling; it moves again as soon as the cube is back. The loop only ends on
     Ctrl+C.
  Once the error stays inside the deadband the log says ALIGNED (ready to grasp).
  With --grasp the aim point is the gripper's axis instead of the image center, and once
  ALIGNED it lowers onto the cube (hover: stop above it; pick: grab, lift, put back), then exits:
    python3 cube_track.py --grasp hover         # safe check of the aim and the height
    python3 cube_track.py --grasp pick
    python3 cube_track.py --grasp rotate        # twist the top layer 90 deg in the fixture
  The annotated image is published on /cube_track/image.

Which image axis matches the arm, and its sign, depend on how the camera is mounted,
so they are flags (--ext-axis y, --ext-sign -1 are verified on our robot).
"""
import argparse
import os
import signal
import subprocess
import sys
import threading
import time

import cv2
import numpy as np
import rclpy
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image
from std_srvs.srv import Trigger

import hello_helpers.hello_misc as hm

# cube_contour parses sys.argv when imported; hide our flags from it.
_argv, sys.argv = sys.argv, sys.argv[:1]
import cube_contour as cc   # noqa: E402  (sticker detector)
sys.argv = _argv

TOPIC = '/gripper_camera/color/image_rect_raw'
PARAMS = (40, 120, 150, 8000)    # canny lo, canny hi, min area, max area (cube_contour defaults)
STICKER_PITCH_M = 0.019          # center-to-center sticker spacing of a standard 3x3 cube
EXT_LIMITS = (0.0, 0.50)         # wrist_extension limits we allow ourselves (m)
# (velocity, acceleration) for the two moves that run slowly to avoid arm jitter: the
# wrist roll that twists the top layer, and lowering a lifted cube back into the fixture.
# stretch_body's 'slow' profile; every other move uses the default speed
# (lift 0.11 m/s, wrist roll 2 rad/s).
SLOW_VA = {
    'joint_lift': (0.05, 0.05),
    'joint_wrist_roll': (1.0, 4.0),
}
LIFT_TOP_M = 1.09                # lift travel ends at ~1.0995 m on this robot; stay just below
# joint_wrist_yaw that puts the gripper in line with the arm on OUR robot. Its yaw zero is
# off, so 0.0 is not straight; set by hand with keyboard teleop on 2026-11-24.
WRIST_YAW_STRAIGHT = 0.769
WIN = 'cube track'

# ---------- grasp geometry (gripper camera, look-down pose, measured 2026-11-24) ----------
# The robot model has no TF from the D405 to the gripper, so these were measured with the
# depth image in the look-down pose (yaw WRIST_YAW_STRAIGHT, pitch -1.5). All in the color
# optical frame (x right, y down the image, z out of the lens), meters.
CAM_K = (433.6, 433.0, 424.3, 244.0)       # fx, fy, cx, cy at 848x480
CAM_DOWN = np.array([-0.077, -0.147, 0.986])  # world "down" (lift), from a table plane fit
TIP_MARKERS = np.array([0.0098, 0.0408, 0.138])  # midpoint of the two fingertip ArUco markers
# Fingertips (the bottom of the rubber pads) reach past the markers. First guess 0.015
# gripped ~3 cm too low on the 2026-11-24 pick test (+0.028 -> 0.043); a side photo of
# `--grasp hover --hover-above-mm 0` then showed the pad bottoms ~6 mm BELOW the cube top
# instead of level with it, so 0.049.
TIP_BEYOND_MARKERS_M = 0.049
# Grip the TOP LAYER only (a layer is 19 mm): gripping lower lets the fingers twist the
# layers against each other and turn the cube. Mind the pads: round discs ~20 mm across,
# i.e. a whole layer tall, and the squeeze slides the cube ~11 mm (TWIST_SQUEEZE) or
# ~25 mm (GRIPPER_CLOSED) up into them, so the tips end that much deeper than this.
GRIP_BELOW_TOP_M = 0.005
# Twist: tips 5 mm into the top layer -> ~16 mm after the ~11 mm lift-out, so the pads
# stay on the top layer. (The earlier 3 mm was really ~9 mm with the old tip offset and
# ended ~20 mm deep: the pads brushed the second layer.)
TWIST_GRIP_BELOW_TOP_M = 0.005
HOVER_ABOVE_TOP_M = 0.03                   # --grasp hover stops the fingertips this far above it
GRASP_RAISE_M = 0.10                       # how high to lift the cube (clears the fixture)
PLACE_ABOVE_M = 0.003                      # release this far above the pick height (no jamming)
# Squeezing bends the compliant fingers and draws the cube UP out of the fixture, so it
# is measured on every grasp (depth to the cube top, open vs closed, at the same lift)
# and the cube is set down that much lower. Capped so a bad reading can't drive the
# fingertips into the fixture.
LIFT_OUT_MAX_M = 0.025
RESEAT_MIN_M = 0.003                       # re-seat the cube when the grip lifted it more
# The lift-out is real: with an 8 mm cap on the push-down the fixture only held the
# bottom layer and the top two turned. Pushing while gripped moves cube and fingers
# together, so the full measured amount is pushed back (same cap as LIFT_OUT_MAX_M).
# (Caveat: closed EMPTY fingers read 68 mm in the same depth patch; with a cube in the
# grip the fingers sit at its sides and the patch sees the cube top.)
RESEAT_MAX_M = LIFT_OUT_MAX_M
ROLL_FIX_TOL_DEG = 3.0                    # cube counts as square to the fixture within this
ROLL_FIX_TRIES = 3                         # camera-checked roll corrections after a turn
ROLL_LIMIT_DEG = 165.0                     # wrist roll range_t 150..3950 ticks = +/-167 deg
DEPTH_TOPIC = '/gripper_camera/depth/image_rect_raw'
DEPTH_K = (240.4, 240.4, 240.8, 136.5)     # fx, fy, cx, cy at 480x270 (D405 depth)
# joint_gripper_finger_left. The fingers are compliant, so the motor angle is not the gap:
# 0.0 only brings them to touching and a held cube slipped. Commanding past 0 squeezes
# (empty gripper: -0.2 -> effort ~-20, -0.4 -> ~-28; the stall limit is 20).
GRIPPER_OPEN, GRIPPER_CLOSED = 0.5, -0.25
# Twist: squeeze gentler. A hard squeeze curls the fingers and drags the cube ~25 mm up
# into them (out of the fixture, fingers onto the second layer). The camera slip check
# corrects the angle if the lighter grip slips while turning.
TWIST_SQUEEZE = -0.10
GRIPPER_OPENED_MIN = 0.15   # joint reading that counts as open (fully open reads ~0.24)


def _intrinsics(width):
    s = width / 848.0
    fx, fy, cx, cy = CAM_K
    return fx * s, fy * s, cx * s, cy * s


def grasp_geometry(center_px, pitch_px, width):
    """Cube face center + sticker pitch (pixels) -> (aim pixel, vertical distance (m)
    from the fingertips down to the cube's top face).

    The aim pixel is where the gripper's axis (a vertical line through the fingertips)
    meets the height of the cube's top face, so "cube center on the aim pixel" means
    the gripper is right above the cube.
    """
    fx, fy, cx, cy = _intrinsics(width)
    z = fx * STICKER_PITCH_M / pitch_px                      # depth of the top face
    top = np.array([(center_px[0] - cx) * z / fx, (center_px[1] - cy) * z / fy, z])
    tip = TIP_MARKERS + TIP_BEYOND_MARKERS_M * CAM_DOWN
    drop = float(CAM_DOWN @ top - CAM_DOWN @ tip)            # fingertips -> top face, vertical
    axis = tip + drop * CAM_DOWN                             # gripper axis at top-face height
    aim = np.array([cx + fx * axis[0] / axis[2], cy + fy * axis[1] / axis[2]])
    return aim, drop


def grip_top_pixel(width, height):
    """Depth-image pixel of the cube's top face while the fingers hold it at grip height."""
    fx, fy, cx, cy = DEPTH_K
    s = width / 480.0
    p = TIP_MARKERS + TIP_BEYOND_MARKERS_M * CAM_DOWN - GRIP_BELOW_TOP_M * CAM_DOWN
    return int(round((cx + fx * p[0] / p[2]) * s)), int(round((cy + fy * p[1] / p[2]) * s))


def wrap90(deg):
    """Angle modulo the cube's 90-degree symmetry, in (-45, 45]."""
    return -((-deg + 45.0) % 90.0 - 45.0)


def grid_angle_deg(grid):
    """In-image angle (deg, atan2 of image x/y, y down) of a face's grid rows, mod 90."""
    u = grid[0][0, 2] - grid[0][0, 0]
    return wrap90(np.degrees(np.arctan2(u[1], u[0])))


def mean_angle90(angles):
    """Mean of angles that are only defined mod 90 (average 4*theta on the circle)."""
    a = np.radians(np.asarray(angles) * 4.0)
    return float(np.degrees(np.arctan2(np.sin(a).mean(), np.cos(a).mean())) / 4.0)


def parse_args():
    p = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    p.add_argument('topic', nargs='?', default=TOPIC)
    p.add_argument('--dry-run', action='store_true', help='print moves, send nothing')
    p.add_argument('--gui', dest='gui', action='store_true', default=True,
                   help='show the camera window (default; kept for compatibility)')
    p.add_argument('--no-launch-camera', dest='launch_camera', action='store_false',
                   help='do not start the D405 camera launch file (started by default '
                        'when nothing publishes the topic)')
    p.add_argument('--no-gui', dest='gui', action='store_false',
                   help='do not open the camera window (it opens by default)')
    p.add_argument('--window', type=int, nargs=4, metavar=('X', 'Y', 'W', 'H'),
                   help='place and size the camera window in screen pixels, '
                        'e.g. 0 0 960 1080 for the left half of a 1080p screen')
    p.add_argument('--lift', type=float, default=LIFT_TOP_M,
                   help='start lift height (m); default is the top of travel')
    p.add_argument('--pitch', type=float, default=-1.5, help='start wrist pitch (rad)')
    p.add_argument('--ext', type=float, default=0.30,
                   help='start arm extension (m), where the camera first sees the cube '
                        '(tracking fine-tunes it)')
    p.add_argument('--keep-ext', dest='ext', action='store_const', const=None,
                   help='do not move the arm in the start pose')
    p.add_argument('--yaw', type=float, default=WRIST_YAW_STRAIGHT,
                   help='wrist yaw that points the gripper along the arm (rad, robot-specific)')
    p.add_argument('--ext-axis', choices=['x', 'y'], default='y',
                   help='image axis that wrist_extension corrects')
    p.add_argument('--ext-sign', type=float, default=-1.0,
                   help='+1 or -1 (-1 verified on the robot 2026-11-23)')
    p.add_argument('--offset-px', type=float, nargs=2, default=(0.0, 0.0), metavar=('DX', 'DY'),
                   help='aim point relative to the image center (camera is off the gripper axis)')
    p.add_argument('--gain', type=float, default=0.5, help='fraction of the error fixed per step')
    p.add_argument('--deadband-m', type=float, default=0.008, help='ignore errors below this (m)')
    p.add_argument('--max-step-m', type=float, default=0.04, help='largest single move (m)')
    p.add_argument('--min-matched', type=int, default=4,
                   help='stickers the detector must really see to trust a detection')
    p.add_argument('--confirm', type=int, default=2,
                   help='consecutive detections required before moving')
    p.add_argument('--grasp', choices=['hover', 'pick', 'rotate', 'rotate-pick'],
                   help='aim the gripper (not the image center) at the cube; once ALIGNED, '
                        '"hover" lowers the fingertips to just above it and stops, "pick" grabs '
                        'it, lifts it, puts it back and lets go, "rotate" grips the top layer and '
                        'twists it by --turn-deg in place (the fixture holds the bottom two '
                        'layers), lets go and returns the wrist roll to 0. "rotate-pick" twists '
                        'like rotate, then keeps hold, lifts the cube, turns it --air-turn-deg in '
                        'the air, puts it back and lets go. '
                        'The twist and the set-down run slowly. Then the program exits.')
    p.add_argument('--turn-deg', type=float, default=90.0,
                   help='--grasp rotate: how far to twist the top layer (a multiple of 90)')
    p.add_argument('--air-turn-deg', type=float, default=-90.0,
                   help='--grasp rotate-pick: once lifted, roll the whole cube this much in '
                        'the air before placing it (relative to the twisted roll; a multiple of '
                        '90; 0 = off). -90 after a +90 twist brings the wrist back near 0')
    p.add_argument('--hover-above-mm', type=float, default=HOVER_ABOVE_TOP_M * 1000,
                   help='--grasp hover: where to stop the fingertips relative to the cube top '
                        '(0 = level with it; used to calibrate TIP_BEYOND_MARKERS_M)')
    p.add_argument('--grasp-after', type=int, default=5,
                   help='consecutive ALIGNED frames required before the grasp starts')
    return p.parse_args()


class CubeTracker(hm.HelloNode):
    def __init__(self, args):
        hm.HelloNode.__init__(self)
        self.args = args
        self.lock = threading.Lock()
        self.frame = None
        self.seq = 0
        self.phase = ''                   # current grasp step, shown in the live window
        self.depth = None                # latest depth frame, meters (0 = no reading)
        self.dseq = 0
        self.camera_proc = None

    # ---------- camera ----------
    def on_image(self, msg):
        # Built by hand: cv_bridge conflicts with the pip OpenCV here.
        if msg.encoding not in ('bgr8', 'rgb8'):
            return
        img = np.frombuffer(msg.data, np.uint8).reshape(msg.height, msg.width, 3)
        if msg.encoding == 'rgb8':
            img = img[:, :, ::-1]
        with self.lock:
            self.frame = img.copy()
            self.seq += 1

    def on_depth(self, msg):
        if msg.encoding not in ('16UC1', 'mono16'):
            return
        d = np.frombuffer(msg.data, np.uint16).reshape(msg.height, msg.width)
        with self.lock:
            self.depth = d.astype(np.float32) / 1000.0
            self.dseq += 1

    def cube_top_distance(self, frames=4, half=15, timeout=2.0):
        """Median depth (m) of the cube's top face under the closed-grip point, over a few
        NEW depth frames (so the reading is from after the last move). None if unreadable."""
        start, vals = self.dseq, []
        end = time.time() + timeout
        while len(vals) < frames and time.time() < end and rclpy.ok():
            with self.lock:
                fresh = self.dseq > start + len(vals) and self.depth is not None
                d = self.depth
            if not fresh:
                time.sleep(0.01)
                continue
            u, v = grip_top_pixel(d.shape[1], d.shape[0])
            win = d[max(v - half, 0):v + half, max(u - half, 0):u + half]
            win = win[win > 0]
            if win.size > 20:
                vals.append(float(np.median(win)))
            else:
                vals.append(float('nan'))
        vals = [x for x in vals if not np.isnan(x)]
        return float(np.median(vals)) if vals else None

    def next_frame(self, after_seq, timeout=1.0):
        """Block until a frame newer than after_seq arrives; (frame, seq) or (None, seq)."""
        end = time.time() + timeout
        while time.time() < end and rclpy.ok():
            with self.lock:
                if self.seq > after_seq and self.frame is not None:
                    return self.frame, self.seq
            time.sleep(0.005)
        return None, after_seq

    def publish_view(self, view, header_stamp=None):
        view = np.ascontiguousarray(view, dtype=np.uint8)
        out = Image()
        out.height, out.width = view.shape[:2]
        out.encoding = 'bgr8'
        out.step = out.width * 3
        out.data = view.tobytes()
        self.view_pub.publish(out)

    def ensure_camera(self):
        """Start d405_basic.launch.py if nothing publishes the camera topic."""
        a = self.args
        # ROS discovery takes a moment; don't start a second camera node by mistake
        end = time.time() + 3.0
        while time.time() < end:
            if self.count_publishers(a.topic) > 0 or 'gripper_camera' in self.get_node_names():
                self.get_logger().info('camera already running')
                return
            time.sleep(0.2)
        if not a.launch_camera:
            self.get_logger().warn(f'nothing publishes {a.topic} (camera launch disabled)')
            return
        self.get_logger().info('starting the D405: ros2 launch stretch_core d405_basic.launch.py')
        self.camera_proc = subprocess.Popen(
            # pointcloud + depth alignment make the D405 drop/freeze color frames
            ['ros2', 'launch', 'stretch_core', 'd405_basic.launch.py',
             'pointcloud.enable:=false', 'align_depth.enable:=false'],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            start_new_session=True)   # own process group, so the camera node dies with it

    def stop_camera(self):
        """Stop the launch AND its camera node (the whole process group)."""
        if self.camera_proc is None:
            return
        try:
            pgid = os.getpgid(self.camera_proc.pid)
        except ProcessLookupError:
            return
        os.killpg(pgid, signal.SIGINT)          # what Ctrl+C on the launch would do
        try:
            self.camera_proc.wait(timeout=8)
        except subprocess.TimeoutExpired:
            pass
        try:
            os.killpg(pgid, signal.SIGKILL)     # anything still holding the D405
        except ProcessLookupError:
            pass

    # ---------- robot ----------
    def move_slow(self, joint, pos):
        """Blocking move of one joint at its SLOW_VA speed."""
        self.move_to_pose({joint: (float(pos), *SLOW_VA[joint])}, blocking=True)

    def call(self, client):
        fut = client.call_async(Trigger.Request())
        while not fut.done() and rclpy.ok():
            time.sleep(0.02)

    def go_to_start_pose(self):
        a = self.args
        self.get_logger().info('moving to the look-down pose')
        if a.dry_run:
            return
        self.call(self.switch_to_position_mode_service)
        # 1. lift to the top, so the camera sees the whole cube (also the scanning pose)
        self.move_to_pose({'joint_lift': a.lift}, blocking=True)
        # 1b. reach out over the fixture; tracking then fine-tunes the extension
        #     (without this the arm stays wherever homing or a power cut left it)
        if a.ext is not None:
            self.move_to_pose({'wrist_extension': float(np.clip(a.ext, *EXT_LIMITS))},
                              blocking=True)
        # 2. straighten the wrist so the gripper points along the arm
        self.move_to_pose({'joint_wrist_yaw': a.yaw, 'joint_wrist_pitch': 0.0,
                           'joint_wrist_roll': 0.0}, blocking=True)
        # 3. only then pitch it down to look at the table
        self.move_to_pose({'joint_wrist_pitch': a.pitch}, blocking=True)
        self.move_to_pose({'joint_gripper_finger_left': 0.5}, blocking=True)   # open
        # A goal that times out (e.g. on a low battery: the lift stayed at 0.979 while
        # the battery read 10.3 V) leaves the robot short of the pose, and every height
        # computed from the camera is then wrong. Check before going on.
        time.sleep(0.3)
        lift, pitch = self.joint('joint_lift'), self.joint('joint_wrist_pitch')
        if abs(lift - a.lift) > 0.01 or abs(pitch - a.pitch) > 0.05:
            raise RuntimeError(
                f'start pose not reached (lift {lift:.3f} of {a.lift:.3f}, wrist pitch '
                f'{pitch:+.2f} of {a.pitch:+.2f}); check the battery and the driver log')

    def wrist_extension(self):
        return hm.get_wrist_state(self.joint_state)[0]

    def command(self, ext_delta):
        """Send one small wrist_extension correction (meters). True if anything was sent."""
        if abs(ext_delta) <= 1e-4:
            return False
        if self.args.dry_run:
            self.get_logger().info(f'[dry-run] wrist_extension {ext_delta:+.3f} m')
        else:
            goal = float(np.clip(self.wrist_extension() + ext_delta, *EXT_LIMITS))
            self.move_to_pose({'wrist_extension': goal}, blocking=True)
        return True

    def joint(self, name):
        js = self.joint_state
        return js.position[js.name.index(name)]

    def cube_angle(self, frames=5, timeout=3.0):
        """In-image angle (deg, mod 90) of the cube face seen in the next few frames."""
        seq, angles = self.seq, []
        end = time.time() + timeout
        while len(angles) < frames and time.time() < end and rclpy.ok():
            frame, seq = self.next_frame(seq, timeout=0.5)
            if frame is None:
                continue
            g = cc.find_face(frame, PARAMS)[3]
            if g is not None and g[2] >= self.args.min_matched:
                angles.append(grid_angle_deg(g))
        return mean_angle90(angles) if len(angles) >= 2 else None

    def squeeze(self):
        """(Re)close the gripper. The gripper eases off by itself ~1 s after squeezing past
        its stall limit, and a loose cube slips when the wrist rolls; re-commanding
        restores the squeeze."""
        self.move_to_pose({'joint_gripper_finger_left': self.closed_cmd()}, blocking=True)

    def twisting(self):
        return self.args.grasp in ('rotate', 'rotate-pick')

    def closed_cmd(self):
        return TWIST_SQUEEZE if self.twisting() else GRIPPER_CLOSED

    def turn_cube(self, turn_deg, angle0):
        """Roll the held cube by turn_deg, then use the camera to undo any slip in the
        fingers so the cube ends square to the fixture (a multiple of 90 deg from angle0).

        The camera rolls with the gripper, so a world-fixed thing at world angle w shows
        at image angle w - roll (checked on the robot: +90 deg roll moved the table from the
        top of the image to the left). A firmly held cube therefore keeps its image angle;
        any change is slip. Cube world angle = image angle + roll, and it must end equal to
        angle0 (its image angle at roll 0, i.e. the fixture's angle) modulo 90.
        """
        log = self.get_logger()
        self.squeeze()
        self.phase = f'twisting the top layer {turn_deg:+.0f} deg'
        self.move_slow('joint_wrist_roll', np.radians(turn_deg))
        for attempt in range(1, ROLL_FIX_TRIES + 1):
            time.sleep(0.2)
            seen = self.cube_angle()
            roll = np.degrees(self.joint('joint_wrist_roll'))
            if seen is None or angle0 is None:
                path = os.path.expanduser('~/.ros/cube_track_noface.png')
                with self.lock:
                    frame = None if self.frame is None else self.frame.copy()
                if frame is not None:
                    cv2.imwrite(path, frame)
                log.warn(f'cannot see the cube face in the gripper; no slip correction '
                         f'(frame saved to {path})')
                return
            fix = wrap90(angle0 - seen - roll)
            log.info(f'turn check {attempt}: roll {roll:+.1f} deg, cube in image {seen:+.1f} '
                     f'(before {angle0:+.1f}) -> off square by {-fix:+.1f} deg')
            if abs(fix) < ROLL_FIX_TOL_DEG:
                log.info('cube is square to the fixture')
                return
            self.squeeze()
            self.phase = f'squaring the top layer ({-fix:+.1f} deg off)'
            self.move_slow('joint_wrist_roll', np.radians(roll + fix))
        log.warn('cube still not square after the roll corrections')

    # ---------- grasp ----------
    def grasp(self, grids, shape):
        """Lower onto the aligned cube; 'hover' stops above it, 'pick' grabs and lifts it.

        grids: the detections from the last ALIGNED frames. The height comes from the
        median over them: one frame's sticker pitch is off by ~1 px, which is ~1.5 cm here.
        """
        a = self.args
        drops = [grasp_geometry(g[0][1, 1], g[1], shape[1])[1] for g in grids]
        drop = float(np.median(drops))
        self.get_logger().info(f'height estimates (mm): {[round(d * 1000) for d in drops]}')
        lift0 = self.joint('joint_lift')
        hover = lift0 - (drop - a.hover_above_mm / 1000.0)
        grip = lift0 - (drop + (TWIST_GRIP_BELOW_TOP_M if self.twisting()
                                else GRIP_BELOW_TOP_M))
        log = self.get_logger()
        log.info(f'cube top is {drop * 1000:.0f} mm below the fingertips; '
                 f'lift {lift0:.3f} -> hover {hover:.3f} / grip {grip:.3f}')
        if not (0.05 < drop < 0.45) or grip < 0.3:
            log.error('grasp geometry out of range; not moving')
            return
        if a.dry_run:
            goal = hover if a.grasp == 'hover' else grip
            log.info(f'[dry-run] would {a.grasp}: lift to {goal:.3f}')
            return
        if a.grasp == 'hover':
            self.move_to_pose({'joint_lift': hover}, blocking=True)
            log.info(f'HOVERING: fingertips should be {a.hover_above_mm:.0f} mm above the cube '
                     'top, and the cube between them')
            return
        if not self.open_gripper():      # closed fingers must not come down onto the cube
            return
        self.phase = 'lowering onto the cube'
        self.move_to_pose({'joint_lift': grip}, blocking=True)
        time.sleep(0.3)
        z_open = self.cube_top_distance()
        self.phase = 'gripping'
        self.move_to_pose({'joint_gripper_finger_left': self.closed_cmd()}, blocking=True)
        time.sleep(0.3)
        z_closed = self.cube_top_distance()
        # how far the squeeze drew the cube up out of the fixture (toward the camera)
        if z_open is None or z_closed is None:
            lifted = 0.0
            log.warn('no depth reading of the cube top; placing without lift-out compensation')
        else:
            lifted = float(np.clip((z_open - z_closed) * CAM_DOWN[2], 0.0, LIFT_OUT_MAX_M))
            log.info(f'cube top {z_open * 1000:.0f} mm open, {z_closed * 1000:.0f} mm gripped: '
                     f'the grip lifted it {lifted * 1000:.0f} mm')
        if self.twisting():
            self.twist_top_layer(grids, grip, lift0, lifted)
            return
        # set it back down into the fixture and let go. The cube sits `lifted` higher in the
        # fingers than when it was gripped, so go that much lower than the grip height.
        self.lift_and_place(grip, lifted, lift0)

    def lift_and_place(self, seated, lifted, lift0, air_turn_deg=0.0):
        """Lift the gripped cube clear of the fixture, then set it back down and let go.

        seated: lift height at which the cube sat in the fixture; lifted: how far above
        that the grip holds the cube now, so placing goes that much lower. The set-down
        is slow; the lift is at normal speed."""
        log = self.get_logger()
        self.phase = 'lifting the cube'
        self.move_to_pose({'joint_lift': seated + GRASP_RAISE_M}, blocking=True)
        log.info('PICKED: holding the cube')
        time.sleep(1.0)
        if air_turn_deg:
            # turn the whole cube while it's clear of the fixture. Relative to the current
            # roll, so a cube held square stays square (mod 90) to the fixture.
            roll0 = np.degrees(self.joint('joint_wrist_roll'))
            goal = roll0 + air_turn_deg
            if abs(goal) > ROLL_LIMIT_DEG:
                log.warn(f'air turn to roll {goal:+.0f} deg is past the wrist limit; skipped')
            else:
                self.phase = f'turning the cube {air_turn_deg:+.0f} deg in the air'
                self.move_to_pose({'joint_wrist_roll': np.radians(goal)}, blocking=True)
                time.sleep(0.3)
                log.info(f'AIR TURN: whole cube {air_turn_deg:+.0f} deg (roll {roll0:+.1f} -> '
                         f'{np.degrees(self.joint("joint_wrist_roll")):+.1f} deg)')
        place = seated + PLACE_ABOVE_M - lifted
        log.info(f'placing at lift {place:.3f} (seated {seated:.3f}, lift-out '
                 f'{lifted * 1000:.0f} mm)')
        self.phase = 'placing the cube back (slow)'
        self.move_slow('joint_lift', place)
        self.phase = 'releasing'
        if not self.open_gripper():
            return False
        self.move_to_pose({'joint_lift': lift0}, blocking=True)
        log.info('PLACED: cube put back, gripper open')
        return True

    def open_gripper(self, tries=3):
        """Open and CHECK it opened. A stalled gripper can time out on the open command
        (the driver logs 'exceeded the default_goal_timeout') and stay shut; lifting then
        carries the cube away. Returns False (and stays put) if it won't open."""
        log = self.get_logger()
        for attempt in range(1, tries + 1):
            try:
                self.move_to_pose({'joint_gripper_finger_left': GRIPPER_OPEN}, blocking=True)
            except Exception as e:                     # a timed-out goal must not abort here
                log.warn(f'gripper open attempt {attempt} raised {e!r}')
            time.sleep(0.3)
            pos = self.joint('joint_gripper_finger_left')
            if pos > GRIPPER_OPENED_MIN:
                return True
            log.warn(f'gripper open attempt {attempt}: still at {pos:+.3f}')
        log.error('GRIPPER WILL NOT OPEN: stopping here with the cube held, nothing else '
                  'moves. Open it by hand / reboot the gripper, then rerun.')
        return False

    def twist_top_layer(self, grids, grip, lift0, lifted):
        """Turn ONLY the top layer: the fixture holds the bottom two layers while the
        gripper, holding the top layer, rolls. The cube is never lifted out.

        If the squeeze drew the cube up (lifted), push it back down into the fixture first,
        or the bottom layers aren't held and the whole cube turns.
        """
        a, log = self.args, self.get_logger()
        push = min(lifted, RESEAT_MAX_M)
        if push > RESEAT_MIN_M:
            self.phase = 'pushing the cube back into the fixture'
            self.move_to_pose({'joint_lift': grip - push}, blocking=True)
            log.info(f'pushed the cube back {push * 1000:.0f} mm into the fixture '
                     f'(measured lift-out {lifted * 1000:.0f} mm, lift {grip - push:.3f})')
        else:
            push = 0.0
        # the top layer must end square to the bottom layers, which sit at the fixture's
        # angle = the face angle seen at roll 0 before the grasp
        angle0 = mean_angle90([grid_angle_deg(g) for g in grids])
        self.turn_cube(a.turn_deg, angle0)
        log.info(f'TWISTED the top layer {a.turn_deg:+.0f} deg')
        if a.grasp == 'rotate-pick':
            # keep hold: squeeze to the full pick grip (the twist grip is too light to lift
            # with), measure how much further that draws the cube up into the fingers, then
            # lift it out and set it back down at the same (twisted) roll, and let go.
            seated = grip - push
            time.sleep(0.3)
            z_twist = self.cube_top_distance()
            self.phase = 'tightening the grip to lift'
            self.move_to_pose({'joint_gripper_finger_left': GRIPPER_CLOSED}, blocking=True)
            time.sleep(0.3)
            z_tight = self.cube_top_distance()
            if z_twist is None or z_tight is None:
                extra = 0.0
                log.warn('no depth reading of the cube top; placing without lift-out compensation')
            else:
                # push + extra is the total draw-up since the open-gripper grip: cap it
                # like the plain pick so the fingertips never go deeper than that
                extra = float(np.clip((z_twist - z_tight) * CAM_DOWN[2], 0.0,
                                      max(LIFT_OUT_MAX_M - push, 0.0)))
                log.info(f'cube top {z_twist * 1000:.0f} mm twist grip, {z_tight * 1000:.0f} mm '
                         f'tight grip: drawn up another {extra * 1000:.0f} mm')
            if not self.lift_and_place(seated, extra, lift0, a.air_turn_deg):
                return
        else:
            self.phase = 'releasing'
            if not self.open_gripper():
                return
            self.move_to_pose({'joint_lift': lift0}, blocking=True)
        # only now, with the fingers open and clear of the cube: wrist back to normal
        self.phase = 'wrist roll back to 0'
        self.move_to_pose({'joint_wrist_roll': 0.0}, blocking=True)
        self.phase = 'checking the top layer'
        log.info('wrist roll back to 0')
        # back at roll 0 the camera sees the top face as at the start
        seen = self.cube_angle()
        if seen is not None and angle0 is not None:
            off = wrap90(seen - angle0)
            log.info(f'top layer is {off:+.1f} deg from square to the bottom layers'
                     + ('' if abs(off) < 2 * ROLL_FIX_TOL_DEG else '  <-- NOT SQUARE?'))
        else:
            log.warn('cannot see the top face after the twist; check the cube')
        log.info('DONE: top layer turned'
                 + (', cube lifted and put back' if a.grasp == 'rotate-pick' else '')
                 + ', gripper open, wrist roll 0')

    # ---------- control law ----------
    def target(self, shape, grid=None):
        """Pixel the cube center should sit on: the gripper axis in --grasp mode,
        else the image center + --offset-px."""
        a = self.args
        h, w = shape[:2]
        if a.grasp and grid is not None:
            return grasp_geometry(grid[0][1, 1], grid[1], w)[0]
        return np.array([w / 2 + a.offset_px[0], h / 2 + a.offset_px[1]])

    def correction(self, grid, shape):
        """Face-center pixel error -> (ext_delta, arm-axis error, cross-axis error), meters."""
        a = self.args
        centers, pitch, _ = grid
        target = self.target(shape, grid)
        err_px = centers[1, 1] - target                 # +x = cube right, +y = cube down
        err_m = err_px * (STICKER_PITCH_M / pitch)      # meters on the cube plane
        along, across = (err_m[0], err_m[1]) if a.ext_axis == 'x' else (err_m[1], err_m[0])
        step = 0.0 if abs(along) < a.deadband_m else a.ext_sign * along * a.gain
        step = float(np.clip(step, -a.max_step_m, a.max_step_m))
        return step, float(along), float(across)

    def annotate(self, frame, grid, status, color):
        view = frame.copy()
        cx, cy = (int(round(x)) for x in self.target(view.shape, grid))
        cv2.drawMarker(view, (cx, cy), cc.WHITE, cv2.MARKER_CROSS, 30, 2)
        if grid is not None:
            centers, pitch, n = grid
            for p in centers.reshape(-1, 2):
                cv2.circle(view, (int(p[0]), int(p[1])), 5, color, 2)
            cv2.drawContours(view, [cc.grid_box(centers, pitch)], -1, cc.RED, 2)
            cv2.line(view, (cx, cy), (int(centers[1, 1][0]), int(centers[1, 1][1])), color, 2)
        # numbers only, no step names: tracking error (if any), then live joint readings
        for i, text in enumerate(t for t in (status, self.readout()) if t):
            cv2.putText(view, text, (10, 30 + 30 * i), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        return view

    def readout(self):
        """Live joint numbers for the overlay: lift (m), arm (m), roll (deg), gripper."""
        try:
            j = self.joint
            return (f'lift {j("joint_lift"):.3f}  ext {j("wrist_extension"):.3f}  '
                    f'roll {np.degrees(j("joint_wrist_roll")):+.1f}  '
                    f'grip {j("joint_gripper_finger_left"):+.2f}')
        except (AttributeError, ValueError, TypeError):    # no joint state yet
            return ''

    def show(self, view, text=None, color=None):
        """Draw the camera window; returns True when the user pressed q."""
        if text:
            view = view.copy()
            cv2.putText(view, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        cv2.imshow(WIN, view)
        return cv2.waitKey(1) & 0xFF == ord('q')

    def grasp_live(self, grids, shape):
        """Run grasp() in a worker thread and keep the camera window live meanwhile.

        Every grasp move blocks until done, so drawing from the same thread froze the
        window for the whole grasp. OpenCV GUI calls stay on this (main) thread; the
        worker only moves the robot and reads frames, and reports its step in self.phase.
        No detection runs here, so the live view is cheap."""
        a = self.args
        self.phase = f'GRASP ({a.grasp})'

        def work():
            try:
                self.grasp(grids, shape)
            except Exception as e:                       # report, don't hang the window
                self.get_logger().error(f'grasp failed: {e!r}')

        worker = threading.Thread(target=work, daemon=True)
        worker.start()
        seq = self.seq
        while worker.is_alive() and rclpy.ok():
            frame, seq = self.next_frame(seq, timeout=0.2)
            if frame is None:
                if a.gui:
                    cv2.waitKey(1)
                continue
            view = self.annotate(frame, None, '', cc.YELLOW)
            self.publish_view(view)
            if a.gui:
                self.show(view)      # q does nothing here: the grasp can't stop mid-move
        worker.join()

    # ---------- main loop ----------
    def run(self):
        a = self.args
        hm.HelloNode.main(self, 'cube_track', 'cube_track', wait_for_first_pointcloud=False)
        self.ensure_camera()
        cb = ReentrantCallbackGroup()
        self.view_pub = self.create_publisher(Image, '/cube_track/image', 1)
        self.create_subscription(Image, a.topic, self.on_image, qos_profile_sensor_data,
                                 callback_group=cb)
        self.create_subscription(Image, DEPTH_TOPIC, self.on_depth, qos_profile_sensor_data,
                                 callback_group=cb)
        self.get_logger().info(f'listening on {a.topic}'
                               + ('  (dry run: no motion)' if a.dry_run else ''))
        if a.gui:
            cv2.namedWindow(WIN, cv2.WINDOW_NORMAL)
            self.show(np.zeros((480, 640, 3), np.uint8), 'waiting for camera...', cc.WHITE)
            if a.window:
                # only after the first imshow: the window manager ignores a move before
                # the window is mapped
                x, y, w, h = a.window
                cv2.waitKey(50)
                cv2.resizeWindow(WIN, w, h)
                cv2.moveWindow(WIN, x, y)
                cv2.waitKey(1)
        self.go_to_start_pose()

        seq, seen, aligned, last_state, last_warn = 0, 0, 0, None, 0.0
        aligned_grids = []                         # detections from the current ALIGNED run
        while rclpy.ok():
            frame, seq = self.next_frame(seq)
            if frame is None:
                if time.time() - last_warn > 5.0:
                    self.get_logger().warn(f'no frames on {a.topic}; is the camera running?')
                    last_warn = time.time()
                if a.gui and cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                continue

            grid = cc.find_face(frame, PARAMS)[3]
            good = grid is not None and grid[2] >= a.min_matched
            seen = seen + 1 if good else 0

            if not good:
                state, status, color, aligned = 'LOST', '', cc.RED, 0
                aligned_grids = []
            elif seen < a.confirm:
                state, status, color = 'ACQUIRE', '', cc.YELLOW
            else:
                ext_d, along, across = self.correction(grid, frame.shape)
                errs = f'arm {along * 1000:+.0f} mm  side {across * 1000:+.0f} mm'
                if ext_d == 0.0:
                    aligned += 1
                    aligned_grids = (aligned_grids + [grid])[-a.grasp_after:]
                    state, color = 'ALIGNED', cc.GREEN
                    status = errs
                    if a.grasp and aligned >= a.grasp_after:
                        self.publish_view(self.annotate(frame, grid, errs, color))
                        self.grasp_live(aligned_grids, frame.shape)
                        break
                else:
                    aligned, aligned_grids = 0, []
                    state, color = 'TRACK', cc.GREEN
                    status = errs
                    if self.command(ext_d):
                        # let the arm settle and drop frames blurred by the move
                        time.sleep(0.15)
                        with self.lock:
                            seq = self.seq

            if state != last_state:                  # log only on change
                self.get_logger().info(state)
                last_state = state
            view = self.annotate(frame, grid if good else None, status, color)
            self.publish_view(view)
            if a.gui and self.show(view):
                break
        cv2.destroyAllWindows()


def main():
    args = parse_args()
    node = CubeTracker(args)
    try:
        node.run()
    except KeyboardInterrupt:
        pass
    finally:
        node.stop_camera()
        if rclpy.ok():
            rclpy.shutdown()
        node.new_thread.join()


if __name__ == '__main__':
    main()
