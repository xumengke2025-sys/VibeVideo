from pathlib import Path
import subprocess,json,hashlib
P=Path(__file__).resolve().parent;FF=Path('D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe');FP=FF.with_name('ffprobe.exe')
frames=P/'render/frames-v16';start=648;count=48
assert all((frames/f'{i:05d}.png').exists() for i in range(start,start+count))
out=P/'delivery/临河宫殿-v16-实际运镜样段.mp4'
subprocess.run([str(FF),'-y','-hide_banner','-loglevel','error','-framerate','24','-start_number',str(start),'-i',str(frames/'%05d.png'),'-ss','27','-i',str(P/'audio/final-mix-v15.wav'),'-map','0:v:0','-map','1:a:0','-frames:v','48','-t','2','-c:v','libx264','-preset','medium','-crf','17','-pix_fmt','yuv420p','-threads:v','2','-c:a','aac','-b:a','256k','-movflags','+faststart',str(out)],check=True)
probe=json.loads(subprocess.check_output([str(FP),'-v','error','-show_streams','-show_format','-count_frames','-of','json',str(out)],encoding='utf8'))
vs=next(s for s in probe['streams'] if s['codec_type']=='video');au=next(s for s in probe['streams'] if s['codec_type']=='audio')
decode=subprocess.run([str(FF),'-v','error','-i',str(out),'-c:v','rawvideo','-c:a','pcm_s16le','-f','null','NUL'],capture_output=True,text=True)
assert (vs['width'],vs['height'],int(vs['nb_read_frames']),au['channels'],decode.returncode)==(1080,1920,48,2,0)
(P/'qa/v16/excerpt-check.json').write_text(json.dumps({'video':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'source_frames':[648,695],'film_seconds':[27,29],'width':1080,'height':1920,'fps':24,'frames':48,'duration':2,'audio':'Original music excerpt, timeline 27-29s, stereo AAC','decode_exit':decode.returncode,'actual_listening':False,'scope':'Production excerpt; not the complete 90-second film'},ensure_ascii=False,indent=2),encoding='utf8')
print('PALACE_EXCERPT_READY',out,flush=True)
