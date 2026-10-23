from pathlib import Path
import json
R=Path(__file__).resolve().parent
p=R/'brief.json';b=json.loads(p.read_text(encoding='utf8'))
b['action']['baby']='双手抱住低位奶瓶→抬至胸前→奶嘴接嘴并倾瓶喝奶→降低到腿上→回到低位'
b['action']['identity_persistence']=[x if x!='star_toy' else 'milk_bottle' for x in b['action']['identity_persistence']]
b['action']['contact_constraints']=['妈妈杯子与握持点持续连接','宝宝只有两只手，两臂连接对应肩膀','奶瓶被双手抱持，喝奶时奶嘴接嘴','跨时代保持共享绝对动作相位']
b['action']['generated_assets']='assets/bottle-v3/：35时代×4姿态；多手问题逐格制作检查，原捡星星素材仅作历史来源'
b['review'].update({'reviewers_used':1,'reviewer_id':'/root/av_review','repair_passes_used':0,'status':'等待奶瓶新版成片；旧v1覆盖不可继承v2'})
b['duration_status']='41.25秒，990帧，24fps，1080×1920'
b['next']='完成宝宝双手奶瓶素材的逐格制作检查，导出v2整片，再由同一审片者接续一轮审核。'
p.write_text(json.dumps(b,ensure_ascii=False,indent=2),encoding='utf8')
p=R/'CHECKPOINT.md';s=p.read_text(encoding='utf8')
s+='\n- current_assets: 35/35时代环境与妈妈动作包齐全；宝宝改为奶瓶动作，7套五时代批次已生成，4个残留多手时代（07、08、09、14）正在单独重画。\n- latest_user_correction: 用户两次指出三只手。已实际确认问题，未宣称解决；必须逐格检查后才启用新素材。旧撑地手不能与新增双手抱瓶同时保留。\n- current_action_override: 宝宝抱起奶瓶喝奶，取代捡星星；妈妈举咖啡杯不变。\n'
p.write_text(s,encoding='utf8')
print('Updated brief and checkpoint for bottle action')
