export const DURATION=60, FPS=24;
export const SHOTS=[
 {id:'standard',start:0,end:6,reads:['eagle','flag','ordered ranks']},
 {id:'guns',start:6,end:14,reads:['preparation','recoil','defensive ridge']},
 {id:'charge',start:14,end:20,reads:['mounted cuirassiers','acceleration','ridge approach']},
 {id:'square',start:20,end:26,reads:['hollow infantry square','closing horses','horses turn aside']},
 {id:'pressure',start:26,end:35,reads:['returning cavalry','advancing standard','flank column']},
 {id:'guard',start:35,end:46,reads:['ordered guard steps','raised standard','defensive line']},
 {id:'collapse',start:46,end:54,reads:['volley','front rank hesitation','staggered retreat']},
 {id:'aftermath',start:54,end:60,reads:['same eagle','scattered ranks','drooping flag']}
];
export const EVENTS=[
 {id:'gun1',t:8.1,kind:'cannon',x:-2.9},
 {id:'gun2',t:9.2,kind:'cannon',x:.3},
 {id:'gun3',t:10.4,kind:'cannon',x:3.1},
 {id:'square-volley',t:22.7,kind:'volley'},
 {id:'guard-volley',t:46.2,kind:'volley'},
 {id:'music-drop',t:45.55,kind:'music'},
 {id:'flag-fall',t:48,kind:'flag'},
];
export const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v));
export const mix=(a,b,p)=>a+(b-a)*p;
export const smooth=(t,a,b)=>{const p=clamp((t-a)/(b-a));return p*p*(3-2*p)};
export const shotAt=t=>SHOTS.find(s=>t>=s.start&&t<s.end)||SHOTS.at(-1);
export const seed=i=>{const n=Math.sin(i*127.1+311.7)*43758.5453;return n-Math.floor(n)};
