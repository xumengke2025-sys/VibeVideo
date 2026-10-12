import {noise,C} from '../scenes/common.mjs';
export function createCompositor(canvas){
 const g=canvas.getContext('2d',{alpha:false});const paper=document.createElement('canvas');paper.width=1080;paper.height=1920;const p=paper.getContext('2d');p.fillStyle=C.paper;p.fillRect(0,0,1080,1920);
 for(let i=0;i<64000;i++){const x=noise(i+100)*1080,y=noise(i+300000)*1920;p.fillStyle=`rgba(65,64,52,${.012+noise(i+8000)*.06})`;p.fillRect(x,y,.4+noise(i+200)*1.8,.5+noise(i+700)*3)}
 const edge=g.createRadialGradient(540,960,550,540,960,1400);edge.addColorStop(0,'rgba(85,79,63,0)');edge.addColorStop(1,'rgba(85,79,63,.12)');
 return {g,compose(source,t){g.setTransform(1,0,0,1,0,0);g.globalAlpha=1;g.globalCompositeOperation='source-over';g.drawImage(paper,0,0);g.filter='saturate(.06)';g.drawImage(source,0,0,1080,1920);g.filter='none';g.globalCompositeOperation='multiply';g.globalAlpha=.18;g.drawImage(paper,0,0);g.globalAlpha=1;g.globalCompositeOperation='source-over';g.fillStyle=edge;g.fillRect(0,0,1080,1920);if(t>59.6){g.fillStyle=C.paper;g.globalAlpha=(t-59.6)/.4;g.fillRect(0,0,1080,1920);g.globalAlpha=1}}};
}
