#!/usr/bin/env python3
"""Find the Rubik's cube in a Stretch camera feed and draw a contour around it.

Usage (run from a regular terminal, or after `unset GTK_PATH`):
    python3 cube_contour.py                                       # gripper camera
    python3 cube_contour.py /camera/color/image_raw               # head camera
    python3 cube_contour.py /gripper_camera/color/image_rect_raw --no-gui

How it works:
  0. Stretch dim frames to full brightness (auto_gain).
  1. Even out the lighting with CLAHE on the L channel (LAB color space).
  2. Find small square regions (the stickers): by edges, and by color
     (non-black blobs split by the black plastic). Results are merged.
  3. Keep the stickers that are similar in size and close together (one face).
  4. Fit a 3x3 lattice to those stickers (pitch + rotation), so missing stickers
     are inferred, and draw its outer box = the cube face contour.
  If too few stickers are found, fall back to a "colorful blob" mask.

The annotated image is also published on /cube_detection/image so you can
watch it in rqt_image_view if the OpenCV window won't open.
Press 'q' in the window to quit, 's' to save a snapshot.
"""
import sys
import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

args = [a for a in sys.argv[1:] if not a.startswith('--')]
TOPIC = args[0] if args else '/gripper_camera/color/image_rect_raw'
ROTATE = 'gripper' not in TOPIC   # Stretch's head camera is mounted sideways
GUI = '--no-gui' not in sys.argv
WIN = 'cube contour'

GREEN, YELLOW, RED, WHITE = (0, 255, 0), (0, 255, 255), (0, 0, 255), (255, 255, 255)


# ---------- step 0: brightness stretch ----------
def auto_gain(bgr, percentile=99.5, max_gain=30.0):
    """Scale a dim frame so its bright end reaches ~255 (no-op if already bright).

    Tuned on dark gripper-camera frames: it raised the number of frames with 5+ of 9
    stickers matched from 20 to 32 of 50. Loosening the color thresholds did not help.
    """
    gain = min(max_gain, 255.0 / max(np.percentile(bgr.max(axis=2), percentile), 1.0))
    if gain <= 1.05:
        return bgr
    return np.clip(bgr.astype(np.float32) * gain, 0, 255).astype(np.uint8)


# ---------- step 1: lighting normalization ----------
CLAHE = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))


def normalize_lighting(bgr):
    """Equalize brightness locally so shadows and glare matter less."""
    lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    return cv2.cvtColor(cv2.merge((CLAHE.apply(l), a, b)), cv2.COLOR_LAB2BGR)


# ---------- step 2: sticker candidates ----------
def find_stickers(bgr, canny_lo, canny_hi, min_area, max_area):
    """Return a list of (contour, center, side_length) for square-ish regions."""
    gray = cv2.GaussianBlur(cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY), (5, 5), 0)
    edges = cv2.Canny(gray, canny_lo, canny_hi)
    edges = cv2.dilate(edges, np.ones((3, 3), np.uint8), iterations=1)
    regions = cv2.bitwise_not(edges)
    contours, _ = cv2.findContours(regions, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    stickers = []
    for c in contours:
        area = cv2.contourArea(c)
        if not (min_area < area < max_area):
            continue
        (cx, cy), (w, h), _ = cv2.minAreaRect(c)
        if w == 0 or h == 0 or not (0.7 < w / h < 1.4):
            continue
        if area / (w * h) < 0.75:
            continue
        # stickers are one solid color; tags and textures are patterned
        mask = np.zeros(gray.shape, np.uint8)
        cv2.drawContours(mask, [c], -1, 255, -1)
        mean, std = cv2.meanStdDev(gray, mask=mask)
        if std[0][0] > 30 or mean[0][0] < 25:   # patterned, or black plastic
            continue
        stickers.append((c, np.array([cx, cy]), (w + h) / 2))
    return dedupe(stickers)


def find_color_stickers(bgr, min_area, max_area, v_min=45, s_min=60, v_white=110):
    """Find stickers as solid-color regions separated by the black plastic.

    Works where edges are too faint (dark red/blue next to black): any pixel that
    is clearly not black plastic counts, a small erosion splits touching stickers,
    and the survivors are filtered for size and squareness.
    Returns the same (contour, center, side_length) tuples as find_stickers.
    """
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    s, v = hsv[:, :, 1], hsv[:, :, 2]
    mask = ((v > v_min) & ((s > s_min) | (v > v_white))).astype(np.uint8) * 255
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    erode = 2
    mask = cv2.erode(mask, np.ones((3, 3), np.uint8), iterations=erode)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    stickers = []
    for c in contours:
        area = cv2.contourArea(c)
        # the erosion shrank each region, so compare against a slightly smaller range
        if not (0.5 * min_area < area < max_area):
            continue
        (cx, cy), (w, hh), _ = cv2.minAreaRect(c)
        if w == 0 or hh == 0 or not (0.7 < w / hh < 1.4):
            continue
        if area / (w * hh) < 0.75:
            continue
        # a sticker is a single color: reject regions spanning several hues
        region = np.zeros(mask.shape, np.uint8)
        cv2.drawContours(region, [c], -1, 255, -1)
        _, sat_std = cv2.meanStdDev(s, mask=region)
        if sat_std[0][0] > 45:
            continue
        # grow the contour back by the erosion so size matches the edge detector
        grown = cv2.dilate(region, np.ones((3, 3), np.uint8), iterations=erode)
        gc, _ = cv2.findContours(grown, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not gc:
            continue
        stickers.append((gc[0], np.array([cx, cy]), (w + hh) / 2 + 2 * erode))
    return stickers


def dedupe(stickers):
    """Drop candidates that sit on top of each other (nested squares)."""
    kept = []
    for s in sorted(stickers, key=lambda s: -s[2]):
        if all(np.linalg.norm(s[1] - k[1]) > 0.5 * max(s[2], k[2]) for k in kept):
            kept.append(s)
    return kept


# ---------- step 3: group stickers into one face ----------
def group_face(stickers):
    """Keep stickers that look like they belong to the same 3x3 face."""
    if len(stickers) < 3:
        return []
    sides = np.array([s[2] for s in stickers])
    med_side = np.median(sides)
    similar = [s for s in stickers if 0.6 * med_side < s[2] < 1.6 * med_side]
    if len(similar) < 3:
        return []

    centers = np.array([s[1] for s in similar])
    seed = centers[np.argmin(np.linalg.norm(centers - np.median(centers, axis=0), axis=1))]
    reach = 2.6 * med_side * 1.15            # center sticker to corner sticker, with gaps
    return [s for s in similar if np.linalg.norm(s[1] - seed) < reach]


# ---------- step 4: force a 3x3 grid from sticker spacing ----------
def fit_grid(face):
    """Fit a 3x3 lattice to the detected stickers of one face.

    Pitch (center-to-center spacing) and rotation come from vectors between
    neighbouring stickers; then every sticker is tried in every one of the 9
    cells and the lattice that explains the most stickers wins. Missing
    stickers therefore don't shrink the face box.
    Returns (centers[3, 3, 2] as (row, col) -> (x, y), pitch, n_matched) or None.
    """
    if len(face) < 3:
        return None
    pts = np.array([s[1] for s in face])
    # Spacing: the typical nearest-neighbour distance. Don't compare with the blob
    # size, which can be inflated by spill into the black gaps. A sticker's nearest
    # neighbour is usually an adjacent one, not a diagonal.
    dist = np.linalg.norm(pts[:, None] - pts[None], axis=2)
    np.fill_diagonal(dist, np.inf)
    pitch0 = float(np.median(dist.min(axis=1)))
    vecs = np.array([pts[j] - pts[i] for i in range(len(pts)) for j in range(i + 1, len(pts))
                     if 0.8 * pitch0 < dist[i, j] < 1.25 * pitch0])
    if len(vecs) == 0:
        return None
    pitch = float(np.median(np.linalg.norm(vecs, axis=1)))
    # a square grid repeats every 90 degrees, so average the angle as 4*theta
    th = np.arctan2(vecs[:, 1], vecs[:, 0])
    phi = np.arctan2(np.sin(4 * th).mean(), np.cos(4 * th).mean()) / 4
    u = np.array([np.cos(phi), np.sin(phi)])      # one step along a grid row
    v = np.array([-np.sin(phi), np.cos(phi)])     # one step down a grid column

    offsets = np.array([[(c - 1) * u + (r - 1) * v for c in range(3)]
                        for r in range(3)]) * pitch          # [r, c] -> (dx, dy)
    best = None
    for p in pts:
        for r in range(3):
            for c in range(3):
                origin = p - offsets[r, c]
                lattice = origin + offsets
                d = np.linalg.norm(pts[:, None, None, :] - lattice[None], axis=3)
                near = d.min(axis=(1, 2)) < 0.35 * pitch
                score = (int(near.sum()), -float(d.min(axis=(1, 2))[near].sum()))
                if best is None or score > best[0]:
                    best = (score, origin, near)
    (n, _), origin, near = best
    if n < 3:
        return None
    # refine the lattice center using the stickers that matched
    shifts = []
    for p in pts[near]:
        k = np.argmin(np.linalg.norm(origin + offsets - p, axis=2))
        shifts.append(p - (origin + offsets.reshape(-1, 2)[k]))
    origin = origin + np.mean(shifts, axis=0)
    return origin + offsets, pitch, n


# ---------- fallback: colorful blob ----------
def find_blob(bgr, min_area):
    """Mask saturated (colored) or bright-unsaturated (white) pixels, take the biggest blob."""
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    s, v = hsv[:, :, 1], hsv[:, :, 2]
    mask = ((s > 70) & (v > 40)) | ((s < 50) & (v > 150))   
    mask = mask.astype(np.uint8) * 255
    k = np.ones((15, 15), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, k)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = [c for c in contours if cv2.contourArea(c) > 9 * min_area]
    return max(contours, key=cv2.contourArea) if contours else None


def grid_box(centers, pitch):
    """Outer corners of the face: the 3x3 lattice grown by half a pitch."""
    u = (centers[0, 2] - centers[0, 0]) / (2 * pitch)    # unit step along a row
    v = (centers[2, 0] - centers[0, 0]) / (2 * pitch)    # unit step down a column
    h = 1.5 * pitch
    mid = centers[1, 1]
    return np.array([mid - h * u - h * v, mid + h * u - h * v,
                     mid + h * u + h * v, mid - h * u + h * v]).round().astype(int)


def draw_grid(view, centers, face):
    """Dots at the 9 cell centers: filled if a sticker was seen, hollow if inferred."""
    seen = np.array([s[1] for s in face])
    tol = 0.35 * np.median([s[2] for s in face])
    for p in centers.reshape(-1, 2):
        found = np.linalg.norm(seen - p, axis=1).min() < tol
        cv2.circle(view, tuple(int(x) for x in p), 5, GREEN if found else YELLOW,
                   -1 if found else 2)


def find_face(frame, params):
    """Run the whole sticker pipeline on a BGR frame.

    Returns (normalized image, all stickers, face stickers, grid or None); grid is
    the fit_grid() result (centers[3, 3, 2], pitch, n_matched).
    """
    norm = normalize_lighting(auto_gain(frame))
    stickers = dedupe(find_stickers(norm, *params)
                      + find_color_stickers(norm, params[2], params[3]))
    face = group_face(stickers)
    return norm, stickers, face, (fit_grid(face) if len(face) >= 3 else None)


def detect(frame, params):
    """Return (annotated image, face box or None, method name)."""
    norm, stickers, face, grid = find_face(frame, params)
    view = frame.copy()

    for c, _, _ in stickers:                             # all candidates, thin yellow
        cv2.drawContours(view, [c], -1, YELLOW, 1)

    if len(face) >= 3:
        for c, _, _ in face:                             # face stickers, green
            cv2.drawContours(view, [c], -1, GREEN, 2)
        if grid is not None:
            centers, pitch, n = grid
            box = grid_box(centers, pitch)
            draw_grid(view, centers, face)
            method = f'grid ({n}/9 stickers)'
        else:
            pts = np.vstack([c.reshape(-1, 2) for c, _, _ in face]).astype(np.float32)
            box = cv2.boxPoints(cv2.minAreaRect(pts)).astype(int)
            method = f'stickers ({len(face)})'
    else:
        blob = find_blob(norm, params[2])
        if blob is None:
            cv2.putText(view, 'no cube', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, RED, 2)
            return view, None, 'none'
        box = cv2.boxPoints(cv2.minAreaRect(blob)).astype(int)
        method = 'color blob'

    cv2.drawContours(view, [box], -1, RED, 3)            # the cube contour
    cv2.putText(view, method, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, WHITE, 2)
    return view, box, method


class CubeContour(Node):
    def __init__(self):
        super().__init__('cube_contour')
        self.bridge = CvBridge()
        self.pub = self.create_publisher(Image, '/cube_detection/image', 1)
        self.create_subscription(Image, TOPIC, self.on_image, qos_profile_sensor_data)
        self.get_logger().info(f'Listening on {TOPIC}')
        self.last_method = None
        if GUI:
            cv2.namedWindow(WIN, cv2.WINDOW_NORMAL)
            for name, val, mx in [('canny lo', 40, 255), ('canny hi', 120, 255),
                                  ('min area', 150, 5000), ('max area', 8000, 40000)]:
                cv2.createTrackbar(name, WIN, val, mx, lambda _: None)

    def params(self):
        if not GUI:
            return 40, 120, 150, 8000
        return tuple(cv2.getTrackbarPos(n, WIN)
                     for n in ('canny lo', 'canny hi', 'min area', 'max area'))

    def on_image(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        if ROTATE:
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

        view, box, method = detect(frame, self.params())
        if method != self.last_method:                   # log only when it changes
            self.get_logger().info(f'detection: {method}')
            self.last_method = method

        view = np.ascontiguousarray(view, dtype=np.uint8)
        out = Image()
        out.header = msg.header
        out.height, out.width = view.shape[:2]
        out.encoding = 'bgr8'
        out.step = view.shape[1] * 3
        out.data = view.tobytes()
        self.pub.publish(out)

        if GUI:
            cv2.imshow(WIN, view)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('s'):
                cv2.imwrite('cube_snapshot.png', view)
                self.get_logger().info('saved cube_snapshot.png')
            elif key == ord('q'):
                rclpy.shutdown()


def main():
    from rclpy.executors import ExternalShutdownException
    rclpy.init()
    node = CubeContour()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
