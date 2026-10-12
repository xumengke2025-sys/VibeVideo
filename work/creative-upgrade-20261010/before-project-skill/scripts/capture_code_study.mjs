// Replay bundled MIT drawing sources. Imports/fonts are adapted; drawing modules remain byte-identical.
import fs from 'node:fs';import path from 'node:path';import http from 'node:http';import {fileURLToPath} from 'node:url';import {createRequire} from 'node:module';import {createHash} from 'node:crypto';
const a=Object.fromEntries(process.argv.slice(2).map(s=>{const i=s.indexOf('=');return [s.slice(2,i<0?undefined:i),i<0?true:s.slice(i+1)];}));
const studies=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../assets/code-studies'),req=createRequire(path.join(studies,'package.json'));
const mode=a.study||'beach';if(!['beach','reel'].includes(mode))throw Error('Use --study=beach or --study=reel');
const study=path.join(studies,mode==='beach'?'particle-beach':'work-reel-26');
const contentRoot=mode==='beach'?study:path.join(study,'skills/kinetic-reel/examples/work-reel-26');
const engine=a.three||path.dirname(req.resolve(mode==='beach'?'three/package.json':'three160/package.json'));
const {chromium}=a.playwright?req(a.playwright):req('playwright-core');
const fontDir=a['font-dir']?path.resolve(a['font-dir']):null;
const out=path.resolve(a.out||'out/code-study-'+mode);fs.mkdirSync(out,{recursive:true});
const evidence={mode,source:JSON.parse(fs.readFileSync(path.join(study,'SOURCE.json'),'utf8')),adaptation:fontDir?'local font cache + local engine':'system font substitution + local engine',requests:[],blocked:[],errors:[]};
const mime={'.html':'text/html','.js':'text/javascript','.mjs':'text/javascript','.json':'application/json','.woff2':'font/woff2','.ttf':'font/ttf'};
const server=http.createServer((req,res)=>{const u=new URL(req.url,'http://local');let p,body;
 try {
  if(u.pathname==='/'){
   p=fontDir?path.join(fontDir,mode+'.html'):mode==='beach'?path.join(study,'index.html'):path.join(study,'skills/kinetic-reel/template/reel/index.html');
   let html=fs.readFileSync(p,'utf8').replaceAll('https://cdn.jsdelivr.net/npm/three@0.169.0/','/engine/').replaceAll('/three169/','/engine/');
   if(!fontDir)html=html.replace(/<link[^>]+https:\/\/fonts\.[^>]+>/g,'');
   body=Buffer.from(html);
  }else {
   const mount=u.pathname.startsWith('/engine/')?engine:u.pathname.startsWith('/three160/')?engine:u.pathname.startsWith('/adapter/')?fontDir:contentRoot;
   const relative=u.pathname.startsWith('/engine/')?u.pathname.slice(8):u.pathname.startsWith('/three160/')?u.pathname.slice(10):u.pathname.startsWith('/adapter/')?u.pathname.slice(9):u.pathname.slice(1);
   if(!mount)throw Error('No font cache');p=path.resolve(mount,decodeURIComponent(relative));if(!p.startsWith(path.resolve(mount)+path.sep))throw Error('Invalid path');
   body=fs.readFileSync(p);
   if(mode==='reel'&&u.pathname==='/reel.js')body=Buffer.from(body.toString().replace('../../site/vendor/three/three.module.js','/engine/build/three.module.js'));
  }
  res.setHeader('Content-Type',mime[path.extname(p)]||'application/octet-stream');res.end(body);
 }catch{res.writeHead(404);res.end('missing');}
});
let browser;
try{
 await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin=`http://127.0.0.1:${server.address().port}`;
 browser=await chromium.launch({executablePath:a.chrome||process.env.CHROME_PATH||(process.platform==='win32'?'C:/Program Files/Google/Chrome/Application/chrome.exe':undefined),headless:true,args:process.platform==='win32'?['--use-angle=d3d11']:[]});
 const width=Number(a.width||960),page=await browser.newPage({viewport:{width,height:Math.round(width/2.39)},deviceScaleFactor:1});
 page.on('pageerror',e=>evidence.errors.push(e.message));await page.route('**/*',async route=>{const u=route.request().url();evidence.requests.push(u);if(!u.startsWith(origin+'/')){evidence.blocked.push(u);return route.abort();}return route.continue();});
 await page.goto(origin+'/?render'+(mode==='beach'?'#trailer':''),{timeout:120000});await page.waitForFunction(mode=>mode==='beach'?!!window.__trailer:window.ready,mode,{timeout:180000});
 evidence.info=await page.evaluate(mode=>mode==='beach'?window.__trailer.info():{duration:window.DUR,fps:30,gpu:window.gpuInfo()},mode);
 async function capture(t,name){const url=await page.evaluate(async({mode,t,width,sub})=>{const src=mode==='beach'?await window.__trailer.frame(Math.round(t*30),{sub,quality:.95}):await window.renderAt(t,'image/jpeg',.95);const im=new Image();im.src=src;await im.decode();const c=document.createElement('canvas');c.width=width;c.height=Math.round(width*9/16);c.getContext('2d').drawImage(im,0,0,c.width,c.height);return c.toDataURL('image/jpeg',.95);},{mode,t,width,sub:Number(a.sub||1)});const bytes=Buffer.from(url.split(',')[1],'base64');fs.writeFileSync(path.join(out,name+'.jpg'),bytes);return createHash('sha256').update(bytes).digest('hex');}
 const times=a.times?a.times.split(',').map(Number):mode==='beach'?evidence.info.shots.map(s=>s.start+s.dur*.5):[2.5,9,16.2,42.75,48.5,50.25,64.5,78.8];
 for(let i=0;i<times.length;i++)await capture(times[i],'still-'+String(i).padStart(2,'0'));
 if(a.range){const [start,end]=a.range.split(':').map(Number);if(start<0||end>evidence.info.duration||end<=start)throw Error('Invalid range');const n=Math.round((end-start)*30);for(let i=0;i<n;i++){await capture(start+i/30,'frame-'+String(i).padStart(4,'0'));if(i%30===0)console.log(`capture ${i}/${n}`);}evidence.range={start,end,frames:n,fps:30,sub:Number(a.sub||1)};}
 const t=times[0],first=await capture(t,'repeat-a');await capture(Math.min(t+.5,evidence.info.duration-1/30),'repeat-other');const second=await capture(t,'repeat-b');evidence.repeat={t,first,second,identical:first===second};
 evidence.requests=[...new Set(evidence.requests)];fs.writeFileSync(path.join(out,'capture-evidence.json'),JSON.stringify(evidence,null,2));
 if(evidence.errors.length||evidence.blocked.length)throw Error('See capture-evidence.json');console.log(JSON.stringify({out,repeat:evidence.repeat.identical,fontMode:evidence.adaptation}));
}finally{if(browser)await browser.close();server.close();}
