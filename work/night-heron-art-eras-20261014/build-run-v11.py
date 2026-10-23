from pathlib import Path
import json
root=Path(__file__).resolve().parent
def revision(src,dst,pairs):
 text=(root/src).read_text('utf8')
 for a,b in pairs:
  assert a in text,(src,a[:100])
  text=text.replace(a,b)
 (root/dst).write_text(text,encoding='utf8')
revision('src/run-v10-gait.mjs','src/run-v11-gait.mjs',[
 ('STRIDE=400, STANCE=.54','STRIDE=280, STANCE=.52'),
 ('rear=.72-STRIDE/size*STANCE','rear=.76-STRIDE/size*STANCE'),
 ('x:.72-STRIDE/size*p','x:.76-STRIDE/size*p'),
 ('xs=[rear,.31,.67,.76,.72]','xs=[rear,.54,.74,.85,.76]'),
 ('heights=[0,.205,.225,.145,0]','heights=[0,.235,.26,.175,0]')])
revision('src/run-v10.js','src/run-v11.js',[
 ('run-v10-legs.js','run-v11-legs.js'),('run-v10-gait.mjs','run-v11-gait.mjs'),('production-plan-run-v10.json','production-plan-run-v11.json'),
 ('bob=-(4+13*swagger)*pulse,angle=swagger*(-.025+.045*Math.sin(cycle*Math.PI*2))',
  'bob=-4*pulse-swagger*(32+22*pulse),angle=swagger*(-.055+.075*Math.sin(cycle*Math.PI*2))')])
revision('run-v10.html','run-v11.html',[('src/run-v10.js','src/run-v11.js')])
revision('audio-run-v10.mjs','audio-run-v11.mjs',[('run-v10','run-v11')])
revision('verify-run-v10.mjs','verify-run-v11.mjs',[('run-v10','run-v11')])
revision('package-run-v10.py','package-run-v11.py',[('run-v10','run-v11')])
revision('render-run-v10.mjs','render-run-v11.mjs',[
 ('run-v10.html','run-v11.html'),('render-run-v10.mjs','render-run-v11.mjs'),('build-run-v10.py','build-run-v11.py'),('verify-run-v10.mjs','verify-run-v11.mjs'),
 ('package-run-v10.py','package-run-v11.py'),('audio-run-v10.mjs','audio-run-v11.mjs'),('production-plan-run-v10.json','production-plan-run-v11.json'),
 ('check-timing-run-v10.mjs','check-timing-run-v11.mjs'),('audio/score-run-v10.wav','audio/score-run-v11.wav'),("'audio','score-run-v10.wav'","'audio','score-run-v11.wav'"),
 ('audio/events-run-v10.json','audio/events-run-v11.json')])
revision('check-timing-run-v10.mjs','check-timing-run-v11.mjs',[
 ('run-v10','run-v11'),('const c=j/3000,bob=-17*Math.sin(c*Math.PI*2)**2,angle=-.025+.045*Math.sin(c*Math.PI*2);',
 'const c=j/3000;for(const swagger of[0,.25,.5,.75,1]){const pulse=Math.sin(c*Math.PI*2)**2,bob=-4*pulse-swagger*(32+22*pulse),angle=swagger*(-.055+.075*Math.sin(c*Math.PI*2));'),
 ('[[0,.47],[.5,.42]]','[[0,.49],[.5,.405]]'),
 ('maxBoundaryJump=0;', 'maxBoundaryJump=0,minHockBelowHip=9;'),
 ('minReach=Math.min(minReach,d);','const along=(.25**2-.26**2+d*d)/(2*d),side=Math.sqrt(.25**2-along*along),hockY=h[1]+(f.y-h[1])/d*along+(f.x-h[0])/d*side;minHockBelowHip=Math.min(minHockBelowHip,hockY-h[1]);minReach=Math.min(minReach,d);'),
 ('maxBoundaryJumpPixels:maxBoundaryJump,sync', 'maxBoundaryJumpPixels:maxBoundaryJump,minHockBelowHipPixels:minHockBelowHip*510,sync'),
 ('if(maxPhaseError>1e-8', 'if(minHockBelowHip<0||maxPhaseError>1e-8'),
 ('}\nfor(let n=2;', '}}\nfor(let n=2;'),
 ("[.035,.415]","[.01,.51]"),('minReach<.035||maxReach>.415','minReach<.01||maxReach>.51'),
 ('[0,.54,.54+.46*.22,.54+.46*.56,.54+.46*.8]','[0,.52,.52+.48*.22,.52+.48*.56,.52+.48*.8]')])
p=json.loads((root/'production-plan-run-v10.json').read_text('utf8'));p['version']='run-v11-fast-leg-silhouette'
p['brief']['revision']='用户再次反馈：步频再快、腿形更明显、更加夸张嚣张。步频提高约43%；平跑时抬高身体露出腿部，大幅折腿/前踢，实体腿段、关节与张开的脚趾；抢鱼窗口收住身体，脚步配乐重算。'
p['audio']={**p['audio'],'score':'audio/score-run-v11.wav','events':'audio/events-run-v11.json','clock':'src/run-v11-gait.mjs'}
(root/'production-plan-run-v11.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
print('v11 isolated sources ready; v10 preserved')
