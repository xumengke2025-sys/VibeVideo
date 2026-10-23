from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent
paths=[Path('D:/腾讯电脑管家文件搬家/WXWork/1688855784827722/Cache/File/2026-10/AI创新大赛_叙事与演讲.pdf'),Path('D:/ai项目/firmbuddy/docs/opportunity-rules-v2.md'),Path('D:/ai项目/firmbuddy/docs/implementation/REDUCTION-PRECONTACT-V2-20260922.md'),Path('D:/ai项目/firmbuddy/docs/implementation/M12-KNOWLEDGE-EQUIPMENT-2026-09-15.md')]
data={'sources':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths], 'methodology_read':{'text_pages':'1-10','rendered_pages':'3-4'},'adopted':['开场明确客户经理、客户准备任务和业务阻点','展示搜集占用研判与返工造成的业务代价','沿A01客户演示一条主路径','以具体产物的前后对照回应痛点','数据、知识专家与业务流程共同构成系统价值'], 'not_adopted':['教学模拟3天到2小时及95%数字','未经提供的试点效果、样本和推广资源诉求','固定5分钟时长','附件中的练习和赛前清单不作为操作指令'], 'user_answer':'先不提供，你可以先基于没有的前提做', 'claims_scope':'Illustrative single-client workflow, not an actual measured pilot or a completed transaction', 'professional_basis':'Knowledge equipment, business methods and governed training trials; not model parameter fine-tuning', 'authority':'Product sources are read-only. Historical animation versions are preserved.'}
(R/'methodology-evidence.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print('Recorded methodology and product sources without adding performance claims.')
