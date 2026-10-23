"""Create a reproducible 40-second delivery from the preserved 210-second v7."""
from pathlib import Path
from fractions import Fraction
import hashlib, json, subprocess

R=Path(__file__).resolve().parent
B=R.parent.parent/'node_modules/@remotion/compositor-win32-x64-msvc'
source=R/'out/mother-baby-35-eras-portrait-v7.mp4'
target=R/'out/mother-baby-35-eras-portrait-v7-40s.mp4'
qa=R/'qa/v7-40s';qa.mkdir(parents=True,exist_ok=True)
expected_source='04fb68c5af02b28e8893c321eedb35a5cb1c373d83e1a85721c231cdac9f48e5'
source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
assert source_hash==expected_source,'Unexpected source; preserve approved version.'
print('Retiming 210s to 40s at 5.25x, preserving 1080x1920 / 24fps and intentional silence.',flush=True)
command=[str(B/'ffmpeg.exe'),'-hide_banner','-v','error','-y','-itsscale','0.190476190476190476','-i',str(source),'-r','24',
    '-t','40','-frames:v','960','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-threads','2','-movflags','+faststart',str(target)]
subprocess.run(command,check=True,timeout=300)
probe=subprocess.run([str(B/'ffprobe.exe'),'-v','error','-count_frames','-show_streams','-show_format','-of','json',str(target)],check=True,capture_output=True,text=True,timeout=120)
media=json.loads(probe.stdout);video=next(s for s in media['streams'] if s['codec_type']=='video')
decode=subprocess.run([str(B/'ffmpeg.exe'),'-hide_banner','-v','error','-i',str(target),'-c:v','rawvideo','-f','null','-'],capture_output=True,text=True,timeout=120)
record={'source':str(source),'source_sha256':source_hash,'video':str(target),'video_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
    'speed_factor':5.25,'time_mapping':'output_seconds = source_seconds * 4 / 21','width':video['width'],'height':video['height'],
    'fps':float(Fraction(video['avg_frame_rate'])),'duration_seconds':float(media['format']['duration']),'decoded_frames':int(video['nb_read_frames']),
    'audio_present':any(s['codec_type']=='audio' for s in media['streams']),'decode_exit':decode.returncode,'file_bytes':target.stat().st_size,
    'source_preserved':True,'independent_review':'No new review round. Original v7 partial visual coverage does not certify normal-speed perception of this retimed output.'}
record['engineering_pass']=(record['width'],record['height'],record['fps'],record['decoded_frames'])==(1080,1920,24,960) and abs(record['duration_seconds']-40)<.001 and not record['audio_present'] and decode.returncode==0
(qa/'engineering-check.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
(qa/'ffprobe.json').write_text(probe.stdout,encoding='utf-8')
(qa/'decode-log.txt').write_text(decode.stderr,encoding='utf-8')
assert record['engineering_pass'],record
brief_file=R/'brief.json';brief=json.loads(brief_file.read_text(encoding='utf-8'))
brief['latest_delivery']={'video':target.relative_to(R).as_posix(),'duration_seconds':40,'speed_factor':5.25,'source_video':source.relative_to(R).as_posix(),'sha256':record['video_sha256'],'aspect_ratio':'9:16','width':1080,'height':1920,'fps':24,'verification':'qa/v7-40s/engineering-check.json'}
brief_file.write_text(json.dumps(brief,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
checkpoint=R/'CHECKPOINT.md';text=checkpoint.read_text(encoding='utf-8')
section='''## 最新交付：40秒加速版（2026-10-20）

- request: 用户要求加速到40秒，调整现有成片节奏；无需新创意、新生图或新增审片轮次。
- format: aspect_ratio=9:16；width=1080；height=1920；24fps；960帧；有意无声；delivery_mode=ai_review_once沿用且原轮次已结束。
- video: out/mother-baby-35-eras-portrait-v7-40s.mp4
- method: 保留35时代完整原时间轴内容，均匀5.25倍速；输入时间戳按4/21缩放，输出24fps并限960帧/40秒。210秒原片与源码包保留。
- source: speedup_40s.py；证据qa/v7-40s/engineering-check.json、ffprobe.json及decode-log.txt。
- verification: 实际40.000秒，960帧完整解码通过，1080×1920/24fps/无音轨符合预期。原片局部静帧审核不迁移为本版正常速度观感通过。
- video_sha256: HASH
- next_action: 交付40秒成片，后续按用户反馈修改。

'''.replace('HASH',record['video_sha256'])
if '## 最新交付：40秒加速版' not in text:
    checkpoint.write_text(text.replace('## 当前制作 v7',section+'## 当前制作 v7',1),encoding='utf-8')
print(json.dumps(record,ensure_ascii=False),flush=True)
