"""Apply the presenter's 10 November review to the original STAP components.
Executed by compose.py, using its writing helpers and template metadata.
"""
import copy as _copy
import xml.etree.ElementTree as E
ROOT=R.parent
SOURCE_MATERIAL=R/'data/source-material'

def leaves(text):
 result=[];depth=0
 for m in re.finditer(r'<section\b[^>]*>|</section>',text):
  if m[0].startswith('</'):
   depth-=1
   if depth==1:result.append(text[start:m.start()])
  else:
   if depth==1:start=m.end()
   depth+=1
 return result

def svgstr(el):
 s=E.tostring(el,encoding='unicode')
 s=re.sub(r' xmlns:ns\d+="[^"]*"','',s)
 return re.sub(r'ns\d+:','',s)

def set_source(file,title,content,template,seconds):
 (S/file).write_text(content)
 meta[file]=dict(file=file,title=title,kind='adapted',seconds=seconds,sources=template,template=template)
 mapping.append(dict(file=file,template=template))

# 1. Original event / author / title animation, with a one-line subtitle.
cover=(ROOT/'2026.10.20 - Diff STAP - Edi & Crysta/slides/01_title.html').read_text()
cover=cover.replace('STAP Meeting &middot; Lund &middot; 20 Oct 2026','Advanced Powder Diffraction &middot; Uppsala University &middot; Nov 2026')
cover=cover.replace('Andrew Sazonov</p>','Andrew Sazonov · andrew.sazonov@ess.eu</p>')
cover=re.sub(r'Reusing crystallographic libraries,\s*and building our own','From reusable libraries to an in-house engine',cover)
set_source('01_title.html','EasyDiffraction and crysta',cover,'STAP animated cover',30)

# 2. ESS map from the specified NOBUGS slide, in the standard STAP figure slot.
shutil.copy2(ROOT/'2026.09.21 - NOBUGS - GUI-ESS/assets/maps/oresund.svg',R/'images/current/oresund.svg')
mapbox='<div class="shotbox" data-id="map" style="--shot-h:405px;--shot-w:750px;background:transparent;border:0"><img src="images/current/oresund.svg" alt="ESS in Lund, Sweden, and DMSC in Lyngby, Denmark"></div>'
write('02_facility.html','One facility, two host countries',[mapbox],'ESS in <span class="blue">Lund</span> · DMSC in <span class="blue">Lyngby</span>, near Copenhagen.','NOBUGS ESS map + STAP shotbox',extra_note='Source: 2026.09.21 - NOBUGS - GUI-ESS/index.html#/2/1. The map is copied unchanged.',seconds=25)

# 11. Actual output from the old library documentation, with historical scope explicit.
# The posterior SVG is copied from the published plot DOM, not generated data.
j=json.loads((SOURCE_MATERIAL/'bayesian-plot-dom.json').read_text())
E.register_namespace('','http://www.w3.org/2000/svg')
a=E.fromstring(j[0])
for part in j[1:]:
 for child in E.fromstring(part):a.append(child)
a.set('viewBox','0 0 717 728.312')
(R/'images/current/legacy-bayesian-posterior.svg').write_text(E.tostring(a,encoding='unicode'))
pdfdata=json.loads((SOURCE_MATERIAL/'pdf-plot-dom.json').read_text()); pdfsvg=E.fromstring(pdfdata[0])
for part in pdfdata[1:]:
 for child in E.fromstring(part):pdfsvg.append(child)
pdfsvg.set('viewBox','0 0 '+pdfsvg.get('width')+' '+pdfsvg.get('height'))
(R/'images/current/legacy-pdf-si-nomad.svg').write_text(E.tostring(pdfsvg,encoding='unicode'))
pdfcol='<div class="why-col" data-id="pdf" style="width:52%"><p class="colcap"><span class="blue">Pair distribution function</span>Si · NOMAD / SNS · PDFfit2</p><div class="imgwrap" style="height:330px"><img src="images/current/legacy-pdf-si-nomad.svg" alt="Si pair distribution function fitted with the earlier EasyDiffraction library" style="height:330px;object-fit:contain;background:#fafafa"></div></div>'
bayescol='<div class="why-col" data-id="bayesian" style="width:43%"><p class="colcap"><span class="blue">Bayesian analysis</span>LBCO · HRPT / PSI · DREAM</p><div class="imgwrap" style="height:330px"><img src="images/current/legacy-bayesian-posterior.svg" alt="Posterior pair distributions from the earlier EasyDiffraction Bayesian tutorial" style="height:330px;object-fit:contain;background:#fafafa"></div></div>'
write('18_advanced-library.html','The library grew beyond standard refinement',['<div class="columns" data-id="advanced">'+pdfcol+'</div>','<div class="columns" data-id="advanced">'+pdfcol+bayescol+'</div>'],'Advanced methods through <span class="blue">reusable libraries</span>.','STAP three-ways columns',extra_note='Earlier diffraction-lib capabilities, not current crysta capabilities. Actual plot screenshots / DOM from https://docs.easydiffraction.org/lib/0.19.1/tutorials/pdf-si-nomad/ and https://docs.easydiffraction.org/lib/0.19.1/tutorials/bayesian-dream-lbco-hrpt/. Short illustrative DREAM run in the tutorial is not converged; no inference about scientific convergence is made here.',seconds=65)

# 12. Exact original LENS slide, changing only its title.
lens=(ROOT/'2026.10.07 - LENS WP4 - EDI/slides/30_crysta.html').read_text()
depth=0
for match in re.finditer(r'<section\b[^>]*>|</section>',lens):
 if match[0].startswith('</'):
  depth-=1
  if depth==0:
   lens=lens[start:match.end()];break
 else:
  if depth==0:start=match.start()
  depth+=1
lens=lens.replace('Back to diffraction: what analysis needs','What modern diffraction analysis needs')
set_source('18b_modern-analysis.html','What modern diffraction analysis needs','<div class="external-slide">'+lens+'</div>','LENS 17/4, unchanged except title',50)

# 13–14. Keep the exact source diagram, then animate its transition to six routes.
source=(ROOT/'2026.10.20 - Diff STAP - Edi & Crysta/slides/30_crysta.html').read_text()
# Extract the complete working Meet crysta stack from the original source.
depth=0
for match in re.finditer(r'<section\b[^>]*>|</section>',source):
 if match[0].startswith('</'):
  depth-=1
  if depth==0:
   candidate=source[start:match.end()]
   if '<h3>Meet crysta</h3>' in candidate:
    source='<div class="external-slide">'+candidate+'</div>';break
 else:
  if depth==0:start=match.start()
  depth+=1
parts=leaves(source)
last=parts[-1]
svgmatch=re.search(r'<svg class="stackfig".*?</svg>',last,re.S)
fullsvg=E.fromstring(svgmatch[0])
fullsvg.set('data-id','stack4')
groups=list(fullsvg)
# Named groups make Reveal retain the original objects while their positions change.
for group,key in zip(groups,['app-envelope','library-envelope','other-engines','project-layer','interface-layer']):group.set('data-id',key)
# Wrap the two original upper boxes (rect + icon + name) separately.
top=groups[-1];topkids=list(top)
for child in topkids:top.remove(child)
for n,(key,children) in enumerate([('family-python',topkids[:3]),('family-app',topkids[3:6])]):
 g=E.SubElement(top,'g',{'data-id':key})
 for child in children:g.append(child)
for child in topkids[6:]:top.append(child)
originalsvg=svgstr(fullsvg)
box=re.search(r'<div class="crystabox slot aa-move".*?</div></div></div></div>',last,re.S)[0]
def fig(svg,slot=box):return '<div class="crystafig" data-id="architecture">'+svg+slot+'</div>'
# Change only names/notes on the original introduction and native diagram state.
first=parts[0]
first=re.sub(r'<aside.*?</aside>','',first,flags=re.S)
intro=re.sub(r'<h3>.*?</h3>','<h3>Meet crysta</h3>',first,flags=re.S)
future=fig(originalsvg)
# Preserve the original two-state animation and its matching figure containers.
future_source=source
future_source=future_source.replace('A new calculation and minimisation engine, <span class="blue">built in-house</span>.','A possible future: <span class="blue">alongside existing libraries</span>.')
set_source('19_future.html','Meet crysta',future_source,'STAP 19, original working animation and geometry',65)

# Keep all scene objects stable through the complete animation.
exec(compile((R/'architecture_sequence.py').read_text(),str(R/'architecture_sequence.py'),'exec'),globals())

# The test-case slide now describes the five-bank fit used for the timing benchmark.
p=S/'26b_test-case.html'; case=p.read_text()
case=case.replace('WISH at ISIS, banks 2 + 9','WISH at ISIS, 5 detector banks')
case=case.replace('3977 points, 627 peaks','20,475 measured points')
case=case.replace('48 free parameters','193 free parameters')
case=case.replace('same start, &chi;&sup2; &asymp; 4.8 for all','same starting values')
case=case.replace('same model, one thread','same model · 6-core VISA Linux VM')
case=re.sub(r'<aside class="notes">.*?</aside>','<aside class="notes">Selected five-bank NCAF benchmark from the abstract: WISH bank pairs 1_10, 2_9, 3_8, 4_7 and 5_6, with 20,475 measured points and 193 free parameters. Default six-core VISA Linux VM; same initial values and structural model. Approximate timing: crysta 3 s, FullProf 20 s. All refined structural parameters agree within 0.3 combined standard uncertainties. The next pattern-agreement slide retains the earlier two-bank verification subset and is explicitly labelled WISH 2+9, 3977 points.</aside>',case,flags=re.S)
p.write_text(case)
meta['26b_test-case.html']['kind']='adapted'
meta['26b_test-case.html']['template']='STAP One of many test cases, five-bank values'

# 17. The requested calculate / compare / adjust loop, without derivatives.
old=(SOURCE_MATERIAL/'2026.09.07-source.html').read_text()
svgs=re.findall(r'<svg viewBox="0 0 830 290">.*?</svg>',old,re.S)
svgs=list(dict.fromkeys(svgs))[:5]
# The build already adds a title-only opening. Skip the source empty diagram.
svgs=svgs[1:]
svgs=[s.replace('<svg viewBox','<svg class="stackfig grouped" data-id="fit-loop" viewBox').replace('repeat, hundreds of times','repeat until convergence') for s in svgs]
write('27c_fit-loop.html','A fit is not one calculation',svgs,'Every fit repeats <span class="blue">calculate, compare and adjust</span>.','DMSC 19, adapted to STAP type and diagram width',extra_note='Source 2026.09.07 - DMSC - Crysta/index.html#/19/5, with the derivatives discussion removed.',seconds=45)

# 18. Same bars, now genuinely linear and without a time axis.
cc=chips([('flask','NCAF'),('wave-square','WISH · 5 banks'),('chart-line','20,475 points'),('sliders','193 parameters'),('flag-checkered','same start')])
def linearbar(id,name,value,cls):
 return f'<div class="bar-row" data-id="row-{id}"><div class="bar-name">{name}</div><div class="bar-track"><div class="bar-fill {cls} aa-move" data-id="fill-{id}" style="width:calc((100% - 110px) * {value/20:g})"></div><span class="bar-value">{value} s</span></div></div>'
fp=linearbar('fp','FullProf <span class="dim">(Fortran)</span>',20,'fortran');cr=linearbar('cr','crysta <span class="dim">(C++20)</span>',3,'crysta')
write('28_speed.html','Speed: a full TOF refinement',[cc+'<div class="bars" data-id="bars">'+rows+'</div>' for rows in ['',fp,fp+cr]],'Structural parameters agree within <span class="blue">0.3 combined σ</span>.','STAP speed bars, linear widths',extra_note='Selected abstract benchmark: approximately 3 s with crysta, 20 s with FullProf, same initial values on a default six-core VISA Linux VM. 20,475 measured points = 4182 + 4166 + 3970 + 4043 + 4114 rows in tests/fixtures/e02_t2_ncaf_5bank/project/experiments of edi. Different case from the earlier two-bank agreement plot.',seconds=65)

# Keep the final sentence's layout space on the speed slide, so only its opacity
# changes on the last click. Other slides retain the original STAP reveal rhythm.
p=S/'28_speed.html'; speed=p.read_text()
close_style='height:auto;margin:calc(var(--gap-close) - (var(--gap) - 0.1em)) 0 var(--gap-close);overflow:visible'
hidden_close='<p class="statement hid" data-id="close" data-auto-animate-duration="1.1" style="'+close_style+'">Structural parameters agree within <span class="blue">0.3 combined σ</span>.</p>'
for leaf in leaves(speed):
 if '<p class="statement"' not in leaf:speed=speed.replace(leaf,leaf+'\n  '+hidden_close+'\n',1)
speed=speed.replace('<p class="statement" data-id="close"','<p class="statement" style="'+close_style+'" data-id="close"')
p.write_text(speed)

# A balanced pair of concise functionality slides, following the original STAP list.
lst('22_physics.html','Current functionality: data and models',[
 ('wave-square','<span class="blue">TOF neutrons</span>, <span class="blue">CW neutrons</span> and <span class="blue">X-rays</span>'),
 ('cubes','<span class="blue">Powder</span> and <span class="blue">neutron single crystal</span> diffraction'),
 ('magnet','<span class="blue">Crystal</span> and <span class="blue">commensurate magnetic</span> structures'),
 ('layer-group','Multiple <span class="blue">phases</span> and <span class="blue">measured datasets</span>'),
 ('sliders','<span class="blue">Peak profiles</span>, <span class="blue">calibration</span> and <span class="blue">sample corrections</span>')],
 'Broad coverage for <span class="blue">crystal and magnetic structure refinement</span>.',
 True,'STAP Current functionality · five concise rows',seconds=65)
p=S/'22_physics.html'; text=p.read_text(); text=re.sub(r'<aside class="notes">.*?</aside>',
 '<aside class="notes">Current crysta/edi coverage, grouped by the data and model rather than by individual parameters. Powder: CW and TOF neutrons, X-rays. Single crystal: neutron diffraction, including extinction models; this is not a claim of X-ray single-crystal support. Crystal models include symmetry, atomic positions, occupancies and isotropic/anisotropic displacement parameters. Commensurate magnetic structures are available. Multiple phases and measured datasets share the project; scales and derived mass fractions are supported. Peak profiles, instrument calibration, backgrounds, absorption and preferred-orientation corrections are included. PDF and Bayesian capabilities from the earlier library belong to the porting roadmap, not this current-coverage list. Source: https://enhantica.github.io/edi/user-guide/features/</aside>',text,flags=re.S);p.write_text(text)
lst('23_powder.html','Current functionality: fitting and results',[
 ('calculator','<span class="blue">Pattern calculation</span> with or without measured data'),
 ('arrows-spin','<span class="blue">Single</span>, <span class="blue">joint</span>, <span class="blue">sequential</span> and <span class="blue">independent</span> fitting'),
 ('sliders','<span class="blue">Weighted least squares</span> and <span class="blue">parameter constraints</span>'),
 ('chart-line','<span class="blue">Uncertainties</span>, <span class="blue">correlations</span> and <span class="blue">parameter evolution</span>'),
 ('file-lines','<span class="blue">Interactive plots</span>, <span class="blue">structure views</span> and <span class="blue">HTML/PDF/CIF reports</span>')],
 'Results stay linked to their <span class="blue">models and measured data</span>.',
 True,'STAP Current functionality · five concise rows',seconds=55)
p=S/'23_powder.html'; text=p.read_text(); text=re.sub(r'<aside class="notes">.*?</aside>',
 '<aside class="notes">Current analysis workflow, grouped from calculation and fitting to inspection and saved results. Free/fixed parameter selection, constraints and weighted least squares are supported. Single and joint fits cover individual and combined experiments; sequential and independent scans cover measurement series. Inspect residuals, parameter uncertainties, correlations and evolution. Interactive maps, stacked patterns and structure views are application capabilities; notebooks and reports offer the views documented for their interface, not identical controls everywhere. Projects retain the analysis, with HTML/PDF/CIF reports for results. PDF export is available in the application; HTML/CIF are available across interfaces. No claim of current Bayesian sampling or PDF is made. Source: https://enhantica.github.io/edi/user-guide/features/</aside>',text,flags=re.S);p.write_text(text)

# Fresh application captures share one window size and display scale. Only the
# native OS title strip are excluded from the view.
def native_picture(file,title,asset,tags,close):
 cc=chips(tags)
 slot=f'<div class="shotbox" data-id="picture" style="--shot-h:411px;--shot-w:721px;overflow:hidden;border-radius:6px"><img src="images/current/{asset}" alt="{escape(title)}" style="width:721px;height:auto;max-width:none;top:-13.49px"></div>'
 write(file,title,[cc,cc+slot],close,'STAP shotbox and casechips · fixed app window',extra_note='Fresh native EasyDiffraction capture at 2992 × 1760 physical pixels. All app controls and status bar retained. Only native OS title strip excluded with the presentation viewport. Capture uses copies of documented example projects, fitted in the application. The screenshot status reports a local capture run, not a repeat of the six-core VISA timing benchmark.',seconds=50)
native_picture('24_application.html','A complete refinement workspace','wish-fit-native.jpg',[
 ('flask','NCAF'),('wave-square','WISH · 5 banks'),('sliders','193 parameters'),('layer-group','Bank 5_6')], 'Measured data, model and <span class="blue">fitted parameters together</span>.')
native_picture('25_scans.html','From one pattern to a measurement series','scan-fit-native.jpg',[
 ('flask','Co₂SiO₄'),('wave-square','D20 / ILL'),('layer-group','213 datasets'),('chart-line','Map view')], 'Fit a series and follow <span class="blue">how the structure changes</span>.')
native_picture('26_magnetism.html','Inspect the magnetic structure','magnetic-fit-native.jpg',[
 ('flask','Co₂SiO₄'),('wave-square','D20 / ILL'),('temperature-low','2.3 K'),('magnet','Commensurate')], 'Connect the fit with <span class="blue">a structural picture</span>.')
native_picture('26c_single-crystal.html','Also single-crystal diffraction','taurine-fit-native.jpg',[
 ('flask','Taurine'),('wave-square','SENJU / J-PARC'),('layer-group','6 datasets'),('atom','Anisotropic ADPs')], 'The same workflow for <span class="blue">single-crystal refinement</span>.')

# The documented AI session is retained as scientific evidence. Match the same
# display width and UI scale, preserving its full frame and original proportions.
cc=chips([('robot','Optional desktop assistant'),('flask','La₀.₅Ba₀.₅CoO₃'),('wave-square','HRPT / PSI')])
slot='<div class="shotbox" data-id="picture" style="--shot-h:405px;--shot-w:721px"><img src="images/current/ai-assistant-fitted.png" alt="Fitted application with built-in AI assistant" style="width:721px;height:auto;max-width:none"></div>'
write('34_ai-desktop.html','AI assistance inside the desktop app',[cc,cc+slot], 'Ask, inspect the actions, and <span class="blue">check the resulting fit</span>.','STAP screenshot template · matched width and UI scale',extra_note='Original documented assistant session retained without changing the conversation or result. Source website/surfaces/docs/assets/gui/assistant/assistant-fitted.webp. Display width matches the fresh app captures, without stretching its slightly shorter window.',seconds=60)

# 27. Compact source-style cards, with all ten requested non-physics features.
features=[('code','Open source','Source and issue tracking on GitHub'),('display','Cross-platform','Web, macOS, Windows and Linux'),('cubes','Packaged application','Dependencies included'),('folder-open','Portable projects','Move the same project between interfaces'),('book-open','25 built-in tutorials','Guides in the app and online'),('arrows-rotate','Undo and redo','Step backwards or forwards through edits'),('chart-line','Live chart updates','See the effect of parameter changes'),('arrows-spin','Built-in updater','Check for desktop application updates'),('circle-half-stroke','Light and dark themes','Choose the display you prefer'),('comment-dots','Feedback and bug reports','Send them from the application')]
def featuregrid(n):
 return '<div class="reflibs" data-id="libs" style="width:960px;max-width:100%;grid-template-columns:repeat(2,1fr);gap:18px">'+''.join(f'<div class="reflib" data-id="lib{i}" style="padding:12px 16px"><span class="rn" style="font-size:24px"><i class="fa-{k} lead"></i>{name}</span><span class="rd" style="font-size:20px;margin-top:4px">{desc}</span></div>' for i,(k,name,desc) in enumerate(features[:n],1))+'</div>'
write('36_software.html','Practical software features',[featuregrid(n) for n in [2,4,6,8,10]],'Designed to make <span class="blue">everyday analysis easier</span>.','STAP What became reusable cards; same type hierarchy',extra_note='Current public documentation https://enhantica.github.io/edi/ and application tutorial index. 25 application tutorials includes the built-in-assistant walkthrough. Desktop distribution is not yet code-signed; built-in updater applies to desktop application. Portable projects are shared scientific project files, not identical interface controls.',seconds=65)

# 28. Status symbols are copied unchanged from the current public feature catalogue.
def status_mark(state,label):
 return f'<img src="images/current/status-{state}.svg" alt="{label}" title="{label}" style="display:inline-block;width:1em;height:1em;vertical-align:-0.12em;margin:0 0 0 0.4em;border:0;box-shadow:none">'
lst('37_status.html','Work in progress / Next steps',[
 ('magnet','<span class="blue">Magnetic structure input</span><span class="sub inline">Manual creation</span>'+status_mark('in-progress','Work in progress')),
 ('display','<span class="blue">Distribution</span><span class="sub inline">Code signing for macOS and Windows</span>'+status_mark('in-progress','Work in progress')),
 ('arrows-rotate','<span class="blue">Port existing capabilities</span><span class="sub inline">PDF and Bayesian analysis · available before crysta</span>'+status_mark('planned','Planned')),
 ('wave-square','<span class="blue">Further models</span><span class="sub inline">Polarised neutrons, twins and incommensurate structures</span>'+status_mark('planned','Planned')),
 ('calculator','<span class="blue">Further methods</span><span class="sub inline">Le Bail, Pawley and 2D Rietveld fitting</span>'+status_mark('proposed','Proposed'))],f'Current status in the <a class="blue" style="color:var(--c-blue)" href="https://easydiffraction.org/user-guide/features/">full feature catalogue</a>.',True,'STAP Work in progress boxed rows',seconds=50)
p=S/'37_status.html';text=p.read_text().replace('</aside>','<br>Status artwork: Twemoji, as embedded in https://easydiffraction.org/user-guide/features/. Construction barrier: work in progress. Calendar: planned. Light bulb: proposed.</aside>');p.write_text(text)

# 29. Student-facing practical plan, with no advance download requirement.
lst('38_hands-on.html','Plan for Thursday and Friday',[
 ('globe','<span class="blue"><a href="https://easydiffraction.org/">easydiffraction.org</a></span><span class="sub">No preparation or advance download of materials needed</span>'),
 ('book-open','<span class="blue">Getting started together</span><span class="sub">Open an example, fit, inspect and save your project</span>'),
 ('display','<span class="blue">Guided tutorials for every interface</span><span class="sub">Built into the application and available online · choose your route</span>'),
 ('user-check','<span class="blue">Work at your own pace</span><span class="sub">A flexible set of examples, with help when you need it</span>')],'Getting started should be <span class="blue">easy</span> <img src="images/current/smile-wink.svg" alt="wink" style="display:inline-block;width:0.95em;height:0.95em;vertical-align:-0.1em;margin:0 0 0 0.08em;border:0;box-shadow:none">','STAP Needs boxed rows',seconds=70)

# Compact the two closing list slides without changing their typography.
for compact_file in ['37_status.html','38_hands-on.html']:
 p=S/compact_file
 text=p.read_text().replace('data-id="dolist"','data-id="dolist" style="width:840px;max-width:100%"')
 p.write_text(text)

# 30. Presenter-selected Success Kid feedback meme, kept as an offline asset.
left='<div class="why-col" data-id="survey-art" style="flex:0 0 400px;width:400px;height:400px"><div class="imgwrap" style="width:400px;height:400px;background:transparent;border:0;border-radius:12px;overflow:hidden"><img src="images/current/success-kid-feedback.jpg" alt="Success Kid: We need your feedback" style="display:block;width:400px;height:400px;object-fit:contain;border-radius:12px;margin:0"></div></div>'
right='<div class="why-col" data-id="survey-invitation" style="flex:1 1 0;height:400px;display:flex;flex-direction:column;justify-content:space-between;align-items:flex-start"><div style="font-size:26px;line-height:1.4"><p style="font-size:inherit;line-height:inherit;margin:0 0 16px"><a href="http://easydiffraction.org/about/survey/">easydiffraction.org/about/survey</a></p><p style="font-size:inherit;line-height:inherit;margin:0">Which interface suits you?<br>What have you tried?<br>What would make it easier?</p></div><a href="http://easydiffraction.org/about/survey/" aria-label="Open the EasyDiffraction survey" style="display:block;width:210px;height:210px;flex:0 0 210px;background:white;border-radius:12px;overflow:hidden"><img src="images/current/survey-qr.svg" alt="QR code for http://easydiffraction.org/about/survey/" style="width:210px;height:210px;display:block;margin:0;border:0;border-radius:12px;box-shadow:none"></a></div>'


write('40_survey.html','EasyDiffraction needs your feedback',['<div class="columns" data-id="survey" style="width:880px">'+left+'</div>','<div class="columns" data-id="survey" style="width:880px">'+left+right+'</div>'],'Please take a moment to fill in the survey.','STAP three-ways columns',extra_note='Presenter-selected option 6: Success Kid, We need your feedback. Source https://makeameme.org/meme/we-need-your-e3a7e24ae5 . Image https://media.makeameme.org/created/we-need-your-e3a7e24ae5.jpg . Downloaded unchanged for offline presentation use. QR code encodes http://easydiffraction.org/about/survey/ exactly as supplied. The presenter will publish the survey later.',seconds=45)

# Keep the final slide's current artwork provenance accurate after regeneration.
p=S/'40_survey.html';text=p.read_text();text=re.sub(r'<aside class="notes">.*?</aside>','<aside class="notes">Presenter-selected option 6: Success Kid, We need your feedback. Source: https://makeameme.org/meme/we-need-your-e3a7e24ae5 . Original image downloaded unchanged for offline use. QR code: http://easydiffraction.org/about/survey/ . Survey will be published by the presenter later.</aside>',text,flags=re.S);p.write_text(text)

# The presenter's exact 30-slide sequence. Keep omitted slides in backup.
order=['00_divider.html','01_title.html','02_facility.html','10_many-tools.html','11_user-friction.html','12_needs.html','13_libraries.html','13b_library-capabilities.html','14_dependencies.html','15_ux.html','16_ux-review.html','18_advanced-library.html','18b_modern-analysis.html','19_future.html','20_architecture.html','26b_test-case.html','27_verification.html','27c_fit-loop.html','28_speed.html','22_physics.html','23_powder.html','24_application.html','25_scans.html','26_magnetism.html','26c_single-crystal.html','34_ai-desktop.html','35_ai-external.html','36_software.html','37_status.html','38_hands-on.html','40_survey.html']
p=R/'build.py';b=p.read_text();b=re.sub(r'^ORDER = .*$',lambda m:'ORDER = '+repr(order),b,flags=re.M)
section_titles={'02_facility.html':'Earlier EasyDiffraction','19_future.html':'EasyDiffraction + crysta','24_application.html':'Selected features','36_software.html':'Using EasyDiffraction'}
b=re.sub(r'^SECTION_TITLES = .*?(?=^ORDER =)',lambda m:'SECTION_TITLES = '+repr(section_titles)+'\n',b,count=1,flags=re.S|re.M)
# Architecture uses the same title opening and horizontal transition as other stacks.
b=b.replace("    'Status and plans': 'flag-checkered',","    'Status and plans': 'flag-checkered',\n    'Selected features': 'eye',\n    'Using EasyDiffraction': 'display',") if "'Selected features': 'eye'" not in b else b
# Preserve removed material for later review, not in the main running order.
backup=eval(re.search(r'^BACKUP_ORDER = (.*)$',b,re.M).group(1))
for f in ['17_three-interfaces.html','21_advantages.html','27b_parameters.html','30_six-interfaces.html','31_graphical.html','32_python.html','33_cli.html','39_online.html','39_takeaway.html']:
 if f not in backup:backup.insert(1,f)
b=re.sub(r'^BACKUP_ORDER = .*$',lambda m:'BACKUP_ORDER = '+repr(backup),b,flags=re.M);p.write_text(b)
# Maintain notes and public URLs on retained slides.
for file in order[1:]:
 p=S/file;s=p.read_text().replace('http://127.0.0.1:8873',PUBLIC);p.write_text(s)
# Source metadata / timing map is based on the actual order, not old slide indices.
(R/'outline.json').write_text(json.dumps([meta[f] for f in order if f in meta],indent=2,ensure_ascii=False))
(R/'template-map.json').write_text(json.dumps(mapping,indent=2,ensure_ascii=False))
print('Applied review: 30 content slides, original templates and new running order.')
