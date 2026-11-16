"""Locate the 3x3 sticker grid of a Rubik's cube face in an RGB image.

Conventions:
  - Input is an HxWx3 uint8 RGB image.
  - centers[row, col] = (x, y) in pixels. Row 0 / col 0 are the top / left of
    the face as seen in the image. The grid may be rotated up to +-45 degrees.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import cv2
import numpy as np


@dataclass
class StickerGrid:
    # (3, 3, 2) float; NaN where not found
    centers: np.ndarray
    # Median sticker side length
    sticker_px: float
    # Center-to-center spacing
    pitch_px: float
    # Grid rotation (image coords, y down)
    theta_deg: float
    # Matched positions out of 9
    n_found: int
    # Mean offset from ideal point / pitch
    residual: float
    # sticker_px / expected_sticker_px
    size_ratio: Optional[float] = None

    @property
    def complete(self) -> bool:
        return self.n_found == 9

    @property
    def center_sticker(self) -> np.ndarray:
        """(x, y) of the middle sticker (always present)."""
        return self.centers[1, 1]


def _sticker_mask(rgb, s_color=70, v_color=60, s_white=60, v_white=150):
    """Mask of saturated (colored) or bright low-saturation (white) pixels."""
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    colored = cv2.inRange(hsv, (0, s_color, v_color), (179, 255, 255))
    white = cv2.inRange(hsv, (0, 0, v_white), (179, s_white, 255))
    mask = cv2.bitwise_or(colored, white)
    return cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))


def _square_candidates(mask, min_side, max_side, min_aspect=0.7, min_fill=0.7):
    """Square-ish blobs as an (N, 3) array of [cx, cy, side]."""
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    out = []
    for c in contours:
        (cx, cy), (w, h), _ = cv2.minAreaRect(c)
        if w < 1 or h < 1:
            continue
        side = float(np.sqrt(w * h))
        if not (min_side <= side <= max_side):
            continue
        if min(w, h) / max(w, h) < min_aspect:
            continue
        if cv2.contourArea(c) / (w * h) < min_fill:
            continue
        out.append((cx, cy, side))
    return np.array(out, dtype=float).reshape(-1, 3)


def _pick_size_cluster(cands, expected_px=None, cluster_tol=0.25, expected_tol=0.4):
    """Keep the largest group of candidates with similar side length."""
    if expected_px is not None and len(cands):
        cands = cands[np.abs(cands[:, 2] / expected_px - 1) <= expected_tol]
    if len(cands) == 0:
        return cands

    sides = cands[:, 2]
    # Tiny bonus for larger sizes so small speckle loses ties.
    scores = [(np.abs(sides / s - 1) <= cluster_tol).sum() + 1e-6 * s for s in sides]
    ref = sides[int(np.argmax(scores))]
    ref = np.median(sides[np.abs(sides / ref - 1) <= cluster_tol])
    return cands[np.abs(sides / ref - 1) <= cluster_tol]


def _lattice_params(pts):
    """Grid pitch (px) and rotation (rad) from nearest-neighbor vectors."""
    dist = np.linalg.norm(pts[:, None, :] - pts[None, :, :], axis=2)
    np.fill_diagonal(dist, np.inf)
    nn = dist.argmin(axis=1)
    pitch = float(np.median(dist[np.arange(len(pts)), nn]))
    vec = pts[nn] - pts
    ang = np.arctan2(vec[:, 1], vec[:, 0])
    # Grid directions repeat every 90 deg, so average 4x the angle.
    theta = float(np.arctan2(np.sin(4 * ang).mean(), np.cos(4 * ang).mean()) / 4)
    return pitch, theta


def _fit_lattice(pts, pitch, theta, tol):
    """Try each point as the center sticker; keep the lattice matching the most points."""
    # Unit vector along a row
    ex = np.array([np.cos(theta), np.sin(theta)])
    # Unit vector down a column
    ey = np.array([-np.sin(theta), np.cos(theta)])
    best = None
    for seed in pts:
        centers = np.full((3, 3, 2), np.nan)
        used, errs = set(), []
        for i in range(3):
            for j in range(3):
                ideal = seed + (j - 1) * pitch * ex + (i - 1) * pitch * ey
                d = np.linalg.norm(pts - ideal, axis=1)
                k = int(d.argmin())
                if d[k] <= tol * pitch and k not in used:
                    centers[i, j] = pts[k]
                    used.add(k)
                    errs.append(d[k] / pitch)
        score = (len(used), -float(np.mean(errs)))
        if best is None or score > best[0]:
            best = (score, centers, errs)
    return best[1], best[2]


def find_stickers(
    image_rgb: np.ndarray,
    expected_sticker_px: Optional[float] = None,
    min_stickers: int = 6,
    lattice_tol: float = 0.3,
    min_side_frac: float = 0.015,
    max_side_frac: float = 0.4,
    mask_params: Optional[dict] = None,
    debug: Optional[dict] = None,
) -> Optional[StickerGrid]:
    """Find the sticker grid of one cube face.

    expected_sticker_px: optional prior for the sticker side length in pixels
        (e.g. from camera intrinsics and depth). Estimated from the image if None.
    min_stickers: minimum matched stickers to accept a grid (keep >= 6).
    lattice_tol: max offset from an ideal grid point, as a fraction of pitch.
    min_side_frac, max_side_frac: sticker size bounds relative to the shorter
        image side.
    mask_params: overrides for the _sticker_mask thresholds.
    debug: if a dict, filled with 'mask', 'candidates' and 'kept'.

    Returns a StickerGrid, or None if no valid grid is found.
    """
    if image_rgb.ndim != 3 or image_rgb.shape[2] != 3:
        raise ValueError("expected an HxWx3 RGB image")

    short = min(image_rgb.shape[:2])
    mask = _sticker_mask(image_rgb, **(mask_params or {}))
    cands = _square_candidates(mask, min_side_frac * short, max_side_frac * short)
    kept = _pick_size_cluster(cands, expected_sticker_px)

    if debug is not None:
        debug.update(mask=mask, candidates=cands, kept=kept)

    if len(kept) < min_stickers:
        return None

    pts = kept[:, :2]
    pitch, theta = _lattice_params(pts)
    centers, errs = _fit_lattice(pts, pitch, theta, lattice_tol)
    n_found = int(np.sum(~np.isnan(centers[..., 0])))
    if n_found < min_stickers:
        return None

    sticker_px = float(np.median(kept[:, 2]))
    return StickerGrid(
        centers=centers,
        sticker_px=sticker_px,
        pitch_px=pitch,
        theta_deg=float(np.degrees(theta)),
        n_found=n_found,
        residual=float(np.mean(errs)),
        size_ratio=(sticker_px / expected_sticker_px) if expected_sticker_px else None,
    )