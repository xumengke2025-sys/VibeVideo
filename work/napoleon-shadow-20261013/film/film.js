import{makeGL}from'./vendor/gl.js';import{DURATION,clamp,ramp,sceneAt,cameraAt}from'./math.js';import{sample}from'./simulation.js';import{general,hospital,alpine,coronation}from'./rig-v2.js';import{scenic,fragments,curtain,stage,lamp}from'./art.js';
const cv=document.querySelector('#film'),p=new URLSearchParams(location.search),W=+(p.get('width')||540),H=W*16/9;cv.width=W;cv.height=H;if(p.has('render'))document.body.classList.add('render');
const make=()=>{const c=document.createElement('canvas');c.width=W;c.height=H;return c;},tr=make(),front=make(),g=tr.getContext('2d'),f=front.getContext('2d'),gl=makeGL(cv),imgs={};
await Promise.all(['general','jaffa','alps','coronation','scenery','horseRig'].map(async k=>{const im=new Image;im.src='/assets/'+(k==='alps'?'alps-v2':k==='horseRig'?'horse-rig-v2':k)+'.png';await im.decode();imgs[k]=im;}));
const[cache,cues]=await Promise.all([fetch('/film/flock-cache.json').then(r=>r.json()),fetch('/film/narration.json').then(r=>r.text()).then(s=>JSON.parse(s.replace(/^\uFEFF/,'')))]);await document.fonts.ready;
function text(c,s,x,y,size=40,color='#50381f',family='SimSun'){c.font=`${size}px "${family}",serif`;c.fillStyle=color;c.textAlign='center';c.fillText(s,x,y);}
const labels={arcole:['1796','意大利 · 阿尔科莱','格罗《阿尔科莱桥上的波拿巴》 · 1796'],jaffa:['1799','东方远征 · 雅法','格罗《波拿巴探访雅法疫病患者》 · 1804'],alps:['1800','阿尔卑斯 · 大圣伯纳山口','大卫《跨越阿尔卑斯山》 · 白马红披风版'],coronation:['1804','巴黎 · 12月2日','大卫《拿破仑加冕礼》 · 1807']};
const subtitles=[];for(const c of cues){let phrases=c.text.match(/[^，。！？]+[，。！？]?/g)||[c.text],total=phrases.reduce((s,v)=>s+v.length,0),used=0;for(const s of phrases){const a=c.start+c.duration*used/total;used+=s.length;const b=c.start+c.duration*used/total;subtitles.push({text:s,start:a,end:b});}}
function overlay(t,scene){
 f.setTransform(W/1080,0,0,W/1080,0,0);f.clearRect(0,0,1080,1920);
 const [year,where,art]=labels[scene],bridge=t>=28.4&&t<34.7;
 if(t<3.3){f.globalAlpha=1-ramp(t,2.7,3.3);text(f,'一顶皇冠之前',540,187,76);text(f,'拿破仑 · 1796—1804',540,255,30);f.globalAlpha=1;}
 else{const cut=[15,32.6,49.6].find(c=>Math.abs(t-c)<.85);f.globalAlpha=cut===undefined?1:(t<cut?1-ramp(t,cut-.85,cut-.15):ramp(t,cut+.15,cut+.85));text(f,bridge?'1799':year,540,215,105,'#653c20','Georgia');text(f,bridge?'回国 · 雾月政变 · 第一执政':where,540,286,35);f.globalAlpha=1;}
 // Work dates identify the painting, distinct from the event dates above.
 const start=scene==='arcole'?4:scene==='jaffa'?16:scene==='alps'?35:51,end=start+5.5;
 const a=ramp(t,start,start+.35)*(1-ramp(t,end-.4,end));if(a>0&&!bridge){f.globalAlpha=a;text(f,art,540,1615,29,'#6b4b29','Microsoft YaHei');f.globalAlpha=1;}
 const sub=subtitles.find(s=>t>=s.start&&t<s.end);if(sub){const chars=Array.from(sub.text),lines=[];while(chars.length)lines.push(chars.splice(0,22).join(''));f.font='40px "Microsoft YaHei",sans-serif';f.textAlign='center';f.fillStyle='#3b2818';lines.forEach((s,i)=>f.fillText(s,540,1707+i*54));}
 if(t>61.8){f.globalAlpha=ramp(t,61.8,62.5);text(f,'从将军，到皇帝',540,1589,43);f.globalAlpha=1;}
 stage(f);if(t>63.55){f.fillStyle=`rgba(21,12,7,${ramp(t,63.55,64)})`;f.fillRect(0,0,1080,1920);}
}
let state;
export function renderAt(t,type='image/png',quality=.96){
 t=clamp(t,0,DURATION-1e-5);const scene=sceneAt(t),cam=cameraAt(t);
 g.setTransform(1,0,0,1,0,0);g.globalCompositeOperation='source-over';g.fillStyle='#fff';g.fillRect(0,0,W,H);g.setTransform(W/1080,0,0,W/1080,0,0);g.translate(540,960);g.scale(cam.z,cam.z);g.translate(-cam.x,-cam.y);g.globalCompositeOperation='multiply';
 scenic(g,imgs.scenery,scene,t,cam);
 const rig=scene==='arcole'?general(g,imgs,t):scene==='jaffa'?hospital(g,imgs,t):scene==='alps'?alpine(g,imgs,t):coronation(g,imgs,t);
 fragments(g,sample(cache,t),t);curtain(g,t);overlay(t,scene);gl.render(tr,front,lamp(t,W,H,cam));state={t,scene,cam,rig,width:W,height:H};return cv.toDataURL(type,quality);
}
window.renderAt=renderAt;window.stateAt=t=>{renderAt(t);return state;};renderAt(0);window.__ready=true;
const seek=document.querySelector('#seek'),tm=document.querySelector('#time'),audio=document.querySelector('#audio'),play=document.querySelector('#play');let playing=false;
seek.oninput=()=>{playing=false;audio.pause();audio.currentTime=+seek.value;renderAt(+seek.value);tm.textContent=(+seek.value).toFixed(2)+'s';play.textContent='播放';};
play.onclick=async()=>{playing=!playing;play.textContent=playing?'暂停':'播放';if(playing){if(audio.currentTime>=DURATION-.1)audio.currentTime=0;await audio.play();}else audio.pause();};
function tick(){if(playing){const t=audio.currentTime;renderAt(t);seek.value=t;tm.textContent=t.toFixed(2)+'s';if(t>=DURATION-.1){playing=false;audio.pause();play.textContent='播放';}}requestAnimationFrame(tick);}requestAnimationFrame(tick);
