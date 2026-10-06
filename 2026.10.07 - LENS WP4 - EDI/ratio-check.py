#!/usr/bin/env python3
"""Render the deck to one PDF per screen ratio, so a projector can be checked before the room.

The deck is a fixed 1200x750 stage that reveal scales to fit whatever it is shown on, so the only
thing that changes between one screen and another is WHICH edge runs out first:

    screen wider than 1.600  ->  height-limited, bands down the sides
    screen narrower          ->  width-limited, bands top and bottom, content to the side edges

That decides whether the title rule clears the screen edge and whether a picture bled to the
bottom of a slide reaches the bottom of the screen. Both are things you can only see by looking,
which is what this produces: one PDF per ratio, one page per slide, each page the shape of that
screen with the deck placed in it exactly as the browser would.

    python3 ratio-check.py                      # every ratio, last step of each slide
    python3 ratio-check.py --steps all          # every step too (slow: ~110 pages per ratio)
    python3 ratio-check.py --ratios 16-9,4-3
    python3 ratio-check.py --slides 10,21       # only these slides, all their steps

FULLSCREEN IS REPRODUCED, not approximated. build.py pins the scale on entering fullscreen wherever
the screen is narrower than 1.600 and the deck would otherwise run edge to edge (see
`fullscreenWouldFillWidth`), which is exactly the set of ratios that would otherwise look cramped.
For those, this renders the deck at the size it has in the WINDOW on that screen -- browser chrome
included, --chrome px of it -- and then centres that in the full screen rectangle, which is what
the cap produces. Wider screens are height-limited, the cap never fires, and they are captured
at full size. Pass --no-cap to see the raw uncapped layout instead.

Needs no installation: it drives whichever Chromium-based browser is already on the machine and
writes the PDF with Pillow.
"""
import argparse, http.server, pathlib, re, shutil, socket, socketserver, subprocess, sys, threading

ROOT = pathlib.Path(__file__).resolve().parent

# name -> (width, height). Modest pixel sizes: only the RATIO changes what the deck does, so there
# is no reason to render 1920 wide and carry the file size.
RATIOS = {
    "16-9":   (1280, 720),   # the common projector and nearly every modern screen
    "16-10":  (1280, 800),   # 1.600 exactly -- the deck's own shape, the one case with no bands
    "3-2":    (1200, 800),
    "laptop": (1496, 967),   # this MacBook's own screen, 1.547
    "4-3":    (1024, 768),   # older projectors and some lecture rooms
    "21-9":   (1280, 549),
}

BROWSERS = [
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Arc.app/Contents/MacOS/Arc",
]


def find_browser():
    for p in BROWSERS:
        if pathlib.Path(p).exists():
            return p
    for name in ("chromium", "chromium-browser", "google-chrome"):
        found = shutil.which(name)
        if found:
            return found
    sys.exit("no Chromium-based browser found -- edit BROWSERS at the top of this file")


def slide_indices(html: str, steps: str):
    """Every (h, v) worth a page, read straight out of the built deck.

    Reveal numbers a stack's steps from 0, so the last step of slide h is v = (number of nested
    sections) - 1. Parsed rather than asked of the browser so the whole run is one pass.
    """
    body = html[html.index('<div class="slides">'):]
    out, depth, h, v = [], 0, -1, 0
    for m in re.finditer(r"<section\b[^>]*>|</section>", body):
        if m.group(0).startswith("</"):
            depth -= 1
            if depth == 0:
                out.append((h, max(v - 1, 0)) if steps == "last" else None)
            if depth < 0:
                break
        else:
            if depth == 0:
                h += 1
                v = 0
            else:
                v += 1
                if steps == "all":
                    out.append((h, v - 1))
            depth += 1
    return [x for x in out if x]


def serve(directory):
    """A throwaway server: the deck loads its fonts over http, and file:// blocks some of them."""
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=str(directory), **kw)

        def log_message(self, *a):
            pass

    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    httpd = socketserver.TCPServer(("127.0.0.1", port), Handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, port


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ratios", default=",".join(RATIOS))
    ap.add_argument("--steps", choices=("last", "all"), default="last")
    ap.add_argument("--slides", default="", help="only these slide numbers, with all their steps")
    ap.add_argument("--out", default="tmp/ratio-check")
    ap.add_argument("--settle", type=int, default=2500, help="ms of virtual time per page")
    ap.add_argument("--chrome", type=int, default=168,
                    help="px of browser chrome above the page when windowed; sets the scale the "
                         "fullscreen cap pins to")
    ap.add_argument("--no-cap", action="store_true",
                    help="render the raw uncapped layout, ignoring build.py's fullscreen cap")
    args = ap.parse_args()

    from PIL import Image  # imported late so --help works without it

    browser = find_browser()
    index = ROOT / "index.html"
    if not index.exists():
        sys.exit("no index.html -- run `python3 build.py` first")

    wanted = [r.strip() for r in args.ratios.split(",") if r.strip()]
    unknown = [r for r in wanted if r not in RATIOS]
    if unknown:
        sys.exit(f"unknown ratio(s): {', '.join(unknown)}. known: {', '.join(RATIOS)}")

    pages = slide_indices(index.read_text(), "all" if args.slides else args.steps)
    if args.slides:
        keep = {int(n) for n in args.slides.split(",")}
        pages = [(h, v) for h, v in pages if h in keep]

    out_dir = ROOT / args.out
    shots = out_dir / "_frames"
    shots.mkdir(parents=True, exist_ok=True)
    httpd, port = serve(ROOT)
    print(f"{browser.split('/')[-1]} | {len(pages)} pages x {len(wanted)} ratios "
          f"| serving on :{port}")
    try:
        for name in wanted:
            w, h = RATIOS[name]
            # build.py caps the scale only where fullscreen would run edge to edge
            capped = (not args.no_cap) and (w / 1200 < h / 750)
            shot_h = h - args.chrome if capped else h
            frames = []
            for n, (sh, sv) in enumerate(pages, 1):
                png = shots / f"{name}-{sh:03d}-{sv:02d}.png"
                subprocess.run(
                    [browser, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                     f"--screenshot={png}", f"--window-size={w},{shot_h}",
                     f"--virtual-time-budget={args.settle}",
                     f"http://127.0.0.1:{port}/index.html#/{sh}/{sv}"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
                if png.exists():
                    if capped:
                        # the cap keeps the windowed size and spends the rest on band, so put the
                        # windowed rendering back in the middle of the real screen rectangle
                        from PIL import Image as _I
                        shot = _I.open(png).convert("RGB")
                        page = _I.new("RGB", (w, h), (25, 25, 25))
                        page.paste(shot, (0, (h - shot.height) // 2))
                        page.save(png)
                    frames.append(png)
                print(f"\r  {name:7} {n}/{len(pages)}"
                      f"{'  (fullscreen cap applies)' if capped else ''}", end="", flush=True)
            if not frames:
                print(f"\r  {name:7} nothing captured")
                continue
            imgs = [Image.open(f).convert("RGB") for f in frames]
            pdf = out_dir / f"deck-{name}-{w}x{h}{'' if capped or args.no_cap else ''}.pdf"
            imgs[0].save(pdf, save_all=True, append_images=imgs[1:])
            print(f"\r  {name:7} {len(frames)} pages -> {pdf.relative_to(ROOT)}")
    finally:
        httpd.shutdown()
    print(f"\nratios rendered at their own shape; compare the side and bottom edges.\n"
          f"frames kept in {shots.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
