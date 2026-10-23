from pathlib import Path
import json,re
R=Path(__file__).resolve().parent
s=(R.parent/'v17/check_layout.mjs').read_text(encoding='utf-8')
old=json.loads(re.search(r'const windows=(\[.*?\]);const plan=',s).group(1))
w=[dict(range=[a+6 for a in x['range']],texts=x['texts']) for x in old[2:-1]]
w[:0]=[
 dict(range=[2,5],texts=['客户经理，怎样找到这家企业的服务切入点？','客户经理','示例客户信息','半导体衬底企业','任务：找到服务切入点']),
 dict(range=[7,11.8],texts=['同一次客户准备，卡在这些地方','收集耗时：每天重复搜、筛、抄','切入不明：有信号，怎么跟？','公告与名单分散，同一事件反复出现','整理占去时间，研判还没有开始','解禁与股东动态，需要结合业务背景','联系谁、何时谈、先谈什么？','A01 · 示例客户信息','代价：搜集挤占研判时间，线索难排出轻重缓急']),
 dict(range=[14,18.8],texts=['背景不全：客户资料拼不齐','专业难找：一个问题跨多领域','企业、股东、行业信息难串成一条线','缺少完整背景，沟通难以深入','行业、合规、客户经营需要共同研判','专业意见分散，服务思路难成形','代价：准备反复返工，客户跟进缺少明确方向']),
 dict(range=[20.4,23.4],texts=['一条线索，卡在行动之前','客户经理需要的，是从信息到服务动作的完整路径','线索','研判','行动','把资料归集、专业研判与客户跟进接起来','FirmBuddy · 让 AI 辅助这条业务流程'])]
w += [dict(range=[135,146],texts=['这次准备，最终得到什么？','为什么关注','与谁沟通','下一步做什么','公司解禁窗口','结合股东与企业资料','形成股东服务研判','了解股份事务接口','结合产业研究背景','准备有针对性的问题','人工审阅沟通提纲','安排联系与后续跟进','记录回流客户档案','分散线索 → 关注依据','零散疑问 → 沟通重点','临时准备 → 行动安排','专业数据 × 知识装备 × 业务流程']),dict(range=[149,153.5],texts=['为什么关注','与谁沟通','下一步做什么','FirmBuddy','把分散线索，变成有依据的客户行动','同一流程，延伸至融资、并购、回购等业务场景'])]
s=re.sub(r'const windows=\[.*?\];const plan=', 'const windows='+json.dumps(w,ensure_ascii=False)+';const plan=',s).replace('/v17/','/v18/')
(R/'check_layout.mjs').write_text(s,encoding='utf-8')
(R/'read-windows.json').write_text(json.dumps(w,ensure_ascii=False,indent=2),encoding='utf-8')
