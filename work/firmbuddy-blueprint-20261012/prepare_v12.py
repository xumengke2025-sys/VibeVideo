from pathlib import Path
import shutil,json

B=Path(__file__).resolve().parent
R=B/'v12'
if R.exists(): raise SystemExit('v12 already exists; edit it in place')
shutil.copytree(B/'v11',R)
for f in ['prepare_v11.py','update_tools.py','collect_delivery.py','package_delivery.py','package_v11.py','check_layout.mjs']:
    (R/f).unlink(missing_ok=True)
for name in ['render.mjs','check_motion.mjs','verify_delivery.py','README.md','setup.py']:
    p=R/name;s=p.read_text(encoding='utf-8').replace('v11-opportunity-cards','v12-business-value').replace('v11','v12').replace('V11','V12')
    p.write_text(s,encoding='utf-8')
plan=json.loads((R/'plan.json').read_text(encoding='utf-8'))
plan.update(revision='V12 business pain → analysis → practical result',aspect_ratio='16:9')
plan['shots']=[
 dict(id='pain',start=0,end=4,name='客户经营的四项困难',reads='1.3–3.5四个业务问题完整可读',action='同纸面落墨，形成问题地图'),
 dict(id='scenarios',start=4,end=11,name='按业务场景进入',reads='4.8–6.4多场景，6.4–8选择减持示例',action='五卡扇形展开，选中卡抽出并连续图纸化入机'),
 dict(id='input',start=11,end=13,name='业务问题进入工作流',reads='11.1–11.5三个入口',action='商机查询、业务答疑、拜访准备；AI理解问题调用工具'),
 dict(id='discovery',start=13,end=18,name='解决找线索慢',reads='14–15源材料；15.4–16.3归集结果',action='公告、股东动态、客户资料沿三条馈线合为客户线索档案',result='减少逐项搜集筛选，把精力放在值得跟进的客户'),
 dict(id='judgement',start=18,end=27,name='解决有线索缺切入点',reads='20–24.1九领域与专家会场，21.3–24.1会商结论',action='需求、时机、切入点三个议题汇入中央会商台，知识装备和业务方法支持专业判断',result='市场信息转成可讨论的服务思路'),
 dict(id='support',start=27,end=37,name='解决专业支持难获取',reads='29–30六类知识；30.5–33.6检索依据和服务方向',action='同一会商议题驶向知识装备仓，剖面打开、资料抽出，AI检索查证并辅助客户分型',result='减少反复找专家查材料，为业务判断提供专业依据'),
 dict(id='preparation',start=37,end=45,name='解决跟进准备重复',reads='37.3–39.3材料归并，40.2–42.7成果包',action='拜访资料、沟通重点和后续安排三份材料汇入策略输出，打印触达建议与跟进节奏',result='研判落实为可用的客户沟通和经营计划'),
 dict(id='continuity',start=45,end=53,name='客户经营持续推进',reads='46–48.1客户记录，48.3–53反馈载体',action='人工审核入库，沟通需求与服务安排随记录载体回流',result='下一次经营可接续之前判断和沟通'),
 dict(id='payoff',start=53,end=60,name='兑现业务价值',reads='55.5–60整机与业务结果',action='沿回路连续拉远，揭示一条贯通发现、判断、准备与经营的工作流',result='找得到机会，讲得清服务，跟得住客户')]
plan['business_messages']=[
 dict(start=11.1,end=12.8,pain='从业务问题出发，进入客户经营工作流',result='商机查询 · 业务答疑 · 客户拜访准备'),
 dict(start=13,end=18,pain='找线索慢：资料分散，搜集筛选耗时',result='归集公告、股东动态与客户资料，聚焦值得跟进的客户'),
 dict(start=18.4,end=26.6,pain='有了线索：客户需要什么，何时切入？',result='AI 组织多专业研判，把市场信号转成服务切入点'),
 dict(start=27,end=36.8,pain='专业支持难：跨领域问题，反复找专家、查资料',result='专业专家团调用知识库，让判断有规则、有经验、有依据'),
 dict(start=37,end=45,pain='跟进准备重复：拜访材料、沟通重点反复整理',result='研判结果形成触达建议、沟通重点与跟进计划'),
 dict(start=45.3,end=53,pain='客户经营难接续：沟通过什么，下一步做什么？',result='保留客户记录，AI 辅助复评，让后续经营接得上')]
(R/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')

s=(R/'intro.js').read_text(encoding='utf-8')
s=s.replace("['信息归集不全','客户、公告与业务资料难串联']","['专业支持难找','复杂业务，反复找专家查资料']").replace("['专业支持难找','行业专家、运营专家难以触达']","['跟进准备重复','拜访材料、沟通重点反复整理']")
s=s.replace("['专业支持难找','复杂业务，反复找专家查资料']","['专业支持难找','跨领域问题，需要专业判断']")
s=s.replace('从发现线索，到形成行动','时间花在找资料，精力耗在做准备').replace('让线索、知识与专业判断，汇入同一条工作流','让时间回到判断需求、服务客户、推进合作上')
(R/'intro.js').write_text(s,encoding='utf-8')

s=(R/'scene-body.js').read_text(encoding='utf-8')
s=s.replace('商机查询：更早发现，提前经营','从业务问题出发，找到服务机会')
start=s.index('function signals()');end=s.index('function experts()',start)
s=s[:start]+'''function signals(){at(...centers.signals,()=>{
 TX('把分散资料，归集为客户线索',-730,-335,46,1);mono('01 / DISCOVER · CONNECT · FILTER',-730,-390,22,1,{v:.5});
 frameBase(-685,-245,1380,475);rail([[-720,220],[700,220]],.42);
 const sources=['公司公告','股东动态','客户资料'];
 sources.forEach((label,i)=>{const u=ease(p(T,6.1+i*.2,7+i*.2)),x=mix(-658,145,u),y=mix(-180+i*134,-80,u),v=1-ease(p(u,.6,1));
   route([[-258,-132+i*134],[-65,-132+i*134],[95,-80],[145,-80]],6.1+i*.2,7+i*.2,2.5,.65);
   if(v>.01){const prior=visibility;visibility*=v;doc(x,y,382,96,1);TX(label,x+30,y+64,36,1);visibility=prior;}
 });
 gear(-460,225,24,6,T*.7,1,.6,18);gear(-310,225,26,6,meshAngle(T*.7,24,26,[-460,225],[-310,225]),1,.55,18);
 doc(145,-208,517,393,1,.85);mono('SIGNAL / REDUCTION EXAMPLE',175,-158,17,1,{v:.55});
 TX('客户线索档案',175,-81,46,show(6.5));L([[175,-43],[620,-43]],show(6.6),1.4,.5);
 TX('减持商机示例',175,22,38,show(6.7));TX('AI 解读信号与客户情况',175,87,33,show(6.9));
 TX('重点客户 · 研判依据',175,147,32,show(7.1));
 });if(T>8.4&&T<11.7)movingRoute(paths.toHall,8.4,11.7);}
''' +s[end:]
s=s.replace('专业培养的 AI 专家团 · 按议题协作','业务研判：需求、时机与服务切入点')
s=s.replace("[[-720,97,'股东增减持'],[0,-121,'解禁预警'],[720,97,'拜访策略']]","[[-720,97,'客户需求'],[0,-121,'联系时机'],[720,97,'服务切入点']]")
s=s.replace('AI 汇总多专业研判','AI 汇总专业判断').replace('规则解读 · 时机研判 · 触达建议','结合客户情况，形成服务思路')
s=s.replace('plaque(label,x,555,670,44,u)','plaque(label,x,480,670,44,u)').replace('port=[x+335,555]','port=[x+335,480]').replace('[port[0],515]','[port[0],455]').replace('[side,515]','[side,455]')
s=s.replace('多源知识库 · 专家专业能力底座','专业问题，有知识依据与多专业支持')
s=s.replace('历史执行＋市场观察','规则 · 案例 · 研究依据').replace('核验主体 / 时效 / 反向条件','结合业务场景，核查适用条件')
s=s.replace('AI 辅助客户分型','AI 关联客户与服务').replace('示例策略：服务回访','服务方向：股份管理').replace('规则依据 · 业务经验 · 原文引用','专业培养的专家团 · 多源知识库 · 可追溯依据')
s=s.replace('AI 生成触达策略，把线索变成行动','减少重复准备，让研判落到客户跟进')
s=s.replace("doc(-50,-123,738,328,1);TX('触达策略包',-12,-65,43,1)","doc(-50,-123,738,328,1);TX('客户跟进准备包',-12,-65,43,1)")
needle="const x=mix(-492,243,ease(p(T,29.4,31.2))),u=1-ease(p(T,31.1,31.6));"
s=s.replace(needle,"""['拜访资料','沟通重点','后续安排'].forEach((label,i)=>{const z=ease(p(T,29.5+i*.25,31.1+i*.25)),v=1-ease(p(z,.65,1));if(v>.01){const prior=visibility;visibility*=v;const xx=mix(-707,-50,z),yy=mix(-110+i*92,-20,z);doc(xx,yy,430,72,1);TX(label,xx+28,yy+49,34,1);visibility=prior;}});
 const x=mix(-492,243,ease(p(T,29.4,31.2))),u=1-ease(p(T,31.1,31.6));""")
s=s.replace('联系时机 · 负责人建议','联系时机 · 服务切入点').replace('话术速查 · 合规要点 · 跟进节奏','拜访材料 · 合规要点 · 跟进节奏')
s=s.replace("['减持商机诊断','触达话术生成','客户经营计划']","['研判有结论','沟通有重点','跟进有计划']")
s=s.replace('人工审核入库，持续经营客户','保留经营记录，后续跟进接得上').replace("TX('商机中心',205,-85,48","TX('客户经营记录',205,-85,45").replace('减持线索 · 客户经营','沟通需求 · 服务安排').replace('触达准备 · 跟进服务','跟进事项 · 经营进展')
s=s.replace('客户池入口','问题入口').replace('前置信号','线索归集').replace('专业专家团','专业研判').replace('知识装备库','知识依据').replace('触达策略\',5600','跟进准备\',5600').replace('记录反馈','持续经营')
s=s.replace('专业知识驱动，让 AI 贯穿客户经营','找得到机会，讲得清服务，跟得住客户').replace('券商客户经营 · AI 专家协作平台','AI 辅助发现 · 专业研判 · 客户经营')
s=s.replace('opening(filmTime);compose','opening(filmTime);businessNarrative(filmTime);compose')
(R/'scene-body.js').write_text(s,encoding='utf-8')
with (R/'intro.js').open('a',encoding='utf-8') as f:f.write('''
// Editorial drafting notes outside the camera: problem and practical business result.
function businessNarrative(t){const q=plan.business_messages.find(q=>t>=q.start&&t<q.end);if(!q)return;
 const a=ease(p(t,q.start,q.start+.32))*(1-ease(p(t,q.end-.32,q.end))),ctx=ov;
 ctx.save();ctx.scale(scale,scale);ctx.globalAlpha=a;
 const shade=(y,h)=>{const z=ctx.createLinearGradient(0,y,0,y+h);z.addColorStop(0,'rgba(5,23,42,.0)');z.addColorStop(.45,'rgba(5,23,42,.94)');z.addColorStop(1,'rgba(5,23,42,.94)');ctx.fillStyle=z;ctx.fillRect(0,y,1920,h);};
 ctx.fillStyle='rgba(5,23,42,.9)';ctx.fillRect(0,0,1920,105);
 ol(ctx,[[96,108],[1824,108]],'rgba(190,171,117,.43)',1);
 ot(ctx,q.pain,960,74,36,'#e4c992','center',500);
 shade(987,93);ot(ctx,q.result,960,1044,34,'#edf2eb','center',400);
 ctx.restore();}
''')
(R/'brief.md').write_text('''# FirmBuddy V12 · 业务痛点与解决价值

- aspect_ratio: 16:9
- width: 1920
- height: 1080
- duration: 60
- fps: 30
- delivery_mode: ai_review_once
- review_budget: already_used；用户反馈修改，不新增独立角色。

本轮目标：讲清客户经营为什么难，以及FirmBuddy解决了哪些具体业务问题。无配音，纯音乐，中文业务文字随各段动作呈现。沿用已认可蓝图机械世界、连续摄影、五场景抽卡与专家半圆阶梯会场。

主线：资料分散与筛选慢→三源汇入客户线索；线索缺切入点→专业会商形成需求/时机/服务思路；专业支持难获取→知识检索与客户分型给出依据；准备工作重复→拜访/沟通/后续材料汇为跟进包；客户记录回流支持持续经营。每段同时交代问题、AI动作与业务结果。

所有站点共用8200×4800纸面，相机C2轨迹保留；载纸通过原路径跨站，不以字幕叠化冒充几何连续。源材料合流与准备材料合装为本轮新增实际动作。屏幕上下图纸旁注分开承载业务问题和业务结果，避免快速运镜中追字。九业务分类与六知识槽保留，减持为示例，入口为商机查询。人工审核保留，不宣称自动外发、参数微调或保证成交。

先用正式代码输出3/6/15.8/23.4/32.7/41.7/47.9/58秒效果图，再制作12.8–20.8秒相邻站点样段，检查资料合流和连续转场；随后60秒成片。复用60秒150BPM开场/主体配乐，新增合流接触与成果落定声音，由同一事件时间生成。
''',encoding='utf-8')
with (B/'CHECKPOINT.md').open('a',encoding='utf-8') as f:f.write('''\n\n## V12 · 2026-10-21 业务价值改版进行中
- objective: 将用户确认的业务痛点讲演稿制成一分钟视频，业务问题→对应解决→业务结果贯穿全片。
- aspect_ratio: 16:9; width:1920; height:1080; fps:30; delivery_mode:ai_review_once; review_budget:already_used。
- 已完成：读取V11绘图/相机/音频/检查源码及产品实施依据；独立v12目录，不修改产品工程；继承蓝图机械/专家会场/分类/纯音乐保护项。
- 新增：三源资料归集、需求/时机/服务切入会商、知识依据检索、准备材料合装、客户经营记录回流；上下旁注直接解释问题与结果。
- 下一步：效果图→合流与跨站正式样段→完整成片→工程检查与源码打包。
- verification: 尚未渲染，本条不代表画面验收。
''')
print('V12 prepared')
