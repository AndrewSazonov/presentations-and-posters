#!/usr/bin/env python3
"""Cut a picture into jigsaw pieces and take some of them out.

The "to fill the gaps" slide wants a puzzle whose picture is scientific, and no such photograph
exists under a free licence — so the deck makes one. Pieces are square cells with a round tab on
each inner edge, given to one side or the other by parity, which is enough for the eye to read
"jigsaw"; the pieces listed in MISSING are simply not drawn.

    python3 tools/make-puzzle-image.py <source> <target>
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance

OUT_W, OUT_H = 1600, 900
COLS, ROWS = 8, 5
BACKGROUND = (26, 26, 26)          # the deck's own background, so the gaps read as holes
GAP = 3                            # the dark line between two pieces
MISSING = {(0, 0), (3, 0), (7, 0), (6, 1), (4, 3), (7, 3), (1, 4)}   # spread over the board, clear of the face


def piece_mask(size, cw, ch):
    """One mask per piece is slow; draw them all into a single mask instead."""
    mask = Image.new("L", size, 0)
    d = ImageDraw.Draw(mask)
    tab = min(cw, ch) * 0.17
    for r in range(ROWS):
        for c in range(COLS):
            if (c, r) in MISSING:
                continue
            x0, y0 = c * cw + GAP / 2, r * ch + GAP / 2
            x1, y1 = (c + 1) * cw - GAP / 2, (r + 1) * ch - GAP / 2
            d.rounded_rectangle([x0, y0, x1, y1], radius=min(cw, ch) * 0.12, fill=255)
            for edge, (cx, cy, out) in {
                "right":  ((c + 1) * cw, (r + 0.5) * ch, (c + r) % 2 == 0),
                "left":   (c * cw,       (r + 0.5) * ch, (c + r) % 2 == 1),
                "bottom": ((c + 0.5) * cw, (r + 1) * ch, (c + r) % 2 == 1),
                "top":    ((c + 0.5) * cw, r * ch,       (c + r) % 2 == 0),
            }.items():
                on_border = ((edge == "right" and c == COLS - 1) or (edge == "left" and c == 0)
                             or (edge == "bottom" and r == ROWS - 1) or (edge == "top" and r == 0))
                if on_border or not out:
                    continue
                d.ellipse([cx - tab, cy - tab, cx + tab, cy + tab], fill=255)
    return mask


def main(src: Path, dst: Path) -> None:
    im = Image.open(src).convert("RGB")
    w, h = im.size                                        # centre-crop to the deck's 16:9
    if w / h > OUT_W / OUT_H:
        new = int(h * OUT_W / OUT_H); im = im.crop(((w - new) // 2, 0, (w + new) // 2, h))
    else:
        new = int(w * OUT_H / OUT_W); im = im.crop((0, (h - new) // 2, w, (h + new) // 2))
    im = im.resize((OUT_W, OUT_H), Image.LANCZOS)
    im = ImageEnhance.Contrast(im).enhance(1.25)      # a projected plate needs the extra bite
    im = ImageEnhance.Brightness(im).enhance(1.06)
    out = Image.new("RGB", (OUT_W, OUT_H), BACKGROUND)
    out.paste(im, (0, 0), piece_mask((OUT_W, OUT_H), OUT_W / COLS, OUT_H / ROWS))
    out.save(dst, quality=90)
    print(f"{dst.name}: {COLS}x{ROWS} pieces, {len(MISSING)} missing")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
