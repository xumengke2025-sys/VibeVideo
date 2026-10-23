from pathlib import Path
import json, math
import numpy as np
ROOT=Path(__file__).resolve().parent
z=np.load(ROOT/'traffic-v12.npz');data={k:z[k].copy() for k in z.files};s=data['state'];old=s.copy()
ids=np.array([i for i,n in enumerate(data['names']) if str(n).startswith('V12 close citizen')])
fixed_ids=np.array([i for i in range(len(data['names'])) if i not in ids and old[0,i,2]<.5])
p=old[0,ids,:2].astype(float);phase=old[0,ids,6].astype(float);yaw=old[0,ids,3].astype(float)
def walkable(q):
 x,y=q
 return -6<x<6 and -23<y<138 and not (-6.6<x<-2.3 and 47.4<y<52.6) and not (-6.5<x<-3 and -14<y<-10) and not ((x+4.8)**2+(y+12)**2<2.1**2)
minimum=100
for row in range(len(s)):
 t=row/8
 patrol=np.array([[1.35+(i%2)*1.28,24.1-(i//2)*1.6+t*1.05] for i in range(10)])
 fixed=np.concatenate([old[row,fixed_ids,:2],patrol]);radii=np.concatenate([data['radii'][fixed_ids]+.38,np.full(10,.90)])
 desired=old[row,ids,:2];v=(desired-p)*2.5
 length=np.linalg.norm(v,axis=1);v*=np.minimum(1,1.45/np.maximum(.01,length))[:,None];q=p+v/8
 for iteration in range(12):
  for i in range(len(q)):
   off=q[i]-fixed;d=np.linalg.norm(off,axis=1)
   for a,dd,rr in zip(off[d<radii],d[d<radii],radii[d<radii]):
    target=q[i]+a/max(.001,dd)*(rr+.005-dd)
    if walkable(target):q[i]=target
  off=q[:,None]-q[None,:];d=np.linalg.norm(off,axis=2)
  for i,j in zip(*np.where(np.triu(d<.70,1))):
   correction=off[i,j]/max(.001,d[i,j])*(.705-d[i,j])*.5
   if walkable(q[i]+correction):q[i]+=correction
   if walkable(q[j]-correction):q[j]-=correction
 for i in range(len(q)):
  if not walkable(q[i]):q[i]=p[i]
 actual=(q-p)*8;speed=np.linalg.norm(actual,axis=1);moving=speed>.08
 angle=np.arctan2(actual[:,0],-actual[:,1]);yaw+=np.clip((angle-yaw+math.pi)%math.tau-math.pi,-.26,.26)*moving
 phase+=speed/8*4.3;pose=((phase%math.tau)/math.tau*6).astype(int);pose[~moving]=0
 s[row,ids,0:2]=q;s[row,ids,2]=.04+np.sin(phase*2)*.012*moving;s[row,ids,3]=yaw;s[row,ids,4]=pose;s[row,ids,5]=moving;s[row,ids,6]=phase;p=q
 if 16<=t<27:minimum=min(minimum,float(np.linalg.norm(q[:,None]-patrol[None,:],axis=2).min()))
np.savez_compressed(ROOT/'traffic-v13.npz',**data)
e={'modified_actors':len(ids),'patrol_clearance_market_seconds_16_27':minimum,'method':'Retarget existing citizen paths with planted patrol exclusion and neighbour separation; preserve all other actors.'}
(ROOT/'qa/v13/traffic-evidence.json').write_text(json.dumps(e,indent=2),encoding='utf8');print(e)
timeline=json.loads((ROOT/'v13-timeline.json').read_text(encoding='utf8'))
timeline['shots'][3]=[27,36.5,[58,39,61],[56,34,60],[29,68,1],[29,62.5,1],45,45]
(ROOT/'v13-timeline.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2),encoding='utf8')
