export const FILM={width:1080,height:1920,fps:30,duration:45,seed:20261011};
export const SHOTS=[
{start:0,end:4,id:'home',name:'家庭排水',focus:0,sub:['家庭排水']},
{start:4,end:9,id:'arrival',name:'排水管网',focus:.5,sub:['排水管网']},
{start:9,end:14,id:'screen',name:'筛选杂物',focus:1,sub:['筛选杂物']},
{start:14,end:18,id:'grit',name:'沉降砂粒',focus:2,sub:['沉降砂粒']},
{start:18,end:25,id:'bio',name:'生物处理',focus:3,sub:['生物处理']},
{start:25,end:31,id:'settle',name:'沉淀分离',focus:4,sub:['沉淀分离']},
{start:31,end:36,id:'return',name:'污泥回流',focus:4,sub:['污泥回流']},
{start:36,end:41,id:'polish',name:'过滤消毒',focus:5,sub:['过滤消毒']},
{start:41,end:45,id:'out',name:'达标排放',focus:6,sub:['达标排放']}
];
export const SOUNDS=[{t:1,type:'flush'},{t:10.1,type:'rake'},{t:12.6,type:'rake'},{t:18.5,type:'air'},{t:31.4,type:'return'},{t:36.6,type:'filter'},{t:38.7,type:'disinfect'},{t:41.5,type:'resolve'}];
export const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v));
export const ease=x=>{x=clamp(x);return x*x*(3-2*x)};
export function shotAt(t){return SHOTS.find(s=>t>=s.start&&t<s.end)||SHOTS.at(-1)}
export function subtitle(t){if(t>=34&&t<36)return ['剩余污泥处理'];return shotAt(t).sub}
