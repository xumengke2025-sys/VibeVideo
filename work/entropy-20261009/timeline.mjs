// Shared contract: seconds in JSON, frames only at the output boundary.
export const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
export const ease=x=>{x=clamp(x);return x*x*(3-2*x);};
export const lerp=(a,b,p)=>a+(b-a)*p;
export const eventById=(plan,id)=>{const ev=plan.events.find(e=>e.id===id);if(!ev)throw Error(`Missing event ${id}`);return ev;};
export const progress=(plan,id,t)=>{const e=eventById(plan,id);return ease((t-e.at)/e.duration);};
export const captionAt=(plan,t)=>plan.captions.find(c=>c.start<=t&&t<c.end);
export const soundEvents=plan=>plan.events.filter(e=>e.sound).map(e=>({...e,visualAt:e.at,at:e.at+(e.sound.offset||0)}));
export function validate(plan){
 const errors=[];const finite=x=>typeof x==='number'&&Number.isFinite(x);
 if(!finite(plan.duration)||plan.duration<=0||!finite(plan.fps)||plan.fps<=0||!Number.isInteger(plan.fps))errors.push('invalid duration/fps');
 if(!plan.id||!['blueprint','dataviz','entropy'].includes(plan.style)||!['voice','music','action','narration'].includes(plan.timingDriver))errors.push('invalid id/style/timingDriver');
 if(plan.style==='dataviz'){
  const d=plan.data;if(!d||!Array.isArray(d.values)||d.values.length<2||d.values.length>12||!finite(d.maximum)||d.maximum<=0||!d.values.every(v=>finite(v)&&v>=0&&v<=d.maximum)||!d.label)errors.push('invalid data/range/label');
 }
 if(plan.style==='entropy'){
  const m=plan.model,choose=(n,k)=>{let r=1;for(let i=0;i<k;i++)r=r*(n-i)/(i+1);return Math.round(r);};
  if(!m||m.particles!==8||!Array.isArray(m.counts)||m.counts.length!==9)errors.push('invalid entropy model');
  else{
   const computed=Array.from({length:9},(_,k)=>choose(m.particles,k));
   if(JSON.stringify(m.counts)!==JSON.stringify(computed))errors.push('model counts do not match C(8,k)');
   if(m.counts.reduce((a,b)=>a+b,0)!==256)errors.push('model counts do not sum to 256');
   if((m.counts[3]+m.counts[4]+m.counts[5])!==182)errors.push('entropy: near-uniform total is not 182');
   if(m.allOnOneSide!==2)errors.push('entropy: merged one-side total must be 2');
  }
 }
 if(!Array.isArray(plan.events)||!Array.isArray(plan.captions)||!Array.isArray(plan.shots))return [...errors,'events/captions/shots must be arrays'];
 const ids=new Set();const ordered=plan.events;
 for(const e of ordered){
  if(!e.id||ids.has(e.id))errors.push(`duplicate/missing event id ${e.id}`);ids.add(e.id);
  if(!finite(e.at)||!finite(e.duration)||e.at<0||e.duration<=0||e.at+e.duration>plan.duration+1e-8)errors.push(`invalid event interval ${e.id}`);
  if(!e.action||!e.result||!e.anchor)errors.push(`event ${e.id} lacks action/result/anchor`);
  if(e.sound&&(!finite(e.sound.gain)||e.sound.gain<0||e.sound.gain>1||!finite(e.sound.duration)||e.sound.duration<=0||!finite(e.sound.offset??0)||(e.sound.offset??0)<0||e.at+(e.sound.offset||0)+e.sound.duration>plan.duration+1e-8||!['paper','click','flow','tone','stamp','tick','whoosh','pluck','chime','sub'].includes(e.sound.kind)))errors.push(`invalid sound ${e.id}`);
 }
 let end=0;const shotIds=new Set();
 for(const s of plan.shots){
  if(!s.id||shotIds.has(s.id))errors.push(`duplicate/missing shot id ${s.id}`);shotIds.add(s.id);
  if(!finite(s.start)||!finite(s.end)||Math.abs(s.start-end)>1e-8||s.end<=s.start||s.end>plan.duration)errors.push(`shot coverage ${s.id}`);
  if(!s.intent||!s.camera||!s.action)errors.push(`missing shot intent ${s.id}`);
  const values=['establish','action','result'].map(k=>s.states?.[k]);
  if(!values.every(v=>finite(v)&&s.start<=v&&v<s.end)||values[0]>values[1]||values[1]>values[2])errors.push(`invalid shot states ${s.id}`);
  end=s.end;
 }
 if(Math.abs(end-plan.duration)>1e-8)errors.push('shots do not cover duration');
 let last=0;
 for(const c of plan.captions){
  if(!finite(c.start)||!finite(c.end)||c.start<last||c.end<=c.start||c.end>plan.duration||!c.text)errors.push('invalid/overlapping caption');
  if(c.event&&!ids.has(c.event))errors.push(`caption references missing event ${c.event}`);
  const min=[...String(c.text)].length/(plan.readingRate||4.5)+(plan.readingBuffer??1.5);
  if(c.end-c.start<min-1e-8)errors.push(`caption too short: ${c.text} needs ${min.toFixed(2)}s`);
  if(c.event&&ids.has(c.event)&&Math.abs(c.start-eventById(plan,c.event).at)>1/plan.fps)errors.push(`caption/event drift: ${c.event}`);
  last=c.end;
 }
 for(const w of plan.silences||[]){if(!Array.isArray(w)||w.length!==2||!w.every(finite)||w[0]<0||w[1]>plan.duration||w[1]<=w[0])errors.push('invalid silence');}
 if(plan.narration!==undefined){
  if(!Array.isArray(plan.narration)||plan.narration.length===0)errors.push('narration must be a non-empty array');
  else for(const n of plan.narration){
   if(!finite(n.start)||!finite(n.end)||n.end<=n.start||n.end>plan.duration+1e-8||!n.text||!n.file)errors.push('invalid narration entry '+(n.file||'?'));
   const cap=plan.captions.find(c=>Math.abs(c.start-n.start)<=1/plan.fps&&c.text===n.text);
   if(!cap)errors.push('narration/caption mismatch: '+n.file);
   if(finite(n.duration)&&Math.abs((n.end-n.start)-n.duration)>0.15)errors.push('narration slot does not match measured duration: '+n.file);
  }
 }
 return errors;
}
export function reviewSchedule(plan){
 return {clip:plan.id,scope:'Sampling schedule, not a visual or listening verdict.',
  states:plan.shots.flatMap(s=>Object.entries(s.states).map(([state,time])=>({shot:s.id,state,time,frame:Math.round(time*plan.fps)}))),
  windows:plan.events.map(e=>({event:e.id,anchor:e.anchor,start:Math.max(0,e.at-.2),end:Math.min(plan.duration,e.at+e.duration+.2),step:.2})),
  captions:plan.captions.map(c=>({text:c.text,start:c.start,end:c.end})),sound:soundEvents(plan).map(e=>({event:e.id,time:e.at,kind:e.sound.kind}))};
}
