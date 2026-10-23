from pathlib import Path
import json,hashlib,shutil
root=Path(__file__).resolve().parent;v='film-run-v11-fast-strut-final-02';out=root/'out'/v;qa=root/'qa'/v
ev=json.loads((out/'evidence.json').read_text('utf8'));manifest=json.loads((out/'source-manifest.json').read_text('utf8'));kin=json.loads((root/'qa/run-v11-kinematics/summary.json').read_text('utf8'));timing=json.loads((root/'qa/run-v11-timing/summary.json').read_text('utf8'));audio=json.loads((qa/'encoded-audio-statistics.json').read_text('utf8'))
assert hashlib.sha256((out/'video.mp4').read_bytes()).hexdigest()==ev['sha256']==manifest['video_sha256']
record={'version':v,'video_sha256':ev['sha256'],'format':{'duration':31,'width':1080,'height':1920,'fps':48,'frames':1488,'audio':'stereo AAC'},'changes':{'stepFrequencyVsV10':400/280,'bodyLiftOutsideFeedingPx':[32,58],'maxFootLiftPx':timing['maxLiftPixels'],'legShape':'tapered solid bones, organic hock, scales, splayed toes'},'sourceFiles':len(manifest['files']),'sourceSignature':manifest['signature'],'decoded':ev['decoded'],'browserErrors':ev['errors'],'kinematics':kin,'timing':timing,'encodedAudio':audio,'actualViewing':{'role':'primary maker; not independent review','sample':'48 ordered decoded frames, 1.125–5.531s global; 4.5-second sample','final':'16 era/year layout frames plus 18 local/transition/ending frames from final MP4','fullContinuousPlayback':False,'listened':False},'limitations':['No complete continuous playback or actual listening; music has timing and signal checks only.','Some small owners are briefly hidden by the foreground heron.'],'deliveryMode':'ai_review_once; existing budget exhausted, no new reviewer'}
(qa/'production-check.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf8')
(qa/'production-check.md').write_text(f'''# v11 制作检查

- 成片SHA256：`{ev['sha256']}`
- 31秒、1080×1920、48fps、1488帧、双声道AAC；全片解码通过；运行错误0。
- {len(manifest['files'])}份源码/素材快照签名核对通过，历史v10保留。
- 步频比v10提高约43%；平跑抬高身体32–58px露出腿部，抬脚约133px；腿部实体轮廓、自然踝部和张开脚趾。
- 16种动物、354时刻岸边固定/看空地与3处乱序寻址通过。
- 152个落脚音与步态共用时钟；16场故事事件时刻不变。5种从正常奔跑到取鱼收身的身体幅度均检查腿长可达。
- AAC解码峰值{audio['peakPCM']:.6f}、RMS{audio['rms']:.6f}、满量程削波样本0。
- 主制作实际查看：4.5秒样段48有序抽帧、最终16场总览与18处局部/转场/结尾。
- 非独立审核；未完整连续播放/实际听音。原一轮预算已用，不新增全面审核。部分小动物短暂被夜鹭遮挡。
''',encoding='utf8')
for filename in ['final-media-run-v11.py','log-delivery-run-v11.py','sample-check-run-v11.py']:shutil.copy2(root/filename,qa/filename)
with (root/'CHECKPOINT.md').open('a',encoding='utf8') as f:f.write(f'''

## 当前交付 run-v11（2026-10-16）
- completed: 步频较v10提高约43%，平跑抬高身体32–58px露腿，最高抬脚约133px、前踢更远、身体摆动更强。腿改为粗细变化的实体轮廓、自然踝部、鳞纹及张开脚趾，152落脚声音与音乐重新踩点。16种动物、清楚年代文字、岸边固定/失鱼看空地保留。
- aspect_ratio: 9:16；width: 1080；height: 1920；delivery_mode: ai_review_once（原预算已用，不新增角色）。
- video_path: out/{v}/video.mp4
- video_sha256: {ev['sha256']}
- verification: 31秒/48fps/1488帧/双声道AAC，全片解码，浏览器错误0；{len(manifest['files'])}文件快照签名通过。354时刻行为与岸边检查、16物种唯一、三处乱序seek通过；152落脚音同步、正常/收身幅度腿长可达，无AAC满量程削波。
- actual_view: 主制作查看样段48有序抽帧、最终16场全幅总览及18局部/转场/结尾帧。非独立审核，未完整连续播放/实际听音。
- delivery: DELIVERY-RUN-V11.md；qa/{v}/production-check.json；历史v10保留。
- next: 展示本次可播放成片，按用户反馈继续，不自动重开审核或其他项目。
''')
print(json.dumps({'sha256':ev['sha256'],'sourceFiles':len(manifest['files']),'report':str(qa/'production-check.json')},ensure_ascii=False))
