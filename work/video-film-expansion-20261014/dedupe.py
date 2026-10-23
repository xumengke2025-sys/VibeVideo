import json,pathlib,sys,statistics,re
from PIL import Image
work=pathlib.Path(__file__).resolve().parent
report=json.loads((work/'media-verification.json').read_text(encoding='utf-8'));before=json.loads((work/'before/catalog.json').read_text(encoding='utf-8'))
root=work.parent.parent;manifest=json.loads((root/'reference-sources/video-films-20261014/manifest.json').read_text(encoding='utf-8'))
def dhash(p):
    with Image.open(p) as im:
        im=im.convert('L').resize((17,16),Image.Resampling.LANCZOS);a=list(im.get_flattened_data());bits=0
        for y in range(16):
            for x in range(16):bits=(bits<<1)|(a[y*17+x]>a[y*17+x+1])
        return bits
items=[x for x in report['items'] if not x.get('error')]
for x in items:x['hashes']=[dhash(p) for p in x['fingerprintFrames']]
old={x['id']:x for x in before['media']};old.update({x['id']:x for x in json.loads((work/'additional-baseline.json').read_text(encoding='utf-8'))});new={x['id']:x for x in manifest['media']};pairs=[]
if '--progress' in sys.argv:
    for p in (root/'reference-sources/video-films-20261014/records').glob('*.json'):
        x=json.loads(p.read_text(encoding='utf-8'));new[x['id']]=x
for i,a in enumerate(items):
    for b in items[:i]:
        if a['id'] not in new and b['id'] not in new:continue
        da=a['metadata']['duration'];db=b['metadata']['duration']
        if abs(da-db)>max(.6,min(da,db)*.015):continue
        distances=[(h1^h2).bit_count() for h1,h2 in zip(a['hashes'],b['hashes'])]
        if max(distances)>32 or statistics.mean(distances)>18:continue
        left=new.get(a['id'],old.get(a['id'],{}));right=new.get(b['id'],old.get(b['id'],{}))
        pairs.append({'a':a['id'],'b':b['id'],'aTitle':left.get('title'),'bTitle':right.get('title'),'durationA':da,'durationB':db,'distances256bit':distances,'meanDistance':statistics.mean(distances),'exactBytes':a['sha256']==b['sha256'],'requiresManualDecision':a['sha256']!=b['sha256']})
post_groups={}
for x in [*old.values(),*new.values()]:
    url=x.get('authorUrl') or '';post=re.search(r'/status/(\d+)',url)
    if post:post_groups.setdefault(post.group(1),[]).append(x['id'])
post_pairs=[{'statusId':k,'ids':list(dict.fromkeys(v))} for k,v in post_groups.items() if len(set(v))>1 and any(i in new for i in v)]
index=json.loads((work/'discovery/Li-Evan--awesome-opus-5.5-video-prompts/site/data.json').read_text(encoding='utf-8'))
existing_posts={}
for x in old.values():
    match=re.search(r'/status/(\d+)',x.get('authorUrl') or '')
    if match:existing_posts.setdefault(match.group(1),[]).append(x['id'])
overlap=[]
for x in index['entries']:
    match=re.search(r'/status/(\d+)',x.get('url') or '')
    if match and match.group(1) in existing_posts:overlap.append({'candidateId':x['id'],'statusId':match.group(1),'existingIds':existing_posts[match.group(1)],'downloadedInRound':'original/'+x['id'] in new})
out={'scope':'原帖URL和status ID、SHA256、三处20/50/80%时刻256bit dHash。近似候选须核对；无法证明不同剪辑/重编码/音轨均不重复。','existingMedia':len(old),'roundMedia':len(new),'checkedMedia':len(items),'existingPostMatches':overlap,'postPairs':post_pairs,'potentialPairs':pairs}
(work/'duplicate-report.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({'checked':len(items),'potentialPairs':len(pairs),'pairs':pairs},ensure_ascii=False,indent=2))
