"""Use the user-supplied track; preserve original render and score versions."""
from pathlib import Path
import subprocess,json,hashlib,shutil,wave,re,io,sys
import numpy as np
ROOT=Path(__file__).resolve().parent;A=ROOT/'audio';D=ROOT/'delivery';D.mkdir(exist_ok=True)
FF=Path('D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe');FP=FF.with_name('ffprobe.exe')
source=Path('D:/ai项目/ai动画/music/亚历山大福音 - _16_巴比伦梦(vangelis - a_爱给网_aigei_com (1).mp3')
local=A/'user-provided-Dream-Of-Babylon.mp3'
if not local.exists():shutil.copy2(source,local)
sr=48000;n=56*sr
def pcm(path):
    b=subprocess.check_output([str(FF),'-v','error','-i',str(path),'-t','56','-f','wav','-c:a','pcm_s16le','-ac','2','-ar',str(sr),'pipe:1'])
    with wave.open(io.BytesIO(b),'rb') as f:x=np.frombuffer(f.readframes(n),dtype='<i2').reshape(-1,2).astype(np.float32)/32768
    if len(x)<n:x=np.pad(x,((0,n-len(x)),(0,0)))
    return x[:n]
music=pcm(local);env=pcm(A/'ambience.wav');t=np.arange(n)/sr
fade=np.sin(np.minimum(t/1.2,1)*np.pi/2)**2*np.sin(np.minimum((56-t)/4,1)*np.pi/2)**2
music*=fade[:,None]
mr=float(np.sqrt(np.mean(music**2)));er=float(np.sqrt(np.mean(env**2)))
egain=min(.65,mr*10**(-24/20)/max(er,1e-9));mix=music+env*egain
def wav(path,x):
    with wave.open(str(path),'wb') as f:
        f.setnchannels(2);f.setsampwidth(2);f.setframerate(sr);f.writeframes((np.clip(x,-.999,.999)*32767).astype('<i2').tobytes())
peak=float(np.max(np.abs(mix)))
if peak>.97:mix*=.97/peak
raw=A/'alexander-mix-raw.wav';wav(raw,mix)
analysis=subprocess.run([str(FF),'-hide_banner','-i',str(raw),'-af','loudnorm=I=-17:TP=-1.5:LRA=11:print_format=json','-f','null','NUL'],capture_output=True,text=True,encoding='utf8',check=True)
measure=json.JSONDecoder().raw_decode(analysis.stderr[analysis.stderr.rfind('{'):])[0]
flt='loudnorm=I=-17:TP=-1.5:LRA=11:linear=true:print_format=json'+''.join(':'+k+'='+measure[v] for k,v in [('measured_I','input_i'),('measured_TP','input_tp'),('measured_LRA','input_lra'),('measured_thresh','input_thresh'),('offset','target_offset')])
mixfile=A/'final-mix-alexander.wav'
r=subprocess.run([str(FF),'-y','-hide_banner','-i',str(raw),'-af',flt,'-ar','48000','-c:a','pcm_s24le',str(mixfile)],capture_output=True,text=True,encoding='utf8',check=True)
normalization=json.JSONDecoder().raw_decode(r.stderr[r.stderr.rfind('{'):])[0]
base=D/'暮河城-巴比伦巨城-1080x1920-v6.mp4';video=D/'暮河城-巴比伦巨城-Dream-of-Babylon-v7.mp4'
if '--verify-only' not in sys.argv:
    subprocess.run([str(FF),'-y','-hide_banner','-loglevel','warning','-i',str(base),'-i',str(mixfile),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','256k','-ar','48000','-t','56','-movflags','+faststart',str(video)],check=True)
probe=json.loads(subprocess.check_output([str(FP),'-v','error','-show_streams','-show_format','-count_frames','-of','json',str(video)],text=True,encoding='utf8'))
decode=subprocess.run([str(FF),'-v','error','-i',str(video),'-c:v','rawvideo','-c:a','pcm_s16le','-f','null','NUL'],capture_output=True,text=True,encoding='utf8')
vs=next(x for x in probe['streams'] if x['codec_type']=='video');au=next(x for x in probe['streams'] if x['codec_type']=='audio')
assert (vs['width'],vs['height'],int(vs['nb_read_frames']))==(1080,1920,1344)
assert vs['r_frame_rate']=='24/1' and abs(float(probe['format']['duration'])-56)<.08 and au['channels']==2 and decode.returncode==0
report={'video':str(video),'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'width':1080,'height':1920,'fps':24,'decoded_frames':1344,'duration':float(probe['format']['duration']),'audio_sample_rate':au['sample_rate'],'audio_channels':au['channels'],'decode_exit':decode.returncode,'decode_errors':decode.stderr,'visual_source':'v6, video stream copied without re-encoding','audio_source':str(source),'audio_source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source_excerpt_seconds':[0,56],'fade_in_seconds':1.2,'fade_out_seconds':[52,56],'ambience_gain':egain,'normalization':normalization,'audio_perceived':False,'independent_review':'pending'}
(D/'engineering-check-v7.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
(D/'ffprobe-v7.json').write_text(json.dumps(probe,ensure_ascii=False,indent=2),encoding='utf8')
(A/'alexander-mix-evidence.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
p=ROOT/'render/pipeline-status.json';s=json.loads(p.read_text(encoding='utf8'));s['stage']='candidate_v7_ready_for_one_review';s['candidate']=str(video);s['candidate_sha256']=report['sha256'];p.write_text(json.dumps(s,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'sha256':report['sha256'],'frames':1344,'duration':56,'audio':'Dream Of Babylon, user supplied','decode':'passed'}),flush=True)
