"""One-time transfer of the existing V3 primitives into the V4 scene.
The generated scene-body.js remains directly editable; do not rerun after editing it.
"""
from pathlib import Path
r=Path(__file__).resolve().parent
s=(r/'v3/scene-body.js').read_text(encoding='utf-8')
helpers=s[s.index('function plaque'):s.index('function caseBox')]
dial=s[s.index('function dial'):s.index('function signal')]
signal=s[s.index('function signal'):s.index('function relations')]
signal=signal.replace("if(T>=9&&T<=13.1)caseBox(1000,1200);",'')
signal=signal.replace("});if(T>=13.1&&T<=17)carrier(paths.evidence,13.1,17);}",'});}')
signal=signal.replace("gear(-540,140,20,5,T*.38", "gear(-540,140,20,5,ease(p(T,6,10))*TAU")
signal=signal.replace("p(T,7,10)","p(T,7,atTime('bind'))")
hall=s[s.index('function hall'):s.index('function screw')]
hall=hall.replace("if(T>=28&&T<=39)caseBox(5900,1600);",'')
hall=hall.replace("});if(T>=39&&T<=42)carrier(paths.snapshot,39,42);}",'});}')
hall=hall.replace("T>=72?", "T>=75?").replace("T>36.7", "T>35.5")
hall=hall.replace("T>=34&&T<37.8", "T>=30&&T<34").replace("p(T,34,36.5)","p(T,30,atTime('knowledge'))")
hall=hall.replace("p(T,33.3,34.3)","p(T,29.5,31)")
hall=hall.replace("TX('检索依据'", "TX('检索依据'")
hall=hall.replace("T>28.8", "T>27").replace("show(29+(j-3)*.5)","show(27+(j-3)*.25,.5)")
screw=s[s.index('function screw'):s.index('function drum')]
body=(r/'v4/body-template.js').read_text(encoding='utf-8')
body=body.replace('// @TRANSFER_HELPERS',helpers+dial+screw).replace('// @TRANSFER_SIGNAL',signal).replace('// @TRANSFER_HALL',hall)
(r/'v4/scene-body.js').write_text(body,encoding='utf-8')
paper=(r/'v3/vendor/paper.js').read_text(encoding='utf-8')
a=paper.index('vec3 paper(vec2 p){');b=paper.index('\nvoid main(){',a)
paper=paper[:a]+'''vec3 paper(vec2 p){
  float cloud=fbm(p/1100.);
  vec3 c=mix(vec3(.025,.071,.118),vec3(.043,.125,.194),cloud);
  float fine=vn(p/3.5);
  c*=.98+.035*fine;
  float brush=fbm(vec2(p.x/1600.,p.y/190.));
  c+=vec3(.007,.009,.012)*(brush-.5);
  float e=min(min(p.x,sheet.x-p.x),min(p.y,sheet.y-p.y));
  c=mix(c,vec3(.085,.16,.22),smoothstep(35.,0.,e)*.25);
  return c;
}'''+paper[b:]
paper=paper.replace('float grainK = .80 + .20*smoothstep(.2, .8, vn(p*.9 + 3.));','float grainK = .98;')
paper=paper.replace('L1*.18 + L2*.10','L1*.07 + L2*.025')
(r/'v4/vendor/paper.js').write_text(paper,encoding='utf-8')
print('Transferred supported geometry; wrote V4 scene and restrained paper shader')
