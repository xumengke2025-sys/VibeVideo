export const FILM={width:1080,height:1920,fps:30,duration:22,seed:20261011};

// 环形交叉带分拣机：体育场形环路。长轴沿世界 (-1,0,-1)/√2 方向，
// 在等距相机（视线 (1,1,1)）下映射为屏幕竖直方向，以适配 9:16 竖屏。
export const LOOP={L:12,R:3,v:1.0,carts:32};
export const P=4*LOOP.L+2*Math.PI*LOOP.R;

const inv=1/Math.SQRT2;
export const toWorld=(p,q)=>({x:(-p+q)*inv,z:(-p-q)*inv});

export function pathAt(s){
  s=((s%P)+P)%P;
  const {L,R}=LOOP,straight=2*L,arc=Math.PI*R;
  if(s<straight)return{p:-L+s,q:R,tp:1,tq:0};
  if(s<straight+arc){const th=(s-straight)/R;return{p:L+R*Math.sin(th),q:R*Math.cos(th),tp:Math.cos(th),tq:-Math.sin(th)};}
  if(s<2*straight+arc)return{p:L-(s-straight-arc),q:-R,tp:-1,tq:0};
  const th=(s-2*straight-arc)/R;return{p:-L-R*Math.sin(th),q:-R*Math.cos(th),tp:-Math.cos(th),tq:Math.sin(th)};
}
// qOff 沿外法线偏移；yaw 使物体局部 +X 沿切线、局部 +Z 沿外法线
export function loopPos(s,qOff=0){
  const a=pathAt(s);const w=toWorld(a.p,a.q+qOff);
  const tw=toWorld(a.tp,a.tq);
  return {x:w.x,z:w.z,yaw:Math.atan2(-tw.z,tw.x)};
}
export const fwd=(a,b)=>((b-a)%P+P)%P;
// 沿外法线偏移 o（side=+1 外圈、-1 内圈）。外法线在 (p,q) 中为 (-tq, tp)，
// 圆弧段上它有 p 分量，所以不能只加在 q 上。
export function loopOff(s,side,o){
  const a=pathAt(s),np=-a.tq,nq=a.tp;
  const w=toWorld(a.p+side*o*np,a.q+side*o*nq);
  const tw=toWorld(a.tp,a.tq);
  return {x:w.x,z:w.z,yaw:Math.atan2(-tw.z,tw.x)};
}

export const S_INDUCT=2.0, S_GATE=8.3, S_HERO_CHUTE=16.8;
export const S_HERO0=3.0;                       // 主角小车在 t=0 的弧长位置（已在上线点之后）
export const heroS=t=>((S_HERO0+LOOP.v*t)%P+P)%P;

// 分拣格口：弧长位置、去向与出格侧（+1 外圈 / -1 内圈）。
// 真实交叉带分拣机两侧都可出格，带面能向任一侧运行。示意，非真实分拣计划。
export const CHUTES=[
  {s:9.0, city:'西安',  side:1},
  {s:10.3,city:'郑州',  side:-1},
  {s:11.6,city:'重庆',  side:1},
  {s:12.9,city:'合肥',  side:-1},
  {s:14.2,city:'长沙',  side:1},
  {s:15.5,city:'南昌',  side:-1},
  {s:16.8,city:'杭州',  side:1},
  {s:18.1,city:'贵阳',  side:-1},
  {s:19.4,city:'武汉',  side:1},
  {s:20.7,city:'兰州',  side:-1},
  {s:22.0,city:'北京',  side:1},
  {s:25.0,city:'南京',  side:1},
  {s:27.6,city:'广州',  side:1},
  {s:30.2,city:'天津',  side:1},
  {s:36.0,city:'成都',  side:1},
  {s:37.3,city:'南宁',  side:-1},
  {s:38.6,city:'福州',  side:1},
  {s:39.9,city:'太原',  side:-1},
  {s:41.2,city:'济南',  side:1},
  {s:42.5,city:'石家庄',side:-1},
  {s:43.8,city:'昆明',  side:1},
  {s:45.1,city:'海口',  side:-1},
  {s:46.5,city:'沈阳',  side:1},
];
export const HERO_CHUTE_INDEX=6;

// 每台小车的上线位、负责格口与抛投时刻（画面与声音共用同一套计算）
export const cartS0=i=>i===0?S_HERO0:((S_HERO0+(P/LOOP.carts)*i)%P+P)%P;
export const cartChute=i=>i===0?CHUTES[HERO_CHUTE_INDEX]:CHUTES[i%CHUTES.length];
export function ejectTime(i){
  const s0=cartS0(i),tgt=cartChute(i).s;
  let t=(tgt-s0)%P;if(t<0)t+=P;return t;
}

export const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v));
export const ease=x=>{x=clamp(x);return x*x*(3-2*x)};
export const lerp=(a,b,u)=>a+(b-a)*u;

export const SHOTS=[
  {start:0,end:3.5,id:'scale',name:'规模',sub:['你昨天点的东西','正在这里，找它的路']},
  {start:3.5,end:7.5,id:'scan',name:'识别',sub:['进门那一刻','只有一次被看清的机会']},
  {start:7.5,end:12.5,id:'belt',name:'交叉带',sub:['它脚下这条带子','可以横着走']},
  {start:12.5,end:16.5,id:'throw',name:'落格',sub:['到站，被横向','甩进它的格口']},
  {start:16.5,end:22,id:'all',name:'每一个',sub:['每一个包裹','都在这样找路']},
];
export function shotAt(t){return SHOTS.find(s=>t>=s.start&&t<s.end)||SHOTS.at(-1)}
export function subtitle(t){return shotAt(t).sub}

// 声音事件：与画面接触/脱离时刻对齐（hero 在 13.8 到达格口）
export const SOUNDS=[
  {t:1.30,type:'load'},
  {t:5.30,type:'scan'},
  {t:11.30,type:'belt'},
  {t:14.21,type:'throw'},
  {t:14.47,type:'chute'},
  {t:20.00,type:'settle'},
];
