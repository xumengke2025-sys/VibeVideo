"""Verify the encoded output and extract bounded evidence for the producer."""
import json, subprocess, hashlib, math
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parent
QA=ROOT/'qa/v12';DEST=QA/'encoded-frames';DEST.mkdir(exist_ok=True)
FF=ROOT.parent/'firmbuddy-blueprint-20261012/tools/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
engineering=json.loads((ROOT/'delivery/engineering-check-v12.json').read_text(encoding='utf8'))
video=Path(engineering['video']);assert hashlib.sha256(video.read_bytes()).hexdigest()==engineering['sha256']
manifest=json.loads((ROOT/'render/frozen-v12-manifest.json').read_text(encoding='utf8'))
for name,digest in manifest['files'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
timeline=json.loads((ROOT/'v12-timeline.json').read_text(encoding='utf8'))
cuts=[math.ceil(s[0]*24-1e-8) for s in timeline['shots'][1:]]
frames=sorted(set([0,12,48,96,168,288,396,528,588,611,732,755,756,1114,1115,1116,1176,1392,1560,1752,1800,1823]+[f for c in cuts for f in [c-1,c]]))
entries=[]
for frame in frames:
 path=DEST/f'{frame:05d}.png'
 subprocess.run([str(FF),'-y','-v','error','-ss',f'{frame/24:.9f}','-i',str(video),'-map','0:v:0','-frames:v','1',str(path)],check=True)
 entries.append({'frame':frame,'seconds':frame/24,'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
sheets=[]
for start in range(0,len(entries),6):
 part=entries[start:start+6];tw=270;th=480;sheet=Image.new('RGB',(tw*3,(th+25)*math.ceil(len(part)/3)),'#202020');draw=ImageDraw.Draw(sheet)
 for i,e in enumerate(part):
  with Image.open(e['path']) as im:
   im.thumbnail((tw,th));x=i%3*tw;y=i//3*(th+25);sheet.paste(im,(x,y+25));draw.text((x+5,y+5),f"f{e['frame']:04d} | {e['seconds']:.3f}s",fill='white')
 path=QA/f'encoded-sheet-{start//6:02d}.jpg';sheet.save(path,quality=94);sheets.append(str(path))
# Inspect every decoded frame for technical colour and temporal discontinuities.
p=subprocess.Popen([str(FF),'-v','error','-i',str(video),'-map','0:v:0','-vf','scale=180:320','-pix_fmt','rgb24','-f','rawvideo','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
size=180*320*3;count=0;green=[];bad=[];differences=[];previous=None;current=None
while True:
 raw=p.stdout.read(size)
 if not raw:break
 assert len(raw)==size
 following=np.frombuffer(raw,np.uint8).reshape(320,180,3).astype(np.float32)
 r,g,b=np.moveaxis(following,-1,0)
 if float(np.mean((g>r+12)&(g>b+10)))>.35:green.append(count)
 if previous is not None:
  before=float(np.abs(current-previous).mean());after=float(np.abs(following-current).mean());f=count-1;differences.append(before)
  if 10<f<1786 and all(abs(f-c)>=3 for c in cuts) and before>18 and after>18 and np.abs(previous-following).mean()<max(before,after)*.7:bad.append(f)
 previous,current=current,following;count+=1
errors=p.stderr.read().decode('utf8','replace');p.wait();assert p.returncode==0 and not errors and count==1824, {'returncode':p.returncode,'errors':errors,'frames':count}
technical={'frames_decoded':count,'abnormal_green_frames':green,'isolated_temporal_candidates':bad,'max_adjacent_difference':max(differences),'cut_frames':cuts,'video_sha256':engineering['sha256'],'method':'Every encoded frame at 180x320; strong-green detector and isolated two-sided RGB discontinuity detector. This does not certify aesthetics or rule out subtle temporal shimmer.'}
(QA/'encoded-temporal-scan.json').write_text(json.dumps(technical,indent=2),encoding='utf8')
assert not green and not bad,technical
windows=[]
for label,start in [('opening-old-flash',12),('egyptian-reception',276),('market-patrol',516),('canal-tow-teams',732),('statue-old-flash',1103),('avenue-panorama',1740)]:
 count_frames=24;w=180;h=320;cell_h=h+22
 command=[str(FF),'-v','error','-ss',f'{start/24:.9f}','-i',str(video),'-map','0:v:0','-frames:v',str(count_frames),'-vf',f'scale={w}:{h}','-pix_fmt','rgb24','-f','rawvideo','-']
 data=subprocess.check_output(command);assert len(data)==w*h*3*count_frames,(label,len(data))
 sheet=Image.new('RGB',(w*6,cell_h*4),'#202020');draw=ImageDraw.Draw(sheet)
 for i in range(count_frames):
  frame=Image.frombytes('RGB',(w,h),data[i*w*h*3:(i+1)*w*h*3]);x=i%6*w;y=i//6*cell_h
  sheet.paste(frame,(x,y+22));draw.text((x+5,y+5),f'f{start+i:04d} | {(start+i)/24:.3f}s',fill='white')
 path=QA/f'encoded-window-{label}.jpg';sheet.save(path,quality=94)
 windows.append({'label':label,'start_frame':start,'end_frame':start+count_frames-1,'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'method':'24 consecutive decoded frames, six columns by four rows, left-to-right then top-to-bottom; visual inspection pending.'})
report={'video':str(video),'video_sha256':engineering['sha256'],'frames':entries,'sheets':sheets,'motion_windows':windows,'actual_viewed_frames':[],'audio_perceived':False,'independent_review':False,'note':'Evidence extraction and engineering checks completed; actual visual observations must be recorded separately.'}
(QA/'producer-evidence-v12.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'frames':len(frames),'sheets':sheets,'motion_windows':windows,'technical':technical},ensure_ascii=False))
