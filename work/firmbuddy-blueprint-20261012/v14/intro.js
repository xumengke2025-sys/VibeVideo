// Screen-space drafting table above the same paper shader. Absolute-time poses.
let filmTime=0;
const cardScenes=[['治理整改','信披与公司治理','合规治理'],['并购重组','资本运作新线索','资本运作'],['股东减持','股东服务新需求','股东服务'],['风险管理','汇率与商品风险','跨境经营'],['上市与分拆','企业成长新阶段','成长融资']];
function pen(ctx,color,width=1){ctx.strokeStyle=color;ctx.lineWidth=width;ctx.lineCap='round';ctx.lineJoin='round';}
function ot(ctx,s,x,y,size,color='#edf1ea',align='left',weight=400){ctx.font=`${weight} ${size}px ${FONT}`;ctx.fillStyle=color;ctx.textAlign=align;ctx.fillText(s,x,y);if(ctx.globalAlpha>=.64&&size>=24){const w=ctx.measureText(s).width,dx=align==='center'?-w/2:align==='right'?-w:0,m=ctx.getTransform(),q=[[x+dx,y-size*.95],[x+dx+w,y-size*.95],[x+dx+w,y+size*.22],[x+dx,y+size*.22]].map(([a,b])=>[(m.a*a+m.c*b+m.e)/scale,(m.b*a+m.d*b+m.f)/scale]);bounds.push({text:s,id:s,box:[Math.min(...q.map(v=>v[0])),Math.min(...q.map(v=>v[1])),Math.max(...q.map(v=>v[0])),Math.max(...q.map(v=>v[1]))],size});}}
function ol(ctx,q,color='#c1d3df',width=1){pen(ctx,color,width);ctx.beginPath();q.forEach(([x,y],i)=>i?ctx.lineTo(x,y):ctx.moveTo(x,y));ctx.stroke();}
function ring(ctx,x,y,r,color='#cfb77d',width=1){pen(ctx,color,width);ctx.beginPath();ctx.arc(x,y,r,0,TAU);ctx.stroke();}
function icon(ctx,x,y,id,s=1,color='#c9b17a'){
 ctx.save();ctx.translate(x,y);ctx.scale(s,s);pen(ctx,color,2);
 if(id===0){ring(ctx,0,0,39,color,2);ring(ctx,0,0,31,color,.7);ol(ctx,[[0,-22],[0,0],[18,12]],color,3);for(let i=0;i<12;i++){let a=i*TAU/12;ol(ctx,[[Math.cos(a)*34,Math.sin(a)*34],[Math.cos(a)*38,Math.sin(a)*38]],color);}}
 if(id===1){ol(ctx,[[-38,30],[-17,30],[-17,-21],[13,-21],[13,4],[37,4]],color,2);ol(ctx,[[25,-7],[37,4],[25,16]],color,2);ring(ctx,-38,30,5,color,2);ring(ctx,-17,-21,5,color,2);}
 if(id===2){for(let i=0;i<3;i++){ctx.save();ctx.translate(i*12-17,-i*9);ctx.strokeRect(-27,-23,54,60);ol(ctx,[[-17,-7],[15,-7]],color);ol(ctx,[[-17,7],[15,7]],color);ctx.restore();}}
 if(id===3){for(const [xx,yy] of [[-29,16],[0,-16],[29,16]]){ring(ctx,xx,yy,12,color,2);ol(ctx,[[xx-18,yy+30],[xx-18,yy+23],[xx+18,yy+23],[xx+18,yy+30]],color,2);}ol(ctx,[[-20,1],[-10,-9]],color);ol(ctx,[[10,-9],[20,1]],color);}
 if(id===4){ol(ctx,[[-33,30],[-33,-12],[0,-35],[33,-12],[33,30],[-33,30]],color,2);ol(ctx,[[-13,30],[-13,2],[13,2],[13,30]],color,2);}
 ctx.restore();
}
function card(ctx,i,x,y,w,h,r,alpha=1,morph=0){
 ctx.save();ctx.globalAlpha*=alpha;ctx.translate(x,y);ctx.rotate(r);
 const cream=1-morph,cut=mix(12,26*.95,morph),gold=morph<.7?'#c9ad72':'#d7e8f3';
 ctx.shadowColor=`rgba(0,10,23,${.4*cream})`;ctx.shadowBlur=22*cream;ctx.shadowOffsetY=15*cream;
 const rgb=(a,b)=>a.map((v,j)=>Math.round(mix(v,b[j],morph))).join(',');const fillAlpha=1-ease(p(morph,.8,1));
 const grad=ctx.createLinearGradient(-w/2,-h/2,w/2,h/2);grad.addColorStop(0,`rgba(${rgb([250,247,235],[21,52,81])},${fillAlpha})`);grad.addColorStop(1,`rgba(${rgb([228,221,200],[21,52,81])},${fillAlpha})`);
 ctx.fillStyle=grad;pen(ctx,gold,mix(1.5,2.2,morph));ctx.beginPath();ctx.moveTo(-w/2,-h/2);ctx.lineTo(w/2-cut,-h/2);ctx.lineTo(w/2,-h/2+cut);ctx.lineTo(w/2,h/2);ctx.lineTo(-w/2,h/2);ctx.closePath();ctx.fill();ctx.stroke();ctx.shadowColor='transparent';
 ctx.save();ctx.globalAlpha*=1-ease(p(morph,.02,.4));ctx.beginPath();ctx.rect(-w/2,-h/2,w,h);ctx.clip();
 pen(ctx,'#b9a170',.8);ctx.strokeRect(-w/2+9,-h/2+9,w-18,h-18);ctx.strokeRect(-w/2+14,-h/2+14,w-28,h-28);
 for(const sx of [-1,1])for(const sy of [-1,1]){ctx.save();ctx.translate(sx*(w/2-23),sy*(h/2-23));ctx.scale(-sx,-sy);ol(ctx,[[0,21],[0,0],[21,0]],'#b79a60',1.3);ring(ctx,5,5,3,'#b79a60');ctx.restore();}
 // Fine diagonal paper guilloche is deterministic, not a flattened screenshot.
 ctx.save();ctx.beginPath();ctx.rect(-w/2+19,-h/2+19,w-38,h-38);ctx.clip();for(let k=-h;k<w+h;k+=27)ol(ctx,[[k-w/2,-h/2],[k-w/2+h,h/2]],'rgba(188,169,131,.09)',.7);ctx.restore();
 const a=cardScenes[i],left=-w/2+31;
 ot(ctx,'SCENARIO / 0'+(i+1),left,-h/2+54,15,'#a28a56');
 icon(ctx,0,-h/2+134,i===2?4:i,.84,'#345570');
 ot(ctx,a[0],0,-h/2+228,i===4?33:37,'#183d5a','center',600);
 ol(ctx,[[left,-h/2+252],[w/2-31,-h/2+252]],'#c7b68f',1);
 ot(ctx,a[1],0,-h/2+295,24,'#587086','center');
 ot(ctx,a[2],0,-h/2+337,19,'#9c885e','center');
 ctx.fillStyle='#1c4261';ctx.fillRect(left,h/2-71,w-62,39);ot(ctx,'发现业务机会  →',0,h/2-44,19,'#f7f2e5','center');ctx.restore();
 if(morph>0){ctx.save();ctx.globalAlpha*=ease(p(morph,.45,.9));ring(ctx,-w/2+16*.95,-h/2+17*.95,5*.95,'#d7e8f3',1);ot(ctx,'示例客户信息',0,15*.95,34*.95,'#d7e8f3','center');ol(ctx,[[w/2-cut,-h/2],[w/2-cut,-h/2+cut],[w/2,-h/2+cut]],'#a5c4db',1);ctx.restore();}
 ctx.restore();
}
function opening(t){if(t>=11)return;const ctx=ov;ctx.save();ctx.scale(scale,scale);
 // Open drafting geometry: registration ticks, rails and a broad arc reserve motion space.
 const backdrop=1-ease(p(t,7.9,8.5));ctx.save();ctx.globalAlpha=backdrop;
 pen(ctx,'rgba(174,204,224,.16)',1);ctx.strokeRect(60,52,1800,976);
 for(let x=100;x<1860;x+=80)for(let y=100;y<1000;y+=80){ol(ctx,[[x-3,y],[x+3,y]],'rgba(185,211,226,.10)');ol(ctx,[[x,y-3],[x,y+3]],'rgba(185,211,226,.10)');}
 ot(ctx,'FIRMBUDDY  /  OPPORTUNITY ENGINE',96,98,18,'#8daec5');ot(ctx,'客户经营 · 业务场景',1824,98,18,'#8daec5','right');
 const painAlpha=1-ease(p(t,3.5,4.3));ctx.save();ctx.globalAlpha*=painAlpha;
 ot(ctx,'B 端商机，为什么总是慢一步？',960,226,64,'#f0f2e8','center',600);
 ot(ctx,'时间花在找资料，精力耗在做准备',960,291,29,'#9db9cf','center');
 const pains=[['商机收集耗时长','线索散落，搜集整理耗费精力'],['不知从何入手','发现信号，缺少清晰切入路径'],['专业支持难找','跨领域问题，需要专业判断'],['跟进准备重复','拜访材料、沟通重点反复整理']];
 pains.forEach((a,i)=>{const u=ease(p(t,.1+i*.21,.6+i*.21));const x=200+(i%2)*850,y=440+Math.floor(i/2)*250;ctx.save();ctx.globalAlpha*=u;ctx.translate(0,(1-u)*22);icon(ctx,x+57,y-12,i,1.03);ot(ctx,a[0],x+144,y-2,45,'#eef2eb');ot(ctx,a[1],x+144,y+53,27,'#a8c1d3');ol(ctx,[[x+144,y+88],[x+650,y+88]],'rgba(170,204,224,.35)');ot(ctx,'0'+(i+1),x+654,y+5,16,'#c2ab75','right');ctx.restore();});
 ot(ctx,'让时间回到判断需求、服务客户、推进合作上',960,942,30,'#d1bb87','center');ctx.restore();
 const cardsAlpha=ease(p(t,3.7,4.5));ctx.save();ctx.globalAlpha*=cardsAlpha*(1-ease(p(t,7.6,8.1)));
 ot(ctx,'商机查询',960,211,63,'#f3f0e5','center',600);ctx.save();ctx.globalAlpha*=1-ease(p(t,6.4,6.9));ot(ctx,'多种业务场景，从一张商机卡开始',960,270,29,'#b1c7d7','center');ctx.restore();
 pen(ctx,'rgba(202,178,119,.35)',1.2);ctx.beginPath();ctx.ellipse(960,799,817,170,0,Math.PI,TAU);ctx.stroke();
 ctx.save();ctx.globalAlpha*=1-ease(p(t,6.4,6.9));ot(ctx,'治理整改  ·  并购重组  ·  股东服务  ·  风险管理  ·  上市与分拆',960,978,26,'#b5cad9','center');ctx.restore();ctx.restore();ctx.restore();
 const reveal=ease(p(t,3.8,4.8)),extract=ease(p(t,6.4,7.7)),travel=ease(p(t,8,10.7));
 for(const i of [0,4,1,3]){const d=i-2;card(ctx,i,960+d*315,655+Math.abs(d)*28+(1-reveal)*430,288,449,d*.085,cardsAlpha*(1-ease(p(t,7.5,8.6))),0);}
 if(cardsAlpha>0){
   const q=[[-110,-73],[510,-73],...paths.query.slice(1).map(([x,y])=>[x-1050,y-1070])];const v=pathPoint(q,ease(p(T,1.2,5.8)));const target=S(v[0]+1050,v[1]+1070).map(x=>x/scale);
   const x=mix(960,target[0],travel),y=mix(620-112*extract+(1-reveal)*430,target[1],travel),w=mix(326+24*extract,270*cam.z/scale,travel),h=mix(488+16*extract,104*cam.z/scale,travel);
   card(ctx,2,x,y,w,h,-.025*Math.sin(extract*Math.PI)*(1-travel),cardsAlpha*(1-ease(p(t,10.7,11))),travel);
   ctx.save();ctx.globalAlpha=extract*(1-ease(p(t,7.9,8.5)));ot(ctx,'以股东减持为例，进入专业研判',960,978,32,'#e4d2a6','center');ctx.restore();
 }
 ctx.restore();
}

// Editorial drafting notes outside the camera: problem and practical business result.
function businessNarrative(t){const q=plan.business_messages.find(q=>t>=q.start&&t<q.end);if(!q)return;
 const a=ease(p(t,q.start,q.start+.32))*(1-ease(p(t,q.end-.32,q.end))),ctx=ov;
 ctx.save();ctx.scale(scale,scale);ctx.globalAlpha=a;
 const shade=(y,h)=>{const z=ctx.createLinearGradient(0,y,0,y+h);z.addColorStop(0,'rgba(5,23,42,.0)');z.addColorStop(.45,'rgba(5,23,42,.94)');z.addColorStop(1,'rgba(5,23,42,.94)');ctx.fillStyle=z;ctx.fillRect(0,y,1920,h);};
 ctx.fillStyle='rgba(5,23,42,.9)';ctx.fillRect(0,0,1920,105);
 ol(ctx,[[96,108],[1824,108]],'rgba(190,171,117,.43)',1);
 ot(ctx,q.pain,960,74,36,'#e4c992','center',500);
 shade(987,93);ot(ctx,q.result,960,1044,34,'#edf2eb','center',400);
 ctx.restore();}
