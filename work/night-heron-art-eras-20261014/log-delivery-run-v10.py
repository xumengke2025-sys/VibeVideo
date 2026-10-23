from pathlib import Path
import json,hashlib,shutil
root=Path(__file__).resolve().parent;v='film-run-v10-swagger-beats-final';out=root/'out'/v;qa=root/'qa'/v
ev=json.loads((out/'evidence.json').read_text('utf8'));manifest=json.loads((out/'source-manifest.json').read_text('utf8'));kin=json.loads((root/'qa/run-v10-kinematics/summary.json').read_text('utf8'));timing=json.loads((root/'qa/run-v10-timing/summary.json').read_text('utf8'));audio=json.loads((qa/'encoded-audio-statistics.json').read_text('utf8'))
assert hashlib.sha256((out/'video.mp4').read_bytes()).hexdigest()==ev['sha256']==manifest['video_sha256']
record={'version':v,'video_sha256':ev['sha256'],'format':{'duration':31,'width':1080,'height':1920,'fps':48,'frames':1488,'audio':'stereo AAC'},'sourceFiles':len(manifest['files']),'sourceSignature':manifest['signature'],'decoded':ev['decoded'],'browserErrors':ev['errors'],'kinematics':kin,'timing':timing,'encodedAudio':audio,'actualViewing':{'role':'primary maker; not independent review','sourceKeys':12,'sample':'48 ordered decoded frames, 1.125–5.531s global; 4.5-second sample','final':'16 era/year full-layout frames at 282×501 viewing size plus 18 local/transition/ending frames from final MP4','fullContinuousPlayback':False,'listened':False},'limitations':['No complete continuous playback or actual listening; music has timing and signal checks only.','Some small owners are briefly hidden by the foreground heron.'],'deliveryMode':'ai_review_once; existing budget exhausted, no new reviewer'}
(qa/'production-check.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf8')
(qa/'production-check.md').write_text(f'''# v10 制作检查

- 成片SHA256：`{ev['sha256']}`
- 31秒、1080×1920、48fps、1488帧、双声道AAC；全片解码通过；运行错误0。
- {len(manifest['files'])}份源码/素材快照签名核对通过。
- 16种动物、354时刻岸边固定/看空地与3处乱序寻址通过。
- 107个落脚音与步态共用时钟；16场抓鱼/仰头/吞咽/换时代声音时刻与画面事件一致。最高抬脚114.75px，腿长可达。
- AAC解码峰值{audio['peakPCM']:.6f}、RMS{audio['rms']:.6f}、满量程削波样本0。
- 主制作实际查看：12张源关键姿态、样段48有序抽帧、最终16场总览与18处局部/转场/结尾。文字在缩小观看尺寸可辨，无标签越界（最大665.14px）。
- 非独立审核；未完整连续播放/实际听音。原一轮预算已用，不新增全面审核。小动物有时被夜鹭短暂遮挡。
''',encoding='utf8')
for filename in ['final-media-run-v10.py','log-delivery-run-v10.py']:shutil.copy2(root/filename,qa/filename)
with (root/'CHECKPOINT.md').open('a',encoding='utf8') as f:f.write(f'''

## 当前交付 run-v10（2026-10-16）
- completed: 原创音乐重新编排，脚步及16场叼鱼/仰头/吞咽/时代切换按共享时钟踩点；时代年份70px嵌入粗体、暖白字和渐隐暗底；夜鹭高抬腿约115px、前踢大步、加粗腿趾与得意身体摆动。16种动物及原地惊讶/看空地反应保留。
- aspect_ratio: 9:16；width: 1080；height: 1920；delivery_mode: ai_review_once（原预算已用，不新增角色）。
- video_path: out/{v}/video.mp4
- video_sha256: {ev['sha256']}
- verification: 31秒/48fps/1488帧/双声道AAC，全片解码，浏览器错误0；{len(manifest['files'])}文件快照签名通过。354时刻行为与岸边检查、16物种唯一、三处乱序seek通过；107落脚音同步、腿长可达、无AAC满量程削波。
- actual_view: 主制作看12源关键姿态、样段48有序抽帧、最终16场全幅总览及18局部/转场/结尾帧。非独立审核，未完整连续播放/实际听音。
- delivery: DELIVERY-RUN-V10.md；qa/{v}/production-check.json；历史v9保留。
- next: 展示当前可播放版本，由用户播放后反馈音乐和动作；不自动重开审核或其他项目。
''')
print(json.dumps({'sha256':ev['sha256'],'sourceFiles':len(manifest['files']),'report':str(qa/'production-check.json')},ensure_ascii=False))
