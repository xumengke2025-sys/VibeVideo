"""Timestamped consecutive-frame sheets for production inspection. Not a review verdict."""
import argparse,json
from pathlib import Path
from PIL import Image,ImageDraw
p=argparse.ArgumentParser();p.add_argument('folder');p.add_argument('--out',required=True);p.add_argument('--start',type=int,required=True);p.add_argument('--end',type=int,required=True);p.add_argument('--step',type=int,default=1);p.add_argument('--width',type=int,default=180);p.add_argument('--cols',type=int,default=6);p.add_argument('--rows',type=int,default=4);a=p.parse_args()
src=Path(a.folder);out=Path(a.out);out.mkdir(parents=True,exist_ok=True);frames=list(range(a.start,a.end+1,a.step));w=a.width;h=round(w*16/9);n=a.cols*a.rows;index=[]
for j in range(0,len(frames),n):
 sub=frames[j:j+n];sheet=Image.new('RGB',(a.cols*w,a.rows*(h+22)),(24,25,25));d=ImageDraw.Draw(sheet)
 for k,f in enumerate(sub):
  with Image.open(src/f'{f:05d}.png') as im:im=im.resize((w,h),Image.Resampling.LANCZOS);x=k%a.cols*w;y=k//a.cols*(h+22);sheet.paste(im,(x,y));d.text((x+4,y+h+4),f'{f/24:.3f}s  f{f}',fill='white')
 path=out/f'{sub[0]:05d}-{sub[-1]:05d}.jpg';sheet.save(path,quality=94);index.append({'path':str(path.resolve()),'frames':sub})
(out/'index.json').write_text(json.dumps(index,indent=2),encoding='utf8');print(len(index),'sheets',len(frames),'frames')
