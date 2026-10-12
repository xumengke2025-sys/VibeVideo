"""Extend existing cards with operating metadata; keep source/provenance untouched."""
import json
from pathlib import Path
root=Path('D:/Codex/skills/vibe-video');p=root/'references/opus-methods.json';d=json.loads(p.read_text(encoding='utf-8'))
rows={
'ui-identity':('Canvas/SVG/WebGL，continuity.mjs','UI/产品/抽象','time + sorted target events → property state','frequency,damping,initial velocity','配合data-state共享值；文字按退入错时','事件叠加O(events)，预计算长表','严格测量/非弹性机械接触','node --test assets/test-motion.mjs'),
'outline-morph':('JS，continuity.mjs morphPoints','抽象/产品/文字','same-topology point arrays + progress → corresponding contour','point count,progress,winding','先建立对应，再配semantic-finale；不支持任意字体自动拓扑','O(points)，路径重采样由调用方负责','孔洞数量/拓扑不同而无设计的映射','node --test assets/test-motion.mjs'),
'portal-scale':('JS，continuity.mjs logZoom','3D/抽象/解释','positive start/end scale + progress → logarithmic zoom','start,end,progress','与reveal-path/持续世界锚点组合','本工具O(1)，极大缩放依赖贴图分级','没有可进入局部的语义关系','node --test assets/test-motion.mjs'),
'data-state':('Canvas，style-studio/film.mjs + timeline.mjs','数据/科学','clip event JSON + t → graph/value/caption','data values,units,event times,readingRate','标签、形状共享状态；用world-anchor-callout定位','Canvas全帧，密集数据需抽稀','单位/轴尺度不稳定或伪造数据','node assets/style-studio/test-contract.mjs'),
'mechanical-section':('Canvas，style-studio/film.mjs','机械/科学','part IDs + section/explode progress → readable internal contact','section time,part offsets,stroke','先保留零件身份，配hold-cause；新机械行程用load-regulated-valve','线绘较轻；当前是剖面示意，无CAD求解','复杂三维公差/接触仿真','node assets/style-studio/test-contract.mjs'),
'reveal-path':('Three.js，cinematic-starter/camera-kit.mjs','3D/产品/科学','absolute t + position/target tracks → pose','position,target,FOV,shot boundaries','与subject-intent先跟随再揭示；查遮挡走廊','路径采样轻，GPU取决场景','无目的持续绕行或相机穿墙','node assets/cinematic-starter/render.mjs --project=assets/cinematic-starter --out=out-camera-check --stills-only'),
'hold-cause':('Canvas/Three，已有绝对时间相机','机械/科学/数据','contact window + fixed pose → readable action','hold start/end,framing,action duration','在受力/接触处停机，再reveal-path','无新增计算，需保护阅读停留','主体会离开画面且不能改变构图','node assets/style-studio/test-contract.mjs'),
'event-story':('JS事件表 + style-studio/timeline.mjs','角色/机械/产品/3D','trigger time + delay + receiver state → causal response','at,duration,delay,receiver ID','先主动作后环境反馈；音轨共享事件，不强制每次有音','直接求值；反馈多时分层控制密度','只为让背景热闹且不改变含义','node assets/style-studio/test-contract.mjs'),
'blueprint-part-states':('Canvas，style-studio/film.mjs','机械/科学','part identity + stage progress → draw/section/assemble','seed,part anchor,stage timing','与load-regulated-valve共享阀瓣/弹簧行程','原生线绘，无工程求解','拿拆解顺序当真实阀工作动作','node assets/style-studio/test-contract.mjs'),
}
for c in d['cards']:
    if c['id'] not in rows:continue
    stack,types,io,params,combo,cost,avoid,verify=rows[c['id']]
    c['operating']={'stack':stack,'video_types':types.split('/'),'input_output':io,'parameters':params,'combine':combo,'performance':cost,'avoid':avoid,'minimum_verification':verify,'scope':'运行验证只证明机制，画面须按本片实际输出审阅。'}
for ident,title,terms,purpose,implementation,avoid,params in [
('subject-intent','主体判断、减速和预备转向',['飞行器','车辆','意图','判断','跟拍','转向'],'环境约束改变主体行为，主体请求引发反馈。','mechanical.mjs pathAt显式位置/速度节点；subject-camera.mjs伴随。路径先减速/等待，再通行；姿态可提前指向新路径。','严格匀速或既定机械运动','knots t/p/v,bank anticipation,camera lag'),
('load-regulated-valve','预载、压差与受限机械行程',['阀','弹簧','受力','约束','止回','机械'],'阀瓣位移、弹簧压缩、流动许可由同一状态控制。','mechanical.mjs valveState: clamp((pressure*area-preload)/stiffness,0,stroke)，固定端由restLength保持；是准静态示意。','动态撞击/流体仿真、无阻尼惯性求解','pressure,area,preload,stiffness,stroke,restLength,seat')]:
    c={'id':ident,'title':title,'terms':terms,'purpose':purpose,'relation':'输入/行为→受限响应→结果；共享绝对时间状态。','decisions':'先保证主动作可读和约束正确，再加入相机/次级动作。','implementation':implementation,'failure':'输入先后错、穿透约束、跟拍遮住接触；均匀插值掩盖判断。','review':'看输入、动作极值、接触和最终结果的连续窗；比较背景与主体。','source_refs':[{'source':'codex-tools','path':'mechanical.mjs','line':3 if ident=='load-regulated-valve' else 14}],'gallery_slugs':[],'status':'independent_regression_pending','status_note':'本轮两例运行与审片完成后更新，不能凭函数名视为验证。','operating':{'stack':'无依赖JavaScript；Canvas/Three接入','video_types':['机械','科学'] if ident=='load-regulated-valve' else ['3D','角色','产品'],'input_output':'带单位输入/绝对t → 状态或位置数组','parameters':params,'combine':'hold-cause + event-story + reveal-path；不固定故事/风格','performance':'valve O(1)，path O(knots)，无模拟历史','avoid':avoid,'minimum_verification':'node --test assets/test-motion.mjs','scope':'局部准静态状态/轨迹；成片须实际审阅'}}
    d['cards'].append(c)
d['schema_version']=str(d['schema_version']) # preserve upstream structures
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Extended 9 existing cards, added 2 original mechanisms')
