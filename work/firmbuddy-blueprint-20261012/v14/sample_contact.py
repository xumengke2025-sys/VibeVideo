from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parent;O=R.parent/'out/sample-v14-unload-transfer'
frames=list(range(0,240,15))+[239]
sheet=Image.new('RGB',(1920,5*300),'#0b1c2c');d=ImageDraw.Draw(sheet);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',21)
for i,f in enumerate(frames):
 im=Image.open(O/'frames'/f'{f:05d}.jpg').convert('RGB');im.thumbnail((480,270));x=i%4*480;y=i//4*300;sheet.paste(im,(x,y));d.text((x+10,y+274),f'{19.6+f/30:.2f}s',font=font,fill='white')
sheet.save(O/'transfer-contact.jpg',quality=95)
print('Sample contact sheet ready')
