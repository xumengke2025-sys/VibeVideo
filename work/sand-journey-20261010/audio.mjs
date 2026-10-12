// Original deterministic stereo sound design: no upstream song or audio samples.
import fs from 'node:fs';import {SETTINGS,EVENTS,ease} from './js/timeline.js';
const SR=48000,N=SR*SETTINGS.duration,L=new Float32Array(N),R=new Float32Array(N);let seed=SETTINGS.seed;
const rnd=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296*2-1};
const gauss=(t,c,w)=>Math.exp(-.5*((t-c)/w)**2);
let lowL=0,lowR=0,midL=0,midR=0,airL=0,airR=0;
for(let i=0;i<N;i++){const t=i/SR,a=rnd(),b=rnd();lowL+=.0035*(a-lowL);lowR+=.0035*(b-lowR);midL+=.080*(a-midL);midR+=.070*(b-midR);airL+=.022*(a-airL);airR+=.025*(b-airR);
 const gust=.025+.10*gauss(t,3.3,1.3)+.05*gauss(t,6.5,2)+.055*gauss(t,14.9,1.1);
 const near=ease((t-7.7)/5.5)*(1-.52*ease((t-18.2)/1.5));
 const swells=.022*gauss(t,2.5,1.8)+.045*gauss(t,8.7,1.8)+(.055+.115*near)*gauss(t,14.1,1.6)+.07*gauss(t,18.0,1.2);
 const hiss=.14*gauss(t,15.35,.22)+.07*gauss(t,5.8,.4)+.05*gauss(t,8.3,.45);
 const windMod=1+.18*Math.sin(t*2.3)+.11*Math.sin(t*4.17);
 const tail=(1-ease((t-19.15)/.85))*ease(t/.12);
 L[i]=tail*((lowL*5.2+airL*1.1)*gust*windMod+(lowL*3.0+midL*1.5)*swells+(a-midL)*hiss*.23);
 R[i]=tail*((lowR*5.2+airR*1.1)*gust*windMod+(lowR*3.0+midR*1.5)*swells+(b-midR)*hiss*.23);
}
// Sparse gritty contacts; impacts at the same story contact time, with a brief rolling tail.
function grainHit(t,amp,len,freq,pan){const start=Math.round(t*SR);let lo=0;for(let j=0;j<len*SR&&start+j<N;j++){const q=j/SR,w=rnd();lo+=.25*(w-lo);const env=Math.exp(-q*85)*(1-Math.exp(-q*2300));const v=amp*env*((w-lo)*.7+Math.sin(q*freq*6.283)*.3);L[start+j]+=v*(1-pan)*.5;R[start+j]+=v*(1+pan)*.5}}
for(let j=0;j<20;j++)grainHit(1.48+j*.053,.023+(j/20)*.028,.055,1600+j*170,-.2+j*.025);
grainHit(SETTINGS.contact,.32,.14,2670,-.12);for(let j=0;j<10;j++)grainHit(SETTINGS.contact+.018+j*.025,.10*Math.exp(-j*.33),.045,3900+j*140,-.12+j*.018);
let peak=0,sum=0;for(let i=0;i<N;i++){peak=Math.max(peak,Math.abs(L[i]),Math.abs(R[i]));sum+=L[i]*L[i]+R[i]*R[i]}const gain=.82/peak;
const wav=Buffer.alloc(44+N*4);wav.write('RIFF',0);wav.writeUInt32LE(36+N*4,4);wav.write('WAVEfmt ',8);wav.writeUInt32LE(16,16);wav.writeUInt16LE(1,20);wav.writeUInt16LE(2,22);wav.writeUInt32LE(SR,24);wav.writeUInt32LE(SR*4,28);wav.writeUInt16LE(4,32);wav.writeUInt16LE(16,34);wav.write('data',36);wav.writeUInt32LE(N*4,40);for(let i=0;i<N;i++){wav.writeInt16LE(Math.round(Math.max(-1,Math.min(1,L[i]*gain))*32767),44+i*4);wav.writeInt16LE(Math.round(Math.max(-1,Math.min(1,R[i]*gain))*32767),46+i*4)}fs.mkdirSync('audio',{recursive:true});fs.writeFileSync('audio/sand-journey.wav',wav);fs.writeFileSync('audio/sound-events.json',JSON.stringify({sampleRate:SR,duration:20,channels:2,original:true,source:'deterministic multiband stochastic synthesis and granular foley',events:EVENTS,peak:.82,rms:Math.sqrt(sum/(N*2))*gain},null,2));console.log('Audio generated: 20 s stereo 48 kHz; contact at '+SETTINGS.contact+' s');
