from pathlib import Path
import json
root=Path(__file__).resolve().parent
for name in ['run-v11.html','src/run-v11.js','src/run-v11-gait.mjs','src/run-v11-legs.js','render-run-v11.mjs','verify-run-v11.mjs','package-run-v11.py','audio-run-v11.mjs','check-timing-run-v11.mjs','sample-check-run-v11.py','final-media-run-v11.py']:
    dst=name.replace('v11','v12')
    text=(root/name).read_text('utf8').replace('run-v11','run-v12')
    (root/dst).write_text(text,encoding='utf8')
p=json.loads((root/'production-plan-run-v11.json').read_text('utf8'))
p['version']='run-v12-natural-night-heron'
p['brief']['revision']='恢复紧凑成年夜鹭体形，短腿、轻快步伐；逐画风按真实眼位置补红色虹膜及两根细长白色枕羽。保留16种动物、低头看空地、字幕、音乐踩点。'
p['audio']={**p['audio'],'score':'audio/score-run-v12.wav','events':'audio/events-run-v12.json','clock':'src/run-v12-gait.mjs'}
(root/'production-plan-run-v12.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
print('v12 base created; historical v11 preserved')

# Apply the anatomical revision after cloning the preserved v11 sources.
def edit(name,pairs):
    p=root/name;s=p.read_text('utf8')
    for a,b in pairs:
        assert a in s,(name,a)
        s=s.replace(a,b)
    p.write_text(s,encoding='utf8')
edit('src/run-v12.js',[
 ("import {generatedBackgrounds}","import {drawIdentity} from './run-v12-identity.js';\nimport {generatedBackgrounds}"),
 ('return{image:partLayer,tip:skin(tip0),eye};','drawIdentity(partG,window.__era,eye,angle);\n return{image:partLayer,tip:skin(tip0),eye};'),
 ('bob=-4*pulse-swagger*(32+22*pulse),angle=swagger*(-.055+.075*Math.sin(cycle*Math.PI*2))','bob=18*swagger-(4+4*swagger)*pulse,angle=swagger*(-.018+.036*Math.sin(cycle*Math.PI*2))')])
edit('src/run-v12-gait.mjs',[
 ('rear=.76-STRIDE/size*STANCE','front=.67-(offset>.1?.06:0),rear=front-STRIDE/size*STANCE'),
 ('x:.76-STRIDE/size*p','x:front-STRIDE/size*p'),
 ('xs=[rear,.54,.74,.85,.76]','xs=[rear,front-.20,front-.07,front+.035,front]'),
 ('heights=[0,.235,.26,.175,0]','heights=[0,.080,.105,.060,0]')])
edit('src/run-v12-legs.js',[
 ('a=.25,b=.26','a=.16,b=.18'),('.015,.012,light','.010,.008,light'),('.012,.008,light','.008,.006,light'),
 ('pixel?5:6.2,pixel?5:5.5','pixel?3.5:4.2,pixel?3.5:4'),
 ('[[.095,.015],[.068,.033],[-.052,.023]]','[[.068,.012],[.049,.025],[-.037,.018]]'),
 ('pixel?9:10','pixel?7:7.5'),('pixel?5.8:6.5','pixel?4.5:4.8')])
edit('check-timing-run-v12.mjs',[
 ('bob=-4*pulse-swagger*(32+22*pulse),angle=swagger*(-.055+.075*Math.sin(c*Math.PI*2))','bob=18*swagger-(4+4*swagger)*pulse,angle=swagger*(-.018+.036*Math.sin(c*Math.PI*2))'),
 ('.25**2-.26**2','.16**2-.18**2'),('Math.sqrt(.25**2-along*along)','Math.sqrt(.16**2-along*along)'),
 ('[.01,.51]','[.02,.34]'),('minReach<.01||maxReach>.51','minReach<.02||maxReach>.34')])
edit('sample-check-run-v12.py',[('sample-run-v12-fast-strut-03','sample-run-v12-natural-heron')])
edit('final-media-run-v12.py',[('film-run-v12-fast-strut-final-02','film-run-v12-natural-heron-final')])
