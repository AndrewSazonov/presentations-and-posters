# Talk outline — Same workflow, different techniques (draft 02, 2026-09-15)

NOBUGS 2026 · GUI Workshop, Session 3 "UX Theory" · **20 minutes including a short demo.**
Budget: ~15 min slides · 4–5 min demo · 1 min close.
One idea per slide · progressive disclosure via auto-animate steps · the demo is the proof, the
slides are the argument.

## Title and description, as sent to the organiser

**Same workflow, different techniques**
*From a diffraction prototype to a reusable EasyScience GUI*

Long description (~145 words):

> Scientific data-analysis software is usually built one technique at a time, and each new
> application starts its interface from an empty window. EasyScience, initiated at the European
> Spallation Source, took another route. A graphical interface prototyped for neutron diffraction
> analysis in 2019 was simplified through several design iterations and an external UX expert
> review, then extracted into a Qt/QML module now shared by applications for reflectometry,
> imaging, quasielastic scattering and more.
>
> This talk is about the reasoning behind that interface rather than its architecture: a linear
> workflow that doubles as the navigation bar, a screen anatomy with a fixed reading order,
> progressive disclosure across basic, advanced and scripted entry points, and the decision to
> design the workflow before any analysis code was connected. It closes with a short demonstration
> of the same journey in two technique-specific applications, naming what is shared and what is not.

Short description (~78 words), if the programme has a tight limit:

> A graphical interface prototyped for neutron diffraction analysis in 2019 became, after several
> design iterations and an external UX expert review, a module now shared by applications for
> reflectometry, imaging and quasielastic scattering. This talk covers the UX reasoning behind it —
> a linear workflow that doubles as the navigation bar, a fixed screen anatomy, progressive
> disclosure, and three entry points sharing one mental model — and ends with a short demonstration
> of the same journey in two techniques.

Both descriptions open with the word *analysis* on purpose: at NOBUGS the unmarked "GUI" is an
instrument-control GUI, and neither half of the title rules that reading out.

Order: the problem → how the design got there → why it works (UX theory) → what became reusable →
demo → close.

| # | steps | slide | section |
|---|---|---|---|
| 0 | 1 | ESS divider | — |
| 1 | 3 | Same workflow, different techniques | — |
| 2 | 6 | Outline — the whole plan, then → The problem | — |
| 3 | 6 | Where analysis sits | The problem |
| 4 | 4 | One step, many tools | The problem |
| 5 | 5 | How an interface gets in the way | The problem |
| 6 | 5 | … and then you do it again | The problem |
| 7 | 1 | Outline → Design evolution | — |
| 8 | 1 | *epigraph* — Saint-Exupéry, “nothing left to take away” | Design evolution |
| 9 | 6 | Several years of taking things away | Design evolution |
| 10 | 4 | Then we asked the experts | Design evolution |
| 11 | 4 | The interface came before the science | Design evolution |
| 12 | 1 | Outline → UX principles | — |
| 13 | 4 | Seeing beats reading | UX principles |
| 14 | 7 | One path through the data | UX principles |
| 15 | 7 | One screen, four zones | UX principles |
| 16 | 5 | The squint test | UX principles |
| 17 | 5 | Show what is needed, when it is needed | UX principles |
| 18 | 5 | Three ways in, one mental model | UX principles |
| 19 | 1 | Outline → Reuse | — |
| 20 | 4 | Same screen, different technique | Reuse |
| 21 | 6 | What became reusable | Reuse |
| 22 | 5 | Where it runs today | Reuse |
| 23 | 5 | What reuse buys | Reuse |
| 24 | 1 | Outline → Demo | — |
| 25 | 3 | One real refinement | Demo |

**26 slides, 105 steps.** Rehearse before trimming — if it runs long, cut slide 14 first
(*One path through the data*): the demo covers the same ground, and the stack only exists so the
argument still lands if the live application is unavailable.

Backup (`backup.html`, 14 slides, never presented in sequence): why Qt and QML · the UX Expert
Review's three phases · its three toolboxes · the review reply in full · every tab is a file you
can read · the diffraction software landscape · Jana on Windows only · a FullProf PCR file ·
what else is shared (ADRs, Copier, Ruff, CI/CD, MkDocs) · EasyTexture, built outside ESS ·
the workflow stated abstractly · in one sentence · thank you (all cut from the main deck).

## Source-to-slide reuse map

| slide | source | what is reused |
|---|---|---|
| 4 Where analysis sits | `tmp/01 data_processing_workflow` | pipeline figures, NICOS / Scipp / EasyDiffraction attribution |
| 5 One step, many tools | `tmp/01 existing_software` | the programs and libraries lists, as two panels |
| 6 How an interface gets in the way | `tmp/01 existing_issues` | FullProf window, PCR file, XQuartz screenshots |
| 7 … and then you do it again | `tmp/11` p.10 "Maintainability" | one-man projects, no modularity — reframed as a UX cost |
| 14 One path through the data | `tmp/01 linear_workflow` | the five tab screenshots of the current application |
| 9 Several years of taking away | `tmp/01 gui_design_evolution`, `tmp/11` p.21–24 | the 2019 / 2020 / 2021 mock-ups + today's screenshot from the IUCr poster; 2023 and today share a click, so `ed-design-2023.png` is no longer used |
| 10 Then we asked the experts | designpsykologi.dk, `tmp/11` p.25 | their own page, then their reply |
| 11 Interface before the science | the brief ("prototyped before all analysis logic is connected") | new slide, built as a contrast of two orders |
| 13 Seeing beats reading | `tmp/20230116_UX_Expert_Review_Manual` p.6–8, `tmp/12` s.15 | Levels-of-Cognition model, reduced to two bands in plain words |
| 16 The squint test | `tmp/12` s.16–17, UX manual p.15 (blur filter) | the method, applied to our own screens with a CSS blur |
| 15 One screen, four zones | `tmp/11` p.14–20 "Intuitive user interface" | the region-by-region dissection and the reading-order arrows |
| 18 Show what is needed | UX manual p.17, current app (Basic / Advanced / Text mode) | the principle and where it shows in the app |
| 19 Three ways in | `tmp/05 Different user groups`, `tmp/11` p.26–28, IUCr poster | basic GUI / advanced GUI / Jupyter |
| 21 Same screen, different technique | IUCr poster (EasyDiffraction + EasyReflectometry captures) | side-by-side |
| 22 What became reusable | `tmp/01 modular_structure` | the layered diagram, redrawn with current module names |
| 23 Where it runs today | IUCr poster, "Domain-Specific Projects" | the project inventory and its status |
| 24 What reuse buys | IUCr poster, "Reusable Components" / "Consistent Look and Feel" | the argument |
| 25 Demo | the brief; `tmp/01 images/live-demo.png` | the demo intent, and the fallback joke |
| backup | `tmp/01 common_project_management`, `tmp/05 Human-readable in/out`, UX manual p.9–17 | shared tooling, CIF project files, the review method |

Deliberately left out of the draft: the DMSC / ESS org slides, the libraries-based-approach stack,
the performance and minimiser-engine material, the collaboration map, the organisation page. All of
it is in `tmp/01–10` if a question needs it — none of it is about the interface.

## Still to fill / to confirm before this is presentable

1. **Design iteration years (slide 11).** The slide says 2019 · 2020 · 2021 · 2023–today,
   following `tmp/01 gui_design_evolution`. The 2022 ISIS deck labels the same pictures
   2019 / 2021 / 2022. Which is right?
2. **Tab names.** The deck uses the current application's names — Project · Model · Experiment ·
   Analysis · Summary. The brief says "Project, Sample Model, Experiment, Analysis, Summary".
   Confirm which to present, and when "Sample" became "Model".
3. **Module naming (slide 22).** The slide calls the frontend module `easyapplication`, and the
   speaker note says it started inside EasyDiffraction, became `EasyApp` and now lives in
   `gui-components`. Confirm the current name, the repository and when the split happened.
4. **Application status (slide 23).** Which of EasyDynamics, EasyImaging and EasyShapes already
   run on the shared GUI components, and which are still being built? The brief explicitly warns
   against claiming equal maturity. The draft marks EasyDiffraction and EasyReflectometry as
   *running*, the three others as *new*, EasyTexture as *external*. The title no longer depends on
   this — "different techniques" makes no count claim, unlike the "many techniques" draft — but the
   slide is still the one place a Q&A question will go, so the labels need to be right.
5. **Design Psychology engagement (slide 10).** Dates and format of the two workshops at DMSC, and
   whether Rune Nørager's 2021 e-mail may be shown on a slide. If not, the slide works with their
   own page and no quotation.
   The screenshot is `images/designpsykologi.png`, the Design Psychology home page — its nav shows
   "UX Design Review", the method being cited. `images/ux-expert-email.png` still carries the orange
   "UI/UX experts approved!" banner, which the slide's own conclusion now says: re-capture it
   without the banner.
6. **Attribution for the UX theory (slides 13 and 16).** The material comes from the Design Psychology
   *UX Expert Review* manual and from Matt Clarke's talk *Improving User Experience in Complex
   Systems*. Slide 14 credits Design Psychology on screen; slide 15's credit was moved into the
   speaker notes, so the blur filter and Matt Clarke are now credited **out loud only** — check that
   is acceptable to both, and get the reference for Matt's talk (venue and year).
7. **Live Preview.** No longer on a slide — it is in the speaker notes for *The interface came
   before the science*, with QML and the frontend/backend boundary. The brief called it optional
   supporting evidence; confirm that saying it rather than showing it is enough.
8. **Screenshot refresh.** `ed-analysis-2026.png`, `er-analysis-2026.png` and `jupyter-2026.png`
   were extracted from the IUCr poster PDF. Two weak spots: `er-analysis-2026.png` still shows the
   older "Sample" tab (slide 21), and `ed-advanced.png` on slide 19 is from the 2023 design, so the
   three panels there do not look like one family.
9. **Title slide event line.** Add "NOBUGS 2026 · GUI Workshop" once the date and venue are fixed.
10. **Demo length.** The brief suggests three or four minutes; you said five. Five leaves ~14 min for
    84 steps — doable, but slide 10 is the first thing to cut if the rehearsal runs over.
11. **Demo rehearsal.** The demo slide names only the journey; the detail is in its speaker
    notes. Record the fallback screencast.
12. **The deck no longer carries a URL.** *In one sentence* and *Thank you* moved to the backup
    deck, so easyscience.org and github.com/easyscience appear nowhere in the main sequence and the
    talk now ends on the ESS mark straight after the demo. Decide: bring *Thank you* back, put the
    links on the demo slide, or accept that the abstract carries them.

## House rules for the slides

Established while making the deck consistent; keep to them when editing.

- **One gap sets the rhythm.** `--gap` is the space under the title AND above the conclusion — one
  variable, so they cannot drift apart. Each rule subtracts its own half-leading, since a line box
  is taller than its glyphs and a raw margin therefore looks larger under bigger text. `h3 + *`
  zeroes the top margin of whatever follows the title, so nothing else competes for that space.
- **Uppercase tracking falls as the size rises.** The need for letter-spacing shrinks as letters
  grow, while an `em` value grows with them — so a 32px uppercase line takes a quarter of what a
  20px label needs. The 20px labels share `--track-label`; the outline rows are set separately.
- **Three greys, by job**, declared with the scale in `extra/talk.css`: `--c-dim` for the
  explanatory line under something, `--c-mute` for the chapter line and credits, `--c-off` for
  something switched off. Do not introduce a fourth.
- **One type scale, five steps.** Every size is one of `--fs-title / --fs-xl / --fs-lg / --fs-md /
  --fs-sm`, declared at the top of `extra/talk.css` in px. Never write a raw `em` size: `em`
  compounds through nesting, which is how this deck once ended up with 42 distinct sizes.
- **`.statement` means one thing:** the conclusion, revealed on the last click. A line that OPENS
  a slide is `.leadin` (--fs-lg); a picture column's heading is `.colcap`; a caption that rotates
  with the steps is `p.step.sub`.
- **Two gaps inside a list, and only two.** `--gap-pair` (6px) holds a line to the dimmer line
  explaining it — together they are ONE item; `--gap-item` (22px) holds that item off the next one.
  The bigger gap is what does the grouping, so it has to be several times the smaller: they were
  once 2.5px and 7px, and six lines read as one block instead of three pairs. Every variant of the
  pattern (`.step`, `.why-col`, `.pstep`, `.twoshots`, `.reflib`) uses these two variables; none of
  them sets its own `em` value, which is how five different gaps happened.
- **A picture's description looks the same everywhere:** one line, `--fs-sm`, `--c-mute`, weight
  200, key words in blue, above the picture. `p.step.sub`, `.squint figcaption`, `.why-col .colcap`
  and `.twoshots figcaption` all take it from one rule. A two-part description names the picture on
  the FIRST line and describes it on the second — `<span class="blue">Everything at once</span>many
  windows and controls, no order` — with no dash between them: the `.blue` span is `display: block`
  inside a column, so the break is the separator. Both lines are the same size, weight and grey; a
  big white line with a small grey one under it is the old form and does not belong here.
- **One blue, `--c-blue`.** `rgb(109, 209, 255)`, declared once with the type scale and used for
  every key phrase, the active chip, the module names, the conclusion box's tint and the title rule.
  It was a literal in a dozen places, which is how a second blue gets in; `.tag-blue` had already
  drifted to `#489ac0` in `extra/style.css`. If you add an accent, take it from the token.
- **One rule beside the title block.** `build.py`'s `wrap_titles()` puts the chapter line and the
  `<h3>` in a `.titlebox`, which shrink-wraps the title (`width: fit-content`, centred); its
  `::before` sits `--rule-gap` (24px — two spaces of the title font, which sets one at 12.1px at
  55px) to the left of it, `--rule` wide (4px: Titillium Light at 55px sets a stem 3px solid, 5px
  counting the antialiased edges, and a CSS rule has no antialiasing of its own). Because the box
  hugs the title, the rule keeps the same distance from it on every slide instead of sitting on the
  slide's edge. The box also carries the `--gap` below the title, since a flex item does not let its
  child's margin collapse out and the rule would otherwise run a whole gap too far down. A cover
  (`.deck-title`) is a title slide rather than a slide with a title, so it is skipped and keeps its
  own spacing.
- **A lone screenshot is sized per slide, on the slide.** `style="--shot-h: 540px"` on the
  `.shotbox`; how much room is left depends on what else is above it (a picture description, a tab
  strip) and how wide the picture comes out depends on its own proportions at that height. Raise the
  number to make that slide's picture wider; the extra height is cut by the bottom edge. Today:
  540px / 540px / 482px / 573px, each cutting 5px off the bottom, with `--shot-w` beside it so the
  box has a width the layout can see.
- **The block is centred vertically too, with `justify-content: safe center`.** `--pad-bot` (76px)
  is deliberately larger than `--pad-top` (44px), so a block settles a little ABOVE true centre,
  where the eye reads centre. `safe` is what makes it usable: it falls back to flex-start the moment
  the content is taller than the frame, which is what a screenshot bled past the bottom edge is —
  plain `center` pushes those slides' titles up by half the overflow. The title now sits at 44px on
  the picture slides and down to 160px on the shortest text slides, a 116px swing; that is the cost
  of balancing each slide, and it is what the old 620px floor was there to prevent.
- **The content block shrink-wraps the slide and is centred in it.** `width: fit-content;
  max-width: 100%; margin: 0 auto`. The picture is sized first (`--shot-h`, for a 5px cut) and the
  block is laid out around it, which is why `.shotbox` also carries `--shot-w`: an absolutely
  positioned picture has no width of its own for the block to measure. Blocks run from 831px to
  1200px, so the left edge moves from slide to slide — that is the price of balancing each slide,
  and it is deliberate. The stage itself is always centred: at 1862x982 it is 1571px wide with 145px
  of background on each side, identically on every slide.
- **The height is fixed, not flexed, and `.sbody` is `height: 750px`, not `min-height`.** A box
  that grows and shrinks with the free space gets matched by auto-animate and given a vertical-only
  scale, which stretches the picture inside it — it appeared 24% too tall for a moment and settled.
  And a picture bled past the bottom GREW the `.sbody`, which reveal then centred, creeping the
  whole slide upwards by half the bleed.
- **The conclusion fades over `data-auto-animate-duration="1.1"`**, against the deck's 0.5s, and
  sits in `--gap-close` (28px) rather than `--gap` (48px) — it belongs to the title block rather
  than closing the slide.
- **Two elements on the same click can animate differently.** Three levers: pin `transform: none`
  to leave an element only its opacity transition (`.statement` does this — it fades where it
  belongs while the picture moves); `data-auto-animate-delay`, `-duration` and `-easing` on the
  element for a different rhythm; and leaving an element unmatched, which reveal fades rather than
  moves. Watch for a matched element whose other copy is `display: none`: its box is 0x0 at the
  origin, so auto-animate carries it in from off the slide — the conclusion was arriving from 876px
  above and 28px to the left before the pin.
- **The cover is a normal slide, not a `freeform` one.** It gets the block, the left edge and the
  blue rule for free, and `build.py` skips its title card because a cover is already a title on an
  empty screen. Its `.titlebox` is written by hand and holds the title AND the subtitle, so the rule
  spans both — the same unit the rule marks everywhere else. `wrap_titles()` leaves that `<h3>` alone
  because it carries `deck-title`, which is also what the two freeform covers use.
- **`?check` walks with `transition: 'none'` as well as auto-animate off.** Both tween a transform,
  and the horizontal slide-in left the first slide of a stack measured while it was still off to the
  side — that was the standing `#/1/0 h-overflow` line, an artefact rather than a defect.
- **No progress bar; the slide number lives in the arrows.** `progress: false`, and `slideNumber`
  is a function returning `[h+1, '/', total]` — an ARRAY, because reveal spreads it into
  `formatNumber(a, delimiter, b)` and a plain string comes back as its first character. It counts
  SLIDES, not clicks: a stack is one slide to the room however many times you press the button.
  reveal's own diamond leaves 28px between the left and right arrows and "10/27" needs 55, so the
  diamond is widened to 60px and the number is centred in it, in the chapter line's grey.
- **A bleed needs `margin: 0` in Reveal.initialize.** reveal insets the whole stage by 4% of the
  viewport by default, so a picture bled to the slide's bottom edge still had a band of background
  under it — about 40px on a 1000px-tall window. With `margin: 0` the stage reaches the window edge
  on whichever axis constrains it. A window TALLER than 1200:750 still letterboxes, and there the
  bleed correctly reaches the slide's edge rather than the window's.
- **Only a slide's TOP-LEVEL blocks move; everything inside is carried.** reveal pairs elements
  independently at every depth — by `data-id`, by a heading's text, by an image's `src` — and each
  match gets its own translate, so a matched child inside a matched parent moves twice. The title
  started 284px too low; the screenshot moved 105px with its box and 105px again by itself and
  jumped to the top of the slide before sliding down; `.squint` has four such levels.
  `.sbody > * *[data-auto-animate-target] { transform: none }` settles all of it. Keyed on the
  attribute reveal puts on what it is animating: a blanket `.sbody > * *` also killed the artwork
  transform inside the ESS logo's `<svg>` and the mark came apart.
  The other half of the rule: a top-level block needs a `data-id` of its own, or it is unmatched and
  lands instead of moving while its pinned children cannot move either. `.pipeline`, `.columns`,
  `.dolist` and `.ways` were missing one.
- **The conclusion reserves its WIDTH but not its HEIGHT.** `.statement.hid { height: 0; margin: 0;
  overflow: hidden }`, so until the last click the picture sits higher and revealing it pushes the
  picture down onto the bleed line rather than fading into a gap that has been sitting empty. It was
  `display: none`, which also took its width out — and since the block shrink-wraps the slide, a
  conclusion wider than the list above it made the block grow on the last click and the whole slide
  shifted left.
- **Never size a picture container in per cent.** The block shrink-wraps the slide, and a
  percentage width contributes NOTHING to that measurement while the screenshot inside still
  contributes its own natural width — so the block blew out to the full slide and there was nothing
  left to centre. `.zonebox` and `svg.modular` were the two; both carry px now.
- **A picture's box is exactly as big as the picture renders in it.** `contain` centres a picture in
  a box that is too tall and the slack reads as a gap under its description. The squint slots were
  391x380 around a 243-tall picture — 137px of empty box each; `.ways-image` had 73px and
  `.twoshots` 34px. Work out the height from the width and the aspect, and widen the container first
  if you want the picture larger: these are all width-limited.
- **A box that holds text you are still editing needs a definite width too.** The block shrink-wraps
  the slide, so with `width: 100%` the panels sized themselves to their own longest line: shortening
  one explanation narrowed the whole panel and pushed the sentence ABOVE it onto two lines. `.samefact`
  is pinned at the column now, so the panels are 559 wide whatever is written in them.
- **A component whose intrinsic width changes between steps needs a definite width.** The block
  shrink-wraps, so anything that sizes itself from its own text moves the slide when that text is
  rewritten. `.squint` is the one: its captions change when both screens go blurred, the block grew
  51px and the slide shifted 26px left. It carries `width: 815px` now. Everything else either has a
  fixed width or keeps the same text across its steps — verified by walking every step of every
  stack and comparing the block's width and left edge.
- **Two things that must line up belong on one slide, not two.** The whole plan and the divider
  that narrows it to chapter 1 are one stack: five rows arrive a click at a time, then the last
  click dims all but the chapter about to start. They were two slides and the running order jumped
  — reveal auto-animates `.sbody` itself (it carries a `data-id`), and the body box is 750px tall
  inside a stack but only as tall as its content on a top-level slide, so reveal SCALED the whole
  outline by 2.5 and dropped it to the top of the screen before it settled. `.sbody` now also
  carries `transform: none` while it is an auto-animate target — it is the layout box, always where
  the CSS puts it, so it has nothing to animate — but the real fix is the merge. The other four
  dividers have no `data-auto-animate`: there is nothing on screen for them to continue from.
- **The rows of the outline carry a `data-id`, because their class is what changes.** A row goes
  from `here` to `later` between the whole plan and the divider, and both the step merge and
  auto-animate fall back to the first class when there is no id — so without one, `reserve_space()`
  read the dimmed rows as four elements the earlier steps were missing and inserted a second copy
  of each.
- **Only a pairable element fades.** reveal's auto-animate matches elements across two steps by
  `data-id`, by a paragraph or heading's text, by an image's `src`, or by a `<pre>`'s text — and by
  nothing else. Hide a plain wrapper `<div>` and it has nothing to animate from, so its whole block
  appears at full opacity on the click instead of fading. Hide the pairable elements inside it
  (`_hide_pairable()` in `build.py` does this for the opening step), or give the wrapper a
  `data-id`.
- **An element without a `data-id` is identified by its tag and its FIRST class.** `Node.key()` in
  `build.py` works that way, so anything that prepends a class — `hid`, say — renames the element
  as far as the merge is concerned, and `reserve_space()` then inserts a second copy of it from the
  final step instead of matching the one already there. Add state classes at the END, or give the
  element a `data-id`.
- **A title card lays out the WHOLE slide and pushes it down.** The content is there, invisible,
  below the title; a `margin-top` on `.titlebox` puts the title at the middle of the frame. It has
  to be a MARGIN: `padding` is on reveal's list of auto-animated styles, so pushing the body down
  with padding moved the block AND left auto-animate giving the title its own translate on top —
  the title dropped 268px below where it had been and only then rose. That is what keeps the
  title in the same column as on every following step — parking the content out of flow instead left
  the block only as wide as the title, so it centred on its own and the first click moved the title
  up AND left. Measured: the horizontal shift from card to first step is 0px on all 18 stacks.
- **Every stack opens on its title alone, then one click per item, conclusion last.** `build.py`
  writes the title-only step (`title_only_step()`), so no slide file carries it; `reserve_space()`
  fills it with the rest of the stack, hidden, and nothing moves when the first item appears. In the
  slide files this means: one picture or one list item per step, and the conclusion on a step of its
  own. A click that reveals two things, or that reveals the last item together with the conclusion,
  is a bug.
- **A conclusion is one line, and it fits in its box.** `.statement` is a faintly blue panel that
  hugs its sentence, so the claim is marked as different in kind, not just larger. Keep new
  conclusions under ~52 characters: past that the line wraps and the boxes stop reading as a set.
- **Every stack ends on a `.statement`, and nothing comes after it** — not a credit, not a link
  row. Two exceptions, both slides that are a title and a picture and nothing else: the cover, and
  *One real refinement* (the demo), whose payoff is the demo itself. A last click that adds
  only a credit, or adds nothing, is a bug.
- **A picture's label goes above the picture**, never below — the name, then the grey note, then
  the image, so the pair reads top-down like everything else on a slide. The `.pstep` software logos
  are the exception: they are attribution marks, not descriptions, so they stay under the picture.
- **A caption is not a conclusion.** Captions that rotate with the steps (`p.step.sub`, --fs-md,
  grey) describe what is currently highlighted; the conclusion (`.statement`, --fs-xl, white)
  arrives once, on the last click, and stays. If a slide's final caption is carrying the argument,
  it wants promoting to a `.statement`.
- **Credits are spoken, not shown.** No attribution is on a slide any more; the speaker notes carry
  what to say on each.
- **Images are sized by their component, never by the theme.** The black theme caps every image at
  `max-width: 95%`, which silently shaved 5% off the right of any picture set to `width: 100%` and
  left it pinned left — a picture visibly off-centre under a title that was not, and zone overlays
  out of register with the screenshot they annotate. `.reveal .sbody img { max-width: none }`
  overrides it; do not remove that rule.
- **Titles follow the ESS Visual Identity Manual.** Titillium Light, sentence case, centred, with a
  numbered uppercase chapter line above ("3.2 UX PRINCIPLES"). Titillium is embedded from
  `extra/fonts/` (SIL OFL) so a borrowed laptop renders it, and it sets the running text too: the
  manual (p19) makes Titillium the main typeface for outward-facing communication and specifies it
  for body text. Segoe is named there (p20) as the OFFICE typeface, for the internal templates — so
  if this deck is ever folded into the ESS PowerPoint template, Segoe is the right answer instead. All-caps titles are gone: they are read letter by letter, and they hid the
  EasyDiffraction / easydiffraction distinction. One- or two-word micro-labels keep their caps.
- **The chapter line is written by `build.py`, never by a slide.** `add_eyebrows()` numbers stacks
  from the section order and takes the section's icon from `SECTION_ICONS`, so the numbers cannot go
  stale when a slide is added, cut or moved. The outline dividers use the same number, icon and
  uppercase treatment, so the divider and the slides under it read as one label. There is no
  "Outline" heading on the divider: a numbered list of sections with one lit says that already.
  The backup deck is excluded — it has no running order for a number to refer to.
- **Two colours, two jobs: blue is the deck speaking, orange is the deck drawing on a picture.**
  `--c-blue` marks words in the deck's own text. `--c-mark` (rgb 209 153 102) is for anything laid
  over somebody else's screenshot: the zone boxes and reading-order arrows on *One screen, four
  zones*, the marker strokes on the UX review e-mail. It is not a second accent — using the deck's
  blue there would be worse than ugly, it would be wrong. The application's own UI blue sits at hue
  197.5°, `--c-blue` at 198.9°: **1.4° apart**, so an annotation in the deck's blue reads as more
  application rather than as a mark made on it, and on that slide the arrows pass directly over the
  blue tab and the blue Continue button. `--c-mark` is 169° away from it at a near-identical
  lightness. The colour lives in one token for the same reason `--c-blue` does.
- **One blue phrase per line, on lines that claim or name.** Every conclusion and every picture
  description carries exactly one `<span class="blue">` marking the word the line turns on. The
  micro-notes under a heading (`.capsub`, `.pstep .ps`, `.twoshots .sub`) stay plain — if every line
  had blue, blue would mark nothing. The `Shared` / `Technique-specific` pair keeps blue/orange:
  there the colour separates two categories rather than picking out a key word.
- **A picture's description is `--fs-sm`, ExtraLight 200, in `--c-mute`** — the smallest step, a
  weight below the body text, and the same grey as the chapter line, because it is a label *about*
  something rather than content. The only 32px caption is `.twoshots figcaption`, which is a product
  name (a heading) rather than a description.
- **`extra/*.css` loads after the theme**, so a rule at equal specificity wins. It used to load
  first, which meant `.reveal h3` silently lost to the theme's `.reveal h1, .reveal h2, .reveal h3`.
- **Content must precede `<aside class="notes">`.** `build.py`'s `wrap_bodies` splits there, so
  anything after the aside falls outside the centring wrapper and overflows the frame.
