from pathlib import Path
import json
R=Path(__file__).resolve().parent
old=R.parent/'v10'
body=(old/'scene-body.js').read_text(encoding='utf-8')
body=body.replace("if(T<5.8){const u=", "if(T<5.8){const priorVisibility=visibility;visibility*=ease(p(filmTime,10.7,11));const u=")
body=body.replace("u,'示例客户信息',270);}","u,'示例客户信息',270);visibility=priorVisibility;}")
start=body.index('window.renderAt=')
end=body.index('window.__ready=true;',start)
body=body[:start]+'''window.renderAt=(t,type='image/png',quality=.95)=>{filmTime=Math.max(0,Math.min(60,t));T=Math.max(0,filmTime-8);bounds=[];const c=cameraAt(T);setCam({...c,z:c.z*scale});proj.k=.43;clear();NIBS.length=0;if(filmTime>8){chassis();intro();signals();experts();knowledge();visit();follow();const a=ease(p(filmTime,8,10.7));if(a<1){g.setTransform(1,0,0,1,0,0);g.globalCompositeOperation='destination-in';g.fillStyle=`rgba(0,0,0,${a})`;g.fillRect(0,0,W,H);g.globalCompositeOperation='source-over';}}opening(filmTime);compose(inkC,fxC,ovC,{sheet:[8200,4800],cam,seed:19});return type?canvas.toDataURL(type,quality):null;};
window.cameraAt=t=>cameraAt(Math.max(0,t-8));window.cameraKeys=keys.map(k=>[k[0]+8,...k.slice(1)]);
window.stateAt=t=>{window.renderAt(t,null);return{time:t,camera:cameraAt(T),buffer:[W,H],duration:60,shot:plan.shots.find(s=>t>=s.start&&t<s.end)?.id,bounds,opening:t<11,selectedCard:'opportunity-reduction-example'};};
'''+body[end:]
body=body.replace("+' / 52'","+' / 60'").replace('base>=52','base>=60').replace('Math.min(52,base','Math.min(60,base').replace('if(t>=52)','if(t>=60)')
(R/'scene-body.js').write_text(body,encoding='utf-8')
helpers=(old/'film.js').read_text(encoding='utf-8').split('// V6 original world geometry.')[0]
(R/'film.js').write_text(helpers+(R/'intro.js').read_text(encoding='utf-8')+'\n'+body,encoding='utf-8')
for filename in ['render.mjs','index.html']:
 s=(old/filename).read_text(encoding='utf-8').replace('/v10/','/v11/').replace('v10-expert-ai','v11-opportunity-cards').replace('args.duration||52','args.duration||60').replace('max="52"','max="60"').replace('0.00 / 52','0.00 / 60')
 (R/filename).write_text(s,encoding='utf-8')
plan=json.loads((old/'plan.json').read_text(encoding='utf-8'))
plan.update(duration=60,aspect_ratio='16:9',revision='V11 pain points and multi-scenario card extraction',concepts=['../concepts/v11/3.png','../concepts/v11/6.png','../concepts/v11/9.5.png'])
for s in plan['shots']:s['start']+=8;s['end']+=8
plan['shots'][0]['start']=11
plan['shots']=[dict(id='00-pain',name='B端商机痛点',start=0,end=4,voiceover='',reads='0.7–3.5秒四个痛点完整可读',action='收集耗时长、不知从何入手、归集不全、专业支持难找；同一蓝图纸上依次落墨'),dict(id='00-cards',name='多业务场景抽卡与连续入机',start=4,end=11,voiceover='',reads='4.8–6.4秒五种商机场景；6.4–7.8秒选中减持示例；8–11秒送入机器',action='五张奶白金边卡扇形展开，中心示例卡抽出；卡片保持身份缩短为蓝图载纸，与原纸载体位置一致',anchor='opportunity-reduction-example',handoff='10.7–11秒同一位置、尺寸、方向与载纸交接，相机保持原C2轨迹')]+plan['shots']
score=plan['soundtrack']
for key in ['events','phrases','density']:
 for e in score[key]:
  for k in ['at','start','end']:
   if k in e:e[k]+=8
score['breaks']=[[a+8,b+8] for a,b in score['breaks']]
score['events']=[dict(id='pain-'+str(i),at=.1+i*.21,sound='tick',action='痛点落墨') for i in range(4)]+[dict(id='cards-open',at=4,sound='downbeat',action='五张场景卡展开'),dict(id='card-extract',at=6.4,sound='accent',action='减持示例卡抽出'),dict(id='card-travel',at=8,sound='travel',action='卡片转为蓝图载纸'),dict(id='card-dock',at=10.7,sound='tick',action='同一载纸接入原流水线')]+score['events']
score['phrases'].insert(0,dict(start=0,end=8,beats=20,bpm=150))
score['density'].insert(0,dict(start=0,end=8,gain=.65))
score['retained_body_audio']='audio/retained-v10.wav; starts exactly at 8s, original action accents shifted by 8s'
(R/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
print('V11 rebuilt: 60s, retained original body at +8s')
