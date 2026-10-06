# Talk outline — What AI can change in crystallographic computing: early lessons from building a diffraction engine from scratch (v06 in progress, 2026-09-04)

30 minutes target · progressive disclosure via auto-animate steps · one idea per slide · no source code on main slides.
Order: motivation → what we built → does it work → why C++ → completeness → how it was built → baby-sitting → lessons → backup.

| # | steps | slide |
|---|---|---|
| 0 | 1 | ESS divider |
| 1 | 3 | What AI can changein crystallographic computing |
| 2 | 2 | AI in scientific software |
| 3 | 3 | How AI enters software development |
| 4 | 3 | The experiment |
| 5 | 3 | Why? |
| 6 | 2 | The existing approach |
| 7 | 3 | Where it falls short |
| 8 | 4 | What modern analysis needs |
| 9 | 4 | One engine, four products |
| 10 | 4 | Who is it for |
| 11 | 1 | Built on |
| 12 | 2 | Pattern calculation vs FullProf |
| 13 | 2 | Structure refinement vs FullProf |
| 14 | 2 | Speed vs FullProf |
| 15 | 2 | One pattern calculation: a near tie |
| 16 | 3 | A fit is not one calculation |
| 17 | 3 | Three ways to get derivatives |
| 18 | 3 | Derivatives for free |
| 19 | 2 | Exact derivatives change the fit |
| 20 | 2 | How complete is the engine? |
| 21 | 3 | Four agents, one human |
| 22 | 3 | An agent that can read the tests will pass the tests |
| 23 | 4 | Tests are not the only gate |
| 24 | 3 | Written down, or it did not happen |
| 25 | 3 | Do's and don'ts |
| 26 | 3 | Ways of working I tried |
| 27 | 2 | Two impressions |
| 28 | 2 | Maybe I was not explaining it clearly enough… |
| 29 | 5 | What the LLM said |
| 30 | 2 | What they have in common |
| 31 | 5 | What you need before you start |
| 32 | 2 | I did not write this code |
| 33 | 1 | I deliberately did not read the code |
| 34 | 1 | Thank you |
| 35 | 1 | ESS divider |
| 36 | 1 | For questions |
| 37 | 1 | And Rust? |
| 38 | 1 | Why a Python Dual class is not the same |
| 39 | 1 | crysta vs EasyDiffraction today |
| 40 | 1 | The full stack |
| 41 | 2 | Every core, eight numbers at a time |
| 42 | 2 | Same answer, every time |
| 43 | 2 | Where Python still wins |
| 44 | 2 | Measure the process, delete the ritual |
| 45 | 2 | By the numbers |
| 46 | 2 | Not there yet |
| 47 | 4 | In one sentence |
| 48 | 1 | What it looks like |
| 49 | 2 | Risks and concerns |
| 50 | 2 | Opportunities |
| 51 | 2 | Small, instant, everywhere |

Main deck: 34 stacks, 92 steps · total incl. backup: 52 stacks, 122 steps.

## Still to fill
- Backup: product screenshot (web or desktop app on a real dataset).
- 7.4: name of the IUCr 2026 speaker whose slide is quoted.
- 4.1: pattern-vs-FullProf overlay chart.
- Photos and logos: replace Wikimedia URLs with local files.
- Title slide: event line.

## Removed from the main deck (in backup or speaker notes)
- Every core / same answer / where Python wins (SIMD, threads, reproducibility); measure the process; by the numbers; not there yet; the one-sentence summary; Rust comparison; the C++ template code and the Python Dual class comparison; the crysta-vs-EasyDiffraction feature chart; the full tool stack; SIMD widths and CI reproducibility gates; the verdict ledger's real row format; the six IUCr microsymposium titles in full.
