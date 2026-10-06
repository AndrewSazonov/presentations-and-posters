#!/usr/bin/env python3
"""Inline slides/*.html (in the order listed below) into index.html.

Same convention as the 2026-01 Shapespyre deck: every slide file wraps its content in
<div class="external-slide"> … </div>; the build strips that wrapper and inlines the
<section> stacks so the deck also works when opened with file://.
"""
from pathlib import Path
import re
from html.parser import HTMLParser
import sys
import time

HERE = Path(__file__).parent
# Section titles live here, not inside the slides: each becomes its own title slide, emitted before the
# first slide of that section. A slide file therefore carries only its own content.
SECTION_TITLES = {
    "10_problem.html": "The problem",
    "20_evolution.html": "Design evolution",
    "30_principles.html": "UX principles",
    "40_reuse.html": "Reuse",
    # The demo closes the talk, so 60_closing continues 50_demo without a divider of its own.
    "50_demo.html": "Demo",
    "90_appendix.html": "Backup",
}

ORDER = [
    "00_divider.html",
    "01_title.html",
    "10_problem.html",
    "20_evolution.html",
    "30_principles.html",
    "40_reuse.html",
    "50_demo.html",
]

# The backup slides are a separate deck: they are never presented in sequence, only opened when a
# question needs them, and keeping them out of index.html means the talk ends where it ends.
BACKUP_ORDER = [
    "90_appendix.html",
]

HEAD = """<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta name="description" content="How a diffraction analysis GUI became a module shared across neutron-scattering techniques">
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
    <meta name="theme-color" content="#333333">
    <title>Same workflow, different techniques — From a diffraction prototype to a reusable EasyScience GUI</title>

    <link rel="stylesheet" href="dist/reset.css">
    <link rel="stylesheet" href="dist/reveal.css">
    <link rel="stylesheet" href="dist/theme/fonts/source-sans-pro/source-sans-pro.css">
    <link rel="stylesheet" href="dist/theme/black.css">
    <link rel="stylesheet" href="plugin/highlight/monokai.css">

    <!-- The deck's own styles load LAST so they win against the theme at equal specificity. With
         them first, a rule like `.reveal h3` lost to the theme's `.reveal h1, .reveal h2, .reveal h3`
         and silently did nothing. -->
    <link rel="stylesheet" type="text/css" href="extra/icons.min.css">
    <link rel="stylesheet" type="text/css" href="extra/style.css">
    <link rel="stylesheet" type="text/css" href="extra/talk.css">
  </head>

  <body>
@ICON_SPRITE@
    <div class="reveal">
      <div class="slides">

        <!-- Slides are inlined by build.py so this deck also works when opened with file://. -->
"""

TAIL = """
      </div>
    </div>

    <script src="dist/reveal.js"></script>
    <script src="plugin/notes/notes.js"></script>
    <script src="plugin/markdown/markdown.js"></script>
    <script src="plugin/highlight/highlight.js"></script>
    <script>
      Reveal.initialize({
          width: 1200,
          height: 750,
          margin: 0,                     // reveal insets the stage by 4% of the viewport by
                                         // default, which put a band of background between a
                                         // picture bled to the slide's bottom edge and the bottom
                                         // of the window. A bleed has to reach the actual edge.
          controlsTutorial: false,
          progress: false,               // the blue bar along the bottom edge
          // "5/26" — the slide you are on out of the slides there are, not the click out of the
          // clicks: a stack is one slide to the room, however many times you press the button.
          // reveal spreads this into formatNumber(a, delimiter, b), so it has to be an array. Three
          // parts, so the separator is its own span and can be set larger than the numbers; the
          // newline and five tabs reveal puts between them are killed by font-size: 0 on the
          // anchor in extra/talk.css.
          slideNumber: function () {
            var h = Reveal.getIndices().h;
            // The ESS mark is a holding screen shown while the room fills, not part of the talk:
            // it carries no number, and the title page is 1. An empty first element renders an
            // empty span, which is also how the separator is suppressed there.
            if (h === 0) return [''];
            return [h, '|', Reveal.getHorizontalSlides().length - 1];
          },
          hash: true,
          transition: 'slide',           // a new slide arrives from the right; steps inside
                                         // one slide are auto-animated, so they stay fades
          backgroundTransition: 'fade',
          autoPlayMedia: null,
          plugins: [RevealMarkdown, RevealHighlight, RevealNotes],
          autoAnimateEasing: 'cubic-bezier(0.770, 0.000, 0.175, 1.000)',
          autoAnimateDuration: 0.5,   // a step is only ever a fade, so it can be quick
      })

      // FULLSCREEN MUST NOT RESIZE THE DECK. The window is already the full width of the display,
      // so pressing F adds only the height the browser chrome was using. reveal spends it: the deck
      // stops being height-limited, grows until width limits it instead, and every slide jumps
      // ~10% larger while the side margins collapse to nothing -- which is what put the title rule
      // hard against the screen edge. Capping maxScale at the scale the deck had in the window
      // keeps fullscreen identical to what was on screen a moment earlier; the height F hands over
      // goes to bands above and below instead of to the content.
      // A number in the config cannot do this: the right cap is whatever this window's height makes
      // it, which differs per machine, per display and per browser chrome.
      var windowedScale = null;
      var isFull = function () {
          return !!(document.fullscreenElement || document.webkitFullscreenElement);
      };
      var remember = function () { if (!isFull()) windowedScale = Reveal.getScale(); };
      // Four readings, because no single one is dependable: reveal's 'resize' only fires when the
      // scale actually CHANGES, so it can never fire at all on a deck opened at its final size...
      Reveal.on('ready', remember);
      Reveal.on('resize', remember);
      window.addEventListener('resize', remember);
      // ...and this last one is the safety net: F is what starts the transition, and on the capture
      // phase we run before reveal's own key handler, so the deck is still certainly windowed. The
      // macOS fullscreen animation resizes the viewport many times on the way, and if any of those
      // landed before fullscreenElement was set they would overwrite the value we want.
      document.addEventListener('keydown', function (e) {
          if (e.key === 'f' || e.key === 'F') remember();
      }, true);
      // ...but only where fullscreen would otherwise have NO side margin at all. On a display
      // narrower than the deck's 1.6 the stage is width-limited in fullscreen and runs edge to
      // edge; on a 16:9 projector it is height-limited and already sits in a band of its own, and
      // capping there would just leave the slides small in the middle of the room's screen. Read
      // off `screen`, not the viewport, which is still mid-animation when this fires.
      var fullscreenWouldFillWidth = function () {
          return screen.width / 1200 < screen.height / 750;
      };
      var onFullscreenChange = function () {
          // configure() re-lays out, which fires 'resize' again; remember()'s guard stops that
          // becoming a loop, since it only writes windowedScale when NOT fullscreen.
          var cap = isFull() && windowedScale && fullscreenWouldFillWidth() ? windowedScale : 2;
          Reveal.configure({ maxScale: cap });
          // ...and re-measure the band, twice. The viewport is mid-animation when this fires, so
          // the first reading is of a window still on its way; the later one catches the size it
          // settles at. Without these, fullscreen keeps the windowed band -- which is none -- and
          // a picture goes on being cut at the canvas edge with screen to spare below it.
          alignControls();
          setTimeout(alignControls, 700);
      };
      document.addEventListener('fullscreenchange', onFullscreenChange);
      document.addEventListener('webkitfullscreenchange', onFullscreenChange);

      // THE ARROWS SIT IN THE TOP RIGHT CORNER, small, and stay there. They used to live in the
      // bottom corner, where they landed on whatever the slide put there -- on a narrow screen the
      // down arrow sits in the third screenshot of "Three ways in". Up beside the title they are
      // clear of every slide's content, because the title band is short and ranged left.
      // The corner is the DECK's, not the window's: on a letterboxed screen those are different
      // places, and the arrows belong with the slide. That is the whole reason this is in script --
      // talk.css keeps the controls in screen pixels, since they live outside .slides and are not
      // scaled with the stage, so lining them up with the stage means measuring it.
      var controlsBaseline = null, controlsOrigin = null;
      var alignControls = function () {
          var reveal = Reveal.getRevealElement();
          var slides = reveal.querySelector('.slides');
          var num = reveal.querySelector('.slide-number');
          var ctl = reveal.querySelector('.controls');
          if (!slides || !num || !ctl) return;
          var r = reveal.getBoundingClientRect(), s = slides.getBoundingClientRect();
          var scale = Reveal.getScale();
          // The title band: 94 stage units tall, starting 44 down. The arrows ride at its middle on
          // every slide -- including the dividers and the cover, which have no title block at all,
          // so a measured height would have been missing exactly where it was needed.
          var TITLE_TOP = 44, TITLE_H = 94;
          var want = s.top + (TITLE_TOP + TITLE_H / 2) * scale;
          // Where the diamond sits with NO shift, measured once and kept. Reading its live position
          // instead would be self-referential -- the rect already includes the shift set last time,
          // so each call would add another and the arrows would walk off the top. Held as a distance
          // from .reveal's BOTTOM edge, which is what the CSS anchors to.
          if (controlsBaseline === null) {
              var n0 = num.getBoundingClientRect();
              controlsBaseline = r.bottom - (n0.top + n0.height / 2);
          }
          reveal.style.setProperty('--ctrl-shift', ((r.bottom - controlsBaseline) - want) + 'px');
          reveal.style.setProperty('--ctrl-right', ((r.right - s.right) + 28 * scale) + 'px');
          // HOW FAR A PICTURE MAY RUN PAST THE BOTTOM OF THE SLIDE. The deck is a fixed 1200x750
          // canvas, so on a window taller than 1.6 -- and in fullscreen, where the scale is pinned
          // and the spare height becomes band -- there is screen below the canvas doing nothing,
          // while a picture that was cut at the canvas edge still has more to show.
          // This is the HALF-BAND under the slide, in stage units. It does not resize or move
          // anything: talk.css spends it purely on the clip, so the layout is identical and the
          // only difference is how much of an overflowing picture survives.
          var extra = Math.max(0, (r.height / scale - 750) / 2);
          reveal.style.setProperty('--vh-extra', extra + 'px');
          // Drawn at the title band's height, so it reads as part of that band rather than as a
          // fixed-size widget parked beside it. The span is NOT measured: reveal hides the up and
          // down arrows on a slide with no vertical steps, and reading it meant un-scaling the
          // cluster on every call, which made it pulse. It is a constant of the arrow offsets in
          // talk.css, so it is declared there, beside them.
          var span = parseFloat(getComputedStyle(reveal).getPropertyValue('--ctrl-span'));
          // Sized from --ctrl-height, a stage-unit target declared in talk.css beside the arrows.
          // It started as the title block's own 94, which read a little small; it is a token so the
          // one number that decides how big the cluster is sits next to the geometry it scales.
          var tall = parseFloat(getComputedStyle(reveal).getPropertyValue('--ctrl-height')) || TITLE_H;
          if (span > 0) reveal.style.setProperty('--ctrl-scale', (tall * scale) / span);
          // The arrows and the number are separate elements, so they only stay a diamond if both
          // scale about the same point. The number is that point -- it sits at the diamond's middle.
          if (controlsOrigin === null) {
              var cr = ctl.getBoundingClientRect(), nr = num.getBoundingClientRect();
              controlsOrigin = ((nr.left + nr.width / 2) - cr.left) + 'px '
                             + ((nr.top + nr.height / 2) - cr.top) + 'px';
              reveal.style.setProperty('--ctrl-origin', controlsOrigin);
          }
      };
      Reveal.on('ready', alignControls);
      // reveal's own 'resize' only fires when the SCALE changes -- and the fullscreen cap below
      // exists precisely to stop it changing, so entering fullscreen fires nothing at all. The
      // viewport still grew, though, and --vh-extra is computed from the viewport. Hence the DOM
      // resize event as well: it fires whatever the scale does.
      Reveal.on('resize', alignControls);
      window.addEventListener('resize', alignControls);
      // TEMPORARY, for choosing how a lone screenshot is sized — delete once the choice is made.
      // index.html?pic=5 (as built) | 80 | 200 | 280 | side  — px cut off the bottom of the picture
      ;(function () {
        const pic = new URLSearchParams(location.search).get('pic');
        if (!pic) return;
        // pic=<px cut off the bottom>: the bigger the cut, the wider the picture.
        const cut = { '5': 5, '80': 80, '200': 200, '280': 280 }[pic];
        const st = document.createElement('style');
        st.textContent = cut
          ? `.reveal .shotbox { margin-bottom: -${cut}px !important; }`
          : `.reveal .sbody > .titlebox, .reveal .sbody > .statement,
             .reveal .sbody > p.step { max-width: 46% !important; }
             .reveal .sbody > .shotbox { position: absolute !important; left: 52% !important;
               right: var(--pad-x) !important; top: var(--pad-top) !important;
               bottom: var(--pad-top) !important; width: auto !important; height: auto !important;
               margin: 0 !important; }
             .reveal .sbody > .shotbox img { height: 100% !important; width: 100% !important;
               object-fit: contain !important; object-position: left top !important; }`;
        document.head.appendChild(st);
        const tag = document.createElement('div');
        tag.textContent = 'pic=' + pic;
        tag.style.cssText = 'position:fixed;left:8px;bottom:8px;z-index:99;font:12px system-ui;' +
                            'color:#6dd1ff;opacity:.7';
        document.body.appendChild(tag);
      })();
      // Layout self-check: open index.html?check to get one line per slide step whose content
      // overflows the 1200x750 slide box (vertical) or spills past its edges (horizontal).
      if (location.search.includes('check')) {
        Reveal.on('ready', () => {
          // Walk with auto-animate AND the slide transition off: both tween a transform, and
          // stepping this fast leaves a half-finished one on the slide being measured. The title
          // card moves the whole block, so every stack reported its first two steps as
          // overflowing; the horizontal slide-in put the first slide of a stack off to the side,
          // which is what the standing "#/1/0 h-overflow" line always was.
          Reveal.configure({ autoAnimate: false, transition: 'none' });
          const out = []; const box = document.querySelector('.reveal .slides').getBoundingClientRect();
          const hs = document.querySelectorAll('.reveal .slides > section');
          hs.forEach((hsec, h) => {
            const vs = hsec.querySelectorAll(':scope > section'); const n = Math.max(vs.length, 1);
            for (let v = 0; v < n; v++) {
              Reveal.slide(h, v); const sec = Reveal.getCurrentSlide(); const r = sec.getBoundingClientRect();
              const issues = [];
              if (r.height > box.height + 1 && !sec.classList.contains('titlecard')) issues.push(`vertical overflow ${Math.round(r.height - box.height)}px`);
              sec.querySelectorAll('*').forEach(el => {
                const e = el.getBoundingClientRect(); if (e.width === 0) return;
                if (e.right > box.right + 2 || e.left < box.left - 2) issues.push(`h-overflow <${el.tagName.toLowerCase()}> "${(el.textContent||'').trim().slice(0,40)}"`);
                // A lone screenshot is MEANT to run off the bottom edge — see --bleed in
                // talk.css — and a title card parks its content below the slide to move it in.
                if (el.closest('.shotbox') || el.closest('.zonebox')
                    || sec.classList.contains('titlecard')) return;
                if (e.bottom > box.bottom + 2) issues.push(`v-spill <${el.tagName.toLowerCase()}> "${(el.textContent||'').trim().slice(0,40)}"`);
              });
              if (issues.length) out.push(`#/${h}/${v} ${(sec.querySelector('h3')||{}).textContent||''}: ` + [...new Set(issues)].slice(0,4).join(' | '));
            }
          });
          Reveal.configure({ autoAnimate: true, transition: 'slide' });
          const pre = document.createElement('pre'); pre.id = 'layout-check'; pre.textContent = out.join(String.fromCharCode(10)) || 'no layout issues'; document.body.appendChild(pre);
        });
      }
    </script>
  </body>
</html>
"""


# One sprite symbol per section, expanded by expand_icons() along with the icons on the slides.
SECTION_ICONS = {
    'The problem': 'magnifying-glass',
    'Design evolution': 'drafting-compass',
    'UX principles': 'brain',
    'Reuse': 'cubes',
    'Demo': 'display',
}


def section_map(current: str | None, upto: int | None = None) -> str:
    """The running order as an outline, with the section about to start lit and the rest held back.

    A listener twelve minutes in should see, in one glance, where they are and how much is left.
    `current=None` lights every row: the whole plan once, before the talk starts narrowing it.
    Backup is deliberately absent: it is not part of the talk.
    """
    rows, n, seen = [], 0, True    # `seen` runs True until the current row, so earlier rows are "done"
    for label in SECTION_TITLES.values():
        if label == "Backup":            # its own deck now: backup.html
            continue
        n += 1
        here = "here" if current is None or label == current else ("done" if seen else "later")
        if label == current:
            seen = False
        if upto is not None and n > upto:   # the opening outline arrives a row at a time
            here += " hid"
        # numbered and iconed exactly like the chapter line on the slides themselves, so the outline
        # and the slide that follows it read as the same label rather than two spellings of one.
        # A data-id, not the class, identifies a row: the class is what CHANGES between the
        # whole plan and the divider that narrows it (`here` becomes `later`), and both the
        # step merge and auto-animate key on the first class when there is no id.
        rows.append(f'<li class="{here}" data-id="row{n}"><span class="no">{n}</span>'
                    f'<i class="fa-{SECTION_ICONS[label]}"></i>{label}</li>')
    # No "Outline" heading: five numbered, iconed rows with one of them lit is self-evidently an
    # outline, and a slide whose job is orientation should not spend a line saying so.
    return f'<ul class="section-map">{"".join(rows)}</ul>'



# --- the manual's chapter line -------------------------------------------------------------------
# ESS's Visual Identity Manual puts a numbered, uppercase chapter line above every heading
# ("2.11 BASIC ELEMENTS"). The deck does the same, and the build writes it rather than the slides:
# the number is the slide's position, so it can only be right if nobody has to maintain it by hand.
EYEBROW = re.compile(r"(<section\b[^>]*>)(\s*)(<h3\b)")


def add_eyebrows(body: str, sec_no: int, sec_name: str, first_stack: int) -> tuple[str, int]:
    """Put "<sec_no>.<n> <SECTION>" above the <h3> of every step, numbering stacks from first_stack."""
    out, pos, depth, n = [], 0, 0, first_stack
    for m in re.finditer(r"<section\b[^>]*>|</section>", body):
        if m.group(0).startswith("</"):
            depth -= 1
            if depth == 0:
                stack = body[start:m.end()]
                if "<h3" in stack:
                    n += 1
                    tag = (f'<p class="eyebrow" data-id="eyebrow">'
                           f'<span class="no">{sec_no}.{n}</span>'
                           f'<i class="fa-{SECTION_ICONS[sec_name]}"></i>{sec_name}</p>\n  ')
                    stack = EYEBROW.sub(lambda mm: mm.group(1) + mm.group(2) + tag + mm.group(3), stack)
                out.append(body[pos:start]); out.append(stack); pos = m.end()
        else:
            if depth == 0:
                start = m.start()
            depth += 1
    out.append(body[pos:])
    return "".join(out), n


H3 = re.compile(r"<h3\b[^>]*>.*?</h3>", re.S)


def title_only_step(body: str) -> str:
    """Open every stack on its title alone, so the first click reveals the first item.

    A stack used to arrive with its first item already on screen: the title got no moment of its
    own, and the first click landed on the second thing. The build writes the extra step rather
    than the slides, because it is the same title copied and a copy is one more thing to keep in
    sync. reserve_space() then fills the new step with the rest of the stack, hidden, so nothing
    moves when the first item appears.
    """
    out, pos, depth = [], 0, 0
    for m in re.finditer(r"<section\b[^>]*>|</section>", body):
        if m.group(0).startswith("</"):
            depth -= 1
            if depth == 0:
                out.append(body[pos:start])
                out.append(open_on_title(body[start:m.end()]))
                pos = m.end()
        else:
            if depth == 0:
                start = m.start()
            depth += 1
    out.append(body[pos:])
    return "".join(out)


def open_on_title(stack: str) -> str:
    """Prepend a title-only step to one stack, or hand it back untouched.

    The new step is the FIRST step with everything but the title hidden, not an empty one. An empty
    step would be filled by reserve_space() from the LAST step instead, and auto-animate matches
    hidden elements too: the tab strip would arrive carrying the final step's highlight, and the
    first click would slide the blue pill from Summary back to Project before the slide settled.
    """
    steps = list(re.finditer(r"<section\b[^>]*>", stack))
    if len(steps) < 2:                       # the stack's own tag, then at least one step
        return stack
    first = steps[1]
    # a cover opens on itself: it is already a title on an empty screen
    if "freeform" in first.group(0) or "cover" in first.group(0):
        return stack
    if not H3.search(stack, first.end()):
        return stack
    end = _step_end(stack, first.start())
    parts = []
    for k in parse(stack[first.end():end]).kids:
        if k.tag == "#text":
            parts.append(k.text)
        elif k.tag == "h3":
            parts.append(k.render())
        elif k.tag != "aside":               # speaker notes belong to the step that carries them
            parts.append(_hide_pairable(k))
    opening = first.group(0).replace(" data-auto-animate-restart", "")
    if "data-auto-animate" not in opening:
        opening = opening[:-1].rstrip() + " data-auto-animate>"
    return (stack[:first.start()]
            + '<section class="titlecard" data-auto-animate data-auto-animate-restart>'
            + "".join(parts) + "</section>\n\n"
            + opening + stack[first.end():])


# What reveal's auto-animate can pair across two steps: anything with a data-id, a paragraph or
# heading (matched on its text), an image (on its src), a <pre> (on its text). Nothing else — a
# plain wrapper <div> is never paired.
PAIRABLE_TAGS = {"p", "li", "h1", "h2", "h3", "h4", "h5", "h6", "img", "video", "iframe", "pre"}


def _hide_pairable(node) -> str:
    """Render `node` with the OUTERMOST auto-animatable descendants hidden, not the node itself.

    Hiding a wrapper gives auto-animate nothing to animate: it cannot pair a plain <div> across two
    steps, so the wrapper's opacity jumps 0 to 1 and the whole block appears at once instead of
    fading. Its pairable children each fade, which is what every other step of the deck does.
    """
    if "data-id" in node.attrs or node.tag in PAIRABLE_TAGS:
        return _hidden(node)
    if not any(k.tag != "#text" for k in node.kids):
        return _hidden(node)
    return (node.raw
            + "".join(k.text if k.tag == "#text" else _hide_pairable(k) for k in node.kids)
            + f"</{node.tag}>")


def _hidden(node) -> str:
    """The element, rendered with its own subtree, but invisible.

    `hid` goes at the END of the class list on purpose. Node.key() identifies an element without a
    data-id by its tag and its FIRST class, so prepending would rename `pipeline` to `hid` and
    reserve_space() would insert a SECOND pipeline below it rather than matching this one.
    """
    m = re.search(r'class="([^"]*)"', node.raw)
    raw = (node.raw[:m.start()] + f'class="{m.group(1)} hid"' + node.raw[m.end():]) if m \
          else node.raw[:-1].rstrip() + ' class="hid">'
    if node.tag in VOID_TAGS or raw.endswith("/>"):
        return raw
    return raw + "".join(k.render() for k in node.kids) + f"</{node.tag}>"


def _step_end(stack: str, start: int) -> int:
    """Where the <section> opening at `start` closes — the index of its `</section>`."""
    depth = 0
    for m in re.finditer(r"<section\b[^>]*>|</section>", stack[start:]):
        if m.group(0).startswith("</"):
            depth -= 1
            if depth == 0:
                return start + m.start()
        else:
            depth += 1
    raise SystemExit("unclosed <section> in a stack")


# The chapter line and the title are one block, so the rule drawn beside them has a height to
# follow. The box is invisible; only extra/talk.css's `.titlebox::before` shows.
TITLE_BLOCK = re.compile(r'(?:<p class="eyebrow"[^>]*>.*?</p>\s*)?<h3\b[^>]*>.*?</h3>', re.S)


def wrap_titles(body: str) -> str:
    """Put the chapter line and the slide title in one .titlebox.

    A cover is a title slide, not a slide with a title: it carries no chapter line and the whole
    screen is already the heading, so `.deck-title` keeps its own spacing and gets no rule.
    """
    def one(m):
        if 'class="deck-title"' in m.group(0):
            return m.group(0)
        return f'<div class="titlebox" data-id="titlebox">{m.group(0)}</div>'
    return TITLE_BLOCK.sub(one, body)


SECTION_TAG = re.compile(r"<section\b[^>]*>|</section>", re.I)


def wrap_bodies(html: str) -> str:
    """Wrap each leaf slide's content in one always-flex .sbody, so centring never switches on.

    Centring the section itself means the rule can only apply to the visible slide (reveal hides the
    rest with `display: none`), so the incoming slide is laid out uncentred, measured by
    auto-animate, and centred a frame later — which reads as everything jumping up and settling
    back. A wrapper inside the section is flex on every slide, present or not, so the geometry
    auto-animate measures is already the final one. It carries a data-id so auto-animate matches it
    and keeps recursing into its children.
    """
    tags = list(SECTION_TAG.finditer(html))
    out, pos, depth = [], 0, 0
    opens = []
    for m in tags:
        if m.group(0).startswith("</"):
            start = opens.pop()
            if not opens or True:
                inner = html[start.end():m.start()]
                if "<section" not in inner.lower() and inner.strip():
                    aside = inner.find("<aside")
                    body, tail = (inner[:aside], inner[aside:]) if aside >= 0 else (inner, "")
                    out.append(html[pos:start.end()])
                    out.append('\n  <div class="sbody" data-id="sbody">' + body + "</div>\n" + tail)
                    pos = m.start()
        else:
            opens.append(m)
    out.append(html[pos:])
    return "".join(out)



# --- reserving the space of later steps -------------------------------------------------------
# FADE_ONLY makes every step of a stack carry the elements the later steps will add, marked `hid`
# so they take their space but do not show. A step then differs from the one before it only in
# which items are visible, so nothing on the slide moves: each item fades in where it already
# belonged. Set it False to have each step carry only what it shows, in which case the block
# re-centres on every click and the earlier items rise.
FADE_ONLY = True

ZERO_WIDTH = re.compile(r'(class="bar-fill[^"]*"[^>]*style="width: )[0-9.]+%')

VOID_TAGS = {"img", "br", "hr", "input", "meta", "link", "use", "path", "rect", "line", "circle",
             "polygon", "polyline", "ellipse", "stop", "source", "col", "area", "base"}


class Node:
    __slots__ = ("tag", "attrs", "raw", "kids", "text")

    def __init__(self, tag="", attrs=None, raw="", text=""):
        self.tag, self.attrs, self.raw, self.kids, self.text = tag, attrs or {}, raw, [], text

    def key(self, ordinal=0):
        """What identifies an element across two steps of the same stack.

        A data-id if it has one. Otherwise the tag and the FIRST class — a step may append a class
        (`why-col` becomes `why-col struck`) but does not rename an element — plus its position
        among siblings of that same kind, so a step that lacks an earlier sibling still lines its
        own elements up with the right ones.
        """
        if "data-id" in self.attrs:
            return ("id", self.attrs["data-id"])
        first = (self.attrs.get("class", "").split() or [""])[0]
        return ("tag", self.tag, first, ordinal)

    def render(self, hide=False):
        if self.tag == "#text":
            return self.text
        raw = self.raw
        if hide:
            m = re.search(r'class="([^"]*)"', raw)
            raw = (raw[:m.start()] + f'class="hid {m.group(1)}"' + raw[m.end():]) if m \
                  else raw[:-1].rstrip() + ' class="hid">'
        if self.tag in VOID_TAGS or raw.endswith("/>"):
            return ZERO_WIDTH.sub(r"\g<1>0%", raw) if hide else raw
        inner = "".join(k.render() for k in self.kids)
        out = raw + inner + f"</{self.tag}>"
        return ZERO_WIDTH.sub(r"\g<1>0%", out) if hide else out


class Tree(HTMLParser):
    """Just enough DOM to merge two steps of the same stack."""

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.root = Node("#root")
        self.stack = [self.root]

    def _add(self, node):
        self.stack[-1].kids.append(node)

    def handle_starttag(self, tag, attrs):
        n = Node(tag, dict(attrs), self.get_starttag_text())
        self._add(n)
        if tag not in VOID_TAGS:
            self.stack.append(n)

    def handle_startendtag(self, tag, attrs):
        self._add(Node(tag, dict(attrs), self.get_starttag_text()))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        self._add(Node("#text", text=data))

    def handle_entityref(self, name):
        self._add(Node("#text", text=f"&{name};"))

    def handle_charref(self, name):
        self._add(Node("#text", text=f"&#{name};"))

    def handle_comment(self, data):
        self._add(Node("#text", text=f"<!--{data}-->"))


def parse(html):
    t = Tree()
    t.feed(html)
    t.close()
    return t.root


def merge(final, current):
    """Render `current`, with every element `final` has and `current` lacks hidden in its place.

    Walks the two children lists together so the current step keeps its own text, its own attribute
    values (a bar's width, a caption's number) and its own order, while anything only a later step
    shows is inserted where it will eventually sit, marked `hid`. Elements are matched by data-id,
    and otherwise by their position among siblings of the same tag — a step often changes an
    element's classes (`why-col` becomes `why-col struck`), so classes cannot identify it.
    """
    def keys(nodes):
        seen, out = {}, []
        for n in nodes:
            if n.tag == "#text":
                out.append(None); continue
            kind = (n.tag, (n.attrs.get("class", "").split() or [""])[0])
            seen[kind] = seen.get(kind, -1) + 1
            out.append(n.key(seen[kind]))
        return out

    fkeys, ckeys = keys(final.kids), keys(current.kids)
    out, ci, kids = [], 0, current.kids
    for f, fk in zip(final.kids, fkeys):
        if fk is None:
            continue
        j = next((k for k in range(ci, len(kids)) if ckeys[k] == fk), None)
        if j is None:
            out.append(f.render(hide=True))
            continue
        for k in range(ci, j):
            out.append(kids[k].render())
        out.append(render_merged(f, kids[j]))
        ci = j + 1
    for k in range(ci, len(kids)):
        out.append(kids[k].render())
    return "".join(out)


def render_merged(final, current):
    if current.tag in VOID_TAGS or current.raw.endswith("/>"):
        return current.raw
    return current.raw + merge(final, current) + f"</{current.tag}>"


def keeps_words(before, after):
    """Every word the step showed is still there, in order — the inserted ones may sit between."""
    it = iter(after.split())
    return all(w in it for w in before.split())


def visible_text(html):
    """The words a step shows, for the build's own check that merging loses none of them."""
    body = re.sub(r"<(script|style|aside)\b.*?</\1>", "", html, flags=re.S | re.I)
    return " ".join(re.sub(r"<[^>]+>", " ", body).split())


def reserve_space(html):
    """Give every step of every stack the space of the steps that follow it."""
    if not FADE_ONLY:
        return html
    out, pos, depth, starts, stacks = [], 0, 0, [], []
    opted_out = set()
    for m in re.finditer(r"<section\b[^>]*>|</section>", html):
        if not m.group(0).startswith("</") and 'data-reserve="off"' in m.group(0):
            opted_out.add(len(stacks))          # a stack can ask to keep re-centring instead
        if m.group(0).startswith("</"):
            depth -= 1
            if depth == 1:
                stacks[-1].append((starts.pop(), m.start()))
        else:
            if depth == 0:
                stacks.append([])
            depth += 1
            if depth == 2:
                starts.append(m.end())
    edits = []
    for n, steps in enumerate(stacks):
        if len(steps) < 2 or n in opted_out:
            continue
        final = parse(html[steps[-1][0]:steps[-1][1]])
        for a, b in steps[:-1]:
            merged = merge(final, parse(html[a:b]))
            if not keeps_words(visible_text(html[a:b]), visible_text(merged)):
                raise SystemExit("reserve_space lost content in a step:\n  "
                                 + visible_text(html[a:b])[:160])
            edits.append((a, b, merged))
    for a, b, text in sorted(edits):
        out.append(html[pos:a]); out.append(text); pos = b
    out.append(html[pos:])
    return "".join(out)


# --- icons ------------------------------------------------------------------------------------
# A slide writes an icon the way a Font Awesome page would — <i class="fa-flask"></i> — and the
# build expands it against extra/icons-sprite.svg, which holds the Font Awesome 6 outlines the
# deck actually uses. No webfont to ship and no CDN to reach: the glyph is already in the page,
# and `lead`/`big` pick the two sizes the stylesheet defines.
# An optional data-id rides through to the generated <svg>: reveal pairs only [data-id] and a
# handful of tags, so an icon inside an element that IS paired would otherwise count as unmatched
# and be faded in on every step. Tags written without one behave exactly as before.
ICON_TAG = re.compile(
    r'<i class="fa-([a-z0-9-]+)((?: (?:lead|big))?)"(?:\s+data-id="([^"]+)")?\s*></i>')


def expand_icons(html: str, sprite: str) -> str:
    boxes = dict(re.findall(r'<symbol id="i-([^"]+)" viewBox="([^"]+)"', sprite))
    missing = set()

    def one(m):
        name, mod, did = m.group(1), m.group(2).strip(), m.group(3)
        if name not in boxes:
            missing.add(name)
            return m.group(0)
        cls = "bigico" if mod == "big" else ("ico lead" if mod == "lead" else "ico")
        ident = f' data-id="{did}"' if did else ""
        return f'<svg class="{cls}"{ident} viewBox="{boxes[name]}"><use href="#i-{name}"/></svg>'

    out = ICON_TAG.sub(one, html)
    if missing:
        raise SystemExit(f"unknown icon name(s): {', '.join(sorted(missing))}")
    return out


def body(fragment: str) -> str:
    m = re.search(r'<div class="external-slide">(.*)</div>\s*$', fragment, re.S)
    return (m.group(1) if m else fragment).strip("\n")


def stamp(html: str) -> str:
    import time
    v = time.strftime("%Y%m%d%H%M%S")
    return re.sub(r'((?:href|src)=")((?:dist|extra|plugin|images)/[^"?]+)"', lambda m: f'{m.group(1)}{m.group(2)}?v={v}"', html)


def render(order, sprite, titles=True):
    parts = []
    seen_title = False
    sec_no, stack_no, sec_name = 0, 0, None
    for name in order:
        text = (HERE / "slides" / name).read_text(encoding="utf-8")
        title = SECTION_TITLES.get(name) if titles else None
        # The backup deck has no running order, so a numbered chapter line would imply one it does
        # not have; `titles` is False there, which is the same switch that suppresses its dividers.
        if titles and SECTION_TITLES.get(name):   # a new chapter restarts the numbering
            sec_no += 1; stack_no = 0; sec_name = SECTION_TITLES[name]
        if title:
            first = not seen_title
            seen_title = True
            if first:
                # The whole plan first, every section equally lit — and arriving a row at a time,
                # because a list of five that lands in one go is read as a block rather than as
                # five things. Then, on the LAST click of the same slide, all but the chapter about
                # to start dims: the plan and the first divider are one slide, not two. Across a
                # slide boundary reveal measures the body box of the slide it is leaving against
                # the body box of the one it is entering, and those two differ in height, so it
                # scaled the running order by 2.5 and dropped it to the top before it settled.
                rows = sum(1 for v in SECTION_TITLES.values() if v != "Backup")
                steps = "".join(
                    '        <section class="section-title" data-auto-animate'
                    + (' data-auto-animate-restart' if k == 1 else '')
                    + f'>{section_map(None, upto=k)}</section>\n'
                    for k in range(1, rows + 1))
                steps += ('        <section class="section-title" data-auto-animate>'
                          f'{section_map(title)}</section>\n')
                parts.append(f'        <!-- ===== section: the whole plan, then {title} ===== -->\n'
                             '        <section>\n' + steps + '        </section>\n')
            else:
                # Every later divider takes the deck's ordinary slide-in. It has no auto-animate:
                # matched against the end of the previous stack it stretched the outline instead of
                # moving it, and there is nothing on screen for it to continue from anyway.
                parts.append(f'        <!-- ===== section: {title} ===== -->\n'
                             f'        <section class="section-title">'
                             f'{section_map(title)}</section>\n')
        chunk = body(text)
        if sec_name:
            chunk = title_only_step(chunk)
            chunk, stack_no = add_eyebrows(chunk, sec_no, sec_name, stack_no)
        # after the eyebrow exists, so the chapter line ends up inside the box with the title
        chunk = wrap_titles(chunk)
        parts.append(f"        <!-- ===== {name} ===== -->\n{chunk}\n")
    # Stamp the WHOLE document, not just its head and tail: the slides carry <img src="images/...">
    # too, and an unstamped picture is served from cache after it is re-cropped — the deck went on
    # showing the old crop until a hard reload, which is exactly the kind of thing that is noticed
    # on stage and not before. One call, so every asset carries the same version.
    doc = stamp(HEAD.replace("@ICON_SPRITE@", sprite)
                + wrap_bodies(reserve_space(expand_icons("\n".join(parts), sprite)))
                + TAIL)
    return doc, sum(len(re.findall(r"<section", p)) for p in parts)


def main() -> None:
    sprite = (HERE / "extra" / "icons-sprite.svg").read_text(encoding="utf-8")
    for target, order, titles in (("index.html", ORDER, True), ("backup.html", BACKUP_ORDER, False)):
        doc, n = render(order, sprite, titles)
        (HERE / target).write_text(doc, encoding="utf-8")
        print(f"{target} written: {len(order)} files, {n} <section> tags", flush=True)


WATCHED = ("slides", "extra")


def _fingerprint():
    """Modification times of everything the build reads, plus this script."""
    stamp = [str(Path(__file__).stat().st_mtime)]
    for folder in WATCHED:
        for f in sorted((HERE / folder).rglob("*")):
            if f.is_file():
                stamp.append(f"{f}:{f.stat().st_mtime}")
    return "".join(stamp)


def serve(port=8000):
    """Serve this folder in a background thread, for the cases file:// cannot handle — a phone or
    another machine on the network, or a browser that refuses local fonts over file://."""
    import functools
    import http.server
    import socketserver
    import threading

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(HERE))
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("", port), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    print(f"serving http://localhost:{port}/", flush=True)


def watch(interval=0.5):
    """Rebuild whenever a slide or stylesheet changes, so editing needs no command.

    A browser cannot assemble the deck itself: loading slides/*.html at run time means fetch() on
    file://, which every browser blocks as a cross-origin read. So the build has to happen outside
    the page — this just makes it automatic. Edit, save, refresh the tab.
    """
    main()
    last = _fingerprint()
    print(f"watching {', '.join(WATCHED)}/ — edit a slide, save, refresh the browser (ctrl-c to stop)", flush=True)
    while True:
        try:
            time.sleep(interval)
            now = _fingerprint()
            if now != last:
                last = now
                print(f"[{time.strftime('%H:%M:%S')}] change detected — ", end="", flush=True)
                main()
        except KeyboardInterrupt:
            print("\nstopped watching")
            return


if __name__ == "__main__":
    if "--serve" in sys.argv:
        serve()
    if "--watch" in sys.argv or "--serve" in sys.argv:
        watch()
    else:
        main()
