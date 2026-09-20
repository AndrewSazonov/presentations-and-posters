# GUI strategies at ESS

reveal.js deck for the NOBUGS 2026 GUI Workshop. Where the user interfaces are across the ESS data
pipeline, what they are built with, what is shared and what is not.

Six slides, one click apart. No section dividers, no running order, no animation.

| | |
| --- | --- |
| 1 | cover |
| 2 | The integrated data pipeline |
| 3 | UI technologies in a nutshell |
| 4 | Challenges, and the controls split |
| 5 | Reusable UI components |
| 6 | UI generation and AI assistants |

## Working on it

`index.html` is the deck. Open it in a browser and edit it — there is no build step.

```bash
python3 -m http.server 8013
```

Serving it is only needed for the embedded fonts: some browsers refuse to load a local `.ttf` over
`file://`, and the deck then falls back to Segoe UI and stops looking like ESS. Everything else
works straight off the file system.

Open `index.html?check` to get one line per slide whose content runs past the 1360×765 slide box,
listed at the foot of the page and outlined on screen. The deck should be clean; if a line appears,
that slide has grown past the frame.

`.claude/launch.json` starts the same server from the editor's preview pane.

## Layout

```
index.html      the whole deck: the icon sprite, then one <section> per slide
deck.css        the design system — type scale, colours, components
assets/fonts/   Titillium Web, ESS's identity typeface (SIL OFL)
assets/logos/   project marks used on the pipeline diagram and the cards
assets/shots/   application screenshots
vendor/         reveal.js 5.1.0 core, minified, plus the speaker-notes plugin
```

Every slide is one `<section>` wrapping one `<div class="sbody">`. `.sbody` is the layout box: a
fixed 765px flex column holding a `.titlebox` ranged from the top and a `.body` that fills whatever
is left. The title's blue rule is drawn in `.sbody`'s left padding, which is what puts the title of
every slide in the same place.

## The design system

The visual language is lifted from the *Same workflow, different techniques* deck, which follows
ESS's Visual Identity Manual: Titillium Web throughout, sentence-case titles ranged from one left
edge, and a blue rule beside the title. The layout — six dense slides, title block on top — is this
deck's own.

- **One type scale.** Five steps, declared in px at the top of `deck.css` (`--fs-title` … `--fs-xs`).
  If a component needs a size, it takes one of these.
- **One blue** (`--c-blue`) for every key phrase, chip and rule. `<em>` is the markup for a key
  phrase; it is set upright and blue, not italic.
- **Two greys, by job**: `--c-dim` explains, `--c-mute` labels.
- **Regular for text, Light for headings.** The manual allows either for body text and specifies
  Light for print; a projector is not print, so only `h3` keeps Light.
- **One accent per card.** A card sets `--accent` and everything in it follows: the technology line
  is set in it, that line's icon inherits it through `currentColor`, and the box's fill and border
  are 10% and 40% washes of it. The app name stays white — on a band of seven accents, seven names
  in seven colours would leave nothing to look at first.
- **Four muted hues** (`--h-blue`, `--h-purple`, `--h-teal`, `--h-amber`), one family at one
  brightness, shared by the pipeline's stages and the columns' pills.
- **A subhead, not a conclusion.** Each title carries one line saying what the slide is about, inside
  the same `.titlebox` so the rule spans both.
- **Two gaps inside a list and only two**: `--gap-pair` binds a line to its own explanation,
  `--gap-item` separates one item from the next. The bigger gap is what does the grouping.

The navigation diamond is laid out as a 3×3 grid with the slide number in the centre cell, and is
scaled with the deck — `index.html` publishes reveal's own scale factor as `--ctrl-scale`. It is
held at two-thirds strength because these slides fill the frame and it sits over them.
