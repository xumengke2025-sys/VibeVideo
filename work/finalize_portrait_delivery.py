"""Save the agent's actual observed findings and tie them to final media hashes."""
from pathlib import Path
import hashlib,json
root=Path(__file__).parent
notes={
 'hot-news-20261009':[
  ['极光、冰面地平线和标题建立南极实景，照片署名可见。','摄影裁切缓慢推进，极光主体保留。','开场历史影像标签与诺贝尔标题留在安全区域。'],
  ['溶入后只保留冰下模块与缆线，文字与球体分离。','模块轻转，反光与向下光电倍增管保持一致。','阵列开始显现，模块与缆线位置保持，准备拉远。'],
  ['模块缩小、阵列覆盖画面，5,160标签保持可读。','光迹生长，蓝色光锥出现，传感器白光响应。','阵列展开成整体，光锥淡出，光迹仍在中心。'],
  ['背景阵列保持，文字切换为获奖者与公告日期。','相机停在全景，淡蓝余光留出阅读空间。','获奖姓名、日期及示意说明持续可见，结尾留白。']
 ],
 'portrait-valve-20261009':[
  ['中心线与主体轮廓开始绘制，无横版裁切。','轮廓沿路径生长，上下入口与纵向构图清晰。','完整外壳建立，上进下出方向明确。'],
  ['剖切开始前完整外壳保持。','剖切扫到内部，阀座阀瓣首先出现。','剖切完成，阀座、阀瓣、弹簧标注可读。'],
  ['拆分开始时内部与壳体在原位。','左右壳壁分开，内部中心线和接触关系保持。','壳壁回到通道边缘，与开启状态衔接。'],
  ['阀瓣贴合阀座，开启前无通过流箭头。','阀瓣下移，弹簧长度变短，间隙与流箭头出现。','开启间隙稳定，流箭头绕过阀瓣流向下游。'],
  ['开启状态延续，准备回座。','阀瓣上移、弹簧伸长，流箭头按开启量淡出。','已完全回座，通道内无通过流箭头。'],
  ['回座状态保持，读结论前主体没有变化。','整体轻微拉回，关闭章出现，标注保持位置。','关闭状态与结论文字稳定，章和底部文字不碰撞。']
 ]}
names={'hot-news-20261009':'icecube-news-portrait','portrait-valve-20261009':'one-way-portrait'}
delivery=[]
for project,shotnotes in notes.items():
    base=root/project;out=base/'out-final';video=out/(names[project]+'.mp4');planpath=base/('production-plan.json' if project.startswith('hot') else 'clips/one-way-portrait.json');plan=json.loads(planpath.read_text(encoding='utf-8'));qa=json.loads((out/'qa/media-evidence.json').read_text(encoding='utf-8'));digest=hashlib.sha256(video.read_bytes()).hexdigest();observations=[]
    for i,shot in enumerate(plan['shots']):
        for j,state in enumerate(['establish','action','result']):
            k=i*3+j;t=shot['states'][state];evidence=Path(qa['keyframes'][k]).relative_to(out).as_posix();assert (out/evidence).is_file()
            observations.append({'shot':shot['id'],'state':state,'time':t,'evidence':evidence,'note':shotnotes[i][j]})
    selected=json.loads((out/'motion-audit/selected-schedule.json').read_text(encoding='utf-8'))
    sequence_notes=({'dissolve':'2.3–3.1秒照片到球体为叠化，未冒充连续几何变形。','pullback':'5.4–6.6秒球体渐缩，缆线与相机位置连续，阵列展开。','light-propagation':'6.7–8.4秒光迹生长、蓝色光锥扩展与传感器响应递进；降低泛光后轮廓可见。','award-handoff':'10.9–11.5秒阵列不跳动，仅奖项文字切换；结尾余光较暗为收束。'} if project.startswith('hot') else {'section':'1.29–2.75秒剖切向下扫过，内部保持固定中心线。','explode-assemble':'3.63–5.92秒左右壳体分开并回位，阀座阀瓣端点保持。','open':'6.08–7.33秒阀瓣向下，弹簧变短，流箭头随开启量出现。','reseat':'9.96–11.42秒阀瓣上移，11秒时贴合阀座，后续帧无通过流箭头。','settle':'12.21–13.71秒关闭机构保持，整体缩小少量；结尾章在概览帧中确认。'})
    seq=[{**s,'evidence':'motion-audit/'+s['sheet'],'note':sequence_notes[s['window']]} for s in selected]
    review={'video_sha256':digest,'reviewer':'primary agent','method':'Observed decoded final-video keyframe contact sheets and selected cropped motion-sequence sheets; representative full-size design stills also observed.','observations':observations,'sequences':seq,'observed_representative_frames':len(observations),'observed_selected_sequence_frames':sum(len(s['frames']) for s in selected),'extracted_frames_are_not_all_observed':True,'realtime_playback':False,'listened':False,'seek_check':'Same browser page: repeated times identical PNG hashes; fresh browser process not tested.','technical_pass':not qa['technical_failures'],'issues_requiring_fix':[],'limitations':['动画为艺术化或机制示意，不是物理精确模拟。','音轨全长采样、无削波检查和事件时刻核对；未实际听音。','序列按所列帧采样观察，不宣称逐帧或实时播放验收。']}
    (out/'visual-review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2),encoding='utf-8')
    auditpath=out/'motion-audit/frame-audit.json';audit=json.loads(auditpath.read_text(encoding='utf-8'));audit['visual_review']={'status':'selected frames observed','reviewed_frames':[f for s in selected for f in s['frames']],'method':review['method'],'issues':[],'review_record':'../visual-review.json'};auditpath.write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
    item={'project':project,'video':str(video),'sha256':digest,'width':qa['width'],'height':qa['height'],'duration':qa['duration'],'fps':qa['fps'],'audio_streams':qa['audio_streams'],'audio_levels':qa['audio_levels'],'full_decode':qa['full_decode'],'representative_frames_observed':len(observations),'motion_sample_frames_observed':review['observed_selected_sequence_frames'],'realtime_playback':False,'listened':False};delivery.append(item)
(root/'portrait-delivery-20261009.json').write_text(json.dumps(delivery,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(delivery,ensure_ascii=False,indent=2))
