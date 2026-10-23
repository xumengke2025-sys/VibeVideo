from pathlib import Path
import json,shutil
root=Path(__file__).resolve().parent
def copyreplace(src,dst,pairs):
 text=(root/src).read_text('utf8')
 for a,b in pairs:
  assert a in text,(src,a[:100])
  text=text.replace(a,b)
 (root/dst).write_text(text,encoding='utf8')
shutil.copy2('C:/Windows/Fonts/msyhbd.ttc',root/'assets/run-v10-era-bold.ttc')
copyreplace('run-v9.html','run-v10.html',[
 ('<style>','<style>@font-face{font-family:EraBold;src:url("assets/run-v10-era-bold.ttc");font-weight:700;font-display:block}'),
 ('src/run-v9.js','src/run-v10.js')])
copyreplace('src/run-v5-legs.js','src/run-v10-legs.js',[
 ('// Continuous two-link avian limbs. Stance feet follow exact world distance.','import {footAt,bodyPoint} from "./run-v10-gait.mjs";\n// High folded avian recovery, forward kick and an emphatic planted step.'),
 ('ctx,cycle,size,bob,era)','ctx,cycle,size,bob,era,angle=0)'),
 ('  const p=(cycle+offset)%1,stance=p<.6,f=stance?0:(p-.6)/.4;\n  // C1 swing return, including a raised toe arc; stance does not slide.\n  const smooth=f*f*(3-2*f),x=stance?.65-(310/size)*p:(.65-(310/size)*.6)+(310/size)*.6*smooth;\n  const y=.84-(stance?0:.125*Math.sin(Math.PI*f)**2);',
  '  const step=footAt(cycle,offset,size),{x,y,stance}=step,f=step.f||0;'),
 ('const hip=[back?.42:.47,.588],foot=[x,y],a=.17,b=.205','const hip=bodyPoint([back?.42:.47,.588],bob,angle,size),foot=[x,y],a=.19,b=.225'),
 ('era===3?8:painted?7:10','era===3?9:painted?9:12'),
 ('era===3?4.5:6.4','era===3?5:7.5'),
 ('const tuck=stance?0:Math.sin(Math.PI*f)*.026;','const tuck=stance?0:Math.sin(Math.PI*f)*.038;'),
 ('y+ty-tuck','y+ty-tuck-(stance?0:.022*Math.sin(Math.PI*f))')])
copyreplace('src/run-v9.js','src/run-v10.js',[
 ("import {drawLegs} from './run-v5-legs.js';", "import {drawLegs} from './run-v10-legs.js';\nimport {cycleAt,bodyPoint,footAt} from './run-v10-gait.mjs';"),
 ('production-plan-run-v9.json','production-plan-run-v10.json'),
 ('await document.fonts.ready;', 'await document.fonts.load("700 70px EraBold");await document.fonts.ready;'),
 ('cycle=((sceneDistance(t)/310)%1)', 'cycle=cycleAt(t)'),
 ('const bob=-4*(1-Math.cos(cycle*Math.PI*4))*.5;', 'const swagger=1-S(e.reachStart-2,e.grab,local)+S(e.fishGone,e.neckTucked,local),pulse=Math.sin(cycle*Math.PI*2)**2,bob=-(4+13*swagger)*pulse,angle=swagger*(-.025+.045*Math.sin(cycle*Math.PI*2));'),
 ('drawLegs(ctx,cycle,sz,bob,window.__era);\n ctx.drawImage(feed.image,0,0,sz,sz);ctx.restore();',
  'drawLegs(ctx,cycle,sz,bob,window.__era,angle);\n ctx.save();ctx.translate(sz*.44,sz*.57);ctx.rotate(angle);ctx.drawImage(feed.image,-sz*.44,-sz*.57,sz,sz);ctx.restore();ctx.restore();'),
 ('const tip={x:x-sz*.45+feed.tip[0]*sz,y:y-sz*.84+bob+feed.tip[1]*sz},eye={x:x-sz*.45+feed.eye[0]*sz,y:y-sz*.84+bob+feed.eye[1]*sz};return{tip,eye,cycle,bob};',
  'const tp=bodyPoint(feed.tip,bob,angle,sz),ep=bodyPoint(feed.eye,bob,angle,sz),tip={x:x-sz*.45+tp[0]*sz,y:y-sz*.84+tp[1]*sz},eye={x:x-sz*.45+ep[0]*sz,y:y-sz*.84+ep[1]*sz};return{tip,eye,cycle,bob,angle,feet:[0,.5].map(o=>footAt(cycle,o,sz))};'),
 ("const lightLabel=[2,5,7,15].includes(i);g.fillStyle=lightLabel?'#f2e0b3':'#30352e';g.shadowColor=lightLabel?'rgba(15,12,8,.75)':'rgba(255,248,225,.85)';g.shadowBlur=5;g.font='60px Kai, KaiTi, serif';g.textAlign='left';const eraLabel=sh.era+' · '+sh.date;g.strokeStyle=lightLabel?'rgba(22,24,20,.4)':'rgba(252,244,223,.5)';g.lineWidth=1.5;g.strokeText(eraLabel,78,160,924);g.fillText(eraLabel,78,160,924);g.shadowBlur=0;",
  "const wash=g.createLinearGradient(0,0,0,280);wash.addColorStop(0,'rgba(18,23,23,.76)');wash.addColorStop(.58,'rgba(18,23,23,.62)');wash.addColorStop(1,'rgba(18,23,23,0)');g.fillStyle=wash;g.fillRect(0,0,W,280);g.font='700 70px EraBold';g.textAlign='left';const eraLabel=sh.era+' · '+sh.date;g.lineJoin='round';g.strokeStyle='rgba(14,20,22,.7)';g.lineWidth=4;g.strokeText(eraLabel,70,169);g.fillStyle='#fff5df';g.fillText(eraLabel,70,169);"),
 ('tip:bp.tip,cycle:bp.cycle','tip:bp.tip,cycle:bp.cycle,bob:bp.bob,bodyAngle:bp.angle,feet:bp.feet')])
p=json.loads((root/'production-plan-run-v9.json').read_text('utf8'))
p['version']='run-v10-swagger-score-type'
p['brief']['onscreenText']='仅时代与年份，嵌入微软雅黑粗体70px；暖白文字与顶部局部深色渐隐底'
p['brief']['revision']='用户反馈：高抬腿/前踢大跨步与得意身体摆动；脚步音乐共享绝对距离时钟，取鱼吞咽和时代变化作配乐重音。16种动物及看空地反应保留。'
p['audio']={'score':'audio/score-run-v10.wav','events':'audio/events-run-v10.json','clock':'src/run-v10-gait.mjs','genre':'原创俏皮潜行爵士：拨弦低音、木琴/短铜管主题、轻鼓与动作标点','perception':'not listened'}
for s in p['timeline']['shots']:
 s['reads']='时代年份稳定可读；高抬腿前踢向前；喙接触鱼后叼起吞下；原主人惊讶并低头看空地，夜鹭得意离开。'
(root/'production-plan-run-v10.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
copyreplace('render-run-v9.mjs','render-run-v10.mjs',[
 ("'.js':'text/javascript'", "'.js':'text/javascript','.mjs':'text/javascript','.ttc':'font/collection'"),
 ('run-v9.html','run-v10.html'),('production-plan-run-v9.json','production-plan-run-v10.json'),
 ("'render-run-v9.mjs','prepare-run-v9.py'", "'render-run-v10.mjs','build-run-v10.py'"),
 ('verify-run-v9.mjs','verify-run-v10.mjs'),('check-reactions-run-v9.py','check-reactions-run-v10.py'),('package-run-v9.py','package-run-v10.py'),
 ('audio-run-v4.mjs','audio-run-v10.mjs'),('audio/score-run-v4.wav','audio/score-run-v10.wav'),
 ("path.join(root,'audio','score-run-v4.wav')", "path.join(root,'audio','score-run-v10.wav')"),
 ("'transitions-run-v4.json',...walk('src')", "'transitions-run-v4.json','check-timing-run-v10.mjs','sample-check-run-v10.py','montage-run-v10.py','assets/run-v10-era-bold.ttc','audio/events-run-v10.json',...walk('src')")])
copyreplace('package-run-v9.py','package-run-v10.py',[('production-plan-run-v9.json','production-plan-run-v10.json')])
copyreplace('check-reactions-run-v9-resting.py','check-reactions-run-v10.py',[('production-plan-run-v9.json','production-plan-run-v10.json')])
copyreplace('verify-run-v9.mjs','verify-run-v10.mjs',[('run-v9-kinematics','run-v10-kinematics'),('production-plan-run-v9.json','production-plan-run-v10.json'),('run-v9.html','run-v10.html'),
 ("'.js':'text/javascript'", "'.js':'text/javascript','.mjs':'text/javascript','.ttc':'font/collection'"),
 ('const owners=plan.timeline.shots.map', "if(records.some(r=>r.states.some(s=>s.eraLabelWidth>940)))throw Error('Era label overflow');\n const owners=plan.timeline.shots.map")])
print('v10 isolated sources created; v9 preserved')
