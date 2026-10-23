"""Bind producer observations to the current encoded 76-second film."""
from pathlib import Path
from datetime import datetime
import json,hashlib,shutil
root=Path(__file__).resolve().parent
read=lambda p:json.loads((root/p).read_text(encoding='utf8'))
write=lambda p,v:(root/p).write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf8')
engineering=read('delivery/engineering-check-v11.json')
video=Path(engineering['video']);digest=hashlib.sha256(video.read_bytes()).hexdigest()
assert digest==engineering['sha256']
manifest=read('render/frozen-v11-manifest.json')
for key,path in manifest['files'].items():
 assert hashlib.sha256((root/path).read_bytes()).hexdigest()==manifest[key],('Changed frozen source',path)
evidence=read('qa/v11/producer-evidence-v11.json')
observations=read('qa/v11/producer-observations-v11.json')
assert evidence['video_sha256']==observations['video_sha256']==digest
assert observations['actual_viewed_encoded_frames']
evidence['actual_viewed_frames']=observations['actual_viewed_encoded_frames']
evidence['observations_file']='qa/v11/producer-observations-v11.json'
write('qa/v11/producer-evidence-v11.json',evidence)
cp=read('CHECKPOINT.json')
cp.update(status='v11_delivered_producer_verified',updated_at=datetime.now().isoformat(timespec='seconds'),final_candidate=str(video),final_candidate_sha256=digest,next_action='Show the 76-second user-feedback revision; follow further user feedback.',delivery_note='76秒竖屏修订版；工程检查及制作角色代表帧、街景连续样段检查已完成。独立审核预算未重置，当前版本未获全片独立视听通过；实际听音未完成。')
cp['verification'].update(render='v11全部1824帧；1080×1920、24fps、76秒，完整音视频解码通过，冻结源码哈希一致。',assets='v11城市模型：独立人畜路线、不同朝向与形制的雕像、庭院神庙、粮仓码头。清除穿过新神庙的旧城墙局部。',audio='用户原曲29.5–105.5秒连续节选；48kHz立体声，0.15秒渐入、73–76秒渐出；实际听音未完成。',producer_evidence='qa/v11/producer-evidence-v11.json 与 producer-observations-v11.json，绑定当前成片哈希。',independent_review='既有一轮预算已用；当前用户反馈修订仅有制作角色检查，非新增独立审核。')
cp['v11_revision'].update(final_candidate_sha256=digest,engineering_check='delivery/engineering-check-v11.json',producer_observations='qa/v11/producer-observations-v11.json',completed_exec_session=cp['v11_revision'].get('tracked_exec_session'),tracked_exec_session=None,active_launcher_pid=None)
cp['completed'].append('v11完成76秒整片、1824帧、连续街景样段和当前编码代表画面核对；修复列队人畜、神像及新增建筑场地冲突。')
cp['unresolved']=['Current revision has producer representative-frame and stated continuous-sample inspection only; no new independent full-film review.','Actual listening was unavailable; perceptual music synchronization is unverified.','Babylon-inspired fantasy city, not an archaeological reconstruction.']
write('CHECKPOINT.json',cp)
plan=read('plan.json');plan['status']='delivered';plan['evidence'].update(status='Current encoded film engineering checks and producer observations complete; see explicit coverage.',video=str(video),sha256=digest,producer_observations='qa/v11/producer-observations-v11.json');write('plan.json',plan)
timeline=read('v11-timeline.json')
rows='\n'.join(f"| {e['start']:g}–{e['end']:g} 秒 | {e['name']} |" for e in timeline['events'])
text=f'''# 暮河城 · 巴比伦巨城 v11

当前成片：76秒，1080×1920竖屏，24fps。由同一座三维城市的连续路网连接街景、河运、庭院与贸易场所。历史成片及计划保留在 history/v10。

## 本次用户反馈修复

- 269个人畜主体采用独立缓存路线、停留与局部避让；交谈、工作、驮畜和山羊各有分布及步态，不使用同速列队。
- 主神像朝向南入口，侧供像转向庭院；区分材质、冠饰及轮廓，增加守护狮、供桌、器物及铭文石碑。
- 新增西侧庭院神庙、相连横街、东岸粮仓与工作码头；切除穿过新神庙的旧城墙局部，并保留庭院外墙体。
- 保留蓝釉与泥砖、暖侧光、窄清晰带、高位俯拍、8Hz世界活动与逐帧平滑相机。

## 镜头时间表

| 时间 | 场景 |
| --- | --- |
{rows}

## 音乐

使用用户提供的《Dream of Babylon》29.5–105.5秒连续节选；0.15秒渐入、最后3秒渐出。环境声低混并以2秒交叉淡化衔接。镜头沿既有音乐能量候选编排；实际听音不可用，未声称主观音画同步通过。

## 可编辑工程与验证

模型：model/babylon-city-v11.blend。建模修订入口 model/revise_city_v11.py → model/finalize_sites_v11.py。摄影与移轴后期入口 render_city_v11.py；固定交通缓存 traffic-v11.npz；镜头时间轴 v11-timeline.json；混音 mix_music_v11.py；完整渲染 run_full_v11.py。

当前视频 SHA256：{digest}。全部1824帧及完整音轨解码检查通过；制作角色实际观看范围见 qa/v11/producer-observations-v11.json。用户选定的既有独立审核一轮预算未重置，本修订没有新的全片独立审核结论。

这是巴比伦风格的幻想城市，不作为考古复原。
'''
(root/'视频制作计划.md').write_text(text,encoding='utf8')
source=read('source-adoption.json');source['current_revision']='v11';source['current_renderer']='render_city_v11.py';write('source-adoption.json',source)
summary={'video':str(video),'sha256':digest,'engineering':engineering,'producer_observations':'qa/v11/producer-observations-v11.json','delivery_mode':cp['delivery_mode'],'new_independent_review':False,'actual_listening':False}
write('delivery/delivery-summary-v11.json',summary)
poster=root/'qa/v11/encoded-frames/01752.png'
if poster.exists():shutil.copy2(poster,root/'delivery/preview-v11.png')
print('V11_DELIVERY_FINALIZED',str(video),digest)
