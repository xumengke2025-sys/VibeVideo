"""Mux the 40-second original score without recompressing the picture; verify."""
from pathlib import Path
from io import BytesIO
import subprocess,hashlib,json,re,sys,wave
import numpy as np
R=Path(__file__).resolve().parent;Q=R/'qa/v21';Q.mkdir(exist_ok=True)
FF=R/'node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe'
if not FF.is_file():FF=Path('D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe')
V=R/'out/mother-baby-20-eras-portrait-v21-40s.mp4';A=R/'assets/audio-v21/warm-family-40s.wav'
O=R/'out/mother-baby-20-eras-portrait-v21-40s-music.mp4'
subprocess.run([str(FF),'-v','error','-y','-i',str(V),'-i',str(A),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-t','40','-movflags','+faststart',str(O)],check=True,timeout=90)
# Decode both streams. This build of FFmpeg requires an explicit null encoder.
p=subprocess.run([str(FF),'-hide_banner','-i',str(O),'-map','0:v:0','-map','0:a:0','-c:v','rawvideo','-c:a','pcm_s16le','-threads','1','-f','null','-'],capture_output=True,text=True,timeout=180)
(Q/'music-decode-log.txt').write_text(p.stderr,encoding='utf8')
assert p.returncode==0,p.stderr[-1000:]
frames=re.findall(r'frame=\s*(\d+)',p.stderr);assert int(frames[-1])==960
assert re.search(r'Duration: 00:00:40\.00',p.stderr) and re.search(r'1080x1920.*24 fps',p.stderr) and 'Audio: aac' in p.stderr
# Packet-level picture hash: adding music must leave the 960 picture packets intact.
def picture_hash(path):
    r=subprocess.run([str(FF),'-v','error','-i',str(path),'-map','0:v:0','-c:v','copy','-bsf:v','h264_mp4toannexb','-f','h264','-'],capture_output=True,check=True,timeout=60)
    return hashlib.sha256(r.stdout).hexdigest()
assert picture_hash(V)==picture_hash(O)
decoded=subprocess.run([str(FF),'-v','error','-i',str(O),'-map','0:a:0','-c:a','pcm_s16le','-f','wav','-ac','2','-ar','48000','-'],capture_output=True,check=True,timeout=60)
with wave.open(BytesIO(decoded.stdout),'rb') as w:x=np.frombuffer(w.readframes(40*48000+8192),'<i2').astype(np.float32).reshape(-1,2)/32768
assert len(x)>=40*48000
windows=[float(np.sqrt(np.mean(x[int(t*48000):int((t+.5)*48000)]**2))) for t in np.arange(.5,39,.5)]
report={'file':O.name,'sha256':hashlib.sha256(O.read_bytes()).hexdigest(),'duration':40,'width':1080,'height':1920,'fps':24,'frames':960,'audio':'AAC stereo 48kHz 192kbps','decode_exit':0,'picture_packet_hash_unchanged':True,'aac_peak_dbfs':round(float(20*np.log10(np.max(np.abs(x)))),2),'aac_rms_dbfs':round(float(20*np.log10(np.sqrt(np.mean(x*x)))),2),'clipped_samples':int(np.count_nonzero(np.abs(x)>=1)),'min_half_second_rms':min(windows),'actual_listening':False,'scope':'Complete video/audio decode and packet equality; waveform checks are not actual listening. Visual samples of the silent master remain valid because picture packets are unchanged.'}
assert report['clipped_samples']==0 and min(windows)>.001
(Q/'music-engineering-check.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print(json.dumps(report))
