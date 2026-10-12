import hashlib,json,shutil,re
from pathlib import Path

work=Path(__file__).resolve().parent
project=work.parent.parent
studio=work/'studio'
installed=Path('D:/Codex/skills/vibe-video')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,data):p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
clips=['blueprint-proof','dataviz-proof','one-way','dataviz-variant']
records=[]
for clip in clips:
    out=studio/'out-approved'/clip
    media=json.loads((out/'media-check/media-evidence.json').read_text(encoding='utf-8'))
    render=json.loads((out/'render-evidence.json').read_text(encoding='utf-8'))
    assert media['full_decode']=='passed' and render['seek']['identical']
    schedule=json.loads((out/'review/schedule.json').read_text(encoding='utf-8'))
    findings=(['剖切揭示内部，拆解标注完整；复位后阀瓣贴合阀座；开放状态弹簧缩短，闭合后无穿流箭头。'] if 'dataviz' not in clip else ['折线连接输入点，柱形落至零基线；数值标签保留，最大值跟随输入更新。'])
    if clip=='one-way':findings+=['六镜头的建立/动作/结果概览已查看；31.5 秒解码大图中闭合结果和结尾标章完整。']
    if clip=='dataviz-variant':findings+=['4.7 秒解码大图中最大值为第一个点 94；标注无裁切，纵轴随输入改为 100。']
    review={'clip':clip,'video_sha256':sha(out/f'{clip}.mp4'),'reviewer':'primary agent','sampled_action_sheets':[{'path':str(p.relative_to(out)),'sha256':sha(p)} for p in sorted((out/'review').glob('actions-*.jpg'))],'sampled_action_frames':schedule['action_frames'],'sample_step_seconds':.2,'findings':findings,'scope':'Action samples observed as contact sheets; not every frame or real-time playback.','realtime_playback':False,'listened':False}
    save(out/'review/observations.json',review)
    records.append({'clip':clip,'video':str((out/f'{clip}.mp4').relative_to(project)),'sha256':review['video_sha256'],'rendered':True,'media_decode_pass':True,'sampled_sequence_observed':True,'sampled_frames':schedule['action_frames'],'seek_same_page_forward_reverse_and_fresh_page':True,'seek_fresh_browser_process':False,'realtime_playback':False,'listened':False,'review':str((out/'review/observations.json').relative_to(project)),'source':render['source']})
cap={'schema_version':1,'skill_version':'0.7.0','evidence_project':str(project),'outputs':records,'validated_capabilities':{'blueprint':['section sweep','housing separation and reassembly','disc/spring/gap linkage','world-space notes'],'dataviz':['eight-point draw and trace','input-derived maximum','line-to-zero-baseline bars','alternate values/scale/maximum position rebuild']},'limitations':['Simplified axial valve schematic; no engineering dimensions or fluid simulation.','Fictitious labeled data, no statistical inference.','No realtime playback or listening performed.','No fresh-browser-process seek test.','No original lemo-opuscar film viewed or reproduced.']}
save(studio/'capabilities.json',cap)
save(work/'delivery-evidence.json',cap)
target=installed/'assets/style-studio'
target.mkdir(parents=True,exist_ok=True)
for p in studio.iterdir():
    if p.is_file():shutil.copy2(p,target/p.name)
shutil.copytree(studio/'clips',target/'clips',dirs_exist_ok=True)
snapshot=project/'skill/vibe-video'
shutil.copytree(installed,snapshot,dirs_exist_ok=True)
files=[]
for p in sorted(installed.rglob('*')):
    if p.is_file():
        rel=p.relative_to(installed);other=snapshot/rel
        assert other.is_file() and sha(p)==sha(other),str(rel)
        files.append({'path':str(rel),'sha256':sha(p)})
save(work/'skill-update-manifest.json',{'version':'0.7.0','installed':str(installed),'snapshot':str(snapshot),'files':files,'copy_verified':True})
for name in ['README.md','PRODUCTION.md','CHECKPOINT.md']:
    p=project/name;p.write_text(p.read_text(encoding='utf-8').replace('out-release','out-approved'),encoding='utf-8')
p=project/'PRODUCTION.md'
p.write_text(p.read_text(encoding='utf-8').replace('早期 `out`','`out-release` 是标注纵向裁切修正前的版本；早期 `out`'),encoding='utf-8')
(work/'CHECKPOINT.md').write_text('''# 风格与视听制作体系 — 2026-10-09

目标：按用户授权，将 lemo-opuscar 风格规范、共享视听时间轴与证据分级用于 VibeVideo，保留旧工程。

已完成：技能 0.7.0；蓝图/数据 STYLE 与 DEMO；原创 studio 渲染、拟音、字幕、时间轴与审查工具；安装 assets/style-studio 并同步项目 skill/vibe-video，逐文件哈希见 skill-update-manifest.json。

交付：studio/out-approved 下两个 10 秒能力片段、32 秒《只向一个方向》和 10 秒数据变体。已修正标签碰撞、接触音偏移和拆解标签纵向裁切。之前输出仅作迭代记录。

验证：四片完整解码、1280×720/24fps/时长/音轨、镜头契约和事件检查通过；同页顺逆序及新页面 PNG 相同。已查看全部事件 0.2 秒抽帧表（55/45/77/45 帧），另查看蓝图拆解、主片结尾和变体最大值解码大图。抽帧不是全帧或实时播放；未听音、未测试新浏览器进程。证据见 delivery-evidence.json 和各片 review/observations.json。

来源：官方文档固定 commit 4d7014aa7ba7d22c00513052dd996a4f200d5102；未观看或复刻原片。工程、故事和拟音原创。蓝图为简化原理示意，数据为演示值。

本轮修改已完成。此前 52 秒《蓝色的建筑》仍按根 CHECKPOINT.md 单独记录，未宣称完成；已取消榫卯工作不恢复。
''',encoding='utf-8')
print(json.dumps({'videos':len(records),'skill_files_verified':len(files),'toolkit':str(target)},ensure_ascii=False))
