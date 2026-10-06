#!/usr/bin/env bash
# Export the decks to PDF exactly as the browser draws them.
#
# decktape drives a real headless Chromium through reveal's own navigation and prints one page per
# step, so the PDF keeps the black background, the fonts, the SVG diagrams and every stack's click
# sequence. Printing from a browser's own print dialog does not: it applies reveal's print
# stylesheet, drops the backgrounds and reflows the slides.
set -euo pipefail
cd "$(dirname "$0")"
python3 build.py
for deck in index backup; do
  [ -f "$deck.html" ] || continue
  out="talk.pdf"; [ "$deck" = backup ] && out="backup.pdf"
  npx -y decktape@3 reveal --size 1200x750 --slides 1-999 "file://$PWD/$deck.html" "$PWD/$out"
done
