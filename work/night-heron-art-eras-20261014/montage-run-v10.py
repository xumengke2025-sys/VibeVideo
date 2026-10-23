from pathlib import Path
import sys
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parent
p=root/'out'/sys.argv[1]
files=sorted(p.glob('time-*.png'))
board=Image.new('RGB',(1440,((len(files)+3)//4)*350),'#242a2c');d=ImageDraw.Draw(board)
for i,f in enumerate(files):
 im=Image.open(f);crop=im.crop((155,1020,875,1660)).resize((360,320))
 x=i%4*360;y=i//4*350;board.paste(crop,(x,y));d.text((x+8,y+326),f.stem,fill='white')
board.save(p/'gait-strip.jpg')
print(p/'gait-strip.jpg')
