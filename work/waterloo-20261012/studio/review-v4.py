from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
ROOT=Path(__file__).resolve().parent
def sheet(paths,out,columns=5,width=216):
 tile_h=int(width*16/9)+26
 canvas=Image.new('RGB',(columns*width,((len(paths)+columns-1)//columns)*tile_h),'#101820')
 d=ImageDraw.Draw(canvas)
 for k,(label,path) in enumerate(paths):
  im=Image.open(path).convert('RGB');im.thumbnail((width,tile_h-26))
  x=(k%columns)*width;y=(k//columns)*tile_h
  canvas.paste(im,(x,y+26));d.text((x+5,y+5),label,fill='white')
 canvas.save(ROOT/out)
sample=ROOT/'out/sample-v4b/frames'
indices=[0,24,72,95,96,125,134,135,136,137,140,144,154,168,191]
sheet([(f'{20+i/24:.3f}s',sample/f'{i:05}.jpg') for i in indices],'out/sample-v4b/sequence.jpg')
stills=ROOT/'out/stills-v4b'
times=sorted([p for p in stills.glob('*.png')],key=lambda p:float(p.stem))
sheet([(p.stem+'s',p) for p in times],'out/stills-v4b/overview.jpg',columns=6,width=216)
