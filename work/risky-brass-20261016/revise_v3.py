from pathlib import Path
import shutil,re,json
R=Path(__file__).parent; old=R/'v2'; new=R/'v3';new.mkdir(exist_ok=True)
for name in ['assets','vendor']:
    shutil.copytree(old/name,new/name,dirs_exist_ok=True)
for name in ['index.html','render.cjs','full-audio.wav','make_audio.py','README.md','BRIEF.md','交付说明.md','finalize.py']:
    shutil.copy2(old/name,new/name)
(new/'qa'/'independent-review').mkdir(parents=True,exist_ok=True)
s=(old/'scene.js').read_text(encoding='utf-8')
# Texture pixels match the exact physical face aspect. Never stretch a minimum-height canvas.
s=s.replace("const tex=engravingTexture(Array.isArray(s)?s:[s],1024,Math.max(160,Math.round(1024*h/w)));", "const faceAspect=(w*.97)/(h*.93),tw=Math.max(1024,Math.ceil(144*faceAspect)),th=Math.round(tw/faceAspect);const tex=engravingTexture(Array.isArray(s)?s:[s],tw,th);textMetrics.push({text:s,textureAspect:tw/th,faceAspect,error:Math.abs((tw/th)/faceAspect-1)});")
s=s.replace('function label(s,w,h,p,','const textMetrics=[];\nfunction label(s,w,h,p,')
replacements={
 '固定这次资料':'固定资料','同一份资料':'同份资料','A17 · 同份资料':'A17 · 同源',
 '已有偿债压力':'已有压力','假设获得资金支持':'假设资金支持',
 '先确认公司和事件':'确认公司与事件','先看资料，再作判断':'核对资料',
 '看看还涉及哪些公司':'梳理公司关系','带着资料，请专家一起看':'专家讨论',
 "const expertNames=['尽调评估专家','产业授信评估专家','合规风险专家','风险监控专家'];":"const expertNames=['尽调','授信','合规','监控'];",
 '出处：示例资料':'示例出处','待核验消息':'待核验','先保留疑问':'待查',
 '不作为已知事实':'暂不采信','不直接接入试验':'不接入试验',
 '资金到位时间':'资金何时到位','相关方影响增大':'影响增大','假设采取措施':'假设支持',
 '每一步，都能回头查':'保留过程记录','与公司沟通核验':'沟通核验',
 '假设寻求资金':'假设筹资','记录措施与变化':'记录变化','示例过程':'示例',
 'A17 · 试验记录':'A17 · 结果','条件、过程、待查问题':'条件 · 过程 · 待查',
 '示例公司':'合成案例','示例事件':'合成案例','借款公司 A':'借款方 A','集团企业 C':'集团 C',
}
for a,b in replacements.items():s=s.replace(a,b)
# Simplify labels rather than horizontally squeezing lengthy names.
s=s.replace("label(name,1.27,.38", "label(name,1.27,.42")
s=s.replace("label(['借款公司 A','担保方 B','集团企业 C'][i]", "label(['借款方 A','担保方 B','集团 C'][i]")
s=s.replace("enterprise('借款公司 A'", "enterprise('借款方 A'").replace("enterprise('集团企业 C'", "enterprise('集团 C'")
# Arc-length motion removes per-segment speed fluctuations.
s=s.replace('curve.getPoint(clamp(u)),D=curve.getTangent(clamp(u))','curve.getPointAt(clamp(u)),D=curve.getTangentAt(clamp(u))')
s=s.replace('q=p(t,a,b);v.token.visible=t>=a&&t<=b;', 'q=ramp(t,a,b);v.token.visible=t>=a&&t<=b;')
s=s.replace('const round=p(t,10,21)', 'const round=ramp(t,10,21)')
# Adjacent monotone camera segments share a bounded tangent; holds remain true holds.
camera_insert='''
// C2 quintics share bounded monotone endpoint velocities; no stop at every transit marker.
for(let i=1;i<poses.length-1;i++)for(const [field,vel] of [['P','v'],['L','lv']])for(let j=0;j<3;j++){
 const a=poses[i-1],b=poses[i],c=poses[i+1],da=(b[field][j]-a[field][j])/(b.t-a.t),db=(c[field][j]-b[field][j])/(c.t-b.t);
 b[vel][j]=da*db>0?Math.sign(da)*Math.min(Math.abs(2*da*db/(da+db)),1.1*Math.min(Math.abs(da),Math.abs(db))):0;
 if(b.t===34.2||b.t===36.2)b[vel][j]=0;
}
'''
s=s.replace('function cameraAt(t){',camera_insert+'\nfunction cameraAt(t){')
# Finish the final reveal before fading, with a longer travel window.
s=s.replace('"t": 76.7','"t": 75.8')
s=s.replace('{"t": 80, "P": [-3, 30, 51], "L": [-3.5, 1.4, -2], "v": [0, 0, 0], "lv": [0, 0, 0], "f": 43}', '{"t": 79.5, "P": [-3.5, 24, 47], "L": [-3.5, 1.4, -2], "v": [0, 0, 0], "lv": [0, 0, 0], "f": 48}, {"t": 80, "P": [-3.5, 24, 47], "L": [-3.5, 1.4, -2], "v": [0, 0, 0], "lv": [0, 0, 0], "f": 48}')
# Cards turn smoothly into each next track during the stationary dwell, not at departure.
needle=' if(full>=66)place(mainCase,returning,ramp(full,66,72),.25);'
s=s.replace(needle,needle+'''
 const nextTurns=[{at:14,path:earlyPaths[1]},{at:22,path:earlyPaths[2]},{at:30,path:earlyPaths[3]},{at:32,path:earlyPaths[4]},{at:55,path:recordPath},{at:66,path:returning}];
 for(const next of nextTurns)if(full>=next.at-.5&&full<next.at){const D=next.path.getTangentAt(0),target=Math.atan2(-D.z,D.x),delta=Math.atan2(Math.sin(target-mainCase.rotation.y),Math.cos(target-mainCase.rotation.y));mainCase.rotation.y+=delta*ramp(full,next.at-.5,next.at);}
''')
# One concise main sentence; supporting conditions remain in mechanical labels.
caps=[
 [0,'Risky 风险视角'],[2.5,'确认公司与事件'],[7,'资料须有出处'],[10,'已核对的归档，待核验的另存'],
 [15,'梳理公司关系'],[19,'行业相近，不等于风险相连'],[23,'同份资料，多方讨论'],[27,'留下意见和疑问'],
 [32,'固定资料，保持同一起点'],[36.4,'选定条件，确认后试验'],[41.4,'A 还款承压，B 提供担保'],
 [43.8,'黄柱越高，示例影响越大'],[45.5,'融资更难：先看 A，再看相关方'],[49.9,'资金支持：压力可能减轻'],
 [54,'比较不同条件下的结果'],[57,'分开记录公司应对与模拟消息'],[61,'模拟消息，不是真实新闻'],
 [66,'带着结果，回到原案件'],[72,'专家复核，留下待查问题'],[77,'查资料 · 请专家 · 试条件 · 再复核']]
s=re.sub(r'const captions=\[.*?\n\];','const captions='+json.dumps(caps,ensure_ascii=False)+';',s,flags=re.S)
a=s.index('function textOverlay(t)');b=s.index('function interpolatePosition',a)
s=s[:a]+'''function textOverlay(t){const z=W/1920;ctx.save();ctx.scale(z,z);let k=0;for(let i=0;i<captions.length;i++)if(t>=captions[i][0])k=i;const cap=captions[k],next=captions[k+1]?.[0]??80;
const alpha=Math.min(ramp(t,cap[0],cap[0]+.18),1-ramp(t,next-.12,next),1-ramp(t,79.2,80));
const gr=ctx.createLinearGradient(0,924,0,1080);gr.addColorStop(0,'rgba(8,14,14,0)');gr.addColorStop(1,'rgba(8,14,14,.8)');ctx.fillStyle=gr;ctx.fillRect(0,924,1920,156);
ctx.globalAlpha=alpha;ctx.textAlign='center';ctx.fillStyle='#f3ead5';ctx.font='400 36px "Microsoft YaHei"';ctx.fillText(cap[1],960,998);
ctx.globalAlpha=Math.min(ramp(t,0,.7),1-ramp(t,79.2,80));ctx.fillStyle='#c3b89f';ctx.font='18px "Microsoft YaHei"';ctx.fillText('合成示例 · 非实际预测',960,1045);ctx.restore();}
''' + s[b:]
s=s.replace('window.sceneInfo={','window.textMetrics=textMetrics;\nwindow.sceneInfo={')
s=s.replace('duration:80,style:', 'duration:80,fps:60,revision:"v3-type-and-motion",style:')
(new/'scene.js').write_text(s,encoding='utf-8')
def ts(t):
    ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
(new/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{ts(c[0])} --> {ts(caps[i+1][0] if i+1<len(caps) else 80)}\n{c[1]}' for i,c in enumerate(caps))+'\n',encoding='utf-8')
f=(new/'finalize.py').read_text(encoding='utf-8').replace("'final-engineering-fixed'","'final-engineering'").replace("'30/1',2400","'60/1',4800").replace("'decoded_frames':2400","'decoded_frames':4800")
(new/'finalize.py').write_text(f,encoding='utf-8')
(new/'BRIEF.md').write_text('80秒，1920×1080，60fps。用户追加要求：修正压扁字形、精简文字、动作更流畅、重新审核。\n\n'+(old/'BRIEF.md').read_text(encoding='utf-8').replace('30fps','60fps'),encoding='utf-8')
(new/'REVISION.md').write_text('文字纹理严格匹配实际平面比例，移除最小高度拉伸；铭牌短句和单行字幕；相机中间节点共享有界速度、夹具停机；主体弧长运行、起停缓动、停留时预转向；60fps输出。保留业务状态、轨道、音轨、80秒叙事。\n',encoding='utf-8')
print('v3 written; captions',len(caps),'source',len(s))
