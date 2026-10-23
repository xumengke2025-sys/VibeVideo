import fs from 'node:fs';
import path from 'node:path';

const rate = 44100;
const duration = 45;
const count = rate * duration;
const pcm = Buffer.alloc(count * 4);
const notes = [
  [0,7.5,[110,164.81,220]],
  [7.5,12.5,[130.81,164.81,261.63]],
  [12.5,17.5,[146.83,220,293.66]],
  [17.5,22.5,[130.81,196,261.63]],
  [22.5,27.5,[110,164.81,233.08]],
  [27.5,37,[110,164.81,220,329.63]],
  [37,43,[98,146.83,196]],
  [43,45,[110,164.81,220]],
];
const events = [0.15,2.8,3.7,4.35,5.05,5.75,6.5,7.5,9.1,10.6,12.7,14.6,16.2,17.7,19.4,21.2,22.5,24.1,26.0,27.7,29.0,30.5,32.1,34.5,37.0,37.8,38.7,39.6,40.5,41.4,42.3,43.4];
const env = (x, a, d) => x < 0 ? 0 : x < a ? x / a : Math.exp(-(x - a) / d);
const smooth = (x) => {const p = Math.max(0,Math.min(1,x)); return p*p*(3-2*p);};
const noise = (n) => {let x = (n * 1664525 + 1013904223) >>> 0; x ^= x >>> 15; x = Math.imul(x, 2246822519); return ((x >>> 0) / 2147483648) - 1;};
let lowNoise = 0;
for (let i=0;i<count;i++) {
  const t=i/rate;
  const section = notes.find(([a,b])=>t>=a && t<b) ?? notes.at(-1);
  const freqs=section[2];
  const fade = smooth(t/1.6) * (1-smooth((t-44.1)/.9));
  const duck = t>=34 && t<37 ? .45 : 1;
  let sound=0;
  for(let k=0;k<freqs.length;k++) {
    const f=freqs[k];
    const breath=1+.003*Math.sin(2*Math.PI*(.11+.035*k)*t);
    sound+=(Math.sin(2*Math.PI*f*breath*t)+.16*Math.sin(2*Math.PI*f*2*t))/(k+2.1);
  }
  sound*=.055*fade*duck;
  const beat=(t/.72)%1;
  const beatEnv=Math.exp(-beat*13);
  sound+=.026*beatEnv*Math.sin(2*Math.PI*82*t)*fade*(t<37?1:.4);
  for(let e=0;e<events.length;e++) {
    const dt=t-events[e];
    if(dt>=0 && dt<.4) {
      const accent=e===23 || e===24 ? 1.45 : .72;
      const ping=Math.sin(2*Math.PI*(440+120*Math.exp(-dt*15))*dt);
      sound+=.035*accent*env(dt,.003,.075)*ping;
      lowNoise=lowNoise*.95+noise(i+e*991)*.05;
      sound+=.015*accent*env(dt,.001,.06)*lowNoise;
    }
  }
  if(t>=37 && t<43.1) {
    const p=(t-37)/6.1;
    const sweep=1100-800*p;
    sound+=.027*Math.sin(2*Math.PI*(sweep*t-20*t*t))*Math.sin(Math.PI*p);
    sound+=.014*noise(i)*Math.sin(Math.PI*p);
  }
  const left=Math.max(-1,Math.min(1,sound*(1+.025*Math.sin(t*.7))));
  const right=Math.max(-1,Math.min(1,sound*(1-.025*Math.sin(t*.7))));
  pcm.writeInt16LE(Math.round(left*32767),i*4);
  pcm.writeInt16LE(Math.round(right*32767),i*4+2);
}
const header=Buffer.alloc(44);
header.write('RIFF',0);header.writeUInt32LE(36+pcm.length,4);header.write('WAVE',8);
header.write('fmt ',12);header.writeUInt32LE(16,16);header.writeUInt16LE(1,20);
header.writeUInt16LE(2,22);header.writeUInt32LE(rate,24);header.writeUInt32LE(rate*4,28);
header.writeUInt16LE(4,32);header.writeUInt16LE(16,34);
header.write('data',36);header.writeUInt32LE(pcm.length,40);
const out=path.join('public','audio','score.wav');
fs.mkdirSync(path.dirname(out),{recursive:true});
fs.writeFileSync(out,Buffer.concat([header,pcm]));
console.log(out,`${duration}s stereo`,Buffer.byteLength(pcm));
