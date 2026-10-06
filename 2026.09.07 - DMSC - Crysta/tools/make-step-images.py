#!/usr/bin/env python3
"""Rebuild the three panels of the "What the software has to do" slide from their sources.

The originals are EasyDiffraction documentation figures: the instrument sketch is drawn on black,
the two plots on white. The deck is dark, so each is reduced to its drawn content on a transparent
background — that way no panel shows as a bright card and the three sit together.

    python3 tools/make-step-images.py
"""
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent.parent / "images"

# (source, target, inset, framed) — the two plots get a rectangular axes box drawn back on;
# the instrument sketch is not a plot and stays unframed.
SOURCES = [
    ("data-acquisition_instrument.png", "step-measure.png", 0, False),
    ("data-reduction_1d-pattern.png", "step-pattern.png", 4, True),
    ("data-analysis_refinement.png", "step-refined.png", 4, True),
]

FRAME_RGB = (153, 153, 153)   # the deck's axis grey, readable on the dark background
FRAME_PAD = 34                # room between the curve and the box
FRAME_W = 9                   # the panels render ~4.4x smaller, so the box needs the width


def framed(a: np.ndarray) -> np.ndarray:
    """Pad the trimmed plot and stroke a rectangle around it — the axes box the source figure had."""
    h, w = a.shape[:2]
    out = np.zeros((h + 2 * FRAME_PAD, w + 2 * FRAME_PAD, 4), dtype=a.dtype)
    out[FRAME_PAD : FRAME_PAD + h, FRAME_PAD : FRAME_PAD + w] = a
    out[:FRAME_W, :] = out[-FRAME_W:, :] = (*FRAME_RGB, 255)
    out[:, :FRAME_W] = out[:, -FRAME_W:] = (*FRAME_RGB, 255)
    return out


def prepare(src: Path, dst: Path, inset: int, frame: bool) -> None:
    a = np.array(Image.open(src).convert("RGBA"))
    if a[..., 3].min() == 255:
        # an opaque source: everything near-white is background
        a[..., 3] = np.where((a[..., :3].astype(int) > 238).all(axis=-1), 0, 255)
    ys, xs = np.where(a[..., 3] > 0)
    # `inset` trims the plot frame, which would otherwise survive as a box around the curve
    a = a[ys.min() + inset : ys.max() + 1 - inset, xs.min() + inset : xs.max() + 1 - inset]
    if frame:
        a = framed(a)
    Image.fromarray(a).save(dst)
    print(f"{dst.name}: {Image.open(dst).size}")


if __name__ == "__main__":
    for src, dst, inset, frame in SOURCES:
        prepare(HERE / src, HERE / dst, inset, frame)
