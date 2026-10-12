import {test} from 'node:test';import assert from 'node:assert/strict';
import {valveState,pathAt} from './mechanical.mjs';
import {springFrom,springTrack,logZoom,morphPoints} from './continuity.mjs';
import {follow3D} from './subject-camera.mjs';
test('pressure/preload/seat/end-stop and fixed spring anchor',()=>{
 for(let pressure=-5;pressure<8;pressure+=.01){const s=valveState({pressure,preload:1,stiffness:2,stroke:1,restLength:3,seat:10});assert(s.displacement>=0&&s.displacement<=1);assert(Math.abs(s.disc+s.springLength-13)<1e-10);assert.equal(s.contact,pressure<=1);assert.equal(s.open,!s.contact);}
 assert.equal(valveState({pressure:4}).limited,true);assert.throws(()=>valveState({pressure:NaN}));assert.throws(()=>valveState({pressure:2,restLength:1}));
});
test('Hermite path C1 join, pause, seek independence and malformed input',()=>{
 const knots=[{t:0,p:[0,0,0],v:[0,0,3]},{t:2,p:[0,0,4],v:[0,0,0]},{t:3,p:[0,0,4],v:[0,0,0]},{t:5,p:[0,0,10],v:[0,0,3]}];
 assert.deepEqual(pathAt(2.5,knots),[0,0,4]);for(const t of [2,3]){const e=1e-5,l=pathAt(t-e,knots),m=pathAt(t,knots),r=pathAt(t+e,knots);assert(Math.abs((r[2]-m[2])/e-(m[2]-l[2])/e)<.001);}
 const times=[4,0,2.2,1,4],v=times.map(t=>pathAt(t,knots));assert.deepEqual(v[0],v[4]);assert.throws(()=>pathAt(1,[knots[0],knots[0]]));
 const camera=follow3D({subject:t=>pathAt(t,knots),range:[0,5],space:'world',offset:[4,2,-7]});assert.deepEqual(camera(2.2),camera(2.2));assert(camera(0).position.every(Number.isFinite));
});
test('existing spring, logarithmic zoom and contour identity remain usable',()=>{
 const events=[{time:1,value:2},{time:2,value:-1}];const before=springTrack(2-1e-8,0,events),after=springTrack(2+1e-8,0,events);assert(Math.abs(before-after)<1e-5);
 assert.equal(springFrom(0,{from:3,to:7}),3);assert(Math.abs(logZoom(1,100,.5)-10)<1e-9);assert.deepEqual(morphPoints([{x:0,y:0}],[{x:4,y:8}],.5),[{x:2,y:4}]);
});
