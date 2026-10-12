from pathlib import Path
from PIL import Image
import hashlib,json
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'assets/components'; OUT.mkdir(parents=True,exist_ok=True)
records=[]
def export(source,ident,box,kind,used):
    src=ROOT/'assets/originals'/source
    im=Image.open(src).convert('RGBA').crop(box)
    a=im.getchannel('A'); bbox=a.point(lambda v:255 if v>12 else 0).getbbox()
    if not bbox: raise ValueError(ident+' empty alpha')
    cropped=im.crop(bbox); target=OUT/(ident+'.png'); cropped.save(target)
    records.append(dict(id=ident,path='assets/components/'+target.name,kind=kind,
      generated_source='Codex内置生图：生成艺术重构',reference_ids=[],
      source='assets/originals/'+source,sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
      canvas_size=list(cropped.size),alpha_bbox=list(cropped.getbbox()),crop_offset=[box[0]+bbox[0],box[1]+bbox[1]],
      pivot=[.5,1],joints={'hip':[.5,.56],'knee':[.5,.78],'foot':[.5,.98]} if kind=='actor' else {},
      world_size=[1.75*cropped.width/cropped.height,1.75],depth='world-space',
      view_range='受限侧面/三分之四姿态；不伪造背面',light='左上柔光',used_in=used))
for row in range(2):
 for col in range(3):
    export('infantry-atlas.png',f'infantry-{row*3+col}',(col*512,row*512,(col+1)*512,(row+1)*512),'actor',['S02','S03','S04','S05','S06','S11'])
    export('cavalry-atlas.png',f'cavalry-{row*3+col}',(col*512,row*512,(col+1)*512,(row+1)*512),'horse',['S04','S05'])
for i,box in enumerate([(0,0,590,1024),(600,0,1015,1024),(1015,0,1536,1024)]):
 export('napoleon-atlas.png',f'napoleon-{i}',box,'actor',[['S01','S02'],['S06'],['S11']][i])
for i in range(2): export('scholars-atlas.png',f'scholar-{i}',(i*768,0,(i+1)*768,1024),'actor',['S09'])
im=Image.open(ROOT/'assets/originals/hands-stone-atlas.png'); w,h=im.size
for i,name in enumerate(['brush-hand','pen-hand','stone-face']):
 export('hands-stone-atlas.png',name,(round(i*w/3),0,round((i+1)*w/3),h),'contact',['S10'])
im=Image.open(ROOT/'assets/originals/boot-contact.png')
export('boot-contact.png','boot-contact',(0,0,*im.size),'contact',['S01'])
im=Image.open(ROOT/'assets/originals/infantry-elevated-atlas.png');w,h=im.size
for row in range(2):
 for col in range(3): export('infantry-elevated-atlas.png',f'infantry-station-{row*3+col}',(round(col*w/3),round(row*h/2),round((col+1)*w/3),round((row+1)*h/2)),'actor',['S04','S05','S06'])
im=Image.open(ROOT/'assets/originals/infantry-lead.png');export('infantry-lead.png','infantry-lead',(0,0,*im.size),'actor',['S03'])
(ROOT/'assets/registry.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'components':len(records),'canvas_sizes':{r['id']:r['canvas_size'] for r in records}},ensure_ascii=False))
