from pathlib import Path
from io import BytesIO
import json,subprocess,re,hashlib,zipfile
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent
O=R/'qa/v20/final';O.mkdir(parents=True,exist_ok=True)
V=R/'out/mother-baby-20-eras-portrait-v20-40s.mp4'
FF=Path('D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe')
r=subprocess.run([str(FF),'-hide_banner','-i',str(V),'-c:v','rawvideo','-f','null','-'],capture_output=True,text=True,timeout=240)
(O/'decode-log.txt').write_text(r.stderr,encoding='utf8')
frames=re.findall(r'frame=\s*(\d+)',r.stderr);stream=re.search(r'Video:.*?(\d{3,5})x(\d{3,5}).*?(\d+(?:\.\d+)?) fps',r.stderr);dur=re.search(r'Duration: (\d+):(\d+):(\d+(?:\.\d+)?)',r.stderr)
d={'sha256':hashlib.sha256(V.read_bytes()).hexdigest(),'decode_exit':r.returncode,'frames':int(frames[-1]),'width':int(stream[1]),'height':int(stream[2]),'fps':float(stream[3]),'duration':int(dur[1])*3600+int(dur[2])*60+float(dur[3]),'audio':bool(re.search(r'Stream.*Audio:',r.stderr))}
assert r.returncode==0 and (d['frames'],d['width'],d['height'],d['fps'],d['duration'],d['audio'])==(960,1080,1920,24,40,False),d
(O/'engineering-check.json').write_text(json.dumps(d,indent=2),encoding='utf8')
for t in [.8,18.8,36.9,39.2]:subprocess.run([str(FF),'-v','error','-y','-ss',str(t),'-i',str(V),'-frames:v','1',str(O/f'frame-{t}.png')],check=True,timeout=30)
sheet=Image.new('RGB',(1080,1968),'#eee6d5');draw=ImageDraw.Draw(sheet)
for k,t in enumerate([.8,18.8,36.9,39.2]):
 with Image.open(O/f'frame-{t}.png') as im:thumb=im.resize((540,960))
 x=k%2*540;y=k//2*984;sheet.paste(thumb,(x,y+24));draw.text((x+8,y+6),f'v20 final | {t}s',fill='#342b23')
sheet.save(O/'final-check-sheet.png')
details=[(t,(180,980,880,1540)) for t in [.35,.65,1.05,1.55]]
details += [(t,(180,980,880,1540)) for t in [36.35,36.65,37.05,37.55]]
details += [(t,(180,980,880,1540)) for t in [37.7,37.95,38.2,38.45]]
details += [(t,(180,980,880,1540)) for t in [38.6,38.9,39.2,39.55]]
def encoded_frame(t):
    r=subprocess.run([str(FF),'-v','error','-ss',str(t),'-i',str(V),'-frames:v','1','-f','image2pipe','-vcodec','png','-'],capture_output=True,check=True,timeout=30)
    return Image.open(BytesIO(r.stdout)).convert('RGB')
detail_sheet=Image.new('RGB',(1280,1696),'#eee6d5');draw=ImageDraw.Draw(detail_sheet)
for k,(t,box) in enumerate(details):
    im=encoded_frame(t).crop(box);im.thumbnail((320,400))
    x=k%4*320;y=k//4*424;detail_sheet.paste(im,(x+(320-im.width)//2,y+24))
    draw.text((x+8,y+6),f'final v20 | {t:.3f}s',fill='#342b23')
detail_sheet.save(O/'repair-and-sky-check-sheet.png')
cut_times=[37.75+j/24 for j in range(12)]
cut_sheet=Image.new('RGB',(1120,1560),'#eee6d5');draw=ImageDraw.Draw(cut_sheet)
for k,t in enumerate(cut_times):
    im=encoded_frame(t).resize((280,498));x=k%4*280;y=k//4*520;cut_sheet.paste(im,(x,y+22));draw.text((x+8,y+6),f'{t:.3f}s',fill='#342b23')
cut_sheet.save(O/'encoded-cut-38-check-sheet.png')
(O/'detail-capture.json').write_text(json.dumps({'video_sha256':d['sha256'],'details_seconds':[t for t,_ in details],'cut_38_seconds':cut_times,'capture_only':True,'note':'Production frame evidence; export alone does not establish viewing or whole-film review.'},indent=2),encoding='utf8')
print(json.dumps(d))
