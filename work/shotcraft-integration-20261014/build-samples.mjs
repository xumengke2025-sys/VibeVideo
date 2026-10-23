import fs from 'node:fs';
import path from 'node:path';
const task=path.resolve('work/shotcraft-integration-20261014');
const skill='D:/Codex/skills/vibe-video';
const source='D:/Codex/skills/video-shotcraft';
let adaptive=fs.readFileSync(source+'/assets/lib/PageCam.tsx','utf8');
adaptive='// Adapted from video-shotcraft@13c74a7, Apache-2.0. See LICENSE-shotcraft.txt.\n'+adaptive;
adaptive=adaptive.replace("useCurrentFrame, Easing", "useCurrentFrame, useVideoConfig, Easing").replace('export const PageCam:', 'export const PageCamAdaptive:');
adaptive=adaptive.replace('  pageH: number;', '  pageW?: number; // CSS page width; layout separately for each aspect\n  pageH: number;');
adaptive=adaptive.replace('({ src, pageH, keys,', '({ src, pageW = 1920, pageH, keys,');
adaptive=adaptive.replace('  const ownFrame = useCurrentFrame();', '  const {width, height} = useVideoConfig();\n  const centerX = width / 2, centerY = height / 2;\n  if (!keys.length || keys.some(k => !(k.zoom > 0))) throw new Error("Camera requires keys with positive zoom");\n  const ownFrame = useCurrentFrame();');
adaptive=adaptive.replaceAll('width: 1920','width: pageW').replaceAll('${960','${centerX').replaceAll('${540','${centerY').replace("perspectiveOrigin: '960px 540px'",'perspectiveOrigin: `${centerX}px ${centerY}px`');
adaptive=adaptive.replace('point centered in the 1920x1080 viewport','point centered in the current composition viewport');
fs.mkdirSync(skill+'/assets/shotcraft',{recursive:true});
fs.writeFileSync(skill+'/assets/shotcraft/PageCamAdaptive.tsx',adaptive);
fs.copyFileSync(source+'/LICENSE',skill+'/assets/shotcraft/LICENSE-shotcraft.txt');
const sample=String.raw`import React from 'react';
import {AbsoluteFill, Sequence, Audio, staticFile, useCurrentFrame, useVideoConfig, interpolate} from 'remotion';
import {PageCamAdaptive} from './PageCamAdaptive';
export const FPS=30, TOTAL=90, BACKGROUND='#faf7f2';
export const Scene: React.FC<Record<string,unknown>> = ({mode='flat'}) => {
 const {width,height}=useVideoConfig();
 const portrait=height>width, pageH=portrait?2500:1500;
 const frame=useCurrentFrame();
 const target=portrait?{cx:width/2,cy:1530}:{cx:width*0.72,cy:850};
 const tilted=mode==='tilt';
 const keys=[{frame:0,cx:width/2,cy:height/2,zoom:0.86,...(tilted?{rotX:8,rotY:-4}: {})},{frame:28,...target,zoom:portrait?1.03:1.4,...(tilted?{rotX:0,rotY:0}: {})},{frame:44,...target,zoom:portrait?1.03:1.4,...(tilted?{rotX:0,rotY:0}: {})}];
 return <PageCamAdaptive src="page.svg" pageW={width} pageH={pageH} keys={keys} ease={t=>t}><div style={{position:'absolute',left:target.cx-14,top:target.cy-14,width:28,height:28,border:'3px solid #df662e',borderRadius:30,opacity:interpolate(frame,[0,20],[0,1],{extrapolateRight:'clamp'})}}/></PageCamAdaptive>;
};
export const Label:React.FC<Record<string,unknown>>=({text='SHOTCRAFT · CAMERA TEST',color='#233735',fontSize=44})=>{
 const {width}=useVideoConfig();
 return <div style={{position:'absolute',left:60,top:48,padding:'18px 28px',background:BACKGROUND,borderLeft:'8px solid '+color,color:String(color),fontSize:Number(fontSize),fontFamily:'Arial',fontWeight:700,maxWidth:width-120}}>{String(text)}</div>;
};
export const SHOTS=[{id:'flat',label:'Flat page camera',from:0,duration:45,component:Scene,props:{mode:'flat'}},{id:'tilt',label:'Tilt page camera',from:45,duration:45,component:Scene,props:{mode:'tilt'}}];
export const CAPTIONS=[{id:'caption',label:'Editable caption',from:0,duration:TOTAL,component:Label,props:{text:'SHOTCRAFT · CAMERA TEST',color:'#233735',fontSize:44},schema:[{type:'text' as const,key:'text',label:'Text',default:'SHOTCRAFT · CAMERA TEST'},{type:'color' as const,key:'color',label:'Color',default:'#233735'},{type:'number' as const,key:'fontSize',label:'Size',default:44,min:20,max:80,step:1}]}];
export const BGM=[{from:0,duration:TOTAL,src:'validation-tone.wav',volume:0.12,label:'Synthetic test tone'}];
export const Original:React.FC<Record<string,unknown>>=()=> <AbsoluteFill style={{background:BACKGROUND}}>{SHOTS.map(s=><Sequence key={s.id} from={s.from} durationInFrames={s.duration}><s.component {...s.props}/></Sequence>)}{CAPTIONS.map(s=><Sequence key={s.id} from={s.from} durationInFrames={s.duration}><s.component {...s.props}/></Sequence>)}{BGM.map((s,i)=><Sequence key={i} from={s.from} durationInFrames={s.duration}><Audio src={staticFile(s.src)} volume={s.volume}/></Sequence>)}</AbsoluteFill>;
`;
function tone(){const rate=48000,n=rate*3,b=Buffer.alloc(44+n*2);b.write('RIFF');b.writeUInt32LE(b.length-8,4);b.write('WAVEfmt ',8);b.writeUInt32LE(16,16);b.writeUInt16LE(1,20);b.writeUInt16LE(1,22);b.writeUInt32LE(rate,24);b.writeUInt32LE(rate*2,28);b.writeUInt16LE(2,32);b.writeUInt16LE(16,34);b.write('data',36);b.writeUInt32LE(n*2,40);for(let i=0;i<n;i++){const t=i/rate;const envelope=Math.min(1,t*20,(3-t)*20);b.writeInt16LE(Math.round(Math.sin(t*Math.PI*2*(t<1.5?440:660))*0.15*32767*envelope),44+i*2);}return b;}
for(const [aspect,width,height] of [['landscape',1920,1080],['portrait',1080,1920]]){
 const dir=task+'/examples/'+aspect;fs.mkdirSync(dir+'/src',{recursive:true});fs.mkdirSync(dir+'/public',{recursive:true});
 fs.copyFileSync(skill+'/assets/shotcraft/PageCamAdaptive.tsx',dir+'/src/PageCamAdaptive.tsx');fs.copyFileSync(source+'/LICENSE',dir+'/src/LICENSE-shotcraft.txt');
 fs.writeFileSync(dir+'/src/film.tsx',sample);
 fs.writeFileSync(dir+'/src/workbench.ts',`import {SHOTS,CAPTIONS,BGM,Original,FPS,TOTAL,BACKGROUND} from './film';\nexport const WORKBENCH={name:'Shotcraft ${aspect} verification',width:${width},height:${height},fps:FPS,total:TOTAL,background:BACKGROUND,shots:SHOTS,captions:CAPTIONS,bgm:BGM,original:Original};\n`);
 fs.writeFileSync(dir+'/package.json',JSON.stringify({name:'shotcraft-'+aspect+'-verification',private:true,description:'Internal adapter smoke sample. Render with locked workbench dependencies.'},null,2));
 const cards=aspect==='portrait'?[{x:120,y:330,w:840,h:700,name:'SOURCE',detail:'Portrait composition'},{x:120,y:1230,w:840,h:600,name:'TARGET',detail:'Focus and settle'}]:[{x:150,y:330,w:700,h:970,name:'SOURCE',detail:'Landscape composition'},{x:1000,y:470,w:760,h:760,name:'TARGET',detail:'Focus and settle'}];
 const page=`<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${aspect==='portrait'?2500:1500}"><rect width="100%" height="100%" fill="#e8e7de"/><path d="M0 210 H${width}" stroke="#b6c6bc" stroke-width="4"/>${cards.map((c,i)=>`<g><rect x="${c.x}" y="${c.y}" width="${c.w}" height="${c.h}" rx="36" fill="${i?'#233735':'#faf7f2'}"/><text x="${c.x+50}" y="${c.y+110}" fill="${i?'#faf7f2':'#233735'}" font-size="54" font-family="Arial" font-weight="bold">${c.name}</text><text x="${c.x+50}" y="${c.y+185}" fill="${i?'#91beac':'#526c65'}" font-size="32" font-family="Arial">${c.detail}</text><path d="M${c.x+50} ${c.y+280} Q${c.x+c.w/2} ${c.y+480} ${c.x+c.w-50} ${c.y+300}" fill="none" stroke="#df662e" stroke-width="14"/>${[0,1,2].map(j=>`<rect x="${c.x+50+j*(c.w-100)/3}" y="${c.y+c.h-180}" width="${(c.w-150)/3}" height="100" rx="12" fill="${i?'#456458':'#c6d7cd'}"/>`).join('')}</g>`).join('')}</svg>`;
 fs.writeFileSync(dir+'/public/page.svg',page);fs.writeFileSync(dir+'/public/validation-tone.wav',tone());
}
console.log('Adaptive component and two 90-frame samples written');
