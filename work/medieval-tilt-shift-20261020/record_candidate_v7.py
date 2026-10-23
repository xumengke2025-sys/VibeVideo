from pathlib import Path
import json,datetime,shutil
R=Path(__file__).resolve().parent
report=json.loads((R/'delivery/engineering-check-v7.json').read_text(encoding='utf8'))
history=R/'history/v6-original-score';history.mkdir(parents=True,exist_ok=True)
for name in ['plan.json','CHECKPOINT.json','视频制作计划.md']:
    if not (history/name).exists():shutil.copy2(R/name,history/name)
p=R/'CHECKPOINT.json';c=json.loads(p.read_text(encoding='utf8'))
c.update(version='v7',status='candidate_complete_independent_visual_review_in_progress',updated_at=datetime.datetime.now().isoformat(timespec='seconds'),final_candidate=report['video'],final_candidate_sha256=report['sha256'])
c['completed'] += ['1344帧完整1080×1920 Cycles渲染完成，56秒24fps；v6原配乐影片保留','用户提供Alexander / Dream Of Babylon本地音频，v7已替换原配乐，画面流直接复制','v7技术检查通过：实际解码1344帧、完整音视频无解码错误、48kHz立体声','全帧审核证据已导出45页；启动唯一独立审片角色babylon_av_review']
c['verification']['render']='全部1344帧已输出并编码；当前v7成片完整解码通过。v6编码后的检查曾遇GBK文本解码与精简ffmpeg null默认编码器缺失，已改UTF-8与显式rawvideo/pcm_s16le。成片本身无解码错误。'
c['verification']['audio']='已使用用户提供Dream Of Babylon原曲0–56秒，1.2秒渐入、52–56秒渐出，环境声低混入。最终混音测得约-17.63LUFS、-1.52dBTP；实际听音未完成。'
c['review_budget']={'reviewer_started':True,'reviewer':'/root/babylon_av_review','repair_rounds_used':0,'max_repair_rounds':1}
c['unresolved']=['独立画面审核进行中','工具无法让模型实际感知音频，听音未完成，不宣称完整视听通过']
c['next_action']='接收同一审片者的实际全帧报告；必要时最多修复一次并局部复核，然后展示当前可播放成片，说明听音限制。'
p.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
p=R/'plan.json';j=json.loads(p.read_text(encoding='utf8'));j['version']='v7';j['status']='candidate_complete_review_in_progress'
j['audio'].update(music='Vangelis — Dream Of Babylon，Alexander电影原声；用户提供本地MP3',source_status='已复制用户文件并混入v7；未实际听音',source_excerpt_seconds=[0,56],fade_in_seconds=1.2,fade_out_seconds=[52,56],master_clock='已渲染56秒画面；原曲连续节选配合画面',planned_bpm=None,planned_bars=None,motif='使用原曲，不新增或重写旋律；连续节选，不作歌曲内部跳切。')
j['audio']['palette']=['用户提供的电影原声成品'];j['audio']['optional_palette']=[]
j['audio']['cues']=[{'start':0,'end':1.2,'music':'原曲从头渐入'},{'start':1.2,'end':52,'music':'原曲连续节选；风水环境低混入'},{'start':52,'end':56,'music':'随全城收束渐弱至结束'}]
j['audio']['notes']='原90BPM原创方案保留在history及audio/music.wav；v7不宣称该电影配乐是90BPM，也不宣称实际听感已审核。'
j['evidence']['engineering_report']='delivery/engineering-check-v7.json';j['evidence']['frame_audit']='qa/v7/frames/frame-audit.json'
p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
p=R/'视频制作计划.md';s=p.read_text(encoding='utf8')
s+='\n## 用户最终选曲（v7）\n\n用户提供本地《Alexander》原声第16轨 Vangelis《Dream Of Babylon》（标签及本地文件已核对，全曲约160.84秒）。成片采用原曲0–56秒连续节选；0–1.2秒渐入，52–56秒渐出，低混入已有风、水等环境声。保留原配乐版及原始分轨。v7音画已合成，实际解码1344帧通过，未进行时间伸缩或歌曲内部跳切。原先90BPM、21小节及原创配器计划仅描述v6历史方案，不用于描述电影原曲。模型无法实际听音，不把响度测量写成听感通过。\n'
p.write_text(s,encoding='utf8')
print('v7 candidate and user music recorded')
