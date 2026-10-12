"""Build bounded action sheets from the decoded final MP4 evidence. No aesthetic verdict."""
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json,math
root=Path(__file__).parent
groups={
 'hot-news-20261009':{'dissolve':[69,75,78,81,85,89,93],'pullback':[162,168,174,180,186,192,198],'light-propagation':[201,207,213,219,225,231,237,243,249,252],'award-handoff':[327,333,336,339,345]},
 'portrait-valve-20261009':{'section':[31,36,41,46,51,56,61,66],'explode-assemble':[87,92,97,102,107,112,117,122,127,132,137,142],'open':[146,151,156,161,166,171,176],'reseat':[239,244,249,254,259,264,269,274],'settle':[293,298,303,308,313,318,323,329]}}
for project,windows in groups.items():
    out=root/project/'out-final/motion-audit';report=json.loads((out/'frame-audit.json').read_text(encoding='utf-8'));fps=30 if project.startswith('hot') else 24;ledger=[]
    for label,frames in windows.items():
        width=280;height=350;cols=4;sheet=Image.new('RGB',(cols*width,math.ceil(len(frames)/cols)*(height+28)),'#09111b')
        for i,f in enumerate(frames):
            with Image.open(out/'frames'/f'frame-{f:06d}.jpg') as im:
                crop=(0,220,540,850) if project.startswith('hot') else (100,250,450,720)
                pic=im.crop(crop);pic.thumbnail((width,height));x=(i%cols)*width;y=(i//cols)*(height+28);sheet.paste(pic,(x+(width-pic.width)//2,y))
                ImageDraw.Draw(sheet).text((x+8,y+height+6),f'{f/fps:.3f}s / F{f}',fill='white',font=ImageFont.load_default(size=16))
        target=out/f'selected-{label}.jpg';sheet.save(target,quality=95);ledger.append({'window':label,'frames':frames,'seconds':[round(f/fps,3) for f in frames],'sheet':target.name})
    (out/'selected-schedule.json').write_text(json.dumps(ledger,indent=2),encoding='utf-8')
    print(project,sum(len(w['frames']) for w in ledger),'sampled frames')
