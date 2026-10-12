import fs from 'node:fs';import {spawnSync} from 'node:child_process';
import {FILM,SOUNDS,LOOP,P,ejectTime,cartChute} from './js/timeline.js';
const SR=48000,N=Math.round(SR*FILM.duration),L=new Float32Array(N),R=new Float32Array(N);
let seed=FILM.seed;
const rand=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296*2-1};
const pan2=(v,p)=>({l:v*Math.sqrt((1-p)/2),r:v*Math.sqrt((1+p)/2)});
const put=(i,l,r)=>{if(i>=0&&i<N){L[i]+=l;R[i]+=r}};

// 1) 底层：低频机械噪声 + 滚轮中频 + 每 1.045 秒一次的过车脉冲
{
  let a=0,b=0,c=0,d=0;
  for(let i=0;i<N;i++){
    const t=i/SR;
    a+=.0035*(rand()-a);b+=.0037*(rand()-b);
    c+=.105*(rand()-c);d+=.110*(rand()-d);
    const ph=(t%1.045)/1.045;
    const tick=Math.exp(-ph*24)*.055, tickR=Math.exp(-Math.pow((ph+.5)%1,2)*24)*.05;
    L[i]=a*2.1+c*.52+tick*rand();
    R[i]=b*2.1+d*.52+tickR*rand();
  }
}
// 2) 低频持续音（缓慢起伏，制造"机器在运转"的底）
{
  for(let i=0;i<N;i++){
    const t=i/SR;
    const v=(Math.sin(2*Math.PI*55*t)*.030+Math.sin(2*Math.PI*82.5*t+1.1)*.015+Math.sin(2*Math.PI*110*t+2.2)*.009);
    const sw=.55+.45*Math.sin(2*Math.PI*t/11-1.2);
    put(i,v*sw,v*sw*.97);
  }
}
function tone(t0,dur,f0,f1,amp,pan,decay=4.5){
  const s0=Math.round(t0*SR),n=Math.round(dur*SR);let ph=0;
  for(let j=0;j<n;j++){
    const u=j/n,f=f0+(f1-f0)*u,env=(1-Math.exp(-u*n/(SR*.004)))*Math.exp(-u*decay);
    ph+=2*Math.PI*f/SR;
    const v=(Math.sin(ph)+.3*Math.sin(2*ph)*Math.exp(-u*6))*.5*env*amp;
    const{l,r}=pan2(v,pan);put(s0+j,l,r);
  }
}
function noiseHit(t0,dur,amp,pan,lpCoef,decay){
  const s0=Math.round(t0*SR),n=Math.round(dur*SR);let st=0;
  for(let j=0;j<n;j++){
    const u=j/n;st+=lpCoef*(rand()-st);
    const env=(1-Math.exp(-u*n/(SR*.002)))*Math.exp(-u*decay);
    const{l,r}=pan2(st*env*amp,pan);put(s0+j,l,r);
  }
}
// 3) 交叉带侧行：电机升速 + 带面摩擦（hero 2.5 秒预转、其余 0.9 秒）
function beltRun(t0,t1,amp,pan){
  const s0=Math.round(t0*SR),s1=Math.round(t1*SR);let ph=0,st=0;
  for(let i=s0;i<s1&&i<N;i++){
    const u=(i-s0)/(s1-s0);
    const env=Math.min(1,u*5)*(1-Math.max(0,(u-.86)/.14));
    ph+=2*Math.PI*(128+96*u)/SR;st+=.30*(rand()-st);
    const v=(Math.sin(ph)*.42+st*.85)*env*amp;
    const{l,r}=pan2(v,pan);put(i,l,r);
  }
}
// 4) 抛出：脱离带面的短促气流 + 落槽撞击
function throwOut(t0,amp,pan){
  noiseHit(t0,.20,amp*.55,pan,.55,7);tone(t0,.16,420,180,amp*.30,pan,6);
}
function landing(t0,amp,pan){
  noiseHit(t0,.13,amp*.85,pan,.22,11);tone(t0,.22,150,88,amp*.34,pan,5);
}
function slide(t0,amp,pan){
  noiseHit(t0,.55,amp*.42,pan,.42,2.6);
}

// ---- 事件排布 ----
const focusGain=t=>(t<3.5||t>16.5)?1:.30;   // 近景段落压掉远处小车的抛投声
// hero 全程
beltRun(11.30,13.82,.100,-.10);
throwOut(14.21,.150,.58);
landing(14.47,.115,.10);
slide(14.60,.070,.10);
tone(5.30,.34,1180,1620,.055,.62,3.2);       // 扫码提示音
noiseHit(5.30,.10,.055,.62,.75,16);
// 其他小车的抛投与落槽
for(let i=0;i<LOOP.carts;i++){
  if(i===0)continue;
  for(let k=0;k<2;k++){
    const t=ejectTime(i)+k*P;if(t<2.2||t>21.4)continue;
    const u=cartChute(i).side,pan=u*.42;
    const g=focusGain(t)*.72;
    beltRun(t-0.9,t,.030*g,pan);
    throwOut(t+0.41,.062*g,pan);
    landing(t+0.52,.050*g,pan);
  }
}
// 结尾收束
tone(19.9,2.4,110,55,.032,0,1.4);tone(19.9,2.2,164.8,82.4,.018,-.25,1.4);
noiseHit(20.0,1.4,.030,0,.12,1.2);
// 首尾淡入淡出
for(let i=0;i<N;i++){
  const t=i/SR,g=Math.min(1,t/.35)*(1-Math.max(0,(t-(FILM.duration-1.3))/1.3));
  L[i]*=g;R[i]*=g;
}
let peak=0;for(let i=0;i<N;i++)peak=Math.max(peak,Math.abs(L[i]),Math.abs(R[i]));
const wav=Buffer.alloc(44+N*4);wav.write('RIFF');wav.writeUInt32LE(36+N*4,4);wav.write('WAVEfmt ',8);
wav.writeUInt32LE(16,16);wav.writeUInt16LE(1,20);wav.writeUInt16LE(2,22);wav.writeUInt32LE(SR,24);
wav.writeUInt32LE(SR*4,28);wav.writeUInt16LE(4,32);wav.writeUInt16LE(16,34);wav.write('data',36);wav.writeUInt32LE(N*4,40);
for(let i=0;i<N;i++){wav.writeInt16LE(Math.round(Math.max(-1,Math.min(1,L[i]))*32767),44+i*4);wav.writeInt16LE(Math.round(Math.max(-1,Math.min(1,R[i]))*32767),46+i*4)}
fs.mkdirSync('audio',{recursive:true});fs.writeFileSync('audio/raw.wav',wav);
const ff='D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe';
const p=spawnSync(ff,['-hide_banner','-y','-i','audio/raw.wav','-af','loudnorm=I=-14:TP=-1.8:LRA=8:print_format=json','-ar','48000','-c:a','pcm_s16le','audio/mix.wav'],{windowsHide:true,encoding:'utf8'});
fs.writeFileSync('audio/loudness-normalization.log',p.stderr||'');if(p.status)throw Error(p.stderr);
fs.writeFileSync('audio/events.json',JSON.stringify({original:true,description:'原创合成机械底噪、滚轮脉冲、交叉带电机与摩擦、抛出与落槽撞击；无旁白、无外部素材',clip_seconds:FILM.duration,events:SOUNDS,hero:{belt:[11.30,13.82],leave:14.21,land:14.47},rawPeak:peak},null,2));
console.log(FILM.duration+'s stereo original soundtrack complete, raw peak '+peak.toFixed(3));
