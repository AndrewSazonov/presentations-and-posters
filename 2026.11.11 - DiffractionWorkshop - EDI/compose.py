#!/usr/bin/env python3
"""Adapt the STAP slide templates. Source styles are reused without overrides."""
from pathlib import Path
from html import escape
import json,re,math,shutil
R=Path(__file__).parent;S=R/'slides';L=S/'library'
PUBLIC='https://enhantica.github.io/edi'
DOCS='http://127.0.0.1:8873'
meta={x['file']:x for x in json.loads((R/'outline.json').read_text())}
notes={}
for f in S.glob('*.html'):
 m=re.findall(r'<aside class="notes">(.*?)</aside>',f.read_text(),re.S)
 if m:notes[f.name]=m[-1]
mapping=[]
def icon(k):return f'<i class="fa-{k}"></i>'
def chips(items):return '<div class="flow casechips" data-id="chips">'+''.join(f'<span class="chip">{icon(k)}{t}</span>' for k,t in items)+'</div>'
def write(file,title,stages,conclusion,template,extra_note='',seconds=None):
 n='<br><br>'.join(dict.fromkeys(notes.get(file,'').split('<br><br>')))
 if extra_note and extra_note not in n:n+=(('<br><br>' if n else '')+extra_note)
 steps=[]
 for i,body in enumerate(stages):
  steps.append('<section data-auto-animate-unmatched="false" data-auto-animate'+(' data-auto-animate-restart' if i==0 else '')+f'>\n  <h3>{title}</h3>\n  '+body+'\n</section>')
 body=stages[-1]
 if conclusion:steps.append(f'<section data-auto-animate-unmatched="false" data-auto-animate>\n  <h3>{title}</h3>\n  {body}\n  <p class="statement" data-id="close" data-auto-animate-duration="1.1">{conclusion}</p>\n  <aside class="notes">{n}</aside>\n</section>')
 else:steps[-1]=steps[-1].replace('</section>',f'<aside class="notes">{n}</aside></section>')
 (S/file).write_text('<div class="external-slide">\n<section>\n'+'\n\n'.join(steps)+'\n</section>\n</div>\n')
 old=meta.get(file,dict(file=file,kind='adapted',seconds=seconds or 30,sources=template))
 old.update(title=title,kind='adapted',template=template)
 if seconds is not None:old['seconds']=seconds
 meta[file]=old;mapping.append(dict(file=file,template=template))
def lst(file,title,rows,close,dense=False,template='How the code is checked',seconds=None):
 def body(n):return '<div class="dolist boxed'+(' dense functionality-list' if dense else '')+'" data-id="dolist">'+''.join(f'<p class="step" data-id="t{i}">{icon(k).replace(chr(34)+chr(62)," lead\" >")} {text}</p>' for i,(k,text) in enumerate(rows[:n],1))+'</div>'
 write(file,title,[body(n) for n in range(1,len(rows)+1)],close,template,seconds=seconds)
def grid(file,title,items,close):
 def body(n):return '<div class="reflibs" data-id="libs">'+''.join(f'<div class="reflib" data-id="lib{i}"><span class="rn"><i class="fa-{k} lead"></i>{name}</span><span class="rd">{desc}</span></div>' for i,(k,name,desc) in enumerate(items[:n],1))+'</div>'
 write(file,title,[body(n) for n in range(2,len(items)+1,2)],close,'What became reusable · reflibs')
def picture(file,title,asset,tags,close):
 # Source .shotbox convention: dimensions are per-slide knobs; no style rules are added.
 import struct
 w,h=struct.unpack('>II',(R/'images/current'/asset).read_bytes()[16:24])
 height=405;width=round(height*w/h)
 cc=chips(tags);slot=f'<div class="shotbox" data-id="picture" style="--shot-h: {height}px; --shot-w: {width}px"><img src="images/current/{asset}" alt="{escape(title)}"></div>'
 write(file,title,[cc,cc+slot],close,'A few live demos · shotbox; Agreement of calculated patterns · casechips')
def copy(file,source,title=None,seconds=None):
 text=(L/source).read_text();m=re.search(r'<h3[^>]*>(.*?)</h3>',text,re.S);oldtitle=re.sub('<[^>]*>','',m.group(1)) if m else ''
 if title:text=text.replace(oldtitle,title)
 (S/file).write_text(text)
 old=meta.get(file,dict(file=file,kind='reused',seconds=seconds or 35,sources='STAP '+source))
 old.update(title=title or oldtitle,kind='reused',template='STAP: '+source)
 if seconds is not None:old['seconds']=seconds
 meta[file]=old;mapping.append(dict(file=file,template='STAP: '+source))
# Requested original slides, including their complete reveal sequences.
copy('13b_library-capabilities.html','what-each-library-brings.html',seconds=30)
copy('16_ux-review.html','reviewed-by-ux-experts.html',seconds=25)
copy('17_three-interfaces.html','three-ways-to-run-the-same-workflow.html',seconds=30)
p=S/'17_three-interfaces.html';p.write_text(p.read_text().replace('`python -m easydiffraction PROJECT fit`','`python -m edi fit PROJECT`'))
# Future possibility: retain the original multi-engine drawing and geometry.
text=(L/'meet-crysta.html').read_text()
leafs=[];depth=0
for m in re.finditer(r'<section\b[^>]*>|</section>',text):
 if not m.group().startswith('</'):
  if depth==1:start=m.end()
  depth+=1
 else:
  depth-=1
  if depth==1:leafs.append(text[start:m.start()])
full=leafs[-1];full=re.sub(r'<h3[^>]*>.*?</h3>','',full,flags=re.S);full=re.sub(r'<p class="statement".*?</p>','',full,flags=re.S);full=re.sub(r'<aside.*?</aside>','',full,flags=re.S)
write('19_future.html','A possible future: several engines',[full],'crysta <span class="blue">alongside existing libraries</span>.','Meet crysta · original multi-engine drawing',extra_note='This is a future idea requested by the presenter, not current edi functionality and not a committed roadmap item. The original STAP diagram is reused unchanged.',seconds=35)
# Current approach: edit the same stack-figure vocabulary and source coordinates.
blue='rgb(96, 188, 232)';brown='rgb(226, 183, 129)';dark='rgb(133, 86, 29)'
def rect(x,y,w,h,fill):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" style="fill:{fill};"/>'
def txt(x,y,t,size=20,fill='#222'):return f'<text x="{x}" y="{y}" text-anchor="middle" style="font-size:{size}px; fill:{fill};">{t}</text>'
def line(x,y,xx,yy,c=brown):return f'<line x1="{x}" y1="{y}" x2="{xx}" y2="{yy}" style="stroke:{c}; stroke-width:3"/>'
current='<svg class="stackfig grouped" data-id="current-core" viewBox="0 -32 830 448">'
current+='<rect x="8" y="-26" width="814" height="154" rx="10" style="fill:rgba(96, 188, 232, 0.12);stroke:rgba(96, 188, 232, 0.55);stroke-width:1.5"/>'+txt(415,2,'EasyDiffraction interfaces',16,blue)
for x,name in [(40,'Application'),(305,'Python library'),(570,'Command line')]:
 current+=rect(x,12,220,60,blue)+txt(x+110,49,name)+line(x+110,150,x+110,84)+f'<polygon points="{x+103},85 {x+117},85 {x+110},72" style="fill:{brown}"/>'
current+=rect(95,150,640,92,dark)+txt(200,173,'Project model · edi',17,brown)+rect(110,182,610,48,brown)+txt(415,213,'Structures · experiments · analysis · results',22)
current+=line(415,296,415,254)+f'<polygon points="408,255 422,255 415,242" style="fill:{brown}"/>'
current+=rect(250,296,330,102,dark)+txt(415,320,'Calculation and refinement',17,brown)+rect(270,330,290,56,brown)+txt(415,353,'crysta',22)+txt(415,374,'C++20',13,'rgb(133, 86, 29)')+'</svg>'
write('20_architecture.html','The current crysta-only approach',[current],'One project model and <span class="blue">one scientific engine</span>.','What we rely on / Meet crysta · stackfig grouped',seconds=45)
lst('21_advantages.html','What the new approach changes',[
 ('folder-open','<span class="blue">One project</span> across the application, Python and command line'),
 ('microchip','<span class="blue">Calculation and refinement</span> developed together'),
 ('magnifying-glass','<span class="blue">Connected results</span> · inspect the fit, parameters and reports')], 'A connected path from <span class="blue">model to checked result</span>.',template='Needs · boxed rows')
# The original Current functionality template, extended and split in two.
lst('22_physics.html','Current functionality: diffraction',[
 ('wave-square','<span class="blue">Powder diffraction</span> · CW neutrons, TOF neutrons and X-rays'),
 ('cubes','<span class="blue">Neutron single crystals</span> · extinction models'),
 ('atom','<span class="blue">Atomic sites</span> · symmetry, occupancies, isotropic and anisotropic ADPs'),
 ('magnet','<span class="blue">Commensurate magnetic structures</span>'),
 ('layer-group','<span class="blue">Multiple phases</span> · scales and derived mass fractions'),
 ('sliders','<span class="blue">Profiles and corrections</span> · calibration, background, absorption, texture')], 'Broad coverage for <span class="blue">structure refinement</span>.',True,'Current functionality · exact dense boxed list')
lst('23_powder.html','Current functionality: analysis',[
 ('calculator','<span class="blue">Calculate patterns</span> with or without observations'),
 ('arrows-spin','<span class="blue">Single and joint fits</span> · multiple measured datasets'),
 ('layer-group','<span class="blue">Sequential and independent scans</span>'),
 ('sliders','<span class="blue">Fit control</span> · free parameters, constraints and weighted least squares'),
 ('chart-line','<span class="blue">Inspection</span> · residuals, uncertainties, correlations and evolution'),
 ('file-lines','<span class="blue">Projects and results</span> · structure views, maps, HTML and CIF reports')], 'Keep the <span class="blue">analysis and its evidence</span> together.',True,'Current functionality · exact dense boxed list')
picture('24_application.html','A complete refinement workspace','wish-five-bank-after-fit.png',[
 ('flask','NCAF'),('wave-square','WISH · 5 banks'),('sliders','193 parameters'),('layer-group','Bank 5_6')], 'Measured data, model and <span class="blue">fitted parameters together</span>.')
picture('25_scans.html','From one pattern to a measurement series','scan-map.png',[
 ('flask','Co₂SiO₄'),('wave-square','D20 / ILL'),('layer-group','213 datasets'),('chart-line','Map view')], 'Fit a series and follow <span class="blue">how the structure changes</span>.')
picture('26_magnetism.html','Inspect the magnetic structure','magnetic-after-fit.png',[
 ('flask','Co₂SiO₄'),('wave-square','D20 / ILL'),('temperature-low','2.3 K'),('magnet','Commensurate')], 'Connect the fit with <span class="blue">a structural picture</span>.')
copy('26b_test-case.html','one-of-many-test-cases.html',seconds=35)
# Exact originals: the dark SVG, tag strip, chart dimensions and parameter table are unchanged.
copy('27_verification.html','agreement-of-calculated-patterns.html',seconds=40)
copy('27b_parameters.html','agreement-of-refined-parameters.html',seconds=35)
# Current benchmark values in the original bar-chart template.
cc=chips([('flask','NCAF'),('wave-square','WISH · 5 banks'),('sliders','193 parameters'),('flag-checkered','same start'),('ruler-horizontal','log scale')])
axis='<div class="bar-row bar-axis" data-id="axis"><div></div><div class="bar-ticks"><span style="left:0%">0.1 s</span><span style="left:25%">1 s</span><span style="left:50%">10 s</span><span style="left:75%">100 s</span><span style="left:100%">1000 s</span><div class="bar-axis-line"></div></div></div>'
def bar(id,name,value,cls):
 width=(math.log10(value)+1)/4
 return f'<div class="bar-row" data-id="row-{id}"><div class="bar-name">{name}</div><div class="bar-track"><div class="bar-fill {cls} aa-move" data-id="fill-{id}" style="width:calc((100% - 190px) * {width:.4f})"></div><span class="bar-value">{"≈" if id=="cr" else ""}{value} s</span></div></div>'
bfp=bar('fp','FullProf <span class="dim">(Fortran)</span>',20,'fortran');bcr=bar('cr','crysta <span class="dim">(C++20)</span>',3,'crysta')
write('28_speed.html','Speed: a full TOF refinement',[cc+'<div class="bars" data-id="bars">'+axis+rows+'</div>' for rows in ['',bfp,bfp+bcr]], 'Structural parameters agree within <span class="blue">0.3 combined σ</span>.','Speed: a full TOF refinement · exact bars and log axis',extra_note='Default six-core VISA Linux VM, identical initial values; selected five-bank benchmark. The earlier two-bank verification is a separate case.')
# Six routes use the existing SVG stack-diagram styling, not a new card component.
# Reuse the original sprite outlines, at the same 20 px size as the old stack icons.
import xml.etree.ElementTree as ET
sprite=ET.fromstring((R/'extra/icons-sprite.svg').read_text())
symbols={e.attrib.get('id'):e for e in sprite.iter() if e.tag.split('}')[-1]=='symbol'}
def diagram_icon(name,cx,y,size=20):
 symbol=symbols['i-'+name];vx,vy,w,h=map(float,symbol.attrib['viewBox'].split())
 scale=size/max(w,h);x=cx-w*scale/2
 paths=''.join(ET.tostring(child,encoding='unicode') for child in symbol)
 paths=re.sub(r' xmlns:ns\d+="[^"]*"','',paths)
 paths=re.sub(r'ns\d+:','',paths)
 return f'<g transform="translate({x:g},{y:g}) scale({scale:g})" style="fill:#222">{paths}</g>'
def interface_label(cx,y,name,key,label_width):
 left=cx-(label_width+28)/2
 return diagram_icon(key,left+10,y-16)+f'<text x="{left+28:g}" y="{y}" style="font-size:20px; fill:#222;">{name}</text>'
svg='<svg class="stackfig grouped" data-id="six-routes" viewBox="0 -32 830 448">'
for x,name,key,width,children in [
 (20,'Application','display',92,[('Web','application','globe'),('Desktop','application','display')]),
 (290,'Python library','python',112,[('Jupyter','notebooks','book-open'),('Python','scripts','code')]),
 (560,'Command line','terminal',109,[('Standalone','executable','terminal'),('Python package','no scripting','python')])]:
 # Six routes at the top join their three interface families underneath.
 for j,(a,b,k) in enumerate(children):
  xx=x+j*132
  svg+=rect(xx,0,118,76,blue)+diagram_icon(k,xx+59,10,18)
  svg+=txt(xx+59,46,a,17 if a=='Python package' else 19)+txt(xx+59,66,b,15)
  svg+=line(xx+59,76,xx+59,96,blue)
 svg+=line(x+59,96,x+191,96,blue)+line(x+125,96,x+125,118,blue)
 svg+=rect(x,118,250,52,blue)+interface_label(x+125,152,name,key,width)
 svg+=line(x+125,170,x+125,220,brown)
svg+=rect(95,220,640,92,dark)+txt(415,245,'Shared EasyDiffraction project',20,brown)+rect(110,258,610,42,brown)+txt(415,286,'Structures · experiments · analysis · results',20)
svg+=line(415,312,415,348,brown)+rect(250,348,330,64,brown)+txt(415,374,'crysta',22)+txt(415,396,'Calculation and refinement · C++20',15,'rgb(133, 86, 29)')+'</svg>'
write('30_six-interfaces.html','One project, six ways to work',[svg], 'The same project, <span class="blue">whichever way you open it</span>.','What we rely on · existing stackfig grouped vocabulary')
lst('31_graphical.html','Web and desktop application',[
 ('globe','<span class="blue">Web application</span><span class="sub">No application installation · save a complete project to keep it</span>'),
 ('display','<span class="blue">Desktop application</span><span class="sub">Local files and archives · optional built-in AI assistant</span>')], 'The same visual workflow, <span class="blue">with different file access</span>.',template='Needs · boxed rows')
lst('32_python.html','Notebooks and Python scripts',[
 ('python','<span class="blue">Jupyter notebooks</span><span class="sub">Explore step by step, with plots and explanations alongside the fit</span>'),
 ('code','<span class="blue">Python scripts</span><span class="sub">Combine edi with your own preparation and analysis tools</span>'),
 ('cubes','<span class="blue">The same Python API</span><span class="sub">Parameters, observations, fitting and reports</span>')], 'Choose <span class="blue">how much of the workflow to script</span>.')
lst('33_cli.html','Command line without writing Python',[
 ('terminal','<span class="blue">Standalone executable</span><span class="sub">edi fit project/ · no Python installation · fitting saved projects</span>'),
 ('python','<span class="blue">Python package command line</span><span class="sub">python -m edi fit project/ · fitting, calculation, reports and more</span>')], 'Run a saved project <span class="blue">without writing a Python script</span>.',template='Needs · boxed rows')
picture('34_ai-desktop.html','AI assistance inside the desktop app','ai-assistant-fitted.png',[
 ('robot','Optional desktop assistant'),('flask','La₀.₅Ba₀.₅CoO₃'),('wave-square','HRPT / PSI')], 'Ask, inspect the actions, and <span class="blue">check the resulting fit</span>.')
lst('35_ai-external.html','AI-ready beyond the built-in assistant',[
 ('folder-open','<span class="blue">Provide the inputs</span><span class="sub">Structure, measured data, conditions, documentation and fit stages</span>'),
 ('robot','<span class="blue">Ask for a notebook or project</span><span class="sub">Use it in Python, the web or desktop app, or the command line</span>'),
 ('circle-check','<span class="blue">Run and check</span><span class="sub">Inspect residuals, parameters and correlations; compare with the tutorial</span>')], 'External assistants can <span class="blue">prepare work for every interface</span>.')
grid('36_software.html','Practical software features',[
 ('code','Open source','Source code on GitHub; contributions and issue reports'),
 ('display','Cross-platform','Web, macOS, Windows and Linux'),
 ('cubes','Packaged application','Application dependencies included'),
 ('folder-open','Portable projects','Readable files; save a folder or archive'),
 ('book-open','Worked examples','Tutorials, notebooks and reference data'),
 ('file-lines','Reports and provenance','HTML and CIF; retain the analysis choices')], 'Keep the result together with <span class="blue">the choices behind it</span>.')
lst('37_status.html','Work in progress / Next steps',[
 ('magnet','<span class="blue">Magnetic model input</span><span class="sub inline">manual creation · work in progress</span>'),
 ('display','<span class="blue">Distribution and installation</span><span class="sub inline">code signing · work in progress</span>'),
 ('wave-square','<span class="blue">Further scientific models</span><span class="sub">PDF, polarised neutrons, twins and incommensurate structures · planned</span>'),
 ('calculator','<span class="blue">Additional fitting methods</span><span class="sub">Le Bail, Pawley and 2D Rietveld fitting · proposed</span>')], f'Current status in the <a class="blue" href="{PUBLIC}/user-guide/features/">full feature catalogue</a>.',True,'Work in progress / Next steps · boxed rows')
lst('38_hands-on.html','Choose a route for the hands-on sessions',[
 ('book-open','<span class="blue">Shorter session</span><span class="sub">Open an example, select parameters, fit, inspect and save</span>'),
 ('sliders','<span class="blue">Longer session</span><span class="sub">Continue with a joint fit or a measurement series in your preferred interface</span>')], 'Start with one example; <span class="blue">extend the analysis when it is clear</span>.',template='Needs · boxed rows')
# Shared current tutorials, using the original online-options template.
facilities=[('ANSTO','ECHIDNA'),('Argonne','SEPD'),('ESRF','BM01'),('ESS','BEER (simulated)'),('FRM II / MLZ','SPODI, HEiDi'),('ILL','D1A, D20'),('ISIS','PEARL, POLARIS, WISH'),('J-PARC','SENJU'),('LLB','5C2'),('PETRA III','P02.1'),('PSI','HRPT')]
def online_option(id,title,url,label):
 return f'<div class="online-option" data-id="{id}"><h4>{title}<span class="online-separator">·</span><span class="online-version"><span class="blue">with crysta</span></span></h4><a class="online-link" href="{url}"><i class="fa-globe"></i>{label}</a><div class="flow online-counts"><span class="chip"><i class="fa-book-open"></i>23 tutorials</span><span class="chip"><i class="fa-globe"></i>11 facilities</span><span class="chip"><i class="fa-microscope"></i>15 instruments</span></div><dl class="online-instruments">'+''.join(f'<div><dt>{f}</dt><dd>{i}</dd></div>' for f,i in facilities)+'</dl></div>'
colab=online_option('colab','Google Colab notebooks',PUBLIC+'/python/tutorials/','Python tutorials · open in Colab')
web=online_option('webapp','Web application','https://app.easydiffraction.org/','app.easydiffraction.org')
write('39_online.html','Test online without installation',['<div class="online-options" data-id="online-options">'+colab+'</div>','<div class="online-options" data-id="online-options">'+colab+web+'</div>'], 'The <span class="blue">same tutorials</span> through both interfaces.','Test online without installation · original two-column template',extra_note='Both interface tutorial introductions state that the same examples have tutorials for every interface. The built notebook catalogue contains 23 cases. Facility/instrument metadata from app/examples/metadata.json for those cases gives 11 facilities after merging FRM II and MLZ, and 15 named physical instruments after excluding blank laboratory labels and McStas (simulation software). BEER is simulated. Laboratory and McStas examples remain in the tutorial count. Public links target the forthcoming site; the reviewed preview is '+DOCS+'.',seconds=35)
lst('39_takeaway.html','EasyDiffraction for your next analysis',[
 ('cubes','A clear workflow built on <span class="blue">experience with existing libraries</span>'),
 ('microchip','crysta for <span class="blue">calculation and refinement</span>'),
 ('folder-open','One project across <span class="blue">all interfaces</span>')], 'Try a worked example, then bring a case from <span class="blue">your own experiment</span>.',seconds=25)
# Placeholder uses the original paired-panel template; no invented survey screenshot.
p1='<div data-id="survey-image"><p class="lbl"><i class="fa-display"></i>Survey page</p><p class="sentence">Screenshot placeholder<br>About page survey to follow</p></div>'
p2='<div data-id="survey-invitation"><p class="lbl"><i class="fa-comment-dots"></i>Your feedback</p><p class="sentence">Please take a moment to fill in the survey.</p></div>'
write('40_survey.html','Help shape EasyDiffraction',['<div class="samefact" data-id="survey">'+p1+'</div>','<div class="samefact" data-id="survey">'+p1+p2+'</div>'], 'Your experience will <span class="blue">help guide development</span>.','Diffraction analysis: many tools · samefact')
# Optional questionnaire uses the original row table, rather than a new HTML table style.
head='<div class="prow phead"><span>interface</span><span>interested?</span><span>tried?</span><span>easy to use?</span><span></span></div>'
rows=''.join(f'<div class="prow" data-id="q{i}"><span>{name}</span><span>○</span><span>○</span><span>○</span><span></span></div>' for i,name in enumerate(['Web application','Desktop application','Jupyter notebooks','Python scripting','Standalone CLI','Python-package CLI']))
write('90_survey.html','Six ways to work: audience feedback',['<div class="ptable" data-id="questions">'+head+rows+'</div>'], 'Which route would you choose for the <span class="blue">hands-on session</span>?','Agreement of refined parameters · ptable')
# Preserve existing cover edits and original copied slides; change only ordering and stylesheet load.
p=R/'build.py';b=p.read_text();order=eval(re.search(r'^ORDER = (.*)$',b,re.M).group(1))
for after,new in [('13_libraries.html','13b_library-capabilities.html'),('15_ux.html','16_ux-review.html'),('16_ux-review.html','17_three-interfaces.html'),('26_magnetism.html','26b_test-case.html'),('27_verification.html','27b_parameters.html'),('38_hands-on.html','39_online.html')]:
 if new not in order:order.insert(order.index(after)+1,new)
if '19_future.html' not in order:order.insert(order.index('20_architecture.html'),'19_future.html')
b=re.sub(r'^ORDER = .*$',lambda m:'ORDER = '+repr(order),b,flags=re.M)
b=b.replace('"20_architecture.html": "crysta + EasyDiffraction"','"19_future.html": "crysta + EasyDiffraction"')
b=b.replace('    <link rel="stylesheet" type="text/css" href="extra/workshop.css">\n','')
p.write_text(b)
(R/'template-map.json').write_text(json.dumps(mapping,indent=2,ensure_ascii=False))
(R/'outline.json').write_text(json.dumps([meta[f] for f in order if f in meta]+[meta['90_survey.html']],indent=2,ensure_ascii=False))
print('Adapted',len(mapping),'slide files using existing STAP components. No workshop stylesheet is loaded.')

# Latest presenter review, retaining the original component vocabulary.
exec(compile((R/'review_updates.py').read_text(),str(R/'review_updates.py'),'exec'),globals())
