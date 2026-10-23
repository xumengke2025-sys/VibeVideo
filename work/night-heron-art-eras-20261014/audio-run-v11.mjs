import fs from 'node:fs';
import {distanceAt,timeAtDistance,STRIDE} from './src/run-v11-gait.mjs';
const plan=JSON.parse(fs.readFileSync(new URL('production-plan-run-v11.json',import.meta.url))),SR=48000,D=31,N=SR*D,L=new Float64Array(N),R=new Float64Array(N),events=[];
let seed=7831;const random=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296},hz=n=>440*2**((n-69)/12),TAU=Math.PI*2;
function put(t,b,gain,pan=.5){const k=Math.round(t*SR),l=Math.cos(pan*Math.PI/2),r=Math.sin(pan*Math.PI/2);for(let j=0;j<b.length&&j+k<N;j++)if(k+j>=0){L[k+j]+=b[j]*gain*l;R[k+j]+=b[j]*gain*r;}}
function note(type,t,midi,dur,gain,pan=.5){
 const f=hz(midi),b=new Float64Array(Math.floor(dur*SR));let lp=0;
 for(let j=0;j<b.length;j++){const x=j/SR,tail=Math.min(1,(dur-x)/.035);let v=0;
  if(type==='bass'){v=(Math.sin(TAU*f*x)+.34*Math.sin(TAU*2*f*x)*Math.exp(-x*7)+.12*Math.sin(TAU*3*f*x)*Math.exp(-x*12))*Math.exp(-x*5)*Math.min(1,x/.003)*tail;}
  else if(type==='mallet'){v=(Math.sin(TAU*f*x+1.7*Math.sin(TAU*f*3*x)*Math.exp(-x*34))+.16*Math.sin(TAU*f*4*x)*Math.exp(-x*20))*Math.exp(-x*9)*Math.min(1,x/.002)*tail;}
  else if(type==='brass'){const a=Math.min(1,x/.018)*Math.min(1,(dur-x)/.075),env=a*(.78+.22*Math.exp(-x*20)),vib=1+.0018*Math.sin(TAU*5*x)*Math.min(1,x/.12),ph=TAU*f*x*vib;v=(Math.sin(ph)+.38*Math.sin(2*ph)+.19*Math.sin(3*ph)+.07*Math.sin(4*ph))*env;lp+=.20*(v-lp);v=lp;}
  else if(type==='chord'){v=(Math.sin(TAU*f*x)+.21*Math.sin(TAU*f*2*x)+.08*Math.sin(TAU*f*3*x))*Math.exp(-x*18)*Math.min(1,x/.004)*tail;}
  b[j]=v;
 }
 put(t,b,gain,pan);events.push({type,time:t,midi,duration:dur,gain});
}
function drum(type,t,gain=.1,pan=.5){const dur=type==='brush'?.12:type==='kick'?.14:type==='sweep'?.16:.07,b=new Float64Array(Math.ceil(dur*SR));let low=0,prev=0;
 for(let j=0;j<b.length;j++){const x=j/SR,n=random()*2-1;low=.78*low+.22*n;const high=n-low;let v;
  if(type==='kick')v=Math.sin(TAU*(50*x+1.6*(1-Math.exp(-x*45))))*Math.exp(-x*34)+.12*low*Math.exp(-x*100);
  else if(type==='brush')v=(high*.30+low*.4+Math.sin(TAU*175*x)*.12)*Math.exp(-x*42);
  else if(type==='hat')v=high*Math.exp(-x*100)*.35;
  else if(type==='sweep')v=low*Math.sin(Math.PI*x/dur)**2*.7;
  else v=(low+.25*Math.sin(TAU*190*x))*Math.exp(-x*90);
  b[j]=v;prev=n;
 }put(t,b,gain,pan);events.push({type,time:t,duration:dur,gain});}
function gulp(t){const b=new Float64Array(SR*.13);for(let j=0;j<b.length;j++){const x=j/SR;b[j]=Math.sin(TAU*(96*x+1.4*(1-Math.exp(-x*30))))*Math.exp(-x*29)*Math.min(1,x/.003);}put(t,b,.08,.55);events.push({type:'gulp',time:t});}
const chords=[
 [48,[0,4,7,9]],[48,[0,4,7,9]],[45,[0,3,7,10]],[45,[0,3,7,10]],
 [50,[0,3,7,10]],[43,[0,4,7,10]],[48,[0,4,7,9]],[40,[0,4,7,10]],
 [45,[0,3,7,10]],[50,[0,4,7,10]],[50,[0,3,7,10]],[43,[0,4,7,10]],
 [48,[0,4,7,9]],[45,[0,4,7,10]],[50,[0,3,7,10]],[43,[0,4,7,10]]
];
const shotAt=t=>{const k=plan.timeline.shots.findIndex(s=>t*24>=s.startFrame&&t*24<s.endFrameExclusive);return k<0?(t<1?0:15):k;};
// Quarter notes follow each complete gait cycle. Half beats are the actual left/right landings.
const ticks=[];
for(let q=0;timeAtDistance(q*STRIDE/4)<30.28;q++){
 const t=timeAtDistance(q*STRIDE/4),i=shotAt(t),[root,ints]=chords[i],beat=q/4,phrase=Math.floor(beat)%8,active=t>.7,beatDuration=timeAtDistance((q/4+1)*STRIDE)-timeAtDistance(q/4*STRIDE);
 if(q%2===0){drum('foot',t,active?.055:.018,q%4===0?.43:.57);ticks.push({time:t,leg:q%4===0?'near':'far',distance:q*STRIDE/4});}
 if(!active)continue;
 if(q%4===0){note('bass',t,root-12+(phrase%4===2?7:0),.35,.22,.46);drum('kick',t,.095);}
 if(q%4===2){drum('brush',t,.16,.55);if(i>=4)note('bass',t,root-12+7,.20,.095,.48);}
 if(i>=2)drum('hat',t,.042,i%2?.64:.36);
 if(q%4===3){const swing=timeAtDistance((q+.26)*STRIDE/4);for(const n of ints.slice(1))note('chord',swing,root+12+n,.12,.025,.35);}
 if(q%4===0&&phrase%4!==3){const sequence=[2,1,0,1,2,3,2,1],tone=ints[sequence[phrase]%ints.length];note(i<4?'mallet':'brass',t,root+24+tone,Math.min(.18,beatDuration*.33),i<4?.09:.052,.60);}
}
// A short call-and-response at the three visible story contacts, in the current harmony.
const sync=[];
for(const [i,s]of plan.timeline.shots.entries()){
 const start=s.startFrame/24,[root,ints]=chords[i],at=k=>(s.startFrame+s.events[k])/24;
 // Era change is a harmonic arrival, with a light pickup rather than a loud crash.
 if(i){drum('sweep',start-.15,.038,.64);note('bass',start,root-12,.30,.11,.44);for(const n of ints)note('chord',start,root+12+n,.17,.03,.34);}
 note('mallet',at('reachStart'),root+24+ints[1],.20,.065,.55);
 note('mallet',at('grab'),root+24+ints[2],.25,.14,.60);drum('brush',at('grab'),.075,.58);
 note('brass',at('headUp'),root+24+ints[3],.14,.055,.60);
 gulp(at('swallowStart'));
 note('mallet',at('fishGone'),root+24,.22,.115,.57);drum('kick',at('fishGone'),.055);
 sync.push({era:i+1,cut:start,grab:at('grab'),headUp:at('headUp'),gulp:at('swallowStart'),gone:at('fishGone')});
}
// Opening wink, then a real tonic cadence after the final G7 rather than an abrupt loop.
for(const [k,m]of[60,64,67].entries())note('mallet',.06+k*.13,m,.35,.12,.43+k*.06);
for(const [k,m]of[48,55,60,64,67,72].entries())note(k<2?'bass':'mallet',30.27+k*.022,m,.60,k<2?.15:.095,.35+k*.05);
// Small room early reflections, keeping the onsets dry and the bass centred.
const dryL=L.slice(),dryR=R.slice();for(const [delay,gain]of[[.047,.075],[.083,.055],[.131,.035]]){const d=Math.round(delay*SR);for(let j=d;j<N;j++){L[j]+=dryR[j-d]*gain;R[j]+=dryL[j-d]*gain;}}
let peak=0,sum=0;for(let j=0;j<N;j++){const fade=Math.min(1,j/(SR*.012),(N-j)/(SR*.18));L[j]=Math.tanh(L[j]*1.15)*fade;R[j]=Math.tanh(R[j]*1.15)*fade;peak=Math.max(peak,Math.abs(L[j]),Math.abs(R[j]));}
const gain=.87/peak,b=Buffer.alloc(44+N*4);b.write('RIFF');b.writeUInt32LE(b.length-8,4);b.write('WAVEfmt ',8);b.writeUInt32LE(16,16);b.writeUInt16LE(1,20);b.writeUInt16LE(2,22);b.writeUInt32LE(SR,24);b.writeUInt32LE(SR*4,28);b.writeUInt16LE(4,32);b.writeUInt16LE(16,34);b.write('data',36);b.writeUInt32LE(N*4,40);
for(let j=0;j<N;j++){const l=L[j]*gain,r=R[j]*gain;sum+=l*l+r*r;b.writeInt16LE(Math.round(l*32767),44+j*4);b.writeInt16LE(Math.round(r*32767),46+j*4);}
fs.writeFileSync(new URL('audio/score-run-v11.wav',import.meta.url),b);
fs.writeFileSync(new URL('audio/events-run-v11.json',import.meta.url),JSON.stringify({duration:D,sampleRate:SR,events,footfalls:ticks,sync,statistics:{peak:.87,rms:Math.sqrt(sum/N/2),clipped:false},attribution:'Original deterministic procedural composition and Foley; no external recordings',perception:'not listened'},null,2));
console.log(JSON.stringify({duration:D,events:events.length,footfalls:ticks.length,peak:.87,rms:Math.sqrt(sum/N/2)}));
