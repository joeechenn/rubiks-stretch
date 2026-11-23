#!/usr/bin/env python3
"""Keep the Stretch gripper camera centered over a Rubik's cube (visual servoing).

Usage (driver + gripper camera must be running; run from a regular terminal for --gui):
    python3 cube_track.py                       # track (moves the arm)
    python3 cube_track.py --dry-run             # print the moves, don't send them
    python3 cube_track.py --no-gui              # headless (window is shown by default)

What it does:
  1. Puts the arm in a "look straight down" pose: lift up, wrist pitched down, gripper open.
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
WIN = 'cube track'


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
    p.add_argument('--lift', type=float, default=0.92, help='start lift height (m)')
    p.add_argument('--pitch', type=float, default=-1.5, help='start wrist pitch (rad)')
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
    return p.parse_args()


class CubeTracker(hm.HelloNode):
    def __init__(self, args):
        hm.HelloNode.__init__(self)
        self.args = args
        self.lock = threading.Lock()
        self.frame = None
        self.seq = 0
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
        self.move_to_pose({'joint_lift': a.lift}, blocking=True)
        self.move_to_pose({'joint_wrist_yaw': 0.0, 'joint_wrist_pitch': a.pitch,
                           'joint_wrist_roll': 0.0}, blocking=True)
        self.move_to_pose({'joint_gripper_finger_left': 0.5}, blocking=True)   # open

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

    # ---------- control law ----------
    def correction(self, grid, shape):
        """Face-center pixel error -> (ext_delta, arm-axis error, cross-axis error), meters."""
        a = self.args
        centers, pitch, _ = grid
        h, w = shape[:2]
        target = np.array([w / 2 + a.offset_px[0], h / 2 + a.offset_px[1]])
        err_px = centers[1, 1] - target                 # +x = cube right, +y = cube down
        err_m = err_px * (STICKER_PITCH_M / pitch)      # meters on the cube plane
        along, across = (err_m[0], err_m[1]) if a.ext_axis == 'x' else (err_m[1], err_m[0])
        step = 0.0 if abs(along) < a.deadband_m else a.ext_sign * along * a.gain
        step = float(np.clip(step, -a.max_step_m, a.max_step_m))
        return step, float(along), float(across)

    def annotate(self, frame, grid, status, color):
        view = frame.copy()
        h, w = view.shape[:2]
        a = self.args
        cx, cy = int(w / 2 + a.offset_px[0]), int(h / 2 + a.offset_px[1])
        cv2.drawMarker(view, (cx, cy), cc.WHITE, cv2.MARKER_CROSS, 30, 2)
        if grid is not None:
            centers, pitch, n = grid
            for p in centers.reshape(-1, 2):
                cv2.circle(view, (int(p[0]), int(p[1])), 5, color, 2)
            cv2.drawContours(view, [cc.grid_box(centers, pitch)], -1, cc.RED, 2)
            cv2.line(view, (cx, cy), (int(centers[1, 1][0]), int(centers[1, 1][1])), color, 2)
        cv2.putText(view, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        return view

    def show(self, view, text=None, color=None):
        """Draw the camera window; returns True when the user pressed q."""
        if text:
            view = view.copy()
            cv2.putText(view, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        cv2.imshow(WIN, view)
        return cv2.waitKey(1) & 0xFF == ord('q')

    # ---------- main loop ----------
    def run(self):
        a = self.args
        hm.HelloNode.main(self, 'cube_track', 'cube_track', wait_for_first_pointcloud=False)
        self.ensure_camera()
        cb = ReentrantCallbackGroup()
        self.view_pub = self.create_publisher(Image, '/cube_track/image', 1)
        self.create_subscription(Image, a.topic, self.on_image, qos_profile_sensor_data,
                                 callback_group=cb)
        self.get_logger().info(f'listening on {a.topic}'
                               + ('  (dry run: no motion)' if a.dry_run else ''))
        if a.gui:
            cv2.namedWindow(WIN, cv2.WINDOW_NORMAL)
            self.show(np.zeros((480, 640, 3), np.uint8), 'waiting for camera...', cc.WHITE)
        self.go_to_start_pose()

        seq, seen, aligned, last_state, last_warn = 0, 0, 0, None, 0.0
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
                state, status, color, aligned = 'LOST', 'cube lost - holding, waiting', cc.RED, 0
            elif seen < a.confirm:
                state, status, color = 'ACQUIRE', 'cube seen - confirming', cc.YELLOW
            else:
                ext_d, along, across = self.correction(grid, frame.shape)
                errs = f'arm {along * 1000:+.0f} mm  side {across * 1000:+.0f} mm'
                if ext_d == 0.0:
                    aligned += 1
                    state, color = 'ALIGNED', cc.GREEN
                    status = f'ALIGNED  {errs}'
                else:
                    aligned = 0
                    state, color = 'TRACK', cc.GREEN
                    status = f'tracking  {errs}'
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
