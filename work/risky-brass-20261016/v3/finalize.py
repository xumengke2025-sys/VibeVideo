from pathlib import Path
import subprocess,json,hashlib,wave
import numpy as np

R=Path(__file__).parent
B=Path('D:/ai项目/ai动画/VibeVideo项目/node_modules/@remotion/compositor-win32-x64-msvc')
OUT=R/'Risky-黄铜机械-完整版.mp4'
QA=R/'qa'/'final-engineering'
QA.mkdir(parents=True,exist_ok=True)
def run(args):
    p=subprocess.run([str(x) for x in args],capture_output=True,text=True,encoding='utf-8',errors='replace')
    if p.returncode:raise RuntimeError(p.stderr[-4000:])
    return p
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
run([B/'ffmpeg.exe','-hide_banner','-y','-i',R/'risky-full-silent.mp4','-i',R/'full-audio.wav','-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart','-shortest',OUT])
meta=json.loads(run([B/'ffprobe.exe','-v','error','-show_format','-show_streams','-of','json',OUT]).stdout)
v=next(s for s in meta['streams'] if s['codec_type']=='video')
a=next(s for s in meta['streams'] if s['codec_type']=='audio')
assert(v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1920,1080,'60/1',4800)
assert abs(float(meta['format']['duration'])-80)<.05
assert a['channels']==2 and a['sample_rate']=='48000'
dec=run([B/'ffmpeg.exe','-v','error','-i',OUT,'-c:v','rawvideo','-c:a','pcm_s16le','-f','null','-'])
assert not dec.stderr.strip(),dec.stderr
render=json.loads((R/'qa'/'render.json').read_text(encoding='utf-8'))
assert render['source']==sha(R/'scene.js') and not render['errors']
checks=json.loads((R/'qa'/'stills-checks.json').read_text(encoding='utf-8'))
assert all(s['identical'] for s in checks['seeks']) and not checks['errors']
with wave.open(str(R/'full-audio.wav')) as w:
    pcm=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float64)/32768
    peak=float(np.max(np.abs(pcm)));rms=float(np.sqrt(np.mean(pcm*pcm)))
assert 0<peak<.99
times=[1.2,4.4,12.5,18.8,26.8,35.7,44,48.9,52.8,58,63,68.8,73.8,75.8,78.3]
for t in times:run([B/'ffmpeg.exe','-v','error','-y','-ss',t,'-i',OUT,'-frames:v','1',QA/f'frame-{t}.png'])
report={'path':str(OUT),'sha256':sha(OUT),'source_sha256':sha(R/'scene.js'),'duration':float(meta['format']['duration']),'width':v['width'],'height':v['height'],'fps':v['r_frame_rate'],'decoded_frames':4800,'full_decode':'passed','audio':{'codec':a['codec_name'],'channels':2,'rate':48000,'original_synthesis':True,'peak_linear':peak,'rms_linear':rms,'listened':False},'not_engine_results':True,'independent_review':'pending','stills_from_actual_mp4':times,'source_addressability':checks['seeks']}
(QA/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
