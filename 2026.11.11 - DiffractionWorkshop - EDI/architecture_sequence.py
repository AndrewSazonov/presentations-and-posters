"""The original STAP diagram, carried through a fixed, consistently ordered scene.
Only independent scene objects are matched by Reveal; their contents travel with them.
Executed by review_updates.py with the existing template helpers in scope.
"""
K=750/830
OFFSET=109
SCENE_WIDTH=1048

def pos(x,y,w,h):
 return f'left:{x*K:.5f}px;top:{(y+32)*K:.5f}px;width:{w*K:.5f}px;height:{h*K:.5f}px;'

def entity(key,x,y,w,h,content='',opacity=1,style='',duration=.8,delay=0,cls=''):
 return (f'<div class="arch-entity aa-move {cls}" data-id="{key}" '
         f'data-auto-animate-duration="{duration}" data-auto-animate-delay="{delay}" '
         f'style="position:absolute;{pos(x,y,w,h)}opacity:{opacity};{style}">{content}</div>')

def native_layer(key,groups,opacity,step):
 root=E.Element('svg',{'xmlns':'http://www.w3.org/2000/svg','viewBox':'0 -32 830 448','style':'display:block;width:100%;height:100%;overflow:visible'})
 for group in groups:
  group=_copy.deepcopy(group)
  for child in group.iter():child.attrib.pop('data-id',None)
  root.append(group)
 markup=svgstr(root).replace('engines-overlap',f'arch-overlap-{step}-{key}')
 return entity(key,OFFSET,-32,830,448,markup,opacity,duration=.32)

def card(key,x,y,w,h,name,ico,opacity=1,sub='',label_height=60,initial_name=None,renamed=False):
 bg=entity(key+'-box',x,y,w,h,opacity=opacity,style=f'background:{"#68B8AA" if sub else blue};border-radius:{6*K:.4f}px;')
 if sub:
  name_style=''
  route_icon=(R/'images/current/jupyter.svg').read_text().replace('<svg ', '<svg class="ico" fill="#222" ') if ico=='jupyter' else icon(ico)
  label=f'<span class="arch-route-icon">{route_icon}</span><span class="arch-route-name" style="{name_style}">{name}</span>'
  cls='arch-route-label'
 else:
  if initial_name:
   label=f'<span class="arch-family-variant" data-id="{key}-old-name" data-auto-animate-duration=".18" data-auto-animate-delay="{.22 if not renamed else 0}" style="opacity:{0 if renamed else 1}"><span class="arch-family-icon">{icon(ico)}</span><span>{initial_name}</span></span><span class="arch-family-variant" data-id="{key}-new-name" data-auto-animate-duration=".25" data-auto-animate-delay="{.22 if renamed else 0}" style="opacity:{1 if renamed else 0}"><span class="arch-family-icon">{icon(ico)}</span><span>{name}</span></span>'
  else:label=f'<span class="arch-family-icon">{icon(ico)}</span><span>{name}</span>'
  cls='arch-family-label'
 # The label has a constant size; resizing its background never stretches its text.
 label_width=320 if not sub else 152
 return bg+entity(key+'-label',x+(w-label_width)/2,y+(h-label_height)/2,label_width,label_height,label,opacity,cls=cls)

def wire(key,cx,top,bottom,opacity,colour=brown,arrow=True,duration=.8):
 content=(f'<span style="position:absolute;left:{-5.5*K:.4f}px;top:0;width:0;height:0;border-left:{7*K:.4f}px solid transparent;border-right:{7*K:.4f}px solid transparent;border-bottom:{12*K:.4f}px solid {colour}"></span>' if arrow else '')
 return entity(key,cx-1.5,top,3,bottom-top,content,opacity,style=f'background:{colour};',duration=duration)

legacy=list(fullsvg)
legacy_arrows=E.Element('g')
for child in list(legacy[3]):
 if child.tag in ['line','polygon']:legacy_arrows.append(_copy.deepcopy(child))

families=[('python','Python library','python',130,'Python library'),('app','Application','display',440,'Desktop application'),('cli','Command line','terminal',1000,'Command line')]
routes=[('python',20,[('Jupyter','route','jupyter'),('Scripts','route','code')]),('app',364,[('Web','route','globe'),('Desktop','route','display')]),('cli',708,[('Standalone','route','terminal'),('Py – no scripts','route','python')])]

def scene(step):
 parts=[native_layer('arch-envelopes',legacy[:2],int(step==0),step),native_layer('arch-legacy-engines',[legacy[2],legacy_arrows],int(step==0),step)]
 scientific=int(step<5)
 fade_duration=.32 if step>=5 else .8
 pyx=130+OFFSET if step<2 else 20
 pyw=260 if step<2 else 320
 apix=95+OFFSET if step==0 else (pyx+(pyw-152)/2)
 apiw=640 if step==0 else 152
 apiy=150 if step==0 else (114 if step<3 else 184)
 apih=92 if step==0 else 52
 parts.append(entity('arch-project',apix,apiy,apiw,apih,opacity=scientific,style=f'background:{dark};border-radius:{10*K:.4f}px;',duration=.32 if step>=5 else .8))
 original='<span class="arch-project-label">Python API</span><span class="arch-project-inner">Unified interface (Python)</span>'
 parts.append(entity('arch-api-original',95+OFFSET,150,640,92,original,int(step==0),duration=.18))
 parts.append(entity('arch-api-label',apix+(apiw-152)/2,apiy,152,52,'Python API',int(1<=step<5),cls='arch-family-label',style=f'color:{brown};',duration=fade_duration,delay=.22 if step==1 else 0))
 family_centers=[]
 for i,(key,name,ico,old_x,old_name) in enumerate(families):
  x=old_x+OFFSET if step<2 else 20+i*344
  y=12 if step<3 else 90
  w=260 if step<2 else 320
  h=60 if step<3 else 52
  visible=int(key!='cli' or step>=2)
  family_centers.append(x+w/2)
  parts.append(card('arch-family-'+key,x,y,w,h,name,ico,visible,initial_name=old_name if key=='app' else None,renamed=step>=2))
  # Only Python goes through the Python API. The other interfaces use crysta directly.
  bus=187 if step<3 else 257
  top=y+h if key!='python' else apiy+52
  wire_x=x+w/2
  if key=='cli' and step<2:
   # The CLI arrives from the side; its connector grows upward at its final x.
   wire_x=868
   top=bus
  parts.append(wire('arch-direct-'+key,wire_x,top,bus,visible*int(1<=step<5),duration=fade_duration))
  if key=='python':parts.append(wire('arch-wire-python',x+w/2,y+h,apiy,scientific,duration=fade_duration))
 for key,x,children in routes:
  shown=int(step>=4)
  for j,(name,sub,ico) in enumerate(children):
   yy=0 if step>=4 else 90
   hh=48 if step>=4 else 52
   parts.append(card('arch-route-'+key+str(j),x+j*168,yy,152,hh,name,ico,shown,sub,label_height=48))
  branches='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 42" style="display:block;width:100%;height:100%"><path d="M76 0V20H244V0 M160 20V42" fill="none" stroke="'+blue+'" stroke-width="3"/></svg>'
  parts.append(entity('arch-branches-'+key,x,48,320,42,branches,shown,delay=.15))
 bus=187 if step<3 else 257
 left=family_centers[0];right=family_centers[1] if step<2 else family_centers[2]
 parts.append(entity('arch-bus',left,bus,right-left,3,opacity=int(1<=step<5),style=f'background:{brown};',duration=fade_duration))
 engine_w=112 if step<3 else 152
 engine_x=420+OFFSET if step==0 else SCENE_WIDTH/2-engine_w/2
 engine_y=330 if step==0 else (208 if step<3 else 278)
 parts.append(wire('arch-wire-engine',SCENE_WIDTH/2,bus,engine_y,int(1<=step<5),arrow=False,duration=fade_duration))
 engine=box.replace('data-id="crystabox"',f'data-id="crystabox" data-auto-animate-duration="{.32 if step>=5 else .8}" style="{pos(engine_x,engine_y,engine_w,56)}opacity:{scientific};"')
 if step>=1:engine=engine.replace('C++ &#8594; Python','C++20')
 parts.append(engine)
 for i,(key,src) in enumerate([('python','jupyter-2026.png'),('app','ed-analysis-2026.png'),('cli','ed-cli.png')]):
  content=f'<span role="img" aria-label="{key} interface example" style="display:block;width:100%;height:100%;background:url(images/{src}) left top / cover no-repeat"></span>'
  parts.append(entity('arch-image-'+key,20+i*344,184,320,273.12676,content,int(step>=5),style='border:1px solid #444;border-radius:6px;background:#202020;overflow:hidden;',duration=.45,delay=.35 if step==5 else 0))
 enter=' data-id="arch-enter" data-enter-as-unit data-auto-animate-duration="0.8"' if step==0 else ''
 return f'<div class="crystafig architecture-sequence"{enter} style="width:{SCENE_WIDTH*K:.5f}px;height:454.51807px">'+''.join(parts)+'</div>'

write('20_architecture.html','One project, six ways to work',[scene(n) for n in [0,1,2,4,5]],'The same project, <span class="blue">whichever way you open it</span>.','STAP original stack · stable objects, source interface order',extra_note='The original source order is retained throughout: Python library, application, command line. Remove third-party engines, centre crysta, introduce the command line, then in one click reveal six routes above the three interfaces while moving the lower boxes and widening crysta. Python API is the same width as one route and only serves Python; application and command line connect directly to crysta. Box rows have 42-unit gaps. Screenshot frames follow the source STAP three-column crop, top-left at 355:303, then fade scientific layers before showing matching interface images. The standalone command line is currently fit-only. Source https://easydiffraction.org/user-guide/.',seconds=140)
p=S/'20_architecture.html';text=p.read_text().replace('<section>','<section data-reserve="off">',1).replace(' data-auto-animate-restart','')
text=text.replace('data-auto-animate-unmatched="false" data-auto-animate>','data-auto-animate-unmatched="false" data-auto-animate data-auto-animate-duration="0.8" data-auto-animate-easing="cubic-bezier(0.4,0,0.2,1)">')
# Reserve the conclusion's real height from the outset. Only opacity changes on its click.
close_style='height:auto;margin:calc(var(--gap-close) - (var(--gap) - 0.1em)) 0 var(--gap-close);overflow:visible'
hidden='<p class="statement" data-id="close" style="'+close_style+';opacity:0" data-auto-animate-duration=".8">The same project, <span class="blue">whichever way you open it</span>.</p>'
for leaf in leaves(text):
 if '<p class="statement"' not in leaf:text=text.replace(leaf,leaf+'\n'+hidden+'\n',1)
text=text.replace('<p class="statement" data-id="close" data-auto-animate-duration="1.1">','<p class="statement" data-id="close" style="'+close_style+';opacity:1" data-auto-animate-duration=".8">')
p.write_text(text)
