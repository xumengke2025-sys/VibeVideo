from pathlib import Path
from PIL import Image
import json, shutil, hashlib
ROOT=Path(__file__).resolve().parent/'studio'
GEN=Path('C:/Users/67236/.codex/generated_images/01a12fda-7b5e-7ff3-913c-c8f79fb2ccc7')
sources={
 'cavalry':'exec-368df4ad-24da-4500-856e-565eee23b853.png',
 'infantry':'exec-ec0979fa-848e-4e7c-a54e-d9c266d912b8.png',
 'hero':'exec-f948891a-dcae-4548-819a-d6136321489a.png',
 'battlefield':'exec-33e39151-08b8-4590-9f66-aef02012d4ab.png',
 'elevated-horse':'exec-300f59b6-2495-4453-aed0-eb76e17888dd.png'}
crops={
 'cavalry':{'horse-body':[0,0,685,426],'horse-front-upper':[687,0,938,423],'horse-front-lower':[976,0,1230,425],'horse-back-upper':[106,425,407,814],'horse-back-lower':[532,427,792,819],'horse-tail':[910,423,1279,826],'rider-body':[45,799,431,1279],'rider-arm':[444,866,913,1279],'rider-leg':[951,824,1279,1279]},
 'infantry':{'guard-body':[0,0,427,428],'british-body':[427,0,852,430],'prussian-body':[853,0,1279,430],'leg-upper':[0,428,427,798],'leg-lower':[428,430,853,797],'guard-arm':[853,430,1279,798],'british-arm':[0,799,427,1279],'musket':[428,799,852,1279],'napoleon':[853,799,1279,1279]},
 'hero':{'eagle':[0,0,635,654],'flag':[637,0,1279,651],'cannon':[0,776,715,1191],'wheel':[711,647,1279,1213]}}
manifest=[]
for name,file in sources.items():
 src=GEN/file;dest=ROOT/'assets'/f'{name}.png';shutil.copy2(src,dest)
 im=Image.open(dest).convert('RGBA')
 manifest.append({'id':name,'kind':'generated_concept_art','tool':'built-in image_gen','original_path':str(src),'file':str(dest),'size':im.size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
 for ident,box in crops.get(name,{}).items():
  c=im.crop(box);bb=c.getchannel('A').getbbox()
  if not bb:raise RuntimeError(ident+' empty')
  c=c.crop(bb);c.save(ROOT/'assets'/f'{ident}.png')
  manifest.append({'id':ident,'kind':'alpha-preserving crop','source':name,'crop':box,'alpha_trim':bb,'size':c.size,'file':f'assets/{ident}.png'})
(ROOT/'assets/manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8')
print('Assets prepared:',len(manifest))
