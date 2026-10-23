/* Native 40-second performance. Absolute time persists across all 35 art eras. */
(()=>{
const clamp=x=>Math.max(0,Math.min(1,x)),e=x=>(x=clamp(x),x*x*x*(x*(x*6-15)+10));
const s=(t,a,b)=>e((t-a)/(b-a)),p=(t,a,b,c,d)=>s(t,a,b)*(1-s(t,c,d));
const mix=(a,b,x)=>a+(b-a)*x;
const times=[0,1.1,2.2,3.3,4.4,5.5,6.7,7.9,9.1,10.3,11.5,12.66,13.83,15,16.16,17.33,18.5,19.6,20.7,21.8,22.9,24,25.14,26.28,27.42,28.56,29.7,30.84,32,33.16,34.33,35.5,36.625,37.75,38.875,40];
ERAS.forEach((era,i)=>{era.t0=times[i];era.t1=times[i+1]});
const shots=[
 {id:'discover',start:0,end:5.5,action:'妈妈指认墙上与庭院纹样，宝宝抬头回应',reads:'先看壁画/纹样，再看妈妈的展示手势，再看宝宝抬头'},
 {id:'story',start:5.5,end:11.5,action:'影偶与图册、窗前竹叶引起两人的注意',reads:'幕前影偶→妈妈展示图册→宝宝探头→窗前竹叶'},
 {id:'garden',start:11.5,end:18.5,action:'妈妈喝一次咖啡，宝宝追看花间蝴蝶后抱起奶瓶',reads:'蝴蝶从花丛飞出→宝宝回应→妈妈举杯饮用'},
 {id:'play',start:18.5,end:24,action:'宝宝喝完奶放下；几何玩具滚近，宝宝轻推',reads:'奶瓶回到地面→手释放→几何玩具响应'},
 {id:'paper',start:24,end:32,action:'两人看漂浮物，妈妈展示纸花，宝宝伸手回应',reads:'梦境漂浮→桌上纸花→妈妈抬起展示→宝宝伸手'},
 {id:'follow',start:32,end:35.5,action:'宝宝追看像素蝴蝶，妈妈向花叶方向示意',reads:'墙上花朵与飞蝶→宝宝视线和手势跟随'},
 {id:'together',start:35.5,end:40,action:'妈妈轻挥手，宝宝回应，最后相视停留',reads:'挥手回应→缓慢落手→相视收尾'}
];
window.ACTION_V8={seconds:40,times,shots,e,s,p,pose(local,t){
 const discover=p(t,.25,1.2,4.5,5.5),story=p(t,5.6,6.5,9.85,10.5),ink=p(t,10.25,10.8,11.4,12.1);
 const lift=p(t,13.2,14.55,16.05,17.35),reach=p(t,12.05,12.95,17.7,18.5),grip=p(t,12.95,13.15,17.4,17.65);
 const toy=p(t,21.7,22.3,23.6,24.3),flower=p(t,26.9,27.7,31.45,32),follow=p(t,32,32.6,35.2,35.7),wave=p(t,36.2,36.8,38.4,39.1);
 const babyLift=p(t,15.3,16.8,19,20.5),babyHold=p(t,14.4,15.1,20.7,21.2);
 const babyWave=p(t,1.4,2.3,3.7,4.6)*.8+p(t,6.4,7.15,9.1,9.8)*.55+p(t,11.6,12.45,13.5,14.3)*.9+p(t,22.4,22.9,23.4,24)*.4+p(t,28.8,29.6,31.0,31.7)*.85+p(t,32.3,33,34.7,35.4)*.9+p(t,36.8,37.4,38.4,39.1)*.65;
 const storyY=1302-42*p(t,6.7,7.3,9.0,9.65);
 const flowerLift=p(t,27.8,28.7,30.35,31.25),flowerTarget=[705-4*flowerLift,1330-126*flowerLift];
 const gestures=[[discover,[690,1190]],[story,[713,storyY]],[ink,[701,1200]],[toy,[705,1286]],[flower,flowerTarget],[follow,[690,1190]],[wave,[695+5*Math.sin((t-36.8)*4)*wave,1175]]];
 const total=gestures.reduce((sum,g)=>sum+g[0],0),gesture=Math.min(1,total);
 const target=total>1e-9?[0,1].map(axis=>gestures.reduce((sum,g)=>sum+g[0]*g[1][axis],0)/total):[705,1192];
 const nod=p(t,7,7.6,8.6,9.4)+p(t,22.7,23,23.7,24)+p(t,38,38.7,39.8,40.2);
 return {
 mother:{stage:lift>.999?'drink':reach>0?'coffee':gesture>.01?'interact':'rest',lift,reach,grip,
 tilt:.18*p(t,14.55,14.95,15.6,16.05),gesture,target,
 hand_angle:(-.28*discover-.12*story-.5*flower-.8*follow-.7*wave),
 torso_angle:-.012*gesture-.016*reach-.014*nod,torso_y:.6*Math.sin(t*1.7),
 head_angle:-.023*discover+.025*story+.018*lift+.025*nod-.025*follow,
 head_y:0,active:gesture>.01||reach>.01},
 baby:{stage:babyLift>.999?'drink':babyHold>.01?'bottle':babyWave>.01?'respond':'rest',lift:babyLift,hold:babyHold,gesture:babyWave,
 tilt:-1.72*p(t,15.5,16.8,18.9,20.3),
 target:[420+9*Math.sin(t*.9),1344+8*Math.sin(t*.8)],
 torso_angle:-.017*babyLift+.024*babyWave,torso_y:-1.5*babyLift+.5*Math.sin(t*1.8+.4),
 head_angle:-.035*babyWave-.025*babyLift+.014*nod,head_y:0,active:babyHold>.01||babyWave>.01},
 local:t,settled:gesture<.01&&reach<.01&&babyWave<.01&&babyHold<.01,story,flower,toy,follow,
 book:p(t,6.65,7.1,9.5,10.05),paper:p(t,27.4,28.1,30.6,31.5),
 shot:shots.find(x=>t>=x.start&&t<x.end)?.id||'together'
 };
}};
})();
