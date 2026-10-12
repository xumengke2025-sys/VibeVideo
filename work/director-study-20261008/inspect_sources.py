import urllib.request,json,pathlib,datetime
ROOT=pathlib.Path(__file__).parent/'source-snapshots'
def get(url):
    req=urllib.request.Request(url,headers={'User-Agent':'Codex-public-reference-study','Accept':'application/vnd.github+json'})
    with urllib.request.urlopen(req,timeout=40) as r:return json.loads(r.read())
for repo in ['Liamrjohnston/remotion-motion-graphics-skill','Lugia123/ai-video','alchaincyf/huashu-art-motion','mexicat/pdoom-video']:
    try:
        info=get('https://api.github.com/repos/'+repo)
        commit=get('https://api.github.com/repos/'+repo+'/commits/'+info['default_branch'])
        tree=get('https://api.github.com/repos/'+repo+'/git/trees/'+commit['sha']+'?recursive=1')
        dest=ROOT/repo.split('/')[0];dest.mkdir(parents=True,exist_ok=True)
        (dest/'repo.json').write_text(json.dumps({'repo':repo,'metadata':info,'commit':commit,'tree':tree},ensure_ascii=False,indent=2),encoding='utf-8')
        print(repo,commit['sha'],commit['commit']['author']['date'],flush=True)
        selected=[x for x in tree.get('tree',[]) if x['type']=='blob' and (x['path'].endswith(('.mp4','.webm','.html','.tsx','.jsx')) or 'timeline' in x['path'] or 'prompt-thread' in x['path'])]
        for x in selected[:30]:print(' ',x['path'],x.get('size'),flush=True)
    except Exception as e:print('UNAVAILABLE',repo,type(e).__name__,str(e),flush=True)
