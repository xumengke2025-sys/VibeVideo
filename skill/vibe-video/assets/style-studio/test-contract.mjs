import assert from 'node:assert/strict';import fs from 'node:fs';import {validate,progress,captionAt,soundEvents} from './timeline.mjs';
const p=JSON.parse(fs.readFileSync(new URL('./clips/one-way.json',import.meta.url),'utf8'));
assert.deepEqual(validate(p),[]);
const clone=()=>structuredClone(p);
let q=clone();q.events[1].id=q.events[0].id;assert(validate(q).some(e=>e.includes('duplicate')));
q=clone();q.events[0].at=-1;assert(validate(q).some(e=>e.includes('interval')));
q=clone();q.shots[1].start+=.2;assert(validate(q).some(e=>e.includes('coverage')));
q=clone();q.captions[0].end=.2;assert(validate(q).some(e=>e.includes('too short')));
q=clone();q.captions[3].event='missing';assert(validate(q).some(e=>e.includes('missing event')));
q=clone();q.events.find(e=>e.id==='open').at+=.5;assert(validate(q).some(e=>e.includes('drift')));
// Changing the event time shifts BOTH visual progress and the shared sound schedule.
q=clone();q.events.find(e=>e.id==='open').at+=2;q.captions[3].start+=2;
assert.equal(progress(q,'open',14.5),0);assert(progress(p,'open',14.5)>0);
assert.equal(soundEvents(q).find(e=>e.id==='open').at,16);assert.equal(captionAt(q,16).event,'open');
assert.equal(soundEvents(p).find(e=>e.id==='close').at,22.7);
const d=JSON.parse(fs.readFileSync(new URL('./clips/dataviz-proof.json',import.meta.url),'utf8'));
const altered=structuredClone(d);altered.data.values[0]=99;assert(validate(altered).some(e=>e.includes('data/range')));
console.log('Contract negative inputs, shared timing and contact offset passed; visual evaluation remains separate.');
