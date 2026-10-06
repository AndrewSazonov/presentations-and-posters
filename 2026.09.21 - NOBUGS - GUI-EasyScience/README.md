# talk — Same workflow, different techniques

reveal.js deck for the NOBUGS 2026 GUI Workshop, session 3 (UX Theory). `slides/*.html` are the
sources; `index.html` is built from them by `build.py`. `outline.md` holds the running order, the
source-to-slide reuse map and the list of things still to confirm.

## Working on it

```bash
pixi run watch     # rebuilds on save — edit a slide, save, refresh the browser tab
```

Open `index.html` straight from the file system; no server is needed. Leave `pixi run watch` running
in a terminal and it rebuilds whenever you save a slide or the stylesheet.

Without pixi, the same thing: `python3 build.py --watch`, or `python3 build.py` once per change.

| task | what it does |
| --- | --- |
| `pixi run build` | build `index.html` and `backup.html` once |
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
extra/      talk.css, style.css, the icon sprite and the local fonts
images/     screenshots and diagrams
dist/       reveal.js and its themes
plugin/     reveal.js plugins
build.py    inlines slides/ into index.html and backup.html
outline.md  running order, reuse map, open questions
```

The backup slides (`slides/90_appendix.html`) build into their own deck, `backup.html`. They are
never presented in sequence — only opened when a question needs them — so each one is its own
stack rather than a step of a neighbour.

## Where the material came from

Screenshots and diagrams are reused from earlier EasyScience decks and from the 2026 IUCr poster;
`outline.md` maps each slide to its source. The UX theory on slides 15–16 is Design Psychology's
*UX Expert Review* method, credited on the slides themselves.
