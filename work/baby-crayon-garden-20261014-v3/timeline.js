import {track,clamp,lerp,ss} from './engine/lib.js';
export const DUR=40,FPS=24;
export const progress=(t,a,b)=>ss(clamp((t-a)/(b-a)));
export const pathX=track([[0,[430]],[5.2,[430]],[10.2,[1060]],[17.5,[1060]],[27,[2250]],[60,[2250]]]);
export const babyX=t=>pathX(t)[0];
export const floorY=x=>1910+(x-430)*.022;
export function babyState(t){
 let crawl=progress(t,3.7,5.1)*(1-progress(t,10.2,11.4));
 if(t>=16) crawl=progress(t,16.3,17.4)*(1-progress(t,27,28.5));
 const reaching=(progress(t,1.8,2.7)*(1-progress(t,3.2,3.7)))
  +(progress(t,12,12.8)*(1-progress(t,14,14.8)))
  +(progress(t,29.3,30.1)*(1-progress(t,31.8,32.5)));
 const wave=progress(t,36.8,37.4)*(1-progress(t,39.1,39.8));
 const yawn=progress(t,50.5,51)*(1-progress(t,51.8,52.4));
 return {x:babyX(t),y:floorY(babyX(t)),crawl,reach:Math.min(1,reaching),wave,yawn,
 look:progress(t,34,35.8),sleep:progress(t,51.7,53),smile:progress(t,11.4,12.3),t};
}
const catPath=track([[0,[1320]],[12,[1320]],[13.1,[1210]],[14.2,[1210]],[15.2,[1320]],[27,[2460]],[60,[2460]]]);
export function catState(t){const x=catPath(t)[0];return{x,y:floorY(x)-4,t,curl:progress(t,49.6,51.4),flip:t>=12&&t<14.5,lookBack:progress(t,15.2,15.6)*(1-progress(t,16.2,16.6))};}
const cam=track([
 [0,[515,1590,Math.log(2.3)]],[4.4,[515,1590,Math.log(2.3)]],
 [8.5,[905,1555,Math.log(2.05)]],[10.8,[1160,1530,Math.log(2.05)]],
 [16.8,[1160,1530,Math.log(2.05)]],[20.7,[1435,1530,Math.log(1.55)]],
 [23,[1855,1530,Math.log(1.55)]],[27.6,[2340,1510,Math.log(2.05)]],
 [33,[2340,1510,Math.log(2.05)]],[36.8,[2420,1350,Math.log(1.25)]],
 [49.5,[2420,1350,Math.log(1.25)]],[51,[2350,1510,Math.log(1.8)]],
 [53,[2350,1510,Math.log(1.8)]],[55,[1460,600,Math.log(.34)]]
]);
export const FULL=[1460,600,.34];
export function camera(t){const [x,y,z]=cam(t);return[x,y,Math.exp(z)];}
export const EVENTS=[{t:2.4,type:'touch'},{t:12.7,type:'cloth'},{t:30.15,type:'petal'},
 {t:42,type:'brush',d:2.1,pan:-.6},{t:44.3,type:'brush',d:2.1,pan:.6},{t:46.6,type:'brush',d:2.1,pan:-.6},
 {t:43.2,type:'sparkle',note:86},{t:45.3,type:'sparkle',note:90},{t:47.4,type:'sparkle',note:93},{t:58,type:'page',d:1.4}];
