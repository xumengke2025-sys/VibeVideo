from pathlib import Path
import json, numpy as np
from PIL import Image, ImageDraw
from datetime import datetime
ROOT=Path(__file__).resolve().parent
QA=ROOT/'qa/v12';QA.mkdir(parents=True,exist_ok=True)
cp=json.loads((ROOT/'CHECKPOINT.json').read_text(encoding='utf8'))
cp.update(objective='修复闪动，增加祭司、军队、埃及使团与互动；全程主干道人潮；细化彩绘船只、船员和纤夫，完成76秒竖屏v12。',version='v12',status='v12_diagnosis',updated_at=datetime.now().isoformat(timespec='seconds'),next_action='诊断连续帧闪动，增补角色、全长人流与船只，样段验证后完整渲染。')
cp['v12_revision']={'requests':['屏幕闪动','祭司、巴比伦军队、埃及使团及互动','全长主干道人群','船只色彩、船员和纤夫'],'preserved':['76s 1080x1920 24fps','music excerpt','horizon reveal','blue glaze and miniature focus','city and connected streets'],'new_review_round':False}
(ROOT/'CHECKPOINT.json').write_text(json.dumps(cp,ensure_ascii=False,indent=2),encoding='utf8')
files=sorted((ROOT/'render/frames-v11').glob('[0-9][0-9][0-9][0-9][0-9].png'))
data=[]
for i,p in enumerate(files):
    with Image.open(p) as im:data.append(np.asarray(im.resize((180,320)),dtype=np.float32))
    if i%400==0:print('READ',i,flush=True)
x=np.array(data);d=np.mean(np.abs(np.diff(x,axis=0)),axis=(1,2,3));lum=x.mean(axis=(1,2,3))
cuts=[192,384,648,876,1068,1284,1493,1623]
valid=np.ones(len(d),bool)
for c in cuts:valid[max(0,c-3):c+3]=False
valid[:12]=False;valid[1786:]=False
top=[int(i+1) for i in np.argsort(np.where(valid,d,-1))[-24:][::-1]]
out={'source':'render/frames-v11','metric':'mean absolute frame difference at 180x320; candidate detection only','top':[(f,float(d[f-1]),float(lum[f]-lum[f-1])) for f in top],'batch_boundaries':[(f,float(d[f-1])) for f in range(96,1824,96)],'cuts':cuts}
(QA/'flicker-diagnosis-v11.json').write_text(json.dumps(out,indent=2),encoding='utf8')
np.savez_compressed(QA/'v11-temporal-metrics.npz',difference=d,luminance=lum)
frames=sorted(set(f+k for f in top[:5] for k in [-1,0,1]))
sheet=Image.new('RGB',(180*5,344*((len(frames)+4)//5)),'#222222');dr=ImageDraw.Draw(sheet)
for j,f in enumerate(frames):
    sheet.paste(Image.fromarray(x[f].astype(np.uint8)),((j%5)*180,(j//5)*344+24));dr.text(((j%5)*180+4,(j//5)*344+4),str(f),fill='white')
sheet.save(QA/'flicker-candidates-v11.jpg',quality=92)
print(json.dumps(out),flush=True)
