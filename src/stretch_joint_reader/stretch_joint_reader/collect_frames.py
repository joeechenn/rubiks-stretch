#!/usr/bin/env python3
"""Save frames from a Stretch camera topic to build a cube dataset.

Usage (regular terminal, or `unset GTK_PATH` first):
    python3 collect_frames.py                        # gripper camera, press SPACE to save
    python3 collect_frames.py --tag dim_lamp         # label this lighting setup
    python3 collect_frames.py --every 1.5            # also auto-save every 1.5 s
    python3 collect_frames.py TOPIC --no-gui --every 1 --max 200

Frames are saved unmodified (BGR PNG, no rotation) to
    ~/ament_ws/cube_dataset/<tag>/<tag>_<timestamp>.png
so they can be labelled and augmented later. Change the lighting, cube pose and
background between sessions and give each session its own --tag.

Keys: SPACE = save a frame, q = quit.
"""
import argparse
import os
import time

import cv2
import numpy as np
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image

WIN = 'collect frames'


def parse_args():
    p = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    p.add_argument('topic', nargs='?', default='/gripper_camera/color/image_rect_raw')
    p.add_argument('--tag', default='session', help='lighting/session label (folder name)')
    p.add_argument('--out', default=os.path.expanduser('~/ament_ws/cube_dataset'))
    p.add_argument('--every', type=float, default=0.0, help='auto-save period in s (0 = off)')
    p.add_argument('--max', type=int, default=0, help='stop after this many frames (0 = no limit)')
    p.add_argument('--no-gui', action='store_true')
    return p.parse_args()


class Collector(Node):
    def __init__(self, args):
        super().__init__('collect_frames')
        self.args = args
        self.dir = os.path.join(args.out, args.tag)
        os.makedirs(self.dir, exist_ok=True)
        self.count = len(os.listdir(self.dir))
        self.bridge = CvBridge()
        self.last_save = 0.0
        self.create_subscription(Image, args.topic, self.on_image, qos_profile_sensor_data)
        self.get_logger().info(f'Listening on {args.topic}; saving to {self.dir}')

    def save(self, frame):
        name = f'{self.args.tag}_{time.strftime("%Y%m%d_%H%M%S")}_{self.count:04d}.png'
        cv2.imwrite(os.path.join(self.dir, name), frame)
        self.count += 1
        self.last_save = time.monotonic()
        self.get_logger().info(f'saved {name} ({self.count} in this folder)')

    def on_image(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        auto = self.args.every > 0 and time.monotonic() - self.last_save >= self.args.every
        key = -1
        if not self.args.no_gui:
            view = np.ascontiguousarray(frame.copy())
            cv2.putText(view, f'{self.args.tag}: {self.count} saved   SPACE=save q=quit',
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            cv2.imshow(WIN, view)
            key = cv2.waitKey(1) & 0xFF
        if key == ord(' ') or auto:
            self.save(frame)
        if key == ord('q') or (self.args.max and self.count >= self.args.max):
            rclpy.shutdown()


def main():
    from rclpy.executors import ExternalShutdownException
    args = parse_args()
    rclpy.init()
    node = Collector(args)
    if not args.no_gui:
        cv2.namedWindow(WIN, cv2.WINDOW_NORMAL)
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
