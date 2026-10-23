from pathlib import Path
import subprocess,json,hashlib,sys
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'delivery';OUT.mkdir(exist_ok=True)
FF=Path('D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe');FP=FF.with_name('ffprobe.exe')
frames=ROOT/'render/frames-v15';missing=[i for i in range(2160) if not (frames/f'{i:05d}.png').exists()]
if missing:raise SystemExit(f'Missing {len(missing)} frames, first: {missing[:10]}')
video=OUT/'风衣骑手-巴比伦巨城-Dream-of-Babylon-v15.mp4'
cmd=[str(FF),'-y','-hide_banner','-loglevel','warning','-framerate','24','-start_number','0','-i',str(frames/'%05d.png'),'-i',str(ROOT/'audio/final-mix-v15.wav'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','slow','-crf','17','-pix_fmt','yuv420p','-threads:v','2','-c:a','aac','-b:a','256k','-ar','48000','-movflags','+faststart','-t','90',str(video)]
subprocess.run(cmd,check=True)
probe=json.loads(subprocess.check_output([str(FP),'-v','error','-show_streams','-show_format','-count_frames','-of','json',str(video)],text=True,encoding='utf8'))
decode=subprocess.run([str(FF),'-v','error','-i',str(video),'-c:v','rawvideo','-c:a','pcm_s16le','-f','null','NUL'],capture_output=True,text=True,encoding='utf8')
vs=next(s for s in probe['streams'] if s['codec_type']=='video');au=next(s for s in probe['streams'] if s['codec_type']=='audio')
report={'video':str(video),'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'width':vs['width'],'height':vs['height'],'frame_rate':vs['r_frame_rate'],'frames':int(vs['nb_read_frames']),'duration':float(probe['format']['duration']),'sample_rate':au['sample_rate'],'channels':au['channels'],'decode_exit':decode.returncode,'decode_errors':decode.stderr,'audio_perceived':False,'independent_review':'single-round budget already used; producer verification only'}
assert (report['width'],report['height'],report['frames'])==(1080,1920,2160)
assert report['frame_rate']=='24/1' and abs(report['duration']-90)<.08 and report['channels']==2 and decode.returncode==0
(OUT/'engineering-check-v15.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');(OUT/'ffprobe-v15.json').write_text(json.dumps(probe,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(report,ensure_ascii=False))
