export const FILM={width:1080,height:1920,fps:30,duration:26,seed:20261012};

// ---- 绿波带的物理（示意参数，非任何真实路口数据）----
// 路口 i 位于 z = -BLOCK*(i+1)，绿灯自 G0+i*DT 开始，持续 GREEN 秒。
// 相位差 DT = 路段长度 / 设计车速 —— 这就是绿波带的全部秘密。
export const BLOCK=28, V_DESIGN=10, DT=BLOCK/V_DESIGN;   // DT = 2.8s
export const G0=1.6, GREEN=5.6;
export const N_INT=10;                                    // z = -28 … -280
export const zInt=i=>-BLOCK*(i+1);
export const greenStart=i=>G0+i*DT;
export const greenEnd=i=>greenStart(i)+GREEN;
export const isGreen=(i,t)=>t>=greenStart(i)&&t<greenEnd(i);

// 主角车：匀速 = 设计车速，始终骑在绿波窗口内、偏前的位置
export const zHero=t=>8-V_DESIGN*t;
export const heroPassT=i=>(zInt(i)-8)/(-V_DESIGN);        // = 3.6 + 2.8i

// 绿波窗口（连续）：某时刻"以设计车速行驶就一定赶得上"的路段区间。
// 前沿以设计车速平滑前移，恰好在该路口变绿的那一刻经过它。
// 推导：车在 t 时刻位于 z、以设计车速前进，能在路口 i 赶上绿灯 ⇔ z ∈ [zLead(t), zLead(t)+BAND]。
export const BAND=GREEN*V_DESIGN;                        // 带宽 56 单位 = 5.6s 绿灯
export const zLead=t=>-V_DESIGN*t-(BLOCK-G0*V_DESIGN);   // = -10t - 12，在 t=greenStart(i) 时恰好经过 zInt(i)
export const bandAt=t=>({lead:zLead(t),trail:zLead(t)+BAND});

// 第二辆车：先在窗口内以设计车速行驶，T2_START 起加速到 2.4 倍设计车速，
// 冲出窗口前沿；前方路口尚未变绿，只能急刹停在停止线。
export const V2=24, T2_START=17.5, Z2_START=-170, ACCEL=20, T_ACC=(V2-V_DESIGN)/ACCEL;
const D_ACC=(V_DESIGN+V2)/2*T_ACC, Z_AT_BRAKE=Z2_START-D_ACC-V2*(1.5-T_ACC);
export const T2_BRAKE=19.0, T2_STOP=20.2, Z2_STOP=zInt(7)+4;   // 停在停止线
export function zCar2(t){
  if(t<=T2_START)return Z2_START+V_DESIGN*(T2_START-t);
  if(t>=T2_BRAKE){
    const u=clamp((t-T2_BRAKE)/(T2_STOP-T2_BRAKE));
    return Z_AT_BRAKE+(Z2_STOP-Z_AT_BRAKE)*(u*u*(3-2*u));
  }
  const dt=t-T2_START;
  return dt<T_ACC?Z2_START-(V_DESIGN*dt+.5*ACCEL*dt*dt):Z2_START-D_ACC-V2*(dt-T_ACC);
}
export const car2OutTime=t=>{for(let s=T2_START;s<22;s+=0.02)if(zCar2(s)<zLead(s))return +s.toFixed(2);return null};
export const car2RearTime=t=>{for(let s=T2_STOP;s<26;s+=0.02)if(zCar2(s)>zLead(s))return +s.toFixed(2);return null};
export const car2FrontTime=t=>{                          // 越过波前（绿波前沿）的时刻
  for(let s=T2_START;s<22;s+=0.02){const w=waveSpan(s);if(w&&zCar2(s)<w.zFront)return +s.toFixed(2)}
  return null;
};

export const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v));
export const ease=x=>{x=clamp(x);return x*x*(3-2*x)};
export const easeIn=x=>{x=clamp(x);return x*x};
export const lerp=(a,b,u)=>a+(b-a)*u;

export const SHOTS=[
  {start:0,end:5,id:'road',name:'夜路',sub:['一条笔直的大道','和一路的红绿灯']},
  {start:5,end:11,id:'run',name:'一路绿灯',sub:['第二个、第三个、第四个','都是绿的']},
  {start:11,end:18,id:'wave',name:'波',sub:['不是运气——','绿灯在按一个速度排队']},
  {start:18,end:22.5,id:'faster',name:'开快一点',sub:['那你就会跑到波前面去','前面全是红的']},
  {start:22.5,end:26,id:'order',name:'排队',sub:['绿波不是把绿灯变长','是让它们按一个速度排好队']},
];
export function shotAt(t){return SHOTS.find(s=>t>=s.start&&t<s.end)||SHOTS.at(-1)}
export function subtitle(t){return shotAt(t).sub}

export const SOUNDS=[
  {t:3.6,type:'pass',n:1},{t:6.4,type:'pass',n:2},{t:9.2,type:'pass',n:3},
  {t:12.0,type:'pass',n:4},{t:14.8,type:'pass',n:5},{t:17.6,type:'pass',n:6},
  {t:23.2,type:'pass',n:7},
  {t:19.0,type:'brake'},{t:20.2,type:'stop'},
  {t:24.5,type:'resolve'},
];
