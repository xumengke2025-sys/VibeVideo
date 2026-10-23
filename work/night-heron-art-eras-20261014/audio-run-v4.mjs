import fs from 'node:fs';
const plan=JSON.parse(fs.readFileSync(new URL('production-plan-run-v4.json',import.meta.url))),SR=48000,D=31,N=SR*D,L=new Float64Array(N),R=new Float64Array(N),events=[];
let seed=409;const rand=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296},hz=n=>440*2**((n-69)/12);
function put(t,data,gain,pan=.5){const k=Math.round(t*SR),l=Math.cos(pan*Math.PI/2),r=Math.sin(pan*Math.PI/2);for(let j=0;j<data.length&&j+k<N;j++)if(j+k>=0){L[k+j]+=data[j]*gain*l;R[k+j]+=data[j]*gain*r}}
function pluck(t,midi,dur,gain=.08,pan=.5){const f=hz(midi),n=Math.floor(dur*SR),buf=new Float64Array(n),period=Math.round(SR/f),delay=new Float64Array(period);for(let j=0;j<period;j++)delay[j]=(rand()*2-1)*.6;let prev=0;
 for(let j=0;j<n;j++){const k=j%period,v=delay[k];delay[k]=(v+prev)*.497;prev=v;buf[j]=(v+.08*Math.sin(2*Math.PI*f*j/SR))*Math.exp(-j/SR*4)*Math.min(1,j/100)}put(t,buf,gain,pan);events.push({type:'pizzicato',time:t,midi,dur,gain})}
function tone(t,f,dur,gain,kind='bell',pan=.5){const buf=new Float64Array(Math.floor(dur*SR));for(let j=0;j<buf.length;j++){const x=j/SR,env=Math.min(1,x/.008)*Math.exp(-x*(kind==='gulp'?22:7)),mod=kind==='gulp'?f*(1+1.8*Math.exp(-x*30)):f;buf[j]=(Math.sin(2*Math.PI*mod*x)+.13*Math.sin(2*Math.PI*mod*2.76*x))*env}put(t,buf,gain,pan);events.push({type:kind,time:t,dur,gain})}
function foot(t){const buf=new Float64Array(2200);let low=0;for(let j=0;j<buf.length;j++){low=.78*low+.22*(rand()*2-1);buf[j]=low*Math.exp(-j/430)+.2*Math.sin(j*.031)*Math.exp(-j/240)}put(t,buf,.042,.45);events.push({type:'foot',time:t})}
const roots=[48,48,50,50,53,53,55,55,48,48,50,50,53,53,55,48],motif=[72,76,79,76];
for(let i=0;i<16;i++){const s=plan.timeline.shots[i],t=s.startFrame/24,beat=s.frames/24/4,root=roots[i];pluck(t,root,1.2,.18,.38);pluck(t+beat*2,root+7,.8,.10,.4);
 for(let j=0;j<4;j++){pluck(t+j*beat,motif[j]+root-48,.65,.17,j%2?.61:.39);if(i>8)tone(t+j*beat+beat/2,hz(84+root-48),.11,.009,'wood',.6)}
 tone((s.startFrame+s.events.grab)/24,1350,.10,.028,'fish',.57);tone((s.startFrame+s.events.swallowStart+2)/24,185,.16,.07,'gulp',.52);
 tone((s.startFrame+s.events.fishGone)/24,130,.12,.033,'gulp',.5);
}
for(let dist=70;dist<550*30.3+5*30.3**2;dist+=155){const t=(-550+Math.sqrt(550**2+20*dist))/10;foot(t)}
pluck(.05,60,1,.18,.45);pluck(.3,67,.85,.15,.55);pluck(.56,72,.8,.13,.6);
for(const [i,midi]of[60,64,67,72].entries())tone(30.28+i*.065,hz(midi),.6,.045,'bell',.4+i*.06);
let peak=0,sum=0;for(let i=0;i<N;i++){const fade=Math.min(1,i/(SR*.015),(N-i)/(SR*.24));L[i]*=fade;R[i]*=fade;peak=Math.max(peak,Math.abs(L[i]),Math.abs(R[i]))}
const gain=.78/peak,b=Buffer.alloc(44+N*4);b.write('RIFF');b.writeUInt32LE(b.length-8,4);b.write('WAVEfmt ',8);b.writeUInt32LE(16,16);b.writeUInt16LE(1,20);b.writeUInt16LE(2,22);b.writeUInt32LE(SR,24);b.writeUInt32LE(SR*4,28);b.writeUInt16LE(4,32);b.writeUInt16LE(16,34);b.write('data',36);b.writeUInt32LE(N*4,40);
for(let i=0;i<N;i++){const l=L[i]*gain,r=R[i]*gain;sum+=l*l+r*r;b.writeInt16LE(Math.round(l*32767),44+i*4);b.writeInt16LE(Math.round(r*32767),46+i*4)}
fs.writeFileSync(new URL('audio/score-run-v4.wav',import.meta.url),b);fs.writeFileSync(new URL('audio/events-run-v4.json',import.meta.url),JSON.stringify({duration:D,sampleRate:SR,events,statistics:{peak:.78,rms:Math.sqrt(sum/N/2),clipped:false},attribution:'Original procedural score and Foley; no external recordings',perception:'not listened'},null,2));console.log('31s stereo original score, '+events.length+' events, peak .78');
