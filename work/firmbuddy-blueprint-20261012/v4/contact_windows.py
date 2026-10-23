import argparse,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

p=argparse.ArgumentParser();p.add_argument('--folder',required=True);args=p.parse_args()
root=Path(args.folder);cfg=json.loads((root/'config.json').read_text(encoding='utf-8'))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',18)
windows=[('overview',list(range(24,47))),('knowledge-open',[27+i/12 for i in range(12)]),('evidence-return',[32.8+i/12 for i in range(12)]),('gap-to-question',[39.3+i/12 for i in range(12)])]
log=[]
for name,times in windows:
    cols=4; rows=(len(times)+cols-1)//cols;cw=480;ch=295
    board=Image.new('RGB',(cols*cw,rows*ch),'#0b1830');d=ImageDraw.Draw(board)
    actual=[]
    for i,t in enumerate(times):
        frame=round((t-cfg['start'])*cfg['fps']);src=root/'frames'/f'{frame:05}.jpg'
        if not src.exists():raise FileNotFoundError(src)
        im=Image.open(src);im.thumbnail((480,270));x=i%cols*cw;y=i//cols*ch
        board.paste(im,(x,y+25));d.text((x+8,y+3),f'{cfg["start"]+frame/cfg["fps"]:.3f}s  /  #{frame}',fill='#dceaf7',font=font)
        actual.append(cfg['start']+frame/cfg['fps'])
    target=root/f'{name}.jpg';board.save(target,quality=92)
    log.append({'sheet':str(target),'times':actual,'source_frames':cfg,'viewing_status':'awaiting_actual_visual_inspection'})
(root/'contact-index.json').write_text(json.dumps(log,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'contact_sheets':[e['sheet'] for e in log]},ensure_ascii=False))
