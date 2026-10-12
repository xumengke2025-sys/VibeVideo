"""Rebuildable short technical fixture; intentionally a schematic, not a quality benchmark."""
import json,math,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parent
FFMPEG=Path('D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe')
FONT=Path('C:/Windows/Fonts/arial.ttf')
small=ImageFont.truetype(str(FONT),30);label=ImageFont.truetype(str(FONT),44);title=ImageFont.truetype(str(FONT),64)
states=json.loads((BASE/'states.json').read_text())
frames=BASE/'frames';frames.mkdir(exist_ok=True)
for i,s in enumerate(states):
    im=Image.new('RGB',(1080,1920),'#111b2b');d=ImageDraw.Draw(im)
    d.text((90,120),'PRESSURE OPENS THE SEAL',font=title,fill='#eef7ff')
    d.text((90,215),'Quasi-static illustration / no fluid solver',font=small,fill='#9dafc6')
    d.rounded_rectangle((160,560,950,1000),50,outline='#9dafc6',width=15)
    d.line((420,585,420,975),fill='#f4b659',width=24)
    x=420+s['displacement']*160
    d.line((x,600,x,960),fill='#76d9e6',width=36)
    spring=[]
    for j in range(41):
        xx=x+30+(860-x-30)*j/40;yy=780+(0 if j in [0,40] else (45 if j%2 else -45));spring.append((xx,yy))
    d.line(spring,fill='#eef7ff',width=8);d.line((860,650,860,910),fill='#9dafc6',width=20)
    d.text((165,1040),'Seat',font=label,fill='#f4b659');d.text((610,1040),'Fixed spring end',font=small,fill='#9dafc6')
    d.text((90,1160),f"Drive: {s['pressure']:.2f} / Preload: 1.00",font=label,fill='#eef7ff')
    d.text((90,1230),f"Travel: {s['displacement']:.2f} / Limit: 1.00",font=label,fill='#76d9e6')
    d.text((90,1300),'OPEN' if s['open'] else 'SEATED',font=label,fill='#76d9e6' if s['open'] else '#f4b659')
    # Stable data axes: pressure from -0.5 to 2.5; displacement from 0 to 1.
    d.line((160,1510,920,1510),fill='#9dafc6',width=3);d.line((160,1410,160,1720),fill='#9dafc6',width=3)
    d.text((90,1770),'pressure (-0.5 to 2.5), constant scale',font=small,fill='#9dafc6')
    pts=[(160+(r['pressure']+.5)/3*760,1710-r['displacement']*260) for r in states[:i+1]]
    if len(pts)>1:d.line(pts,fill='#76d9e6',width=7)
    xx,yy=pts[-1];d.ellipse((xx-10,yy-10,xx+10,yy+10),fill='#f4b659')
    im.save(frames/f'{i:04d}.png')
subprocess.run([str(FFMPEG),'-y','-framerate','30','-i',str(frames/'%04d.png'),'-c:v','libx264','-threads:v','1','-pix_fmt','yuv420p','-crf','24',str(BASE/'fixture.mp4')],check=True,capture_output=True)
plan={'duration':2,'fps':30,'width':1080,'height':1920,'shots':[{'id':'threshold','start':0,'end':2,'intent':'Read pressure crossing preload, constrained travel, and reseating','action':'Increase pressure past preload, reach stop, decrease through contact','camera':'Fixed close schematic: hold contact readable; data shares same state','states':{'establish':.2,'action':.85,'result':1.85},'risks':[[.4,1.2],[1.5,1.9]]}],'connections':[]}
(BASE/'plan.json').write_text(json.dumps(plan,indent=2),encoding='utf-8')
print('built 1080x1920 / 30fps / 2 seconds / no audio')
