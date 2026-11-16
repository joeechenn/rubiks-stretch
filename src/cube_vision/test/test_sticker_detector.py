"""Tests for find_stickers using synthetic cube-face images."""
import cv2
import numpy as np

from cube_vision.sticker_detector import find_stickers

RGB = {
    "W": (240, 240, 240), "Y": (230, 210, 30), "R": (200, 30, 30),
    "O": (240, 120, 20), "G": (20, 160, 60), "B": (30, 60, 200),
}
FACE = ["WYR", "OGB", "RWY"]


def make_face(angle=0.0, sticker=90, gap=12, size=640, bg=(110, 120, 130),
              clutter=False, hide=None):
    """Return (image, expected centers of shape (3, 3, 2))."""
    img = np.full((size, size, 3), bg, np.uint8)
    pitch = sticker + gap
    # Center of the top-left sticker
    origin = np.array([size / 2, size / 2]) - pitch
    pad = sticker // 2 + gap
    x0, y0 = (origin - pad).astype(int)
    x1, y1 = (origin + 2 * pitch + pad).astype(int)
    cv2.rectangle(img, (x0, y0), (x1, y1), (15, 15, 15), -1)

    centers = np.zeros((3, 3, 2))
    for i in range(3):
        for j in range(3):
            c = origin + np.array([j, i]) * pitch
            centers[i, j] = c
            if hide == (i, j):
                continue
            p0 = (c - sticker / 2).astype(int)
            p1 = (c + sticker / 2).astype(int)
            cv2.rectangle(img, tuple(p0), tuple(p1), RGB[FACE[i][j]], -1)

    if clutter:
        cv2.rectangle(img, (10, 10), (70, 40), RGB["R"], -1)
        cv2.rectangle(img, (560, 20), (620, 120), RGB["B"], -1)
        cv2.rectangle(img, (20, 560), (50, 590), RGB["G"], -1)
        cv2.circle(img, (580, 580), 30, RGB["Y"], -1)

    M = cv2.getRotationMatrix2D((size / 2, size / 2), angle, 1.0)
    img = cv2.warpAffine(img, M, (size, size), borderValue=bg)
    pts = np.concatenate([centers.reshape(-1, 2), np.ones((9, 1))], axis=1) @ M.T
    return img, pts.reshape(3, 3, 2)


def _assert_centers(grid, expected, tol=3.0):
    assert grid is not None
    ok = ~np.isnan(grid.centers[..., 0])
    err = np.linalg.norm(grid.centers[ok] - expected[ok], axis=1)
    assert err.max() < tol, f"max center error {err.max():.1f}px"


def test_upright_complete():
    img, exp = make_face()
    g = find_stickers(img)
    assert g.complete
    _assert_centers(g, exp)


def test_rotated_20_degrees():
    img, exp = make_face(angle=20)
    g = find_stickers(img)
    assert g.complete
    _assert_centers(g, exp)
    assert abs(abs(g.theta_deg) - 20) < 2


def test_clutter_is_ignored():
    img, exp = make_face(angle=-12, clutter=True)
    g = find_stickers(img)
    assert g.complete
    _assert_centers(g, exp)


def test_expected_size_prior():
    img, _ = make_face()
    g = find_stickers(img, expected_sticker_px=90)
    assert g.complete and abs(g.size_ratio - 1) < 0.1
    assert find_stickers(img, expected_sticker_px=300) is None


def test_missing_edge_sticker_still_anchored_on_center():
    img, exp = make_face(hide=(0, 2))
    g = find_stickers(img)
    assert g.n_found == 8
    assert np.isnan(g.centers[0, 2, 0])
    _assert_centers(g, exp)


def test_no_cube_returns_none():
    img = np.full((640, 640, 3), (110, 120, 130), np.uint8)
    cv2.rectangle(img, (50, 50), (120, 90), RGB["R"], -1)
    cv2.rectangle(img, (300, 400), (330, 480), RGB["B"], -1)
    cv2.circle(img, (500, 200), 40, RGB["G"], -1)
    assert find_stickers(img) is None