#!/usr/bin/env python3
"""Inline slides/*.html (in the order listed below) into index.html.

Taken over from the 2026-09 DMSC crysta deck, so this talk has its layout and style. Same
convention as the 2026-01 Shapespyre deck: every slide file wraps its content in
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
    "10_why.html": "Why new software",
    "20_easydiffraction.html": "EasyDiffraction",
    "30_crysta.html": "crysta",
    "40_outlook.html": "Outlook",
}

ORDER = [
    "00_divider.html",
    "01_title.html",
    "10_why.html",
    "20_easydiffraction.html",
]

# No backup deck for this talk; list files here to have build.py write backup.html as well.
BACKUP_ORDER: list[str] = []

HEAD = """<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta name="description" content="EasyDiffraction and crysta — reusing crystallographic libraries, and building our own">
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
    <meta name="theme-color" content="#333333">
    <title>EasyDiffraction and crysta — reusing crystallographic libraries, and building our own</title>

    <link rel="stylesheet" type="text/css" href="extra/icons.min.css">
    <link rel="stylesheet" type="text/css" href="extra/style.css">
    <link rel="stylesheet" type="text/css" href="extra/talk.css">
    <link rel="stylesheet" type="text/css" href="extra/edi.css">

    <link rel="stylesheet" href="dist/reset.css">
    <link rel="stylesheet" href="dist/reveal.css">
    <link rel="stylesheet" href="dist/theme/fonts/source-sans-pro/source-sans-pro.css">
    <link rel="stylesheet" href="dist/theme/black.css">
    <link rel="stylesheet" href="plugin/highlight/monokai.css">
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
          controlsTutorial: false,
          hash: true,
          transition: 'slide',           // a new slide arrives from the right; steps inside
                                         // one slide are auto-animated, so they stay fades
          backgroundTransition: 'fade',
          autoPlayMedia: null,
          plugins: [RevealMarkdown, RevealHighlight, RevealNotes],
          autoAnimateEasing: 'cubic-bezier(0.770, 0.000, 0.175, 1.000)',
          autoAnimateDuration: 0.5,   // a step is only ever a fade, so it can be quick
      })
      // Layout self-check: open index.html?check to get one line per slide step whose content
      // overflows the 1200x750 slide box (vertical) or spills past its edges (horizontal).
      if (location.search.includes('check')) {
        Reveal.on('ready', () => {
          // Measured mid-transition, a slide reads as overflowing, so the check switches both off.
          Reveal.configure({ transition: 'none', autoAnimate: false });
          const out = []; const box = document.querySelector('.reveal .slides').getBoundingClientRect();
          const hs = document.querySelectorAll('.reveal .slides > section');
          hs.forEach((hsec, h) => {
            const vs = hsec.querySelectorAll(':scope > section'); const n = Math.max(vs.length, 1);
            for (let v = 0; v < n; v++) {
              Reveal.slide(h, v); const sec = Reveal.getCurrentSlide(); const r = sec.getBoundingClientRect();
              const issues = [];
              if (r.height > box.height + 1) issues.push(`vertical overflow ${Math.round(r.height - box.height)}px`);
              sec.querySelectorAll('*').forEach(el => {
                // Inside a clipping window (the carousel), leaving the box is the point.
                if (el.closest('.carousel')) return;
                const e = el.getBoundingClientRect(); if (e.width === 0) return;
                if (e.right > box.right + 2 || e.left < box.left - 2) issues.push(`h-overflow <${el.tagName.toLowerCase()}> "${(el.textContent||'').trim().slice(0,40)}"`);
                if (e.bottom > box.bottom + 2) issues.push(`v-spill <${el.tagName.toLowerCase()}> "${(el.textContent||'').trim().slice(0,40)}"`);
              });
              if (issues.length) out.push(`#/${h}/${v} ${(sec.querySelector('h3')||{}).textContent||''}: ` + [...new Set(issues)].slice(0,4).join(' | '));
            }
          });
          const pre = document.createElement('pre'); pre.id = 'layout-check'; pre.textContent = out.join(String.fromCharCode(10)) || 'no layout issues'; document.body.appendChild(pre);
        });
      }
    </script>
  </body>
</html>
"""


# Sprite names: the outline goes through expand_icons() with the rest of the deck.
SECTION_ICONS = {
    "Why new software": "lightbulb",
    "EasyDiffraction": "cubes",
    "crysta": "microchip",
    "Outlook": "flag-checkered",
}


def section_map(current: str | None) -> str:
    """The running order as an outline, with the section about to start lit and the rest held back.

    A listener twelve minutes in should see, in one glance, where they are and how much is left.
    `current=None` lights every row: the whole plan once, before the talk starts narrowing it.
    Backup is deliberately absent: it is not part of the talk.
    """
    rows = []
    for label in SECTION_TITLES.values():
        here = "here" if current is None or label == current else "later"
        rows.append(f'<li class="{here}"><i class="fa-{SECTION_ICONS[label]}"></i>{label}</li>')
    return ('<h2 class="outline-head">Outline</h2>\n'
            f'          <ul class="section-map">{"".join(rows)}</ul>')


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
ICON_TAG = re.compile(r'<i class="fa-([a-z0-9-]+)((?: (?:lead|big))?)"\s*></i>')


def expand_icons(html: str, sprite: str) -> str:
    boxes = dict(re.findall(r'<symbol id="i-([^"]+)" viewBox="([^"]+)"', sprite))
    missing = set()

    def one(m):
        name, mod = m.group(1), m.group(2).strip()
        if name not in boxes:
            missing.add(name)
            return m.group(0)
        cls = "bigico" if mod == "big" else ("ico lead" if mod == "lead" else "ico")
        return f'<svg class="{cls}" viewBox="{boxes[name]}"><use href="#i-{name}"/></svg>'

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
    return re.sub(r'((?:href|src)=")((?:dist|extra|plugin)/[^"?]+)"', lambda m: f'{m.group(1)}{m.group(2)}?v={v}"', html)


def render(order, sprite, titles=True):
    parts = []
    seen_title = False
    for name in order:
        text = (HERE / "slides" / name).read_text(encoding="utf-8")
        title = SECTION_TITLES.get(name) if titles else None
        if title:
            first = not seen_title
            if first:
                # The whole plan first, every section equally lit; the divider that follows dims
                # all but the one starting, and auto-animate carries the list across.
                parts.append('        <!-- ===== section: the whole plan ===== -->\n'
                             '        <section class="section-title" data-auto-animate '
                             f'data-auto-animate-restart>{section_map(None)}</section>\n')
            # Only the divider right after the whole-plan slide auto-animates (the rows dim in
            # place). Every later one takes the deck's ordinary slide-in: matched against the end
            # of the previous stack, auto-animate stretched the outline instead of moving it.
            aa = ' data-auto-animate' if first else ''
            seen_title = True
            parts.append(f'        <!-- ===== section: {title} ===== -->\n'
                         f'        <section class="section-title"{aa}>'
                         f'{section_map(title)}</section>\n')
        parts.append(f"        <!-- ===== {name} ===== -->\n{body(text)}\n")
    doc = (stamp(HEAD).replace("@ICON_SPRITE@", sprite)
           + wrap_bodies(reserve_space(expand_icons("\n".join(parts), sprite)))
           + stamp(TAIL))
    return doc, sum(len(re.findall(r"<section", p)) for p in parts)


def main() -> None:
    sprite = (HERE / "extra" / "icons-sprite.svg").read_text(encoding="utf-8")
    for target, order, titles in (("index.html", ORDER, True), ("backup.html", BACKUP_ORDER, False)):
        if not order:
            continue
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
