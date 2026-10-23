from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parent;O=R.parent/'out/final-v18-business-story'
groups={'opening-sequence':[0,1.2,2.4,4.8,5.8,6.2,6.6,8.4,11.6,12.4,12.8,13.2,15.2,18.8,19.2,19.6,20.4,22.4,23.2,23.6,24,24.4,25.2,27.2], 'handoff-sequence':[33.2,34,35.2,36.4,38,40,41.2,42,42.8,43.2,43.6,44,44.4,45,46,48], 'closing-sequence':[128,129,130,131,132,132.8,133.2,133.6,134.4,135.6,138,140.8,142.4,142.8,143.2,143.6,146.8,147.2,147.6,148,148.4,149.2,151.2,153.6]}
for name,times in groups.items():
 paths=[O/'frames'/f'{round(t*30):05d}.jpg' for t in times]
 if not all(p.exists() for p in paths):continue
 w,h=480,270;cols=4;sheet=Image.new('RGB',(cols*w,((len(times)+3)//4)*(h+27)),'#101e2c');d=ImageDraw.Draw(sheet);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',18)
 for j,(t,p) in enumerate(zip(times,paths)):
  im=Image.open(p).convert('RGB').resize((w,h));x=j%cols*w;y=j//cols*(h+27);sheet.paste(im,(x,y));d.text((x+8,y+h+2),f'{t:.2f}s',font=font,fill='white')
 sheet.save(O/(name+'.jpg'),quality=94)
 print(name+': '+str(len(times))+' frames')
