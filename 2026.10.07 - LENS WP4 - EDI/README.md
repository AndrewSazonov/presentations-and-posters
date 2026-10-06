# talk — EasyDiffraction and crysta

*Reusing crystallographic libraries, and building our own.* LENS WG4, 7 October 2026.

reveal.js deck. `slides/*.html` are the sources; `index.html` is built from them by `build.py`.
The deck is a copy of the NOBUGS 2026 talk `2026.09.21 - NOBUGS - GUI-EasyScience` — its build,
layout, type scale and style — with slides from the DMSC crysta talk (`2026.09.07 - DMSC - Crysta`)
and the J-PARC EasyDiffraction talk (`2024.09.18 - J-PARC - EasyDiffraction`) redrawn in that style.
`extra/edi.css` holds this talk's additions, on `talk.css`'s variables only.

## Working on it

```bash
pixi run watch     # rebuilds on save — edit a slide, save, refresh the browser tab
```

Open `index.html` straight from the file system; no server is needed. Leave `pixi run watch` running
in a terminal and it rebuilds whenever you save a slide or the stylesheet.

Without pixi, the same thing: `python3 build.py --watch`, or `python3 build.py` once per change.

| task | what it does |
| --- | --- |
| `pixi run build` | build `index.html` once |
| `pixi run watch` | rebuild on every save |
| `pixi run serve` | rebuild on every save **and** serve <http://localhost:8000/> |

`serve` is for the cases `file://` cannot handle — viewing from a phone or another machine, or a
browser that refuses local fonts over `file://`.

Open `index.html?check` to get one line per slide step whose content overflows the 1200×750 slide
box. The deck should be clean; if a line appears, the step has grown past the frame.

## Why there is a build step at all

The browser cannot assemble the deck itself. Pulling `slides/*.html` in at run time means `fetch()`
on `file://`, which every browser blocks as a cross-origin read, so the slides have to be inlined
into one file beforehand. `build.py` does that, in the order listed in its `ORDER` list, and emits
a section-divider slide for each entry in `SECTION_TITLES`.

`build.py` also gives every step of a stack the space of the steps that follow it, so an item fades
in where it already belonged instead of the block re-centring on each click. Write each step with
only what it shows; the build inserts the rest, hidden. Write an element explicitly with `class="hid"`
only when it must be present *and* invisible in that step — a screenshot in a `.shotbox`, say.

## Layout

```
slides/     one file per section; each wraps its stacks in <div class="external-slide">
            10_why · 20_easydiffraction · 30_crysta · 40_outlook
extra/      talk.css, style.css (from the NOBUGS deck), edi.css (this talk), the icon sprite, fonts
images/     screenshots and diagrams
dist/       reveal.js and its themes
plugin/     reveal.js plugins
build.py    inlines slides/ into index.html
```

There is no backup deck for this talk.

A block marked `data-cascade` is hidden item by item, so a list of names can arrive one after
another (each name with its own `data-auto-animate-delay`).

## Where the material came from

- NOBUGS 2026 EasyScience talk: the cover, many tools, what users run into, what we rely on, the
  design evolution, the expert review, three ways to run the workflow, same screen, what became
  reusable, where EasyScience runs.
- J-PARC 2024 EasyDiffraction talk: the names arriving one by one, site susceptibility and 2D
  Rietveld, needs, the libraries-based approach, future plans, the project-page pan.
- DMSC crysta talk: what analysis needs, AI in scientific software, the pilot project, the test
  case, both agreement slides, speed, 'I did not write this code', the checks, credits, how much is
  done. Numbers there come from `enhantica/bench`.

## Still to do

- Partner logos on "Where EasyScience runs today": the chips are text until
  `images/logo-mlz-jcns.svg`, `images/logo-goettingen.svg` and `images/logo-shapespyre.svg` exist
  (each chip's `data-logo` names its file).
