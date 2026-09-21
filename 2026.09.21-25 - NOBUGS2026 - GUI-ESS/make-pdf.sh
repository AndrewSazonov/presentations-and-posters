#!/usr/bin/env bash
# Export the deck to PDF, one page per slide, drawn the way the browser draws it.
#
# decktape drives a real headless Chromium and photographs what reveal renders on screen, so the
# PDF keeps the near-black ground, Titillium, the SVG pipeline and the cards' washes. Printing from
# a browser's own print dialog does not: reveal switches to its print stylesheet, which drops the
# backgrounds and reflows the slides.
#
# `?pdf` is the deck's own flag: it leaves every slide whole rather than building it into a stack of
# steps, so decktape finds seven slides and prints seven pages instead of one page per click.
# The size is the stage's own 1360x765. reveal's 8% margin is kept, so a page is the slide with the
# same band round it that the screen shows.
set -euo pipefail
cd "$(dirname "$0")"
npx -y decktape@3 reveal --size 1360x765 --slides 1-999 "file://$PWD/index.html?pdf" "$PWD/GUI-approaches-at-ESS.pdf"
