import json,subprocess,sys,math,hashlib
from pathlib import Path
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parent;version=sys.argv[1];out=root/'out'/version;qa=root/'qa'/version;qa.mkdir(exist_ok=True)
cfg=json.loads((out/'config.json').read_text('utf8'));plan=json.loads((root/'production-plan-run-v6.json').read_text('utf8'));manifest={m['era']:m for m in json.loads((root/'assets/run-v6/manifest.json').read_text('utf8'))}
ff='D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe';shots=plan['timeline']['shots'];records=[];pages=[]
distance=lambda t:550*t+5*t*t
sx=lambda t:375+20*math.sin(t*.6)
for n,sh in enumerate(shots,1):
 e=sh['events'];times=[(sh['startFrame']+e['grab']+.8+u*(e['neckTucked']+1-e['grab']-.8))/24 for u in [.02,.19,.41,.79,.94]]
 if times[0]<cfg['start'] or times[-1]>=cfg['start']+cfg['duration']:continue
 board=Image.new('RGB',(1600,350),'#474b4c');d=ImageDraw.Draw(board)
 m=manifest[n];model=plan['fauna']['models'][sh['owner']];mh=next(model[k] for k in ['modelStandingHeightM','modelSeatedHeightM','modelPerchedHeightM','modelShoulderHeightM'] if k in model)
 oh=mh*510*.6/.4;ow=oh*m['neutralWidth']/m['neutralHeight'];grab=(sh['startFrame']+e['grab'])/24
 for k,t in enumerate(times):
  f=round(t*48);t=f/48;file=qa/f'era-{n:02}-reaction-{k}.png';subprocess.run([ff,'-v','error','-y','-ss',str(t-cfg['start']),'-i',str(out/'video.mp4'),'-frames:v','1',str(file)],capture_output=True,check=True)
  im=Image.open(file).convert('RGB');camera=distance(t)-sx(t);ox=distance(grab)+510*.52-camera+ow*.40+min(80,oh*.12)
  size=max(ow*1.45,oh*1.3,180);cx=ox-ow*.15;cy=1305-oh*.50;crop=im.crop((round(cx-size/2),round(cy-size/2),round(cx+size/2),round(cy+size/2))).resize((320,320));board.paste(crop,(k*320,0));d.text((k*320+6,326),f'era {n:02}  {t:.3f}s  frame {f}',fill='white')
  records.append({'era':n,'frame48':f,'time':t,'file':str(file)})
 pages.append((n,board))
for p in range(math.ceil(len(pages)/4)):
 subset=pages[p*4:p*4+4];im=Image.new('RGB',(1600,350*len(subset)),'#474b4c')
 for row,(n,board) in enumerate(subset):im.paste(board,(0,row*350))
 im.save(qa/f'reaction-check-{p+1}.jpg')
(qa/'reaction-extraction.json').write_text(json.dumps({'video_sha256':hashlib.sha256((out/'video.mp4').read_bytes()).hexdigest(),'records':records,'viewing':'extracted; record actual viewing separately'},indent=2),encoding='utf8')
print(json.dumps({'scenes':len(pages),'frames':len(records),'qa':str(qa)}))
