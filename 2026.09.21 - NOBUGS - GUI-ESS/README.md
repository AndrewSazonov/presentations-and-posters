# GUI approaches at ESS

reveal.js deck for the NOBUGS 2026 GUI Workshop. Where the user interfaces are across the ESS data
pipeline, what they are built with, what is shared and what is not.

Seven slides behind an ESS holding screen. No section dividers, no running order.

| | | clicks |
| --- | --- | --- |
| | the ESS mark — a holding screen, unnumbered | |
| 1 | cover | 2 |
| 2 | One facility, two host countries | 1 |
| 3 | The integrated data pipeline | 6 |
| 4 | UI technologies in a nutshell | 7 |
| 5 | Challenges and controls | 3 |
| 6 | Reusable UI components | 4 |
| 7 | UI generation and AI assistants | 3 |

## Driving it

**Left and right move between slides. Up and down move through the boxes on a slide.** Space does
both — it is what a presentation remote sends, and it walks the whole deck from the first click to
the last. None of that is configured: a step is a vertical slide, so these are reveal's own keys
doing their own job, and the diamond in the corner follows without being told.

Every content slide opens as a **title card** — the title alone in the middle of an empty frame —
and the first click carries it up to where it lives and brings the first box with it. The cover
builds the other way, upwards: the event line is already there when it arrives, then the speaker,
then the title, each one pushing what is there down to make room.

## How a step works

Each step is its own `<section>`, and reveal's **auto-animate** measures the difference between one
and the next and tweens it — half a second on `cubic-bezier(0.770, 0, 0.175, 1)`, the reference
deck's own numbers. That tween is the whole point: it is what gives the move its acceleration, and
a hand-written CSS transition cannot imitate it. Two earlier attempts here did try, and both read
as wrong — one stalled and then lurched, the other glided at a flat speed.

The reference deck writes every step of every slide out in full, which is why its `index.html` is
336KB of near-duplicates. This deck keeps **one copy of the markup** and builds the duplicates at
load: a box carries `data-step="3"`, and `buildSteps()` in `index.html` turns the slide into a stack
of sections where step *k* holds everything up to *k* and everything later carries `hid`. So the
source stays one slide per slide, and reveal still gets the two DOM states it needs.

A box waiting its turn keeps its place in the layout and only its ink is missing, so nothing moves
when it arrives — the slide is built, not rearranged. The cover is the exception: there a line not
yet reached takes **no height**, so the stack grows and pushes what is already there down, and
auto-animate — pairing a line of no height with a full one — opens it out rather than fading it in.
It keeps its *width* throughout, which is what holds that shrink-wrapped block still: left out of
the markup instead, the block was only as wide as its widest visible line, so it re-centred and
everything slid sideways each time a longer line arrived.

### What auto-animate is allowed to touch

This is the part that is easy to get wrong, and it took three wrong answers to get right. Reveal
writes every pair it finds **a transform of its own**, and a transform nests: pair a box and the
paragraph inside it and the paragraph gets both, so it starts twice as far away as its box and races
it home. Left to itself reveal pairs headings, paragraphs and list items too — it matches them by
their text — so a slide moving 290px had card text starting 1158px below the frame, four levels
down. It also fades in anything it *cannot* pair, on every click, whether or not that thing is
already on screen, which is what made the boxes flicker.

So the deck supplies its own `autoAnimateMatcher`. It pairs **the direct children of `.sbody` and
nothing else** — on a content slide that is the title block and the body, on the cover it is the
four lines. They are siblings, so no pair sits inside another, nothing compounds, and each carries
its whole subtree in one piece. Scale is allowed only on the cover, and only going
forward. A change of height *is* the cover's effect; on a content slide the block's height changes
merely because a box arrived inside it, and scaling there stretches the whole block open instead of
moving it. Backwards it is wrong even on the cover — the tween that opens a line out, run in
reverse, squashes the title flat on its way out, which is not the reverse of an entrance but a
different and worse animation. Stepping back, a line keeps its size and simply fades. The
matcher returns nothing at all when the two sections belong to different slides: pairing across
slides made an arriving title animate *down* into the middle of the frame before it could come up.
It also skips anything with no box to measure — the speaker notes are `display: none`, and dividing
by a height of zero hands auto-animate a `scale(NaN, NaN)`.

With `autoAnimateUnmatched: false` nothing is faded for want of a pair. The box a click brings in
carries its own fade instead — `buildSteps()` marks it `arriving` and deck.css gives that class a
keyframe animation. The rule is hung off the step's own `present`, not off `.arriving` alone: reveal
keeps the steps either side of the current one rendered so it can transition to them, so an
animation written on the class alone has already played, off screen, long before the click. The
cover needs none of this — its lines are paired, and auto-animate opens them out and fades them in
the same movement.

## Working on it

`index.html` is the deck. Open it in a browser and edit it — there is no build step; the per-step
sections are made in the browser at load.

```bash
python3 -m http.server 8013
```

Serving it is a convenience, not a requirement: `index.html` opens straight off the file system and
looks the same. It used to matter, because the typeface was fetched from `assets/fonts/` and some
browsers refuse a local `.ttf` over `file://` — the deck then came up in the system sans. The faces
are now carried inside `deck.css` as base64, so there is no request to refuse, and no moment where
the text is painted in one face and re-set in another. `assets/fonts/` still holds the originals;
they are the source and the stylesheet holds the copies.

Open `index.html?check` to get one line per slide whose content runs past the 1360×765 slide box,
listed at the foot of the page and outlined on screen. The deck should be clean; if a line appears,
that slide has grown past the frame. The check puts the deck in its END state first — every box
revealed, no title card — since a slide holding one title always fits.

`.claude/launch.json` starts the same server from the editor's preview pane.

## The PDF

```bash
./make-pdf.sh
```

Seven pages, one per slide, each one whole. decktape drives a headless Chromium and photographs
what reveal draws, so the near-black ground, the card washes and the SVG pipeline survive; a
browser's own print dialog does not work, because reveal switches to its print stylesheet and drops
the backgrounds. `index.html?pdf` is the deck's own flag for this: `buildSteps()` returns early, so
no slide is split into steps, nothing is hidden and nothing opens as a title card. It is
deliberately not called `print-pdf` — reveal watches the query string for that one.

## Layout

```
index.html      the whole deck: the icon sprite, then one <section> per slide
deck.css        the design system — type scale, colours, components
assets/fonts/   Titillium Web, ESS's identity typeface (SIL OFL) — the source of the embedded copies
assets/logos/   project marks used on the pipeline diagram and the cards
assets/maps/    the Oresund map, recoloured into the deck's ground
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
- **One box per click**, and the title card that opens every slide — see *How a step works*.
- **Two gaps inside a list and only two**: `--gap-pair` binds a line to its own explanation,
  `--gap-item` separates one item from the next. The bigger gap is what does the grouping.

The navigation diamond is laid out as a 3×3 grid with the slide number in the centre cell, and is
scaled with the deck — `index.html` publishes reveal's own scale factor as `--ctrl-scale`. It is
held at two-thirds strength because these slides fill the frame and it sits over them. It holds one
position for the whole deck, at the height the title sits and with its right tip on the deck's own
right margin; `index.html` measures both, because the controls live outside the slide and are
offset from the window rather than from the stage.
