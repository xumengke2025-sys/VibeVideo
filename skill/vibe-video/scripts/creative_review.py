"""Prepare real video evidence and check agent-written creative review coverage.
Does not inspect images or certify quality. Reuses shot_contract/video_evidence/frame_audit.
"""
import argparse, hashlib, json, math, subprocess, sys
from pathlib import Path
from shot_contract import validate, check_review, number

HERE=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,value):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
def digest(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def run(script,args):
    r=subprocess.run([sys.executable,'-X','utf8',str(HERE/script),*map(str,args)],capture_output=True,text=True,encoding='utf-8',timeout=240)
    if r.returncode:raise ValueError(f'{script}: {r.stderr[-1800:]} {r.stdout[-1800:]}')
def weights(audio):
    w={'idea':25,'reveal':20,'motion':20,'camera':10,'composition':10,'correctness':10}
    if audio:w['audio']=5
    return {k:v*100/sum(w.values()) for k,v in w.items()}
def merge_windows(windows):
    merged=[]
    for w in sorted(windows,key=lambda x:x['start_frame']):
        if merged and w['start_frame']<=merged[-1]['end_frame']+1:
            merged[-1]['end_frame']=max(merged[-1]['end_frame'],w['end_frame'])
            merged[-1]['reason']+='; '+w['reason']
        else:merged.append(dict(w))
    return merged
def prepare(a,p,schedule):
    out=a.out.resolve();out.mkdir(parents=True,exist_ok=True)
    if (out/'review.json').exists():raise ValueError('review.json exists; use a new output directory to preserve observations')
    times=sorted(set([0,(math.ceil(p['duration']*p['fps'])-1)/p['fps'],*[r['time'] for r in schedule['representatives']]]))
    binaries=[]
    for key in ('ffmpeg','ffprobe'):
        if getattr(a,key):binaries += ['--'+key,getattr(a,key)]
    run('video_evidence.py',[a.video,'--out',out/'media','--duration',p['duration'],'--fps',p['fps'],'--size',f"{p.get('width',1080)}x{p.get('height',1920)}",'--times',','.join(map(str,times)),*(['--require-audio'] if a.audio else []),*binaries])
    media=read(out/'media/media-evidence.json')
    observations=[{**r,'evidence':str(Path('media')/Path(media['keyframes'][times.index(r['time'])]).name), 'note':''} for r in schedule['representatives']]
    windows=[]
    for i,w in enumerate(merge_windows(schedule['continuous_windows'])):
        folder=out/f'window-{i:02d}'
        end=min(w['end_frame'],round(p['duration']*p['fps'])-1)
        run('frame_audit.py',[a.video,'--out',folder,'--start-frame',w['start_frame'],'--end-frame',end,'--width',a.width,*binaries])
        report=read(folder/'frame-audit.json')
        windows.append({**w,'end_frame':end,'report':f'window-{i:02d}/frame-audit.json','required_pages':[f'window-{i:02d}/{s}' for s in report['atlases']], 'viewed_pages':[], 'method':'','note':''})
    review={'video_sha256':digest(a.video),'status':'pending','type':a.type,'weight_reason':'无音频按95归一化；可按题材调整并说明。' if not a.audio else '基础权重；按题材调整并说明。',
            'observations':observations,'continuous':windows,
            'dimensions':[{'dimension':k,'weight':v,'start':None,'end':None,'evidence':'','finding':''} for k,v in weights(a.audio).items()],
            'issues':[],'refinements':[],'limits':[],'scope':'Extraction is not observation. Fill only after viewing; consistency checks do not prove aesthetics.'}
    write(out/'schedule.json',schedule);write(out/'review.json',review)
    print(json.dumps({'review':str(out/'review.json'),'windows':len(windows),'status':'pending'},ensure_ascii=False))

def check(p,schedule,review,video,base):
    errors,h=check_review(p,review,video,base)
    def file(value):return isinstance(value,str) and bool(value) and (base/value).is_file()
    if review.get('status')!='observed':errors.append('review is pending (must be based on actual observation)')
    if not review.get('type') or not review.get('weight_reason'):errors.append('missing type/weight reasoning')
    for expected in schedule['continuous_windows']:
        end=min(expected['end_frame'],round(p['duration']*p['fps'])-1)
        found=[r for r in review.get('continuous',[]) if r.get('start_frame',math.inf)<=expected['start_frame'] and r.get('end_frame',-1)>=end]
        valid=False
        for r in found:
            if not file(r.get('report')) or not r.get('method') or not r.get('note'):continue
            audit=read(base/r['report']);pages=[(Path(r['report']).parent/n).as_posix() for n in audit['atlases']]
            if audit['video_sha256']!=h:continue
            if audit['window_inclusive'][0]>expected['start_frame'] or audit['window_inclusive'][1]<end:continue
            viewed={Path(v).as_posix() for v in r.get('viewed_pages',[]) if isinstance(v,str)}
            if not set(pages)<=viewed or not all(file(v) for v in pages):continue
            valid=True
        if not valid:errors.append(f"unobserved/mismatched continuous window {expected['start_frame']}:{end}")
    dims=review.get('dimensions',[])
    if not dims or not all(number(d.get('weight')) and d['weight']>0 for d in dims) or abs(sum(d.get('weight',0) for d in dims)-100)>1e-5:errors.append('dimension weights must sum to 100')
    if len({d.get('dimension') for d in dims})!=len(dims):errors.append('duplicate dimension')
    if not {'motion','composition','correctness'}<={d.get('dimension') for d in dims}:errors.append('motion/composition/correctness evidence is required (weights may vary by type)')
    for d in dims:
        if not d.get('finding') or not file(d.get('evidence')) or not all(number(d.get(k)) for k in ('start','end')) or not 0<=d['start']<=d['end']<=p['duration']:errors.append('missing timed dimension evidence: '+str(d.get('dimension')))
    rounds=review.get('refinements',[])
    if len(rounds)>2:errors.append('more than two major creative refinements')
    for r in rounds:
        if not r.get('outcome') or not file(r.get('before')) or not file(r.get('after')) or not r.get('issues') or len(r['issues'])>3:errors.append('refinement needs top 1–3 issues and before/after evidence')
        for issue in r.get('issues',[]):
            if issue.get('category') not in ('creative','camera','motion','render') or not issue.get('fix') or not issue.get('visible_issue') or not number(issue.get('start')) or not number(issue.get('end')) or not 0<=issue['start']<=issue['end']<=p['duration']:errors.append('invalid refinement issue')
    return {'ok':not errors,'video_sha256':h,'errors':errors,'scope':'Evidence consistency only; actual observation and quality remain the reviewer responsibility.'}

def main():
    ap=argparse.ArgumentParser(description=__doc__);sp=ap.add_subparsers(dest='command',required=True)
    prep=sp.add_parser('prepare');ch=sp.add_parser('check')
    for parser in (prep,ch):parser.add_argument('plan',type=Path);parser.add_argument('video',type=Path)
    prep.add_argument('--out',type=Path,required=True);prep.add_argument('--width',type=int,default=720);prep.add_argument('--type',default='general');prep.add_argument('--audio',action='store_true');prep.add_argument('--ffmpeg');prep.add_argument('--ffprobe')
    ch.add_argument('--review',type=Path,required=True);ch.add_argument('--out',type=Path)
    a=ap.parse_args();p=read(a.plan);errors,schedule=validate(p)
    if errors:raise ValueError('; '.join(errors))
    # Check main actions as well as cuts, even when only transitions have risks.
    last=round(p['duration']*p['fps'])-1
    for s in p['shots']:
        action=round(s['states']['action']*p['fps'])
        if not any(w['start_frame']<=action<=w['end_frame'] for w in schedule['continuous_windows']):
            schedule['continuous_windows'].append({'shot':s['id'],'reason':'action fallback','start_frame':max(0,math.floor((s['states']['action']-.35)*p['fps'])),'end_frame':min(last,math.ceil((s['states']['action']+.35)*p['fps']))})
    if a.command=='prepare':prepare(a,p,schedule);return 0
    result=check(p,schedule,read(a.review),a.video,a.review.parent)
    if a.out:write(a.out,result)
    print(json.dumps(result,ensure_ascii=False));return 0 if result['ok'] else 2
if __name__=='__main__':
    try:raise SystemExit(main())
    except (OSError,ValueError,TypeError,KeyError,subprocess.TimeoutExpired) as e:print(str(e),file=sys.stderr);raise SystemExit(2)
