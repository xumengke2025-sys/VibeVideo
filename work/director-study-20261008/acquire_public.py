"""Read anonymous public Bilibili metadata and its advertised low-res stream.
No cookies, login, premium formats, token forging or access-control bypass.
"""
import urllib.request, json, sys, datetime, pathlib, hashlib
ROOT=pathlib.Path(__file__).parent/'references'
HEADERS={'User-Agent':'Mozilla/5.0','Referer':'https://www.bilibili.com/'}
def get(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers=HEADERS),timeout=35) as r:
        return r.read()
for bvid in sys.argv[1:]:
    try:
        dest=ROOT/bvid;dest.mkdir(parents=True,exist_ok=True)
        meta=json.loads(get('https://api.bilibili.com/x/web-interface/view?bvid='+bvid))
        if meta.get('code')!=0: raise RuntimeError('metadata code '+str(meta.get('code')))
        data=meta['data'];(dest/'metadata.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
        published=datetime.datetime.fromtimestamp(data['pubdate'],datetime.timezone(datetime.timedelta(hours=8))).isoformat()
        print(bvid,data['owner']['name'],published,data['duration'],data['title'],flush=True)
        p=json.loads(get(f'https://api.bilibili.com/x/player/playurl?bvid={bvid}&cid={data["cid"]}&qn=16&fnval=1&fnver=0&fourk=0'))
        if p.get('code')!=0 or not p.get('data',{}).get('durl'): raise RuntimeError('anonymous stream unavailable: '+str(p.get('code')))
        stream=p['data']['durl'][0]['url'];target=dest/'reference.mp4'
        if not target.exists():
            with urllib.request.urlopen(urllib.request.Request(stream,headers=HEADERS),timeout=45) as r, target.open('wb') as out:
                while block:=r.read(1024*1024):out.write(block)
        ledger={'bvid':bvid,'author':data['owner']['name'],'published_shanghai':published,'duration_claimed':data['duration'],'acquisition':'anonymous public qn16 advertised stream','quality':p['data'].get('quality'),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'source_url':'https://www.bilibili.com/video/'+bvid+'/','rights':'study only; no redistribution in original film','file':str(target)}
        (dest/'acquisition.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2),encoding='utf-8')
        print('SAVED',target.stat().st_size,flush=True)
    except Exception as e: print('UNAVAILABLE',bvid,type(e).__name__,str(e),flush=True)
