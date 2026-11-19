#!/usr/bin/env python3
"""Scan all six faces of a Rubik's cube from a Stretch camera and show the whole cube.

Usage (regular terminal, or `unset GTK_PATH` first):
    python3 cube_scanner.py                          # gripper camera
    python3 cube_scanner.py /camera/color/image_raw  # head camera (rotated 90 deg)

The window shows the live view (with the fitted 3x3 grid) on the left and the
unfolded cube on the right. Show the faces in this order, each time pressing SPACE
while the grid is locked on the face (the prompt on screen says how to orient it):
    F, R, B, L (turn the cube about its vertical axis, same "up" edge), then U, then D.

Colors are never compared with fixed thresholds. Each sticker is given the letter of
the face whose CENTER sticker looks most like it, using brightness-independent
chromaticity, so it adapts to whatever lighting the camera sees. The result is the
54-letter facelet string in URFDLB order (the Kociemba solver's input format).

Keys: SPACE capture face | u undo last face | c clear all | p print state | q quit
"""
import sys
from collections import deque

import cv2
import numpy as np

import cube_contour as cc   # sticker detector (parses sys.argv itself; harmless here)

ORDER = ['F', 'R', 'B', 'L', 'U', 'D']          # scan order
FACELET_ORDER = 'URFDLB'                        # output order
PROMPTS = {
    'F': 'F: show any face. Remember which edge is UP.',
    'R': 'R: turn cube so the face on the RIGHT of F faces the camera (same top edge up).',
    'B': 'B: turn the same way again (same top edge up).',
    'L': 'L: turn the same way again (same top edge up).',
    'U': 'U: from F, tip the TOP toward the camera. F must be at the BOTTOM of the image.',
    'D': 'D: from F, tip the BOTTOM toward the camera. F must be at the TOP of the image.',
}
# top-left cell of each face in the unfolded net, in units of one face (3 stickers)
NET_POS = {'U': (1, 0), 'L': (0, 1), 'F': (1, 1), 'R': (2, 1), 'B': (3, 1), 'D': (1, 2)}
PARAMS = (40, 120, 150, 8000)
MIN_MATCHED = 5          # stickers the detector must really see before a capture is allowed
WIN = 'cube scanner'
CELL = 44                # net sticker size in pixels


# ---------- color sampling and classification (pure functions) ----------
def chromaticity(rgb):
    """Brightness-independent color: (r, g) of r+g+b. Shape (..., 3) -> (..., 2)."""
    rgb = np.asarray(rgb, np.float32)
    return rgb[..., :2] / np.maximum(rgb.sum(axis=-1, keepdims=True), 1.0)


def sample_face(frame, centers, pitch):
    """Median BGR of a small patch at each of the 9 lattice cells -> array [9, 3]."""
    gained = cc.auto_gain(frame)
    r = max(2, int(0.2 * pitch))
    h, w = gained.shape[:2]
    out = []
    for cx, cy in centers.reshape(-1, 2):
        x0, x1 = int(max(cx - r, 0)), int(min(cx + r + 1, w))
        y0, y1 = int(max(cy - r, 0)), int(min(cy + r + 1, h))
        patch = gained[y0:y1, x0:x1].reshape(-1, 3)
        out.append(np.median(patch, axis=0) if len(patch) else np.zeros(3))
    return np.array(out, np.float32)


def classify(faces):
    """faces: {letter: [9, 3] BGR samples}. Return {letter: list of 9 letters}.

    Each sticker gets the letter of the scanned face whose center sticker has the
    nearest chromaticity.
    """
    letters = list(faces)
    refs = np.array([chromaticity(faces[k][4][::-1]) for k in letters])   # BGR -> RGB
    result = {}
    for k in letters:
        chroma = chromaticity(faces[k][:, ::-1])                          # [9, 2]
        d = np.linalg.norm(chroma[:, None, :] - refs[None], axis=2)       # [9, n]
        result[k] = [letters[i] for i in d.argmin(axis=1)]
    return result


def facelet_string(labels):
    """54-letter URFDLB string, or None until all six faces are labelled."""
    if any(k not in labels for k in FACELET_ORDER):
        return None
    return ''.join(''.join(labels[k]) for k in FACELET_ORDER)


def check_counts(state):
    """Return None if each letter appears 9 times, else a short problem description."""
    bad = {k: state.count(k) for k in FACELET_ORDER if state.count(k) != 9}
    return None if not bad else ', '.join(f'{k}x{n}' for k, n in bad.items())


# ---------- drawing ----------
def display_color(bgr):
    """Scale a measured color to a comfortable brightness for the net."""
    bgr = np.asarray(bgr, np.float32)
    return tuple(int(v) for v in np.clip(bgr * 220.0 / max(bgr.max(), 1.0), 0, 255))


def draw_net(faces, labels, height):
    net = np.full((3 * 3 * CELL, 4 * 3 * CELL, 3), 40, np.uint8)
    for letter, (fx, fy) in NET_POS.items():
        for i in range(9):
            x = (fx * 3 + i % 3) * CELL
            y = (fy * 3 + i // 3) * CELL
            if letter in labels:
                center = faces[labels[letter][i]][4]
                cv2.rectangle(net, (x + 2, y + 2), (x + CELL - 2, y + CELL - 2),
                              display_color(center), -1)
                cv2.putText(net, labels[letter][i], (x + 14, y + 29),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
            else:
                cv2.rectangle(net, (x + 2, y + 2), (x + CELL - 2, y + CELL - 2), (70, 70, 70), 1)
        cv2.putText(net, letter, (fx * 3 * CELL + 4, fy * 3 * CELL + 14),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)
    scale = height / net.shape[0]
    return cv2.resize(net, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)


def draw_live(view, grid):
    """Overlay the fitted lattice: filled dot = sticker seen, hollow = inferred."""
    if grid is None:
        return
    centers, pitch, n = grid
    for p in centers.reshape(-1, 2):
        cv2.circle(view, (int(p[0]), int(p[1])), 6, cc.GREEN if n >= MIN_MATCHED else cc.YELLOW, 2)
    box = cc.grid_box(centers, pitch)
    cv2.drawContours(view, [box], -1, cc.RED, 2)


# ---------- ROS node ----------
class Scanner:
    def __init__(self):
        self.faces = {}                 # letter -> [9, 3] BGR samples
        self.recent = deque(maxlen=5)   # recent samples, so a capture is a median
        self.grid = None
        self.frame = None

    @property
    def next_letter(self):
        return next((k for k in ORDER if k not in self.faces), None)

    def on_frame(self, frame):
        self.frame = frame
        self.grid = cc.find_face(frame, PARAMS)[3]
        if self.grid is not None and self.grid[2] >= MIN_MATCHED:
            self.recent.append(sample_face(frame, self.grid[0], self.grid[1]))
        else:
            self.recent.clear()

    def capture(self):
        letter = self.next_letter
        if letter is None or not self.recent:
            return None
        self.faces[letter] = np.median(np.array(self.recent), axis=0)
        self.recent.clear()
        return letter

    def undo(self):
        if self.faces:
            del self.faces[[k for k in ORDER if k in self.faces][-1]]

    def state(self):
        labels = classify(self.faces) if self.faces else {}
        return labels, facelet_string(labels)

    def render(self):
        view = self.frame.copy()
        draw_live(view, self.grid)
        labels, state = self.state()
        nxt = self.next_letter
        n = self.grid[2] if self.grid else 0
        status = (PROMPTS[nxt] if nxt else 'All faces scanned.')
        lock = f'grid {n}/9' + ('  READY - press SPACE' if nxt and n >= MIN_MATCHED else '')
        cv2.putText(view, lock, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, cc.WHITE, 2)
        cv2.putText(view, status[:70], (10, view.shape[0] - 14),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, cc.WHITE, 2)
        net = draw_net(self.faces, labels, view.shape[0])
        if state:
            problem = check_counts(state)
            cv2.putText(net, 'state OK' if not problem else f'check: {problem}', (8, 24),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, cc.GREEN if not problem else cc.RED, 2)
        return np.hstack([view, net]), state


def main():
    import rclpy
    from cv_bridge import CvBridge
    from rclpy.executors import ExternalShutdownException
    from rclpy.node import Node
    from rclpy.qos import qos_profile_sensor_data
    from sensor_msgs.msg import Image

    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    topic = args[0] if args else '/gripper_camera/color/image_rect_raw'
    rotate = 'gripper' not in topic

    rclpy.init()
    node = Node('cube_scanner')
    bridge, scanner = CvBridge(), Scanner()

    def on_image(msg):
        frame = bridge.imgmsg_to_cv2(msg, 'bgr8')
        if rotate:
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        scanner.on_frame(frame)
        shown, state = scanner.render()
        cv2.imshow(WIN, shown)
        key = cv2.waitKey(1) & 0xFF
        if key == ord(' '):
            letter = scanner.capture()
            node.get_logger().info(f'captured {letter}' if letter else
                                   'nothing captured (no grid lock, or all faces done)')
        elif key == ord('u'):
            scanner.undo()
        elif key == ord('c'):
            scanner.faces.clear()
        elif key == ord('p'):
            node.get_logger().info(f'facelets (URFDLB): {state}')
        elif key == ord('q'):
            rclpy.shutdown()

    node.create_subscription(Image, topic, on_image, qos_profile_sensor_data)
    node.get_logger().info(f'Listening on {topic}')
    cv2.namedWindow(WIN, cv2.WINDOW_NORMAL)
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
