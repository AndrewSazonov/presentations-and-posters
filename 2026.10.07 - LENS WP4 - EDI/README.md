# talk — EasyDiffraction and crysta

LENS WP4, 7 October 2026. *Reusing crystallographic libraries, and building our own.*

reveal.js deck. `slides/*.html` are the sources; `index.html` is built from them by `build.py`.
The layout, styles and build are those of the DMSC crysta talk (`2026.09.07 - DMSC - Crysta`);
slides taken from the NOBUGS 2026 EasyScience talk and the 2024 J-PARC EasyDiffraction talk were
redrawn in that style.

## Working on it

```bash
pixi run watch     # rebuilds on save — edit a slide, save, refresh the browser tab
```

Open `index.html` straight from the file system; no server is needed. Without pixi, the same thing:
`python3 build.py --watch`, or `python3 build.py` once per change.

| task | what it does |
| --- | --- |
| `pixi run build` | build `index.html` once |
| `pixi run watch` | rebuild on every save |
| `pixi run serve` | rebuild on every save **and** serve <http://localhost:8000/> |

Open `index.html?check` to get one line per slide step whose content overflows the 1200×750 box.

## Layout

```
slides/     one file per section; each wraps its stacks in <div class="external-slide">
extra/      style.css + talk.css (from the crysta deck, unchanged), edi.css (this talk's additions),
            the icon sprite and the local fonts
images/     figures and screenshots
dist/       reveal.js and its themes
plugin/     reveal.js plugins
build.py    inlines slides/ into index.html, adds the outline dividers
```

Every step of a stack carries the elements later steps add, hidden, so items fade in where they
belong. Write each step with only what it shows; `build.py` inserts the rest. A stack that has to
re-lay out between steps opts out with `<section data-reserve="off">`.

Icons are written `<i class="fa-NAME"></i>` and expanded from `extra/icons-sprite.svg` (Font
Awesome 6 outlines); a name missing from the sprite stops the build.
