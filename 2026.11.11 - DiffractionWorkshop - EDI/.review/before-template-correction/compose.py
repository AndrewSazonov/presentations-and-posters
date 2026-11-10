#!/usr/bin/env python3
"""Assemble a workshop draft; original slides remain in source-slides/ and slides/library/."""
from pathlib import Path
import json,re,html
HERE=Path(__file__).parent
S=HERE/'slides';S.mkdir(exist_ok=True)
inv=json.loads((HERE/'source-slides/inventory.json').read_text())
bytitle={r['title']:r for r in inv}
outline=[]
def ico(name):return f'<i class="fa-{name}"></i>'
def note(text,sources=''):
 return '<aside class="notes">'+html.escape(text)+(('<br><br>Sources: '+html.escape(sources)) if sources else '')+'</aside>'
def new(file,title,body,close,seconds,notes='',sources='',kind='new'):
 # Every conclusion gets its own click, following the source deck's convention.
 content=f'<h3>{title}</h3><div class="work-content" data-id="work-content">{body}</div>'
 steps=f'<section data-auto-animate data-auto-animate-unmatched="false" data-auto-animate-restart>{content}</section>'
 if close:steps+=f'<section data-auto-animate data-auto-animate-unmatched="false">{content}<p class="statement" data-id="close">{close}</p>{note(notes,sources)}</section>'
 else:steps=steps.replace('</section>',note(notes,sources)+'</section>')
 (S/file).write_text('<div class="external-slide">\n<section>\n'+steps+'\n</section>\n</div>\n')
 outline.append(dict(file=file,title=re.sub('<[^>]*>','',title),seconds=seconds,kind=kind,sources=sources))
def reuse(file,title,seconds,rename=None,notes=''):
 r=bytitle[title];text=(S/r['path']).read_text()
 if rename:text=text.replace(title,rename)
 if notes:text=text.replace('</aside>',html.escape(' '+notes)+'</aside>')
 if file=='12_needs.html':
  text=text.replace('Functionality the ESS instruments need and no single program has;','Functionality across instruments and experiments;')
  text=text.replace('for the ESS instruments','across facilities and experiments').replace('No existing solution <span class="blue">offers all three</span>.','The aim is to bring <span class="blue">all three together</span>.')
 (S/file).write_text(text)
 outline.append(dict(file=file,title=rename or title,seconds=seconds,kind='adapted' if rename or file=='12_needs.html' else 'reused',sources=r['source']))
def bullets(rows):
 return '<div class="w-list">'+''.join(f'<p>{ico(k)}<span>{t}</span></p>' for k,t in rows)+'</div>'
def panels(items,cls=''):
 return f'<div class="w-panels {cls}">'+''.join(f'<div class="w-panel"><h4>{ico(k)} {t}</h4><p>{d}</p></div>' for k,t,d in items)+'</div>'
def shot(src,label,cls=''):
 return f'<figure class="w-shot {cls}"><figcaption>{label}</figcaption><img src="images/current/{src}" alt="{html.escape(re.sub("<[^>]*>","",label))}"></figure>'
DOC='http://127.0.0.1:8873/'
# Holding slide and cover preserve the original visual identity.
(S/'00_divider.html').write_text((S/bytitle['00_divider']['path']).read_text())
cover='''<section class="cover"><div class="titlebox"><h3 class="deck-title"><span class="blue">EasyDiffraction</span> and <span class="blue">crysta</span></h3><p class="subtitle">From reusable crystallographic libraries<br>to a shared project and workflow</p></div><p class="author">Andrew Sazonov · andrew.sazonov@ess.eu</p><p class="affil">European Spallation Source (ESS)<br>Data Management and Scientific Computing (DMSC)</p><p class="event">Advanced Powder Diffraction · Uppsala University · Nov 2026</p>'''+note('Day 1, 30-minute introduction. Explain why EasyDiffraction was built, what has changed with crysta and edi, and how participants can choose an interface for the hands-on sessions. ')+'</section>'
(S/'01_title.html').write_text('<div class="external-slide"><section>'+cover+'</section></div>')
outline.append(dict(file='01_title.html',title='EasyDiffraction and crysta',seconds=30,kind='adapted',sources='STAP cover'))
# 1. Motivation and the earlier route.
reuse('10_many-tools.html','Diffraction analysis: many tools',40)
reuse('11_user-friction.html','What users run into',65,rename='What users ran into',notes='Historical examples motivating the project; the screenshots do not claim the current installation or operating-system support of those other programs.')
reuse('12_needs.html','Needs',45)
reuse('13_libraries.html','Built on existing libraries',65,notes='This is the original pre-crysta approach. CrysFML, CrysPy and PDFfit2 are historical calculation engines in this part of the talk, not engines currently exposed by edi.')
reuse('14_dependencies.html','What we rely on',65,rename='Earlier software stack',notes='Explain the integration trade-off respectfully: reuse validated physics, but adapt differing data models, parameter conventions and fitting behaviour. The new product still uses third-party libraries; it is not dependency-free.')
reuse('15_ux.html','Several years of improving UI/UX',40)
# 2. New scientific core and current examples.
new('20_architecture.html','The new scientific core',panels([
 ('cubes','EasyDiffraction · edi','Projects, interfaces, parameters and results'),
 ('microchip','crysta · C++20','Diffraction calculation and refinement, with Python bindings')],'w-core')+bullets([('folder-open','One saved project holds the model, observations and analysis choices.'),('arrows-rotate','Open it visually, script it, or run it from a terminal.')]),'One project model across the product.',65,'Separate the public name EasyDiffraction from package/code name edi and the calculation/refinement engine crysta. A complete project can be exchanged; controls and file-saving behaviour differ between interfaces.',DOC+'user-guide/; '+DOC+'about/')
new('21_advantages.html','What the new approach changes','''<div class="w-compare"><div><h4>Earlier library integration</h4><p>Reuse several established engines</p><p>Translate models and conventions</p><p>Capabilities depend on the engine</p></div><div><h4>crysta + EasyDiffraction</h4><p>Develop the model and refinement together</p><p>Keep one project across interfaces</p><p>Connect fast fits to inspection and reports</p></div></div>''','A more connected path from model to checked result.',60,'These are architectural advantages and product goals, not a claim that the new implementation already matches every capability of the old libraries. Speed evidence follows with a specific benchmark.','STAP slides Built on existing libraries and What we rely on; '+DOC+'user-guide/')
new('22_physics.html','Current diffraction coverage',bullets([
 ('wave-square','<span class="blue">Powder:</span> CW neutrons, TOF neutrons and X-rays'),
 ('cubes','<span class="blue">Neutron single crystals</span> with extinction models'),
 ('magnet','<span class="blue">Commensurate magnetic structures</span>'),
 ('layer-group','Multiple structures, experiments and scan datasets'),
 ('calculator','Single, joint, sequential and independent fits')]),'Choose the model that matches the measurement.',70,'Current status is from the forthcoming Features catalogue. For magnetic work, opening a saved project preserves moments; creating magnetic structures by hand remains work in progress. Powder diffraction is the workshop focus. Do not imply X-ray single-crystal support.',DOC+'user-guide/features/')
new('23_powder.html','Powder refinement in more detail',panels([
 ('chart-line','Profiles and corrections','CW pseudo-Voigt and asymmetry<br>TOF Jorgensen-family profiles<br>Absorption and preferred orientation'),
 ('sliders','Models and fit assessment','Isotropic and anisotropic displacement<br>Background estimation and excluded regions<br>Uncertainties, correlations and R factors')]),'Inspect both the pattern and the parameters.',55,'Examples, not a complete list. Current CW models include direct pseudo-Voigt, TCH, Bérar–Baldinozzi and Finger–Cox–Jephcoat. TOF includes Jorgensen, Jorgensen–Von Dreele and symmetric pseudo-Voigt. Ikeda–Carpenter is planned, not current. Weighted least squares with Levenberg–Marquardt is current; MCMC is not current.',DOC+'user-guide/features/; '+DOC+'physics/')
new('24_application.html','A complete refinement workspace',shot('wish-five-bank-after-fit.png','NCAF · WISH / ISIS · five detector banks · joint fit · bank 5_6'),'Measured data, model and fitted parameters together.',75,'Show measured/calculated patterns, background, Bragg markers, residual and selected parameters. Mention that the picture is a five-bank joint fit, and this view shows one bank. Do not use the time from the screenshot as a benchmark.','2026.11.17 poster assets; abstract-11-2.pdf')
new('25_scans.html','From one pattern to a measurement series',shot('scan-map.png','Co₂SiO₄ · D20 / ILL · 213 datasets · intensity map'),'Fit a series and follow how the structure changes.',70,'The application provides map, stacked-pattern and parameter-evolution views. Sequential and independent scans are available. The Python interface can run an existing saved scan project but does not currently define a scan; map/stacked plotting is not identical across interfaces.',DOC+'user-guide/features/; '+DOC+'application/tutorials/cases/pd-neut-cwl_cosio-d20_scan-213f/')
new('26_magnetism.html','Inspect the magnetic structure','<div class="w-magnetic">'+('<figure class="w-shot"><figcaption>Co₂SiO₄ · D20 / ILL · 2.3 K · after fitting</figcaption><div class="w-magnet-frame"><img class="model" src="images/current/magnetic-after-fit-detail.png" alt="Refined commensurate magnetic structure and moment arrows"><img class="legend" src="images/current/magnetic-gui-legend.png" alt="GUI atom legend: Co, Si and O"></div></figure>')+bullets([('magnet','Commensurate magnetic refinement'),('eye','Moment arrows in the application'),('folder-open','Start from a saved magnetic project')])+'</div>','Connect the fitted pattern with a structural picture.',55,'Available commensurate magnetism goes beyond the October STAP deck. Magnetic CIF import and manual construction are not complete. Python add_from_edi_path currently drops moments; Project.load retains them. This is why the suggested entry point is a complete saved project.',DOC+'user-guide/features/#magnetic-structure-model; '+DOC+'user-guide/features/#defining-structures-and-experiments')
new('27_verification.html','Comparison with an independent program','<div class="w-verification">'+shot('verification-vs-fullprof-wide.png','NCAF · WISH banks 2+9 · 48 refined parameters')+'<div><p class="w-metric">0.69 σ</p><p>largest parameter difference</p><p class="w-metric">0.05 σ</p><p>median parameter difference</p><p class="w-small">σ combines the two reported standard uncertainties.</p></div></div>','Every parameter is within 0.69 combined σ of FullProf.',75,'This is the earlier two-bank, 48-parameter verification. Do not combine its statistics with the following five-bank, 193-parameter timing case. It compares fits to the same observations; it is not an independent significance test. The original traces have been replotted without refitting.','LENS/STAP Agreement of calculated patterns and Agreement of refined parameters; poster verification')
new('28_speed.html','Speed: a full TOF refinement','''<div class="w-timings"><div class="w-time crysta"><p>crysta</p><strong>≈3 s</strong></div><div class="w-time"><p>FullProf</p><strong>20 s</strong></div></div><div class="w-bench">NCAF · WISH / ISIS · five banks · 193 parameters<br>Same initial values · default six-core VISA Linux VM</div><p class="w-small">Refined structural parameters agree within 0.3 combined σ.</p>''','A selected benchmark for structure refinement.',65,'Use the abstract figures: approximately 3 seconds with crysta and 20 seconds with FullProf. Same initial values, default six-core VISA Linux VM used as an ESS remote desktop. This is one selected benchmark, not a general speed guarantee. The older STAP timing comparison remains in backup as a separate experiment.','abstract-11-2.pdf; 2026-early-science-poster-easydiffraction-sazonov')
# 3. Interfaces and workshop choices.
routecols=[]
for title,icon,children in [('Application','docs-application',[('Web application','No application installation'),('Desktop application','Local files · optional AI')]),('Python library','docs-python',[('Jupyter notebooks','Cells, plots and narrative'),('Python scripting','Your own analysis pipeline')]),('Command line','docs-cli',[('Standalone tool','No Python installation'),('Python package CLI','No Python scripting')])]:
 routecols.append(f'<div class="w-route"><h4>{ico(icon)} {title}</h4><div class="w-route-pair">'+''.join(f'<div><strong>{a}</strong><span>{b}</span></div>' for a,b in children)+'</div></div>')
new('30_six-interfaces.html','One project, six ways to work','<div class="w-routes">'+''.join(routecols)+'</div><div class="w-shared">'+ico('folder-open')+' Shared EasyDiffraction project <span>structures · experiments · analysis · results</span></div><div class="w-engine">crysta <span>calculation and refinement</span></div>','Choose an interface without rebuilding the scientific model.',100,'These are six user routes grouped into three interface families. CLI means commands, including python -m edi, without writing Python code. Interface coverage differs: standalone currently fits only; Python-package CLI has more commands. Web has no built-in assistant. This diagram shows shared scientific inputs and engine, not identical controls or availability.',DOC+'user-guide/; '+DOC+'application/; '+DOC+'python/; '+DOC+'cli/')
new('31_graphical.html','Web and desktop application',panels([
 ('globe','Web application','Open in a browser<br>Try an example without installation<br>Download a complete project to keep it'),
 ('display','Desktop application','Native file access<br>Local project folders and archives<br>Optional built-in AI assistant')]),'The same visual workflow, with different file access.',50,'Both applications have the same layout and scientific workflow. Browser saving differs: Chrome/Edge may retain chosen local handles, Safari/Firefox use browser storage plus zip export. New projects/examples begin in browser storage in all browsers. The preview is under active development. Desktop installer links are not yet published in the local docs.',DOC+'application/browser/; '+DOC+'application/desktop/')
new('32_python.html','Notebooks and Python scripts','''<div class="w-python"><div><h4>Jupyter notebooks</h4><p>Explore one step at a time</p><p>Keep the explanation beside the fit</p><h4>Python scripts</h4><p>Combine with your own data tools</p><p>Repeat a defined analysis</p></div><pre><code class="language-python">import easydiffraction as edi

path = edi.download_data("pd-neut-cwl_y2o3-spodi")
project = edi.Project.load(path)
result = project.analysis.fit()
project.report.save_html("fit.html")</code></pre></div>''','The same Python API in two working styles.',70,'This slide is an orientation, not a live coding lesson. Current calls verified in Python data, reference and report docs. The current setup imports easydiffraction as edi; the command-line module remains edi. Follow the preview setup page rather than copying the old PyPI command.',DOC+'python/; '+DOC+'python/data/; '+DOC+'python/reports/; '+DOC+'python/setup/')
new('33_cli.html','Command line without writing Python',panels([
 ('terminal','Standalone executable','<code>edi fit project/</code><br>No Python installation<br>Currently: fitting saved projects'),
 ('python','Python package command line','<code>python -m edi fit project/</code><br>Fit, calculate, report, export and more<br>Python environment · no Python script')]),'Prepare a project once, then run it from a terminal.',65,'The standalone and Python-package CLIs are not feature-equivalent. The Python package also has undo, collection tools, downloads and streaming fit progress. Both use saved projects. The standalone installer is documented but downloads are not yet published in this preview.',DOC+'cli/; '+DOC+'cli/reference/; '+DOC+'cli/python/')
new('34_ai-desktop.html','AI assistance inside the desktop app',shot('ai-assistant-fitted.png','Built-in assistant · La₀.₅Ba₀.₅CoO₃ · HRPT / PSI · after fitting'),'Ask, inspect the actions, and check the resulting fit.',70,'Optional desktop component. It can explain a fit, suggest parameter stages and carry out supported actions in the open project. Show actions exposes actions on app controls; Stop interrupts. Requires internet and a compatible ChatGPT account. No built-in assistant in the web app. Avoid promising autonomous scientific correctness.',DOC+'user-guide/ai-assistant/; '+DOC+'application/tutorials/assistant/')
new('35_ai-external.html','AI-ready beyond the built-in assistant','''<div class="w-ai-flow"><div><h4>Provide</h4><p>Structure + measured data</p><p>Experimental conditions</p><p>Docs, examples and fit stages</p></div><div><h4>Ask for</h4><p>A runnable Jupyter notebook</p><p>or a saved EasyDiffraction project</p><p>for the app or command line</p></div><div><h4>Check</h4><p>Run each fit stage</p><p>Inspect residuals and correlations</p><p>Compare with the worked example</p></div></div><p class="w-small">Documentation for assistants: <span class="blue">llms.txt</span> and plain Markdown reference pages</p>''','An external assistant can prepare work for any interface.',70,'Based on the user-guide matrix and the Python/CLI assistant tutorials. The same saved project can be opened in web or desktop. The supplied La/Ba example explicitly links their Biso values after inspecting near-perfect correlation. Built-in desktop control and external preparation are distinct routes. Do not imply remote AI integration inside a browser.',DOC+'user-guide/ai-assistant/; '+DOC+'python/tutorials/assistant/; '+DOC+'cli/tutorials/assistant/; '+DOC+'llms.txt')
new('36_software.html','Practical software features',panels([
 ('code','Open source','Inspect the code and report issues'),
 ('display','Cross-platform','Web · macOS · Windows · Linux'),
 ('cubes','Packaged desktop app','Application dependencies included'),
 ('folder-open','Portable projects','Readable files · folder or archive'),
 ('book-open','Worked examples','Guides, notebooks and reference data'),
 ('file-lines','Reports and provenance','HTML and CIF · retain analysis choices')]),'Keep the result together with the choices behind it.',65,'Inspired by the old landing page and both posters; current availability checked in new docs. Code BSD 3-Clause; desktop/browser app GPLv3, with dependency licences retained. Desktop and standalone downloads are not yet published, and signing is work in progress. Do not imply installers are already publicly downloadable. PDF reports are application-only.',DOC+'about/licence/; '+DOC+'application/desktop/; '+DOC+'user-guide/analysis-workflow/report/; https://easydiffraction.org/')
new('37_status.html','Available, planned and proposed','''<div class="w-status"><div><h4>Available</h4><p>Powder Rietveld refinement</p><p>Joint fits and scan analysis</p><p>Commensurate magnetism</p></div><div><h4>Planned</h4><p>Total scattering / PDF</p><p>Polarised neutrons and twins</p><p>Incommensurate structures</p></div><div><h4>Proposed</h4><p>Le Bail and Pawley fitting</p><p>2D Rietveld fitting</p><p>FullProf / GSAS-II / TOPAS import</p></div></div>''','Current coverage and future priorities are different lists.',60,'The forthcoming feature catalogue distinguishes available, partial, work in progress, planned and proposed. This slide gives selected examples only. MCMC sampling is planned for Python, proposed for app/CLI. Ikeda–Carpenter and instrument-resolution separation are planned. Magnetic manual creation remains work in progress.',DOC+'user-guide/features/')
new('38_hands-on.html','Choose a route for the hands-on sessions',panels([
 ('book-open','Shorter session','Start with a worked powder example<br>Open, inspect, choose parameters, fit<br>Keep the saved project and report'),
 ('sliders','Longer session','Continue in your preferred interface<br>Try joint fitting or a measurement series<br>Inspect correlations and explain the result')]),'Start with one example; extend the analysis when it is clear.',60,'Suggested scope for the workshop, not a confirmed timetable. Participants choose one software per day. Offer GUI-first and notebook/CLI paths through the same example. AI is optional; no account should be necessary for the core exercise. Prepare local examples in case networking fails.', 'User workshop description; '+DOC+'user-guide/tutorials/; '+DOC+'python/tutorials/; '+DOC+'cli/tutorials/')
new('39_takeaway.html','EasyDiffraction for your next analysis',bullets([
 ('cubes','A clear workflow built on experience with existing libraries'),
 ('microchip','crysta for calculation and refinement'),
 ('folder-open','One project across six ways of working')])+'''<p class="w-link"><a href="https://app.easydiffraction.org/">app.easydiffraction.org</a></p>''','Try a worked example, then bring a case from your own experiment.',35,'Close with an invitation to the hands-on sessions. Web and current docs are under active development. Recheck download and documentation links before the workshop. Do not replace old easydiffraction.org with localhost in audience-facing copy.',DOC+'user-guide/')
new('40_survey.html','Help shape EasyDiffraction','<div class="w-survey"><div class="w-survey-placeholder"><i class="fa-display"></i><p>Survey page screenshot</p><span>Placeholder · About page survey to follow</span></div><div><p>Please take a moment<br>to fill in the survey.</p><p class="w-small">Your experience with the six ways of working will help guide development.</p></div></div>','Please share your feedback.',45,'Keep this slide on screen while participants complete the survey. The actual survey screenshot and its confirmed public link/QR will replace the marked placeholder when the About page survey is available. No responses are shown or invented.','User request: placeholder for the forthcoming survey under '+DOC+'about/')

# Optional audience poll, kept in backup rather than in the 30-minute route.
poll='<table class="w-poll"><thead><tr><th>Way to work</th><th>Interested?</th><th>Tried?</th><th>Easy to use?</th></tr></thead><tbody>'+''.join(f'<tr><td>{name}</td><td>○</td><td>○</td><td>○</td></tr>' for name in ['Web application','Desktop application','Jupyter notebooks','Python scripting','Standalone command-line tool','Python-package command line'])+'</tbody></table>'
new('90_survey.html','Six ways to work: audience feedback',poll,'Which route would you choose for the hands-on session?',0,'Optional show-of-hands or questionnaire slide. These are questions, not measured results. Ask interest, previous use and ease of use separately for each of the six routes.','User interface list',kind='optional')
# Add a source/provenance index, with old coverage clearly labelled as historical.
(HERE/'outline.json').write_text(json.dumps(outline,indent=2,ensure_ascii=False))
main=[r['file'] for r in outline if r['kind']!='optional']
# Keep old content in one separate deck, including old benchmarks and discontinued feature claims.
backup=['00_divider.html','90_survey.html']
for r in inv:
 if r['title'] in ['00_divider','EasyDiffraction and crysta']:continue
 backup.append(r['path'])
b=HERE/'build.py';text=(HERE.parent/'2026.10.20 - Diff STAP - Edi & Crysta/build.py').read_text()
a=text.index('SECTION_TITLES =');z=text.index('\nHEAD =',a)
text=text[:a]+'''SECTION_TITLES = {
    "10_many-tools.html": "Why this approach",
    "20_architecture.html": "crysta + EasyDiffraction",
    "30_six-interfaces.html": "Choose how to work",
}
ORDER = '''+repr(['00_divider.html']+main)+'''\nBACKUP_ORDER = '''+repr(backup)+'''\n'''+text[z:]
text=text.replace("'Why new software': 'lightbulb',","'Why new software': 'lightbulb',\n    'Why this approach': 'lightbulb',\n    'crysta + EasyDiffraction': 'microchip',\n    'Choose how to work': 'display',")
text=text.replace('EasyDiffraction and crysta — reusing crystallographic libraries, and building our own','EasyDiffraction and crysta — Advanced Powder Diffraction Workshop')
text=text.replace('<link rel="stylesheet" type="text/css" href="extra/edi.css">','<link rel="stylesheet" type="text/css" href="extra/edi.css">\n    <link rel="stylesheet" type="text/css" href="extra/workshop.css">')
text=text.replace("transition: 'slide',","transition: new URLSearchParams(location.search).has('review') ? 'none' : 'slide',\n          autoAnimate: !new URLSearchParams(location.search).has('review'),")
text=text.replace('        chunk = body(text)', "        chunk = body(text)\n        if not titles and name.startswith('library/'):\n            origin = 'NOBUGS · Sep 2026' if 'nobugs-' in name else 'STAP · 20 Oct 2026'\n            chunk = re.sub(r'(<h3\\b[^>]*>)', lambda m: '<p class=\"eyebrow\">Source slide · ' + origin + '</p>' + m.group(1), chunk)")
b.write_text(text)
print(len(main),'content slides;',len(backup),'backup slides;',sum(r['seconds'] for r in outline),'seconds allocated before dividers/questions')
