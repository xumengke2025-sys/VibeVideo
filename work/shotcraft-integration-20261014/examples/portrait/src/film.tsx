import React from 'react';
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
