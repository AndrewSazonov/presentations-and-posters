# EasyDiffraction and crysta — Advanced Powder Diffraction Workshop

Day 1 presentation, revised to the presenter’s 10 November review. There are 30 content slides, an opening outline and three section transitions, plus the unnumbered ESS holding screen. The speaking allocations total about 27 minutes, leaving about three minutes for transitions or questions.

## Open and edit

Open `index.html` directly or through a local server. Arrow keys advance, **S** opens notes, **Esc** shows the overview, and **F** enters full screen.

`slides/` contains the editable slide sources. `build.py` assembles them into `index.html` and `backup.html`. `compose.py` regenerates adapted slides and then applies `review_updates.py`, which implements the latest review and applies the wording in `text_updates.py`. Run `python3 compose.py` followed by `python3 build.py` when intentionally regenerating adapted slides. Run only `python3 build.py` after a manual slide edit.

## Design and animation

The presentation retains the STAP stylesheets unchanged. New slides reuse its lists, screenshot slots, columns, diagrams, icons and timing bars.

The modern-analysis slide is copied exactly from LENS slide 17, changing only the title. Meet crysta retains the original two-state STAP animation: the large engine box moves into the original multi-engine diagram. Its caption marks this as a possible future. The following slide removes the other engines, centres crysta, adds CLI, expands six routes above the three interface families, then replaces the scientific layers with interface screenshots.

The cover uses the original event / author / title reveal and a single-line subtitle. The original opening outline and section transitions are retained alongside the chapter labels. The 30 content slides keep the requested order. Omitted material is retained in `backup.html`.

## Scientific scope and sources

Current features and links follow the published documentation at https://enhantica.github.io/edi/. The application index lists 25 tutorials, including its built-in-assistant walkthrough. The PDF and Bayesian output figures come from the earlier library documentation and are shown in the historical part of the talk. Both are existing capabilities to port to crysta, rather than new methods to develop.

The two-bank NCAF verification case remains separate from the five-bank benchmark. The latter shows approximately 3 s with crysta versus 20 s with FullProf, 193 parameters, identical initial values and the six-core VISA Linux machine specified in the abstract. Its five input banks contain 20,475 measured points. Bar lengths use a linear scale, with no top time axis.

The taurine image is an actual edi GUI capture. Images and figures retain their source data. References and qualifications are recorded in speaker notes.

The last slide uses the presenter-selected Success Kid “We need your feedback” image. The survey QR code points to http://easydiffraction.org/about/survey/, which the presenter will publish later. The selected image source is recorded in the slide notes.

## Running order

| Content slide | Topic |
| --- | --- |
| 1 | EasyDiffraction and crysta |
| 2 | One facility, two host countries |
| 3 | Diffraction analysis: many tools |
| 4 | Limits of existing tools |
| 5 | What EasyDiffraction should offer |
| 6 | Built on existing libraries |
| 7 | What each library brings |
| 8 | Earlier software stack |
| 9 | Several years of improving UI/UX |
| 10 | Reviewed by UX experts |
| 11 | The library grew beyond standard refinement |
| 12 | What modern diffraction analysis needs |
| 13 | Meet crysta |
| 14 | One project, six ways to work |
| 15 | One of many test cases |
| 16 | Agreement of calculated patterns |
| 17 | A fit is not one calculation |
| 18 | Speed: a full TOF refinement |
| 19 | Current functionality: data and models |
| 20 | Current functionality: fitting and results |
| 21 | A complete refinement workspace |
| 22 | From one pattern to a measurement series |
| 23 | Inspect the magnetic structure |
| 24 | Also single-crystal diffraction |
| 25 | AI assistance inside the desktop app |
| 26 | AI-ready beyond the built-in assistant |
| 27 | Practical software features |
| 28 | Work in progress / next steps |
| 29 | Plan for Thursday and Friday |
| 30 | EasyDiffraction needs your feedback |
