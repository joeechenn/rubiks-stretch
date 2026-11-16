"""Run find_stickers on images and save annotated copies.

Usage:
    python scripts/draw_grid.py IMAGE [IMAGE ...] [--out DIR] [--max-dim N] [--sticker-px PX]

Writes <name>_grid.png (detected centers drawn on the image) and
<name>_mask.png (the sticker mask) to the output directory. Images are
downscaled so the longer side is at most --max-dim before detection;
--sticker-px refers to the downscaled image.
"""
import argparse
import sys
from pathlib import Path

import cv2
import numpy as np

# Allow running as a plain script.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cube_vision.sticker_detector import find_stickers  # noqa: E402

# Drawing colors (RGB)
GREEN, RED, YELLOW = (0, 255, 0), (255, 0, 0), (255, 255, 0)


def draw_grid(image_rgb, grid, kept=None):
    """Annotated RGB copy: center sticker in red, others green, candidates boxed."""
    out = image_rgb.copy()
    if kept is not None:
        for cx, cy, side in kept:
            p0 = (int(cx - side / 2), int(cy - side / 2))
            p1 = (int(cx + side / 2), int(cy + side / 2))
            cv2.rectangle(out, p0, p1, YELLOW, 1)

    if grid is None:
        cv2.putText(out, "NO GRID FOUND", (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1.2, RED, 3, cv2.LINE_AA)
        return out

    r = max(4, int(grid.sticker_px * 0.15))
    for i in range(3):
        for j in range(3):
            x, y = grid.centers[i, j]
            if np.isnan(x):
                continue
            color = RED if (i, j) == (1, 1) else GREEN
            cv2.circle(out, (int(x), int(y)), r, color, -1)
            cv2.putText(out, f"{i},{j}", (int(x) + r + 2, int(y) - r),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)

    status = "complete" if grid.complete else f"partial {grid.n_found}/9"
    cv2.putText(out, f"{status}  sticker={grid.sticker_px:.0f}px  resid={grid.residual:.2f}",
                (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, GREEN, 2, cv2.LINE_AA)
    return out


def main():
    ap = argparse.ArgumentParser(description="Annotate detected cube-face sticker grids.")
    ap.add_argument("images", nargs="+")
    ap.add_argument("--out", default="debug_out")
    ap.add_argument("--max-dim", type=int, default=1000)
    ap.add_argument("--sticker-px", type=float, default=None,
                    help="expected sticker side in pixels (downscaled image)")
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    for path in args.images:
        bgr = cv2.imread(path)
        if bgr is None:
            print(f"{path}: could not read, skipping")
            continue
        scale = args.max_dim / max(bgr.shape[:2])
        if scale < 1:
            bgr = cv2.resize(bgr, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

        dbg = {}
        grid = find_stickers(rgb, expected_sticker_px=args.sticker_px, debug=dbg)

        name = Path(path).stem
        annotated = draw_grid(rgb, grid, dbg.get("kept"))
        cv2.imwrite(str(out_dir / f"{name}_grid.png"), cv2.cvtColor(annotated, cv2.COLOR_RGB2BGR))
        cv2.imwrite(str(out_dir / f"{name}_mask.png"), dbg["mask"])

        if grid is None:
            print(f"{path}: no grid (candidates={len(dbg['candidates'])}, kept={len(dbg['kept'])})")
        else:
            print(f"{path}: n_found={grid.n_found}/9  sticker={grid.sticker_px:.0f}px  "
                  f"pitch={grid.pitch_px:.0f}px  theta={grid.theta_deg:.1f}deg  "
                  f"resid={grid.residual:.3f}")


if __name__ == "__main__":
    main()