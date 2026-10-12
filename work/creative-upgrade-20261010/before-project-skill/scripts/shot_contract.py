"""Validate executable shot plans and emit a review schedule; never score art.
Optional review: {video_sha256, observations:[{shot,state,time,evidence,note}]}.
Only user/agent-written observations count as reviewed. Standard library only.
"""
import argparse, json, hashlib, math, sys
from pathlib import Path
STATES=('establish','action','result')
def number(x): return isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x)
def validate(p):
    errors=[];duration=p.get('duration');fps=p.get('fps',30);shots=p.get('shots',[])
    if not number(duration) or duration<=0:errors.append('duration must be positive');return errors,{}
    if not number(fps) or fps<=0:errors.append('fps must be positive');return errors,{}
    if not shots:errors.append('no shots');return errors,{}
    end=0;ids=set();times=[];windows=[]
    for sh in shots:
        ident=sh.get('id');a=sh.get('start');b=sh.get('end')
        if not ident or ident in ids:errors.append(f'duplicate/missing shot id: {ident}')
        ids.add(ident)
        if not number(a) or not number(b) or not 0<=a<b<=duration:errors.append(f'{ident}: invalid interval');continue
        if abs(a-end)>1e-6:errors.append(f'{ident}: gap/overlap at {a}; expected {end}')
        end=b
        if not sh.get('intent') or not sh.get('action') or not sh.get('camera'):errors.append(f'{ident}: missing intent/action/camera')
        state=sh.get('states',{});ts=[state.get(s) for s in STATES]
        if not all(number(t) and a<=t<b for t in ts) or any(ts[i]>ts[i+1] for i in range(2) if number(ts[i]) and number(ts[i+1])):errors.append(f'{ident}: establish/action/result must be ordered inside shot')
        else:times.extend({'shot':ident,'state':s,'time':t,'frame':round(t*fps)} for s,t in zip(STATES,ts))
        for window in sh.get('risks',[]):
            if len(window)!=2 or not all(number(x) for x in window) or not a<=window[0]<=window[1]<b:errors.append(f'{ident}: invalid risk window')
            else:windows.append({'shot':ident,'reason':'risk','start_frame':math.floor(window[0]*fps),'end_frame':math.ceil(window[1]*fps)})
    if abs(end-duration)>1e-6:errors.append(f'timeline ends at {end}, expected {duration}')
    boundaries=[sh['start'] for sh in shots[1:] if number(sh.get('start'))];connection_times=[]
    for c in p.get('connections',[]):
        t=c.get('time');window=c.get('window')
        if not number(t) or not 0<t<duration or not c.get('kind') or not c.get('anchor'):errors.append('invalid connection intent');continue
        connection_times.append(t)
        if not window or len(window)!=2 or not all(number(x) for x in window) or not 0<=window[0]<=t<=window[1]<duration:errors.append(f'connection {t}: invalid review window')
        else:windows.append({'reason':c['kind'],'anchor':c['anchor'],'start_frame':math.floor(window[0]*fps),'end_frame':math.ceil(window[1]*fps)})
    for t in boundaries:
        if not any(abs(t-c)<1e-6 for c in connection_times):errors.append(f'boundary {t} missing connection')
    return errors,{'duration':duration,'fps':fps,'representatives':times,'continuous_windows':windows}
def check_review(p,review,video,base):
    errors=[];digest=hashlib.file_digest(video.open('rb'),'sha256').hexdigest()
    if review.get('video_sha256','').lower()!=digest:errors.append('review hash does not match video')
    for sh in p['shots']:
        for state in STATES:
            obs=[o for o in review.get('observations',[]) if o.get('shot')==sh['id'] and o.get('state')==state and number(o.get('time')) and sh['start']<=o['time']<sh['end']]
            if not obs:errors.append(f'{sh["id"]}: missing observed {state}')
            for o in obs:
                if not o.get('note') or not o.get('evidence') or not (base/Path(o['evidence'])).is_file():errors.append(f'{sh["id"]}/{state}: missing note or evidence file')
    return errors,digest
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('plan',type=Path);ap.add_argument('--out',type=Path);ap.add_argument('--video',type=Path);ap.add_argument('--review',type=Path);a=ap.parse_args()
    try:
        p=json.loads(a.plan.read_text(encoding='utf-8'));errors,schedule=validate(p)
        if a.review:
            if not a.video:errors.append('--review requires --video')
            elif not errors:
                e,h=check_review(p,json.loads(a.review.read_text(encoding='utf-8')),a.video,a.review.parent);errors+=e;schedule['video_sha256']=h
        schedule['errors']=errors;schedule['scope']='Plan/evidence consistency only; visual and sound judgments require actual observation.'
        if a.out:a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(schedule,ensure_ascii=False,indent=2),encoding='utf-8')
        print(json.dumps({'shots':len(p.get('shots',[])),'representatives':len(schedule.get('representatives',[])),'continuous_windows':len(schedule.get('continuous_windows',[])),'errors':errors},ensure_ascii=False));return 2 if errors else 0
    except (OSError,ValueError,KeyError,TypeError) as e:print('Invalid input:',e,file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
