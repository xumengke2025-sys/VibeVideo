import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url));
const write=(name,value)=>fs.writeFileSync(path.join(root,name),JSON.stringify(value,null,2));
const seq=(family,items)=>items.map(([index,hold,support='both'])=>({pose:`${family}.${index}`,holdTicks:hold,support}));
const actions={
  rest:seq('heron_neck',[[0,12],[1,8],[0,4]]),
  look:seq('heron_neck',[[1,8],[2,4],[1,12]]),
  walk:seq('heron_walk',[[0,2,'front'],[1,1,'front'],[2,2,'front'],[3,2,'back'],[4,1,'back'],[5,2,'back']]),
  disguise_enter:[...seq('heron_neck',[[1,6],[0,6]]),...seq('heron_disguise',[[0,12]])],
  disguise_walk:seq('heron_disguise',[[0,3],[1,2,'left'],[2,3],[3,2,'right'],[0,2]]),
  disguise_hold:seq('heron_disguise',[[0,12]]),
  grab:[...seq('heron_neck',[[1,4],[2,3],[3,3]]),...seq('heron_contact',[[0,3],[1,3],[2,4]]),...seq('heron_neck',[[3,3],[2,3],[1,10]])],
  caught:seq('heron_neck',[[1,12],[2,4],[1,8]]),
  feed:[...seq('heron_neck',[[1,4],[2,4]]),...seq('heron_contact',[[3,4],[1,4],[2,4],[1,4]]),...seq('heron_neck',[[2,4],[1,8]])],
  settle:seq('heron_neck',[[1,12],[0,12]]),
  penguin_idle:seq('penguin_react',[[0,12]]),
  penguin_react:seq('penguin_react',[[0,4],[1,4],[2,10],[3,6],[2,8],[1,4],[0,12]]),
  chick_beg:seq('chick',[[0,4],[1,4],[2,8],[1,4],[0,4]]),
  chick_feed:seq('chick',[[0,4],[1,4],[2,12],[3,8],[0,8]]),
  chick_settle:seq('chick',[[3,8],[0,16]])
};
const shots=[
 {id:'S01',start:0,end:60,title:'晨光里出门',stage:'willow',heron:[[0,24,'rest'],[24,36,'look'],[36,60,'walk']],x:[260,680],scale:0.60},
 {id:'S02',start:60,end:120,title:'沿步道来到动物园',stage:'zoo_gate',heron:[[0,60,'walk']],x:[160,700],scale:0.62},
 {id:'S03',start:120,end:180,title:'看到企鹅和鱼桶',stage:'penguin_pool',heron:[[0,60,'look']],x:[240,240],scale:0.55},
 {id:'S04',start:180,end:252,title:'缩颈并脚学企鹅',stage:'penguin_pool',heron:[[0,24,'disguise_enter'],[24,72,'disguise_walk']],x:[240,450],scale:0.55},
 {id:'S05',start:252,end:324,title:'跟在队尾挪到桶旁',stage:'bucket_close',heron:[[0,48,'disguise_walk'],[48,72,'disguise_hold']],x:[220,440],scale:0.60},
 {id:'S06',start:324,end:384,title:'伸颈探桶合嘴抢鱼',stage:'bucket_contact',heron:[[0,36,'grab'],[36,60,'caught']],x:[360,360],scale:0.62},
 {id:'S07',start:384,end:432,title:'企鹅回头长嘴露馅',stage:'penguin_pool',heron:[[0,48,'caught']],x:[430,430],scale:0.57},
 {id:'S08',start:432,end:492,title:'叼鱼快步回家',stage:'return_path',heron:[[0,60,'walk']],x:[180,860],scale:0.60},
 {id:'S09',start:492,end:552,title:'低头把鱼交入巢中',stage:'nest_close',heron:[[0,12,'look'],[12,48,'feed'],[48,60,'settle']],x:[280,280],scale:0.62},
 {id:'S10',start:552,end:600,title:'幼鸟围食一家安定',stage:'nest_wide',heron:[[0,48,'settle']],x:[270,270],scale:0.52}
];
function sample(action,tick,loop=true){
 const frames=actions[action];const length=frames.reduce((a,f)=>a+f.holdTicks,0);
 let q=loop?tick%length:Math.min(tick,length-1);
 for(let i=0;i<frames.length;i++){const f=frames[i];if(q<f.holdTicks)return {...f,keyIndex:i,keyTick:q};q-=f.holdTicks;}
 throw Error('unreachable');
}
const frames=[];
for(let tick=0;tick<600;tick++){
 const s=shots.find(s=>tick>=s.start&&tick<s.end),local=tick-s.start;
 const b=s.heron.find(([a,z])=>local>=a&&local<z),a=sample(b[2],local-b[0]);
 const motion=b[2]==='walk'||b[2]==='disguise_walk';
 let progress=local/(s.end-s.start-1);
 if(s.id==='S01')progress=Math.max(0,(local-36)/23);
 if(s.id==='S04')progress=Math.max(0,(local-24)/47);
 if(s.id==='S05')progress=Math.min(1,local/47);
 const hero={id:'heron',action:b[2],pose:a.pose,root:[Math.round(s.x[0]+(s.x[1]-s.x[0])*progress),s.stage.startsWith('nest')?1260:1430],torsoScale:s.scale,support:a.support,registrationRequired:true,rootPathIsLayoutGuide:true,footLock:motion?'solve_root_from_registered_support_foot':'both_feet_fixed',rotationDeg:0};
 const actors=[hero];
 if(tick>=120&&tick<432){
   const ps=tick>=384?sample('penguin_react',tick-384,false):sample('penguin_idle',tick);
   actors.push({id:'penguin_1',pose:ps.pose,root:[700,1420],torsoScale:0.46,footLock:'both_feet_fixed'});
   actors.push({id:'penguin_2',pose:tick>=392?sample('penguin_react',tick-392,false).pose:'penguin_react.0',root:[850,1375],torsoScale:0.40,footLock:'both_feet_fixed'});
 }
 if(tick>=492){
   for(let i=0;i<2;i++){
     const delayed=tick-i*3;
     const pose=delayed<504?'chick.0':delayed<512?'chick.1':delayed<528?'chick.2':delayed<540?'chick.3':'chick.0';
     actors.push({id:`chick_${i+1}`,pose,root:[660+i*145,1370-i*18],torsoScale:0.25,footLock:'nest_anchor',phaseOffsetTicks:i*3});
   }
 }
 let fish={id:'hero_fish',pose:'fish.0',visible:tick>=120&&tick<530,owner:tick<340?'bucket':tick<524?'heron.beak':'nest',rotationDeg:tick<340?-12:tick<524?-65:-18,contactRequired:tick===340||tick===524,occlusion:tick<340?'bucket_front':tick<524?'beak_grip':'nest_front'};
 if(tick>=528)fish.occlusion='fully_behind_nest_front';
 frames.push({poseTick:tick,time:tick/12,outputFrames:[tick*2,tick*2+1],shot:s.id,stage:s.stage,actors,fish,cut:tick===s.start,camera:'locked_within_shot',interpolation:'none_between_character_poses'});
}
const outputFrames=frames.flatMap(f=>f.outputFrames.map(frame=>({frame,time:frame/24,poseTick:f.poseTick,shot:f.shot,actors:f.actors,fish:f.fish})));
write('action-library.json',{poseFps:12,outputFps:24,holdUnit:'one pose tick = 2 output frames',actions});
write('shot-plan.json',{size:[1080,1920],duration:50,poseFps:12,outputFps:24,shots});
write('pose-timeline.json',frames);
write('frame-plan-1200.json',outputFrames);
const manifest=JSON.parse(fs.readFileSync(path.join(root,'asset-manifest.json'),'utf8'));
const known=new Set(manifest.assets.flatMap(a=>a.poses.map(p=>p.id)));
for(const f of frames){for(const a of [...f.actors,f.fish])if(!known.has(a.pose))throw Error(`Unknown pose ${a.pose}`);}
if(frames.length!==600||outputFrames.length!==1200||outputFrames.at(-1).frame!==1199)throw Error('timeline length');
if(frames[339].fish.owner!=='bucket'||frames[340].fish.owner!=='heron.beak'||frames[523].fish.owner!=='heron.beak'||frames[524].fish.owner!=='nest')throw Error('fish ownership');
write('plan-validation.json',{passed:true,poseTicks:600,outputFrames:1200,allPoseReferencesExist:true,fishPickupPoseTick:340,fishDeliveryPoseTick:524,scope:'Structure only. No video render, foot lock solve, contact geometry or motion quality has been verified.'});
console.log('Wrote 600 pose ticks / 1200 output-frame records; all pose references resolve. No animation render performed.');
