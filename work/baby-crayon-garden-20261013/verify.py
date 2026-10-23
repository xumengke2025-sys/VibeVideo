"""Basic engineering checks only. Does not claim visual or listening review."""
from pathlib import Path
import subprocess,json,hashlib,datetime
root=Path(__file__).resolve().parent
target=root/'out/宝宝和太阳的晚安-v1.mp4'
bin=Path('D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc')
r=subprocess.run([str(bin/'ffprobe.exe'),'-v','error','-show_streams','-show_format','-of','json',str(target)],capture_output=True,text=True,encoding='utf-8',timeout=60,check=True)
meta=json.loads(r.stdout)
v=next(s for s in meta['streams'] if s['codec_type']=='video')
a=next(s for s in meta['streams'] if s['codec_type']=='audio')
checks={
    'file_nonempty':target.stat().st_size>0,
    'portrait_1080x1920':(v['width'],v['height'])==(1080,1920),
    'fps_24':v['avg_frame_rate']=='24/1',
    'duration_60s':abs(float(meta['format']['duration'])-60)<.05,
    '1440_video_frames':int(v.get('nb_frames',0))==1440,
    'h264_8bit_420':v['codec_name']=='h264' and v['pix_fmt'] in ('yuv420p','yuvj420p'),
    'aac_stereo_48khz':a['codec_name']=='aac' and a['channels']==2 and a['sample_rate']=='48000',
}
decode=subprocess.run([str(bin/'ffmpeg.exe'),'-hide_banner','-v','error','-xerror','-i',str(target),'-map','0:v:0','-map','0:a:0','-c:v','rawvideo','-c:a','pcm_s16le','-f','null','-'],capture_output=True,text=True,encoding='utf-8',timeout=180)
checks['full_video_audio_decode']=decode.returncode==0 and not decode.stderr.strip()
report={'output':str(target),'checkedAt':datetime.datetime.now().isoformat(),'delivery_mode':'user_feedback','sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'sizeBytes':target.stat().st_size,'checks':checks,'allPassed':all(checks.values()),'decodeReturnCode':decode.returncode,'decodeStderr':decode.stderr[-2000:],'metadata':meta,'reviewScope':'Basic engineering checks; representative stills and 16 samples from 17–24.5s viewed during production. No independent review, full-frame review or complete listening review.'}
report['sourceHashes']={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.glob('*.js'))+sorted((root/'engine').glob('*.js'))+[root/'index.html',root/'render.mjs',root/'score.py',root/'score.wav']}
(root/'out/verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'allPassed':report['allPassed'],'checks':checks,'sha256':report['sha256'],'sizeBytes':report['sizeBytes']},ensure_ascii=False))
if not report['allPassed']:raise SystemExit(1)
