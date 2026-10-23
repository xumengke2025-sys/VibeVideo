import React from 'react';
import {Audio, Composition, Img, registerRoot, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {LEVEL_PATHS, ORGANIC_LEAVES, TREE, WIDTH, HEIGHT, MAIN_IDS, COUNTS} from './tree';
import heroImage from '../public/assets/10-five-choices-organic-corrected.png';
import mapImage from '../public/assets/01-global-engraving.png';

const clip = (x) => Math.max(0, Math.min(1, x));
const ease = (x) => {const u = clip(x); return u * u * (3 - 2 * u);};
const mix = (a, b, p) => a + (b - a) * p;
const ramp = (t, a, b) => ease((t - a) / (b - a));
const pulse = (t, a, b, c, d) => ramp(t, a, b) * (1 - ramp(t, c, d));
const key = (t, ts, vs) => {
  if (t <= ts[0]) return vs[0];
  for (let i = 1; i < ts.length; i++) {
    if (t <= ts[i]) return mix(vs[i - 1], vs[i], ramp(t, ts[i - 1], ts[i]));
  }
  return vs[vs.length - 1];
};

const LABELS = [
  {a: 0, b: 3.3, title: '要去另一座城市吗？', sub: '此刻，所有路线还未写下'},
  {a: 3.5, b: 7.4, title: '五种选择', sub: '镜头跟随「搬去新城」'},
  {a: 7.8, b: 12.1, title: '收入提高，房租也涨', sub: '麻将·万｜赚钱与花钱'},
  {a: 12.5, b: 17.3, title: '在新城市遇见一个人', sub: '塔罗·恋人｜选择靠近'},
  {a: 17.4, b: 22.0, title: '开始带队', sub: '扑克牌花人 J → Q｜职业角色改变'},
  {a: 22.1, b: 27.1, title: '项目取消，一起找新路', sub: '塔罗·高塔 → 星星｜变故与重建'},
];

const PAPER = '#f2ebdf';
const INK = '#191814';
const RED = '#bd1f1b';

function GraphicTexture() {
  return <svg width={WIDTH} height={HEIGHT} style={{position: 'absolute', inset: 0, pointerEvents: 'none'}}>
    <defs>
      <filter id="paperNoise" x="0" y="0" width="100%" height="100%">
        <feTurbulence type="fractalNoise" baseFrequency="0.52" numOctaves="3" seed="11" stitchTiles="stitch"/>
        <feColorMatrix type="saturate" values="0"/>
        <feComponentTransfer><feFuncA type="linear" slope="0.075"/></feComponentTransfer>
      </filter>
    </defs>
    <rect width={WIDTH} height={HEIGHT} fill="#fff" filter="url(#paperNoise)" opacity="0.55"/>
  </svg>;
}

function Graph({t, visibleX, redBand}) {
  const levels = LEVEL_PATHS.map((item, i) => {
    const at = [3, 7.4, 12.2, 17.2, 22.4][i];
    const done = [7, 12.6, 17.5, 22.7, 27.8][i];
    const p = ramp(t, at, done);
    const x0 = [70, 290, 495, 670, 820][i];
    const width = [280, 255, 225, 200, 195][i] * p;
    const opacity = 0.08 * (1 - ramp(t, 37 + (5 - item.depth) * 0.92, 38 + (5 - item.depth) * 0.92));
    return <g key={item.depth} clipPath={`url(#grow-${i})`} opacity={opacity}>
      <defs><clipPath id={`grow-${i}`}><rect x={x0 - 5} y={0} width={width + 10} height={HEIGHT}/></clipPath></defs>
      <path d={item.edges} fill="none" stroke={INK} strokeWidth={[1.65, 1.15, .76, .48, .28][i]} strokeLinecap="round" strokeLinejoin="round"/>
    </g>;
  });
  const mainNodes = MAIN_IDS.map((id) => TREE.byId.get(id));
  const mainPath = mainNodes.map((n, i) => `${i ? 'L' : 'M'} ${n.x} ${n.y}`).join(' ');
  const beadX = key(t, [0, 3, 7, 12, 17, 22, 27, 37, 43], [90, 90, 310, 515, 690, 840, 980, 980, 90]);
  const secondOpacity = ramp(t, 14.2, 14.7) * (1 - ramp(t, 41.3, 41.7));
  const oneOpacity = ramp(t, 2.4, 3.1) * (1 - ramp(t, 42.8, 43.4));
  return <svg width={WIDTH} height={HEIGHT} viewBox={`0 0 ${WIDTH} ${HEIGHT}`} style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
    <defs>
      <clipPath id="worldVisible"><rect x={0} y={0} width={Math.max(0, visibleX)} height={HEIGHT}/></clipPath>
      <clipPath id="redBand"><rect x={redBand - 78} y={0} width={135} height={HEIGHT}/></clipPath>
    </defs>
    <g clipPath="url(#worldVisible)">
      {levels}
      <path d={ORGANIC_LEAVES} fill="none" stroke={INK} strokeWidth=".67" opacity={pulse(t, 4, 8, 35, 42) * .53}/>
      <path d={mainPath} fill="none" stroke={INK} strokeWidth="4.4" strokeLinecap="round" strokeLinejoin="round" opacity={pulse(t, 7.5, 11, 36.8, 42.7) * .58}/>
      <circle cx={beadX} cy={960} r={5.4} fill={INK} opacity={oneOpacity}/>
      <circle cx={beadX - 18} cy={968} r={4.3} fill={INK} opacity={secondOpacity}/>
    </g>
    {t >= 37 && t < 43 && <g clipPath="url(#redBand)" opacity={.62}>
      <path d={mainPath} fill="none" stroke={RED} strokeWidth="5" strokeLinecap="round"/>
    </g>}
  </svg>;
}

function RedReverseCard({t}) {
  const enter = ramp(t, 34.15, 35.2);
  const leave = 1 - ramp(t, 39.0, 40.5);
  if (t < 34 || t >= 40.5) return null;
  const x = mix(1130, 750, enter);
  const y = mix(1420, 1270, enter);
  const rotation = mix(43, 15, enter);
  return <svg width={WIDTH} height={HEIGHT} style={{position: 'absolute', inset: 0, opacity: enter * leave}}>
    <g transform={`translate(${x} ${y}) rotate(${rotation})`}>
      <rect x="-174" y="-239" width="348" height="478" rx="25" fill={PAPER} stroke={RED} strokeWidth="13"/>
      <rect x="-155" y="-220" width="310" height="440" rx="18" fill={RED} stroke={PAPER} strokeWidth="5"/>
      <rect x="-137" y="-201" width="274" height="402" rx="11" fill="none" stroke={PAPER} strokeWidth="2" opacity=".8"/>
      <path d="M-72 18 C-89-71-35-107 43-83 L51-119 L105-53 L39 2 L43-39 C-4-54-37-37-35 9" fill={PAPER}/>
      <path d="M72-18 C89 71 35 107-43 83 L-51 119 L-105 53 L-39-2 L-43 39 C4 54 37 37 35-9" fill={PAPER}/>
    </g>
  </svg>;
}

function Caption({t}) {
  const current = LABELS.find((l) => t >= l.a && t < l.b);
  if (!current) return null;
  const opacity = pulse(t, current.a, current.a + .35, current.b - .42, current.b);
  return <div style={{position: 'absolute', left: 90, right: 90, bottom: 123, opacity, textAlign: 'center', color: INK, fontFamily: 'SimSun, Songti SC, serif', textShadow: '0 1px 1px #f5f0e4'}}>
    <div style={{fontSize: 54, fontWeight: 600, letterSpacing: 3, lineHeight: 1.38}}>{current.title}</div>
    <div style={{width: 240, height: 2, background: INK, opacity: .42, margin: '17px auto 17px'}}/>
    <div style={{fontSize: 28, letterSpacing: 4, lineHeight: 1.35}}>{current.sub}</div>
  </div>;
}

function Count({t}) {
  if (t < 3.3 || t >= 30.3) return null;
  const depth = t < 7 ? 1 : t < 12.5 ? 2 : t < 17.5 ? 3 : t < 22.5 ? 4 : 5;
  const str = COUNTS.slice(0, depth + 1).join(' → ');
  const opacity = pulse(t, 3.4, 3.9, 28.8, 30.3);
  return <div style={{position: 'absolute', top: 90, right: 68, fontSize: 25, letterSpacing: 2.5, color: INK, opacity, fontFamily: 'Georgia, SimSun, serif'}}>{str}</div>;
}

const EVENTS = [
  {a: 7.6, b: 12.3, kind: '麻将 · 万', mark: '萬', name: '收支', top: '工作带来收入', bottom: '房租也随之上涨', note: '赚钱与花钱，是同一次迁居的两面'},
  {a: 12.3, b: 17.3, kind: '塔罗 · 恋人', mark: 'VI', name: '相遇', top: '在新城市遇见一个人', bottom: '两个人选择靠近', note: '第二滴墨，从此走进同一条路'},
  {a: 17.3, b: 22.1, kind: '扑克牌 · 花人', mark: 'J  Q', name: '带队', top: '从独立执行', bottom: '到开始带领团队', note: '职位改变，同行的人没有消失'},
  {a: 22.1, b: 27.4, kind: '塔罗 · 高塔 / 星星', mark: 'XVI  ✶', name: '变故', top: '项目突然取消', bottom: '两人一起寻找新路', note: '命运没有定案，选择仍在继续'},
];

function EventInset({t}) {
  const e = EVENTS.find((item) => t >= item.a && t < item.b);
  if (!e) return null;
  const opacity = pulse(t, e.a, e.a + .45, e.b - .55, e.b);
  return <div style={{position:'absolute', left:618, top:485, width:395, height:725, opacity, color:INK, fontFamily:'SimSun, Songti SC, serif'}}>
    <div style={{fontSize:23, letterSpacing:4, borderBottom:`2px solid ${INK}`, paddingBottom:13, width:310}}>{e.kind}</div>
    <div style={{width:306, height:405, margin:'38px 0 26px 22px', position:'relative', background:'#f7f0e4e8', border:`7px double ${INK}`, borderRadius:13, boxShadow:'4px 5px 0 #3b30271d', overflow:'hidden'}}>
      <svg width="100%" height="100%" viewBox="0 0 300 400" style={{position:'absolute', inset:0}}>
        <defs><pattern id="hatch" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(22)"><line x1="0" y1="0" x2="0" y2="9" stroke={INK} strokeWidth=".65" opacity=".3"/></pattern></defs>
        <rect x="10" y="10" width="280" height="380" rx="7" fill="none" stroke={INK} strokeWidth="1.2"/>
        <rect x="18" y="18" width="264" height="364" rx="5" fill="url(#hatch)" opacity=".25"/>
        <path d="M35 80 Q150 32 265 80 M35 320 Q150 368 265 320" stroke={INK} strokeWidth="1.2" fill="none" opacity=".7"/>
        <circle cx="150" cy="196" r="113" fill="none" stroke={INK} strokeWidth="1" opacity=".55"/>
        <circle cx="150" cy="196" r="104" fill="none" stroke={INK} strokeWidth=".6" opacity=".6"/>
        {Array.from({length:24},(_,i)=><line key={i} x1="150" y1="67" x2="150" y2="88" transform={`rotate(${i*15} 150 196)`} stroke={INK} strokeWidth=".75" opacity=".5"/>)}
      </svg>
      <div style={{position:'absolute', top:105, left:0, right:0, textAlign:'center', fontSize:e.mark.length>3?64:112, lineHeight:1.5, fontWeight:700, letterSpacing:e.mark.length>3?2:0, textShadow:'2px 2px 0 #f7f0e4'}}>{e.mark}</div>
      <div style={{position:'absolute', left:0, right:0, bottom:35, textAlign:'center', fontSize:30, letterSpacing:9}}>{e.name}</div>
    </div>
    <div style={{fontSize:30, lineHeight:1.55, letterSpacing:2.5}}>{e.top}<br/>{e.bottom}</div>
    <div style={{fontSize:19, lineHeight:1.5, letterSpacing:1.5, marginTop:12, opacity:.68}}>{e.note}</div>
  </div>;
}

function LifeBranches() {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const introOpacity = t < 8.7 ? 1 - ramp(t, 7.3, 8.7) : t >= 42.7 ? ramp(t, 42.7, 43.6) : 0;
  const introReveal = t < 7.5 ? mix(235, 1220, ramp(t, 2.7, 7.0)) : t >= 42.7 ? 235 : 1220;
  const worldOpacity = pulse(t, 7.15, 8.8, 42.1, 43.5);
  const focus = t < 27 ? key(t, [7, 12, 17, 22, 27], [310, 515, 690, 840, 980]) :
    t < 34 ? mix(980, 540, ramp(t, 27, 34)) :
    t < 38 ? 540 : mix(540, 90, ramp(t, 38, 43.4));
  const scale = t < 27 ? 2.34 : t < 34 ? mix(2.34, 1, ramp(t, 27, 34)) : t < 38 ? 1 : mix(1, 2.42, ramp(t, 38, 43.4));
  const cameraX = mix(430, 540, ramp(t, 27, 34)) - focus * scale;
  const cameraY = 960 - 960 * scale;
  const worldReveal = t < 37 ? mix(320, 1080, ramp(t, 7, 28.4)) : mix(1080, 0, ramp(t, 37, 43.3));
  const redBand = t < 37 ? 1160 : mix(1080, 0, ramp(t, 37, 43.2));
  const reverseOpacity = t >= 37 && t <= 43 ? Math.sin(Math.PI * clip((t - 37) / 6)) * .14 : 0;
  return <div style={{width: WIDTH, height: HEIGHT, overflow: 'hidden', position: 'relative', backgroundColor: PAPER}}>
    <GraphicTexture/>
    {introOpacity > 0 && <Img src={heroImage} style={{position: 'absolute', width: WIDTH, height: HEIGHT, inset: 0, objectFit: 'cover', opacity: introOpacity, maskImage: `linear-gradient(90deg, #000 0px, #000 ${introReveal - 18}px, transparent ${introReveal + 34}px)`, WebkitMaskImage: `linear-gradient(90deg, #000 0px, #000 ${introReveal - 18}px, transparent ${introReveal + 34}px)`}}/>}
    {worldOpacity > 0 && <div style={{position: 'absolute', width: WIDTH, height: HEIGHT, transformOrigin: '0 0', transform: `translate(${cameraX}px, ${cameraY}px) scale(${scale})`, opacity: worldOpacity}}>
      <Img src={mapImage} style={{position: 'absolute', width: WIDTH, height: HEIGHT, inset: 0, objectFit: 'cover', opacity: .9, maskImage: `linear-gradient(90deg, #000 0px, #000 ${worldReveal - 74}px, transparent ${worldReveal + 74}px)`, WebkitMaskImage: `linear-gradient(90deg, #000 0px, #000 ${worldReveal - 74}px, transparent ${worldReveal + 74}px)`}}/>
      <Graph t={t} visibleX={worldReveal} redBand={redBand}/>
    </div>}
    <EventInset t={t}/>
    {reverseOpacity > 0 && <div style={{position: 'absolute', inset: 0, background: RED, opacity: reverseOpacity, mixBlendMode: 'multiply'}}/>}
    <RedReverseCard t={t}/>
    <Count t={t}/>
    <Caption t={t}/>
    {t >= 43.2 && <div style={{position: 'absolute', top: 257, left: 0, right: 0, textAlign: 'center', opacity: ramp(t, 43.35, 44.1), color: INK, fontFamily: 'SimSun, Songti SC, serif', fontSize: 74, letterSpacing: 10}}>此刻</div>}
    <Audio src={staticFile('audio/score.wav')}/>
  </div>;
}

const Root = () => <Composition id="LifeBranches" component={LifeBranches} durationInFrames={45 * 30} fps={30} width={WIDTH} height={HEIGHT}/>;
registerRoot(Root);
