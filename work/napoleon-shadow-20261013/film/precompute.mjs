import fs from'node:fs';import{createHash}from'node:crypto';import{simulate,sample}from'./simulation.js';
const hash=x=>createHash('sha256').update(JSON.stringify(x)).digest('hex');
const a=simulate(),b=simulate(),off=simulate({social:false});
const checks={fixedSeed:hash(a)===hash(b),socialRulesChangeTrajectory:hash(a.frames)!==hash(off.frames),neighbourInteractions:a.interactions,finite:a.frames.every(f=>f.every(p=>p.every(Number.isFinite))),seek:[13.5,30,49.8].every(t=>hash(sample(a,t))===hash(sample(a,t)))};
fs.writeFileSync(new URL('flock-cache.json',import.meta.url),JSON.stringify(a));fs.writeFileSync(new URL('simulation-checks.json',import.meta.url),JSON.stringify(checks,null,2));console.log(checks);if(!checks.fixedSeed||!checks.socialRulesChangeTrajectory||!checks.finite)throw Error('simulation failed');
