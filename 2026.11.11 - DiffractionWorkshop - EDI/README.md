# EasyDiffraction and crysta — Advanced Powder Diffraction Workshop

Day 1 draft for a 30-minute introduction. This broad selection includes the requested original STAP slides and can be trimmed after review.

## Design and source

The deck loads only the original STAP `style.css`, `talk.css` and `edi.css`, unchanged. There is no workshop layout stylesheet. Reused slides preserve their original structures and reveal sequences. Updated slides use those same components: boxed lists, the two-column project cards, case tags, screenshot slots, dark agreement figures, parameter rows, speed bars and stack diagrams.

`template-map.json` records which source template each adapted slide uses. The former custom layouts are retained privately under `.review/before-template-correction/` for recovery only and are not loaded.

## Open and edit

- `index.html`: main presentation, speaker notes and source references.
- `backup.html`: additional original slides plus an optional questionnaire.
- `source-stap.html`: unchanged original STAP deck.
- `slides/`: editable selected slides; `slides/library/` holds the copied originals.
- `source-slides/`: original fragments and provenance inventory.

Open `index.html` directly or through a local server. Arrow keys advance; **S** opens speaker notes; **Esc** opens the overview; **F** opens full screen. Run `python3 build.py` after editing. `python3 build.py --watch` rebuilds on changes.

`compose.py` adapts the STAP templates and regenerates the selected new slide files. It preserves the cover and already selected legacy slide files. Run it only when intentionally regenerating those adapted files. Use the existing STAP components for later edits rather than adding a new layout system.

## Current selection

There are 37 numbered slides, including three section dividers, plus the ESS holding screen. The individual content allocations sum to 29 min 50 s, before brief section transitions or audience responses. This is a broad review selection; allow a little trimming for a strict 30-minute slot.

The requested source slides are in the main sequence: library capabilities, UX review, three ways to work, a possible multi-engine future, the test case, both agreement slides, the two extended functionality slides, updated work in progress and the online tutorials.

The possible multi-engine future is followed immediately by the current crysta-only diagram. The two-bank / 48-parameter agreement case is kept separate from the five-bank / 193-parameter timing benchmark.

| Editable file | Topic | Time |
| --- | --- | --- |
| `01_title.html` | EasyDiffraction and crysta | 0:30 |
| `10_many-tools.html` | Diffraction analysis: many tools | 0:40 |
| `11_user-friction.html` | What users ran into | 1:05 |
| `12_needs.html` | Needs | 0:45 |
| `13_libraries.html` | Built on existing libraries | 1:05 |
| `13b_library-capabilities.html` | What each library brings | 0:30 |
| `14_dependencies.html` | Earlier software stack | 1:05 |
| `15_ux.html` | Several years of improving UI/UX | 0:40 |
| `16_ux-review.html` | Reviewed by UX experts | 0:25 |
| `17_three-interfaces.html` | Three ways to run the same workflow | 0:30 |
| `19_future.html` | A possible future: several engines | 0:35 |
| `20_architecture.html` | The current crysta-only approach | 0:45 |
| `21_advantages.html` | What the new approach changes | 1:00 |
| `22_physics.html` | Current functionality: diffraction | 1:10 |
| `23_powder.html` | Current functionality: analysis | 0:55 |
| `24_application.html` | A complete refinement workspace | 1:15 |
| `25_scans.html` | From one pattern to a measurement series | 1:10 |
| `26_magnetism.html` | Inspect the magnetic structure | 0:55 |
| `26b_test-case.html` | One of many test cases | 0:35 |
| `27_verification.html` | Agreement of calculated patterns | 0:40 |
| `27b_parameters.html` | Agreement of refined parameters | 0:35 |
| `28_speed.html` | Speed: a full TOF refinement | 1:05 |
| `30_six-interfaces.html` | One project, six ways to work | 1:40 |
| `31_graphical.html` | Web and desktop application | 0:50 |
| `32_python.html` | Notebooks and Python scripts | 1:10 |
| `33_cli.html` | Command line without writing Python | 1:05 |
| `34_ai-desktop.html` | AI assistance inside the desktop app | 1:10 |
| `35_ai-external.html` | AI-ready beyond the built-in assistant | 1:10 |
| `36_software.html` | Practical software features | 1:05 |
| `37_status.html` | Work in progress / Next steps | 1:00 |
| `38_hands-on.html` | Choose a route for the hands-on sessions | 1:00 |
| `39_online.html` | Test online without installation | 0:35 |
| `39_takeaway.html` | EasyDiffraction for your next analysis | 0:25 |
| `40_survey.html` | Help shape EasyDiffraction | 0:45 |
| `90_survey.html` | Six ways to work: audience feedback | 0:00 |

## Current functionality and tutorials

Current features were checked against the rebuilt local documentation at `http://127.0.0.1:8873/`. The scientific overview follows that catalogue; old feature coverage and roadmap slides in backup are historical source material.

The updated online-entry slide uses the same 23 tutorials for the application and Python/Colab. The catalogue contains examples from 11 named facilities and 15 named physical instruments after merging FRM II / MLZ and excluding blank laboratory labels and McStas software from facility/instrument counts. Simulations remain included in the tutorial count; BEER is explicitly labelled simulated. The speaker notes record the count basis.

The public documentation links target the forthcoming `https://enhantica.github.io/edi/` pages. The local preview supplied the current content. Recheck public links when the site is published.

The built-in AI assistant is desktop-only. External assistants can prepare projects and notebooks. Standalone CLI currently fits saved projects; the Python package's CLI supports the broader command set without Python scripting.

The final slide remains an explicitly labelled survey placeholder, as requested. Replace it with the actual About-page survey screenshot and confirmed link when available.
