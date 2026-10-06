#!/usr/bin/env python3
"""Turn a phone photograph of a projected conference slide into a deck-ready 1600x900 image.

A projection photograph arrives skewed, warm and washed out, with the projector's own falloff
across the screen. Four steps fix that, in this order:

  1. crop away the screen surround (the dark strip at the frame edge),
  2. deskew by the text itself — the rotation whose row profile has the sharpest peaks,
  3. flatten the illumination by dividing out a heavily blurred copy (the projector's gradient),
  4. neutralise the colour cast and stretch the levels so the text reads.

    python3 tools/make-slide-photo.py <source.jpg> images/<target>.jpg
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

OUT_W, OUT_H = 1600, 900
DARK_EDGE = 0.75        # a column dimmer than this fraction of the median is screen surround
BLUR = 420              # radius of the background estimate: broad enough to leave the
                        # headline alone and only take out the projector falloff
BG_LEVEL = 0.46         # where the slide background should land (0..1)
TEXT_LEVEL = 0.995      # where the brightest text should land
INSET = 0.022           # trim the screen bezel the threshold crop leaves in the corners


def crop_surround(a: np.ndarray) -> np.ndarray:
    g = a.mean(axis=2)
    col = g.mean(axis=0)
    thr = np.median(col) * DARK_EDGE
    keep = np.where(col > thr)[0]
    x0, x1 = keep[0], keep[-1] + 1
    row = g.mean(axis=1)
    keep = np.where(row > np.median(row) * DARK_EDGE)[0]
    y0, y1 = keep[0], keep[-1] + 1
    return a[y0:y1, x0:x1]


def deskew_angle(a: np.ndarray) -> float:
    """The rotation whose row-sum profile varies most — text lines line up with the rows."""
    g = np.asarray(Image.fromarray(a.astype("uint8")).convert("L").resize((900, 500)), dtype=float)
    mask = g > np.percentile(g, 88)                      # the text, not the background
    best, best_score = 0.0, -1.0
    for deg in np.arange(-3.0, 3.01, 0.25):
        rot = np.asarray(Image.fromarray((mask * 255).astype("uint8")).rotate(deg, resample=Image.BILINEAR))
        score = rot.mean(axis=1).var()
        if score > best_score:
            best, best_score = float(deg), score
    return best


def flatten(a: np.ndarray) -> np.ndarray:
    bg = np.asarray(Image.fromarray(a.astype("uint8")).filter(ImageFilter.GaussianBlur(BLUR)), dtype=float)
    flat = a / np.maximum(bg, 1.0)                       # illumination and colour cast both go
    flat /= np.percentile(flat, 99.5)                    # the text becomes the white point
    return np.clip(flat, 0, 1)


def levels(a: np.ndarray) -> np.ndarray:
    g = a.mean(axis=2)
    bg = np.percentile(g, 50)                            # the slide's own background
    hi = np.percentile(g, 99.5)
    out = (a - bg) * ((TEXT_LEVEL - BG_LEVEL) / max(hi - bg, 1e-6)) + BG_LEVEL
    return np.clip(out, 0, 1)


def main(src: Path, dst: Path) -> None:
    a = np.asarray(Image.open(src).convert("RGB"), dtype=float)
    a = crop_surround(a)
    deg = deskew_angle(a)
    if abs(deg) > 0.05:
        a = np.asarray(Image.fromarray(a.astype("uint8")).rotate(deg, resample=Image.BICUBIC, expand=False), dtype=float)
        m = int(abs(np.sin(np.deg2rad(deg))) * max(a.shape[:2])) + 2      # drop the rotation's blank wedges
        a = a[m:-m or None, m:-m or None]
    h0, w0 = a.shape[:2]
    dy, dx = int(h0 * INSET), int(w0 * INSET)
    a = a[dy:h0 - dy, dx:w0 - dx]
    a = levels(flatten(a))
    im = Image.fromarray((a * 255).round().astype("uint8"))
    w, h = im.size                                        # centre-crop to 16:9, then resize
    if w / h > OUT_W / OUT_H:
        new = int(h * OUT_W / OUT_H); im = im.crop(((w - new) // 2, 0, (w + new) // 2, h))
    else:
        new = int(w * OUT_H / OUT_W); im = im.crop((0, (h - new) // 2, w, (h + new) // 2))
    im.resize((OUT_W, OUT_H), Image.LANCZOS).save(dst, quality=90)
    print(f"{dst.name}: deskew {deg:+.2f}deg, {Image.open(dst).size}")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
