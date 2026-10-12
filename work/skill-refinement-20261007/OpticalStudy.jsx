import React from 'react';
import {AbsoluteFill, Audio, Img, staticFile, useCurrentFrame} from 'remotion';

const clamp=(v)=>Math.max(0,Math.min(1,v));
const ease=(v)=>{const q=clamp(v);return q*q*(3-2*q)};
const font='"Microsoft YaHei", sans-serif';
const label={fontFamily:font,color:'#eef4f6',position:'absolute'};
const bands=[['F090W','#526fff'],['F187N','#55d7ee'],['F200W','#5bcc95'],['F470N','#ecd57d'],['F335M','#f0a662'],['F444W','#d86758']];

function Photograph({scale=1,x=0,y=0,gray=false,opacity=1}){
  return <Img src={staticFile('carina-nasa.png')} style={{position:'absolute',width:1920,height:1112,top:-16,left:0,objectFit:'cover',transform:`translate(${x}px,${y}px) scale(${scale})`,transformOrigin:'center',filter:gray?'grayscale(1)':'none',opacity}}/>;
}

export function OpticalStudy(){
  const frame=useCurrentFrame();
  const scene=frame<90?0:frame<180?1:2;
  const local=scene===0?frame:scene===1?frame-90:frame-180;
  const show=scene===1?1:ease(local/14);
  return <AbsoluteFill style={{background:'#050d15',fontFamily:font,overflow:'hidden'}}>
    <Audio src={staticFile('study-sound.wav')} />
    {scene===0&&<>
      <Photograph scale={1.24-0.14*ease(local/89)} x={-40+40*ease(local/89)} y={18-18*ease(local/89)}/>
      <AbsoluteFill style={{background:'linear-gradient(90deg,rgba(2,9,16,.72),rgba(2,9,16,.05) 65%),linear-gradient(0deg,rgba(2,9,16,.88),transparent 65%)'}}/>
      <div style={{...label,left:100,top:85,fontSize:24,letterSpacing:7,color:'#a8c8d9'}}>宇宙的另一种颜色</div>
      <div style={{...label,left:100,top:558,fontSize:90,lineHeight:1.36,letterSpacing:-2,fontWeight:500,transform:`translateY(${12*(1-ease(local/20))}px)`}}>这些颜色，<br/>来自不可见的光。</div>
      <div style={{...label,left:104,top:884,fontSize:27,color:'#d2e2e8'}}>韦布望远镜 · NGC 3324 · 近红外成像</div>
      <div style={{...label,left:104,bottom:43,fontSize:20,color:'#b6c8d2'}}>真实观测影像：NASA / ESA / CSA / STScI</div>
    </>}
    {scene===1&&<>
      <Photograph scale={1.1} opacity={.23}/>
      <AbsoluteFill style={{background:'linear-gradient(90deg,#050d15 15%,rgba(5,13,21,.7) 55%,rgba(5,13,21,.18))'}}/>
      <div style={{position:'absolute',right:100,top:120,width:760,height:760,borderRadius:'50%',background:'radial-gradient(ellipse,rgba(72,130,155,.13),transparent 65%)'}}/>
      <Img src={staticFile('optical-mirror-concept.png')} style={{position:'absolute',width:1500,left:668-32*ease(local/89),top:150-18*ease(local/89),transform:`scale(${1+.035*ease(local/89)})`,transformOrigin:'65% 50%',filter:'brightness(.9) contrast(1.03)',opacity:show}}/>
      <svg width="1920" height="1080" style={{position:'absolute',inset:0,opacity:.8*ease((local-12)/20)}}>
        <defs><linearGradient id="signal"><stop stopColor="#83d3e6" stopOpacity="0"/><stop offset="1" stopColor="#bde9f4"/></linearGradient></defs>
        {[0,1,2].map(i=><path key={i} pathLength={1} d={`M 85 ${610+i*60} C 430 ${555+i*48}, 670 ${575+i*22}, 780 492`} fill="none" stroke="url(#signal)" strokeWidth={i===1?3:1.5} strokeDasharray="1" strokeDashoffset={1-ease((local-15-i*5)/50)}/>)}
        {[0,1,2].map(i=>{const p=ease((local-22-i*5)/48),u=1-p;return <circle key={i} cx={u*u*u*85+3*u*u*p*430+3*u*p*p*670+p*p*p*780} cy={u*u*u*(610+i*60)+3*u*u*p*(555+i*48)+3*u*p*p*(575+i*22)+p*p*p*492} r={i===1?4:2.5} fill="#c8f0ff" opacity={p>0&&p<1?.9:0}/>})}
      </svg>
      <div style={{...label,left:100,top:85,fontSize:24,letterSpacing:7,color:'#a8c8d9'}}>01 / 接收</div>
      <div style={{...label,left:100,top:270,fontSize:118,fontWeight:500,letterSpacing:-4,opacity:show}}>红外观测</div>
      <div style={{...label,left:108,top:438,fontSize:34,lineHeight:1.7,color:'#c2d6e1',opacity:show}}>眼睛看不到的波段，<br/>可以由仪器记录。</div>
      <div style={{...label,left:104,bottom:80,fontSize:23,color:'#afc1cd'}}>观测过程示意 · AI 生成概念装置</div>
    </>}
    {scene===2&&<>
      <Photograph scale={1.09-.07*ease(local/119)} gray opacity={.28}/>
      {bands.map(([name,color],i)=>{const joined=ease((local-5-i*2)/58),colored=ease((local-48-i*4)/30);return <div key={name} style={{position:'absolute',width:320,height:1080,overflow:'hidden',left:i*320+(i-2.5)*72*(1-joined),top:(i%2?65:-65)*(1-joined)}}>
        <div style={{position:'absolute',left:-i*320,width:1920,height:1080}}><Photograph scale={1.09-.07*ease(local/119)}/><Photograph scale={1.09-.07*ease(local/119)} gray opacity={1-colored}/></div>
        <div style={{position:'absolute',inset:0,background:color,opacity:.22*(1-colored),mixBlendMode:'screen'}}/>
        <div style={{position:'absolute',right:0,top:0,height:1080,width:1,background:color,opacity:1-joined}}/>
      </div>})}
      <AbsoluteFill style={{background:'linear-gradient(0deg,rgba(2,9,16,.91),transparent 66%),linear-gradient(90deg,rgba(2,9,16,.6),transparent 80%)'}}/>
      <div style={{...label,left:100,top:85,fontSize:24,letterSpacing:7,color:'#d0dfeb'}}>02 / 赋色合成</div>
      <div style={{...label,left:100,top:575,fontSize:86,fontWeight:500,lineHeight:1.35,opacity:show}}>多波段，<br/>合成一幅图。</div>
      <div style={{...label,left:105,top:824,fontSize:30,color:'#d6e3e9',opacity:show}}>不同滤镜的灰度影像，被赋予颜色后合成。</div>
      <div style={{position:'absolute',right:108,top:88,display:'flex',gap:4,opacity:.85*show}}>{bands.map(([name,color])=><div key={name} style={{width:90}}><div style={{height:5,background:color}}/><div style={{fontSize:18,color:'#d9e7eb',marginTop:12,fontFamily:'monospace'}}>{name}</div></div>)}</div>
      <div style={{...label,left:104,bottom:72,fontSize:19,color:'#b5c7d2'}}>颜色合成流程示意，非原始滤镜数据重建</div>
      <div style={{...label,left:104,bottom:35,fontSize:19,color:'#b5c7d2'}}>观测影像：NASA / ESA / CSA / STScI</div>
    </>}
  </AbsoluteFill>;
}
