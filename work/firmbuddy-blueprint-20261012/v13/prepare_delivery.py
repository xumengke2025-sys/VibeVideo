from pathlib import Path
import shutil,json
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parent;B=R.parent
for name,target in [('mix.wav','base-v11.wav'),('timing.json','base-v11-timing.json')]:
 shutil.copy2(B/'v11/audio'/name,R/'audio'/target)
p=R/'make_audio.py';s=p.read_text(encoding='utf-8').replace("R.parent/'v11/audio/mix.wav'","R/'audio/base-v11.wav'").replace("R.parent/'v11/audio/timing.json'","R/'audio/base-v11-timing.json'");p.write_text(s,encoding='utf-8')
C=B/'concepts/v13';C.mkdir(exist_ok=True)
for p in (B/'out/stills-v13-business-concepts').glob('*.png'):shutil.copy2(p,C/p.name)
O=B/'out/sample-v13-business-handoff'
frames=[(t,O/'frames'/f'{round((t-12.8)*30):05d}.jpg') for t in [12.8,13.4,14,14.6,15.2,15.8,16.4,17,17.6,18.2,18.8,19.4,20,20.6]]
cols=4;w=480;h=270;sheet=Image.new('RGB',(cols*w,((len(frames)+cols-1)//cols)*(h+28)),'#091a2c');d=ImageDraw.Draw(sheet);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',20)
for i,(t,p) in enumerate(frames):
 im=Image.open(p).convert('RGB');im.thumbnail((w,h));x=i%cols*w;y=i//cols*(h+28);sheet.paste(im,(x,y));d.text((x+10,y+h+2),f'{t:.1f}s',font=font,fill='white')
sheet.save(O/'handoff-contact.jpg',quality=94)
print('Saved sample contact sheet and standalone base audio')
