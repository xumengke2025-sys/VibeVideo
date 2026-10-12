import fs from 'node:fs';
import {valveState,pathAt} from 'file:///D:/Codex/skills/vibe-video/assets/mechanical.mjs';
import {worldToScreen,seeded} from 'file:///D:/Codex/skills/vibe-video/assets/motion.mjs';
const checks=[];
function test(name,fn){try{fn();checks.push({name,ok:true})}catch(e){checks.push({name,ok:false,error:e.message})}}
function assert(v,m){if(!v)throw Error(m)}
const params={area:1,preload:1,stiffness:1,stroke:1,restLength:2,seat:0};
test('reverse and below-threshold pressure remain seated',()=>{for(const pressure of [-100,-1,0,.99,1]){const s=valveState({...params,pressure});assert(s.disc===0&&s.contact&&!s.open,'unseated')}});
test('stroke / spring compression / fixed end remain consistent',()=>{for(let p=-2;p<=5;p+=.01){const s=valveState({...params,pressure:p});assert(s.displacement>=0&&s.displacement<=1,'stroke');assert(Math.abs(s.disc+s.springLength-2)<1e-9,'fixed spring end');assert(s.springForce>=1,'preload')}});
test('excess pressure saturates at mechanical stop',()=>assert(valveState({...params,pressure:100}).displacement===1,'stop'));
test('invalid mechanical parameters rejected',()=>{for(const change of [{area:0},{preload:-1},{stiffness:0},{stroke:0},{restLength:1},{pressure:NaN}]){let refused=false;try{valveState({...params,pressure:1,...change})}catch(e){refused=e instanceof RangeError}assert(refused,JSON.stringify(change))}});
const knots=[{t:0,p:[0,0],v:[0,0]},{t:1,p:[2,1],v:[0,0]},{t:2,p:[3,0],v:[0,0]}];
test('Hermite path deterministic under shuffled evaluation',()=>{const times=[0,.1,.7,1,1.3,1.9,2],a=times.map(t=>pathAt(t,knots));[...times].reverse().forEach(t=>assert(JSON.stringify(pathAt(t,knots))===JSON.stringify(a[times.indexOf(t)]),'history-dependent'))});
test('path rejects mismatched dimensions / nonascending times',()=>{for(const k of [[knots[0],{...knots[1],t:0}],[knots[0],{...knots[1],p:[1]}]]){let refused=false;try{pathAt(.2,k)}catch(e){refused=e instanceof RangeError}assert(refused,'accepted invalid path')}});
test('world camera focus maps to viewport centre across zooms',()=>{for(const zoom of [.1,1,5]){const p=worldToScreen({x:42,y:-10},{x:42,y:-10,zoom},{width:1080,height:1920});assert(p.x===540&&p.y===960,'bad centre')}});
test('seeded randomness recreates under new factory',()=>{const a=seeded(42),b=seeded(42);for(let i=0;i<100;i++)assert(a()===b(),'seed inconsistent')});
const state=t=>{const pressure=t<.4?.6:t<1? .6+(t-.4)/.6*1.8:t<1.25?2.4:t<1.8?2.4-(t-1.25)/.55*2.9:-.5;return {t,pressure,...valveState({...params,pressure})}};
fs.writeFileSync(new URL('./mechanical-checks.json',import.meta.url),JSON.stringify({checks,scope:'Constraint / deterministic-state checks. No aesthetic judgement or fluid simulation.'},null,2));
fs.writeFileSync(new URL('./states.json',import.meta.url),JSON.stringify(Array.from({length:60},(_,i)=>state(i/30)),null,2));
console.log(JSON.stringify({passed:checks.filter(x=>x.ok).length,total:checks.length}));
if(checks.some(x=>!x.ok))process.exitCode=1;
