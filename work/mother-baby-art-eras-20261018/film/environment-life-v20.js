/* Local semantic motion fields. Pots, shelves, walls, frames and furniture are
 * untouched. Only registered foliage / textile pixels and their 10px edge
 * neighbourhood are sampled by the tiny elastic displacement. Absolute time. */
(()=>{'use strict';
const W=1080,H=1920,mk=()=>Object.assign(document.createElement('canvas'),{width:W,height:H});
// x,y,w,h, fixed root y, excursion in px, semantic paint selector.
const regions=[
 [],
 [[0,550,155,550,1100,7,'green'],[900,600,180,520,1120,6,'green']],
 [[920,300,160,500,800,5,'dark']],
 [[0,640,240,400,1040,7,'green'],[820,400,260,690,1090,6,'green']],
 [[0,650,225,460,1110,6,'green'],[925,760,155,400,1160,5,'green']],
 [[805,275,145,330,275,7,'red'],[0,760,220,445,1205,6,'green'],[910,850,170,350,1200,5,'green']],
 [[0,790,250,330,1120,5,'plant'],[825,740,255,385,1125,5,'plant']],
 [[0,650,180,365,1015,6,'green'],[820,690,260,335,1025,6,'green']],
 [[0,55,350,390,35,6,'ink'],[830,420,245,295,715,5,'ink'],[580,65,44,200,65,4,'dark']],
 [[0,550,180,450,1000,5,'green'],[920,580,160,460,1040,5,'green'],[650,650,225,480,650,5,'cloth']],
 [[825,375,255,430,375,6,'green'],[0,710,255,355,1065,5,'green']],
 [[830,140,250,600,140,6,'green'],[0,730,275,385,1115,5,'plant']],
 [[860,300,220,490,300,6,'green'],[0,890,235,375,1265,5,'green']],
 [[930,380,150,420,380,6,'green'],[850,860,230,360,1220,6,'green']],
 [[938,300,142,480,300,5,'dark'],[0,900,280,245,1145,5,'dark']],
 [[855,300,225,500,300,7,'green'],[0,770,190,365,1135,5,'green']],
 [[850,370,230,450,370,7,'green'],[0,890,300,350,1240,5,'green']],
 [[850,365,230,420,365,5,'green'],[0,900,300,235,1135,4,'green']],
 [[900,365,180,440,365,7,'green'],[0,950,310,350,1300,6,'plant']],
 [[865,355,215,435,355,7,'green'],[0,1000,230,270,1270,5,'green']]
];
const source=mk(),sg=source.getContext('2d'),cv=mk(),gl=cv.getContext('webgl',{alpha:false,antialias:false,preserveDrawingBuffer:true});
if(!gl)throw Error('WebGL required for local foliage sampling');
function shader(kind,s){const q=gl.createShader(kind);gl.shaderSource(q,s);gl.compileShader(q);if(!gl.getShaderParameter(q,gl.COMPILE_STATUS))throw Error(gl.getShaderInfoLog(q));return q}
const vs=shader(gl.VERTEX_SHADER,'attribute vec2 p;varying vec2 uv;void main(){uv=(p+1.0)*.5;gl_Position=vec4(p.x,-p.y,0.,1.);}');
const fs=shader(gl.FRAGMENT_SHADER,`precision highp float;varying vec2 uv;uniform sampler2D src;uniform sampler2D field;uniform float t;uniform float pix;void main(){vec4 m=texture2D(field,uv);float wave=sin(t*1.65+m.g*6.28318);float dx=m.r*9.0*wave;float dy=m.r*1.4*sin(t*1.65+m.g*6.28318+.8);if(pix>.5){dx=floor(dx/2.+.5)*2.;dy=0.;}vec2 at=uv+vec2(dx/1080.,dy/1920.);gl_FragColor=texture2D(src,at);}`);
const prog=gl.createProgram();gl.attachShader(prog,vs);gl.attachShader(prog,fs);gl.linkProgram(prog);if(!gl.getProgramParameter(prog,gl.LINK_STATUS))throw Error(gl.getProgramInfoLog(prog));gl.useProgram(prog);
const buff=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buff);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,-1,1,1,-1,1,1]),gl.STATIC_DRAW);const loc=gl.getAttribLocation(prog,'p');gl.enableVertexAttribArray(loc);gl.vertexAttribPointer(loc,2,gl.FLOAT,false,0,0);
function texture(unit){gl.activeTexture(gl.TEXTURE0+unit);const x=gl.createTexture();gl.bindTexture(gl.TEXTURE_2D,x);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.LINEAR);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MAG_FILTER,gl.LINEAR);return x}
const tex=texture(0),field=texture(1);gl.uniform1i(gl.getUniformLocation(prog,'src'),0);gl.uniform1i(gl.getUniformLocation(prog,'field'),1);
const cache=new Map();let current=-1;
function accepts(r,g,b,k){if(k==='green')return g>r*.96&&g>b*1.08&&Math.max(r,g,b)-Math.min(r,g,b)>12;if(k==='plant')return (g>r*.92&&g>b*1.07)||(r>175&&g>160&&b<g*.88);if(k==='dark')return Math.max(r,g,b)<130;if(k==='ink')return g>r*.94&&Math.max(r,g,b)<160;if(k==='red')return r>g*1.3&&r>b*1.35;return r>175&&g>150&&b>100;}
function prepare(im,i){if(cache.has(i))return cache.get(i);const s=mk(),g=s.getContext('2d',{willReadFrequently:true});g.drawImage(im,0,0,W,H);const data=g.getImageData(0,0,W,H).data,f=mk(),fg=f.getContext('2d'),fd=fg.createImageData(W,H);
 for(let n=0;n<regions[i].length;n++){const[x,y,w,h,root,amp,kind]=regions[i][n],mask=mk(),mg=mask.getContext('2d'),md=mg.createImageData(W,H);for(let yy=y;yy<Math.min(H,y+h);yy++)for(let xx=x;xx<Math.min(W,x+w);xx++){const k=(yy*W+xx)*4;if(accepts(data[k],data[k+1],data[k+2],kind))md.data[k+3]=255}mg.putImageData(md,0,0);const spread=mk(),pg=spread.getContext('2d',{willReadFrequently:true});pg.filter='blur(6px)';pg.drawImage(mask,0,0);pg.filter='none';pg.drawImage(mask,0,0);const sd=pg.getImageData(0,0,W,H).data;
  for(let yy=Math.max(0,y-14);yy<Math.min(H,y+h+14);yy++)for(let xx=Math.max(0,x-14);xx<Math.min(W,x+w+14);xx++){const k=(yy*W+xx)*4,rootWeight=Math.min(1,Math.abs(yy-root)/Math.max(70,h*.8)),edge=Math.max(0,Math.min(1,(xx-x)/14,(x+w-xx)/14,(yy-y)/14,(y+h-yy)/14)),v=sd[k+3]/255*rootWeight*rootWeight*edge*amp/9*255;if(v>fd.data[k]){fd.data[k]=v;fd.data[k+1]=(i*.137+n*.29)%1*255;fd.data[k+3]=255}}
  mask.width=spread.width=1;
 }fg.putImageData(fd,0,0);cache.set(i,f);if(cache.size>4){const k=cache.keys().next().value;cache.get(k).width=1;cache.delete(k)}return f;}
function draw(c,im,t,i,cel){sg.resetTransform();sg.clearRect(0,0,W,H);STOP_ENV_V15.draw(sg,im,t,i,cel);if(!regions[i].length){c.drawImage(source,0,0);return}const m=prepare(im,i);gl.useProgram(prog);gl.viewport(0,0,W,H);gl.activeTexture(gl.TEXTURE0);gl.bindTexture(gl.TEXTURE_2D,tex);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,i===17?gl.NEAREST:gl.LINEAR);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MAG_FILTER,i===17?gl.NEAREST:gl.LINEAR);gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,gl.RGBA,gl.UNSIGNED_BYTE,source);gl.activeTexture(gl.TEXTURE1);gl.bindTexture(gl.TEXTURE_2D,field);if(current!==i){gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,gl.RGBA,gl.UNSIGNED_BYTE,m);current=i}gl.uniform1f(gl.getUniformLocation(prog,'t'),t);gl.uniform1f(gl.getUniformLocation(prog,'pix'),i===17?1:0);gl.drawArrays(gl.TRIANGLES,0,6);c.drawImage(cv,0,0);}
window.ENV_LIFE_V20={draw,regions,prepare,description:'independently rooted leaves, hanging vines, lantern tassel and curtain hem; fixed furniture and supports; absolute-time local deformation, excursion <=7px'};
})();
