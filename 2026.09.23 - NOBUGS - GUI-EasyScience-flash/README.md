# flash — EasyScience poster flash, NOBUGS 2026

Three minutes, **exactly one title slide and one content slide**, no questions afterwards. A hard
slide and time limit set by the organisers.

Built with the same machinery and stylesheet as the talk deck in
`../2026.09.21-25 - NOBUGS - GUI-EasyScience`, so the two read as one set of work.

## The two slides

| | what it carries |
| --- | --- |
| **1** | title, presenter, and the poster's own band: core modules down the first column, the six domain projects across the other three, each with the face of the person who builds it |
| **2** | the same screen in two techniques — EasyDiffraction and EasyReflectometry — under "Only the science differs." |

The photographs replace an author line: at three minutes nobody reads five names, and a face says
"team" in one glance. EasyTexture carries its `external` tag instead of a face, because it is built
outside ESS.

## Working on it

```bash
pixi run watch     # rebuilds on save
./make-pdf.sh      # flash.pdf — 2 pages, exactly as the browser draws them
```

`slides/10_flash.html` is the source; `index.html` is built from it by `build.py`. Open
`index.html` straight from the file system.

`make-pdf.sh` can fail in the headless browser and still exit — check the page count of `flash.pdf`
afterwards rather than assuming it wrote.

## What is different from the talk deck

`build.py` is the talk's, with `SECTION_TITLES` emptied (no chapters, dividers or numbered eyebrow
line), `ORDER` naming the single slide file, and `BACKUP_ORDER` empty. One pass was added,
`pair_logo_with_title`, which puts the ESS mark in a row with the title block so it centres against
what the blue rule spans — `.sbody` centres its content, so no fixed offset can track the title
across slides.

`extra/talk.css` is the talk's stylesheet with one block appended at the end, holding only the rules
these two slides need.

Both slides are single static sections: **no build steps**, so the PDF has one page per slide and
cannot overrun the two-slide limit by accident.

## Content

Facts come from `input/abstract-easyscience.pdf` (the accepted abstract) and
`input/poster-easyscience.pdf`, which is also where the five photographs were extracted from.

`tmp/` holds the other speakers' flash decks, kept for reference. Neither folder is used by the
build.

## Still to confirm

- The country flags are Unicode emoji, drawn by the presenting machine's own emoji font. The PDF
  embeds them, so presenting from `flash.pdf` avoids any surprise on a borrowed laptop.
