"""One-time V17 -> V18 migration. Normal builds use setup.py."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent
def edit(name,old,new):
 p=R/name;s=p.read_text(encoding='utf-8');assert old in s,(name,old);p.write_text(s.replace(old,new),encoding='utf-8')

# Story/conductor split and render route were completed before this checkpoint.
# index.html is version-neutral. Continue from packaging and plan edits.
edit('package_source.py','v17-blueprint-sources','v18-business-story')
edit('package_source.py',"Path('v17')","Path('v18')")
edit('verify_delivery.py','v17-blueprint-sources','v18-business-story')
edit('verify_delivery.py','3720','4620')
edit('verify_delivery.py','124','154')
edit('verify_delivery.py','times=[2,6,12,16,20,25,29,31,34,36,38,43,50,60,68,74,77,82,90,95,101,111.4,115.8,122]','times=[2,8,15,21,26,31,35,40,44,49,56,66,74,80,88,96,101,107,117,122,128,134,141,151]')
edit('verify_delivery.py','[8,20.4,32,37.6,48.4,72.8,86.4,109.2,121.6]','[6,26.4,38,43.6,54.4,78.8,92.4,115.2,134.4,143.2,148.8]')

p=json.loads((R/'plan.json').read_text(encoding='utf-8'))
p.update(revision='V18 / One customer task becomes evidence-backed action',duration=154,base='v17',world=[9800,6500])
intro=[(0,6.4,'task','客户经理要找到这家企业的服务切入点','客户经理→A01任务档案→准备目的'),(6.4,12.8,'collect-pain','搜集耗时与切入不明','资料反复搜筛→联系谁何时谈→研判时间被占用'),(12.8,19.6,'expert-pain','背景不全与专业难找','资料缺口→跨领域专业意见→准备返工'),(19.6,24,'cost','业务代价与方案承诺','线索和行动之间的断开齿轮→完整流程承诺')]
shots=[dict(start=a,end=b,id=i,name=n,voiceover='',reads=r,action='A01持续留在同一蓝图工作台；主动作与文字错时建立') for a,b,i,n,r in intro]
for s in p['shots'][1:]:
 s['start']+=6;s['end']+=6;shots.append(s)
shots[-1]['end']=128
shots.extend([dict(start=128,end=134,id='unfold',name='从完整机器回到同一A01成果',voiceover='',reads='机器总图→下方成果图纸→单一档案展开',action='相机沿图纸向下滑行，A01展开为三联成果页'),dict(start=134,end=148,id='outcomes',name='用具体产物回应开头的业务问题',voiceover='',reads='为什么关注→与谁沟通→下一步做什么→传动闭合',action='三页依次标记落定；脱开的传动齿轮接合启动'),dict(start=148,end=154,id='promise',name='品牌价值与业务延展',voiceover='',reads='有依据的客户行动→可延伸业务场景',action='三页结果保留，品牌承诺在图纸底部落定')])
p['shots']=shots
texts=[
 ('先解决搜集问题：把同一家客户的资料放在一起','工具取数与规则筛选，AI 辅助解读、归纳来源'),
 ('资料归到 A01：主体、事件、时间与出处','输出：一份能回到原文的客户线索档案'),
 ('发现解禁窗口后，为什么值得继续关注？','结合公司与股东资料，研判股份管理服务背景'),
 ('把线索变成业务问题：联系谁，先了解什么？','AI 辅助整理关注理由、适用条件与沟通问题'),
 ('一个业务问题，需要哪些专业判断？','九大业务领域的专家，依托知识装备与培养试炼'),
 ('同一份 A01 档案，交给有分工的专家会商','股东增减持看服务需求，解禁预警看时机，拜访策略看切入'),
 ('再深入一步：这家企业在产业链的什么位置？','会商后的产业研究，继续围绕同一个客户展开'),
 ('把客户放回产业链，业务背景才更完整','AI 辅助检索年报、专利与产业资料，关联来源'),
 ('产业研究得到的依据，回到 A01 客户档案','让股份服务的沟通准备，也理解客户的产业背景'),
 ('专业意见为什么有依据？','从规则、案例与研究资料中检索，并保留引用'),
 ('研判之后，客户经理拿着什么去沟通？','AI 辅助整理联系目的、客户背景、沟通问题与后续安排'),
 ('准备包形成后，由业务人员审阅并安排跟进','AI 支持准备与整理，客户经理负责判断和沟通'),
 ('这次沟通的记录，成为下一次研判的起点','需求、服务安排与跟进事项，留在同一份客户档案')]
for q,(a,b) in zip(p['business_messages'],texts):q.update(start=q['start']+6,end=q['end']+6,pain=a,result=b)
# Texts are concise, with concrete outputs instead of claimed commercial gains.
score=p['soundtrack'];score['phrases']=[dict(start=round(a*.4,2),end=round(min(a+16,385)*.4,2),beats=min(16,385-a)) for a in range(0,385,16)]
events=[dict(at=e['at']+6,**{k:v for k,v in e.items() if k!='at'}) for e in score['events'] if e['at']>=18 and e['id']!='brand']
events += [dict(at=a,id=i,sound=s) for a,i,s in [(0.4,'client-task','accent'),(6.4,'collect-pain','tick'),(12.8,'professional-pain','tick'),(19.6,'stalled-workflow','accent'),(128,'outcome-camera','travel'),(132.4,'dossier-unfold','travel'),(134.4,'three-outputs','drop'),(135.6,'why','tick'),(138,'who','tick'),(140.8,'next','accent'),(143.2,'clutch-engaged','drop'),(148.8,'brand-promise','resolve')]]
score['events']=sorted(events,key=lambda e:e['at'])
score['density']=[dict(start=a,end=b,gain=g) for a,b,g in [(0,6.4,.48),(6.4,19.2,.58),(19.2,24,.4),(24,34,.8),(34,44,.98),(44,72,.68),(72,86,.55),(86,91,.9),(91,100,.56),(100,110,.78),(110,122,.68),(122,134.4,.9),(134.4,143.2,.62),(143.2,148.8,.88),(148.8,154,.28)]]
score['breaks']=[[37.6,38],[133.96,134.4],[142.8,143.2]]
p['connections']=[dict(time=t,kind='shared-world',anchor='A01 customer dossier; same blueprint rails',window=[t-.5,t+.5]) for t in [6.4,12.8,19.6,24,34,44,58,72,86,102,109,122,128,134,148]]
p['methodology']={'source':'AI创新大赛_叙事与演讲.pdf','pages_read':'1–10 text; 3–4 rendered','structure':['人和痛点','业务代价','单一主路径','具体成果对照','应用方向'],'no_pilot_metrics':True,'user_confirmed_no_metrics':True}
(R/'plan.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8')
base={f:hashlib.sha256((R.parent/'v17'/f).read_bytes()).hexdigest() for f in ['film.js','plan.json','audio/mix.wav']}
(R/'v17-preserved.json').write_text(json.dumps(base,indent=2),encoding='utf-8')
print('V18 prepared. Run setup.py for subsequent rebuilds.')
