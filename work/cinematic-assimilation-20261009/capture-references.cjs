// Windows adapter: original drawing modules unchanged; only imports/fonts/output size are localized.
const {chromium}=require('C:/CodexTemp/pdoom-review-20261008/app/node_modules/playwright-core');
const fs=require('fs'),path=require('path'),http=require('http'),crypto=require('crypto');
const base='C:/CodexTemp/vibe-github-20261009', root=__dirname;
const mode=process.argv[2]||'beach';
const mime={'.html':'text/html','.js':'text/javascript','.mjs':'text/javascript','.json':'application/json','.woff2':'font/woff2','.css':'text/css'};
const server=http.createServer((req,res)=>{
  const u=new URL(req.url,'http://local');let p;
  if(u.pathname==='/')p=path.join(root,'reference-adapter',mode+'.html');
  else if(u.pathname.startsWith('/adapter/'))p=path.join(root,'reference-adapter',u.pathname.slice(9));
  else if(u.pathname.startsWith('/three169/'))p=path.join(base,'runtime/node_modules/three',u.pathname.slice(10));
  else if(u.pathname.startsWith('/three160/'))p=path.join(base,'runtime/node_modules/three160',u.pathname.slice(10));
  else p=path.join(base,mode==='beach'?'particle-beach':'opus-video-skills/skills/kinetic-reel/examples/work-reel-26',u.pathname);
  try {let body=fs.readFileSync(p);if(mode==='reel'&&u.pathname==='/reel.js')body=Buffer.from(body.toString().replace('../../site/vendor/three/three.module.js','/three160/build/three.module.js'));
    res.setHeader('Content-Type',mime[path.extname(p)]||'application/octet-stream');res.end(body);
  }catch(e){res.statusCode=404;res.end('missing');}
});
(async()=>{await new Promise(r=>server.listen(0,'127.0.0.1',r));
  const browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true,args:['--use-angle=d3d11','--disable-background-timer-throttling']});
  const page=await browser.newPage({viewport:{width:960,height:402},deviceScaleFactor:1});
  const errors=[],requests=[],blocked=[];
  page.on('pageerror',e=>errors.push(e.message));
  await page.route('**/*',async route=>{const url=route.request().url();requests.push(url);if(!url.startsWith('http://127.0.0.1:')){blocked.push(url);return route.abort();}await route.continue();});
  await page.goto(`http://127.0.0.1:${server.address().port}/?render${mode==='beach'?'#trailer':''}`,{timeout:120000});
  await page.waitForFunction(m=>m==='beach'?!!window.__trailer:window.ready,mode,{timeout:180000});
  const info=await page.evaluate(m=>m==='beach'?window.__trailer.info():{duration:window.DUR,fps:30,gpu:window.gpuInfo()},mode);
  const out=path.join(root,'reference-output',mode);fs.mkdirSync(out,{recursive:true});
  fs.writeFileSync(path.join(out,'info.json'),JSON.stringify(info,null,2));console.log(mode+' ready '+JSON.stringify({duration:info.duration,shots:info.shots?.length}));
  async function frame(t,name){const data=await page.evaluate(async ({mode,t})=>{
    const src=mode==='beach'?await window.__trailer.frame(Math.round(t*30),{sub:1,quality:.92}):await window.renderAt(t,'image/jpeg',.92);
    // reel stays 1920x1080 internally; scale only the captured output.
    if(mode==='beach')return src;
    const im=new Image();im.src=src;await im.decode();const c=document.createElement('canvas');c.width=960;c.height=540;c.getContext('2d').drawImage(im,0,0,960,540);return c.toDataURL('image/jpeg',.94);
  },{mode,t});const bytes=Buffer.from(data.split(',')[1],'base64');fs.writeFileSync(path.join(out,name+'.jpg'),bytes);return crypto.createHash('sha256').update(bytes).digest('hex');}
  const times=mode==='beach'?info.shots.map(s=>+(s.start+s.dur*.5).toFixed(3)):[2.5,5,9,12.25,16.2,20.25,42.75,48.5,50.25,64.5,78.8];
  for(let i=0;i<times.length;i++){await frame(times[i],`still-${String(i).padStart(2,'0')}`);console.log('still '+times[i]);}
  const start=mode==='beach'?info.shots.find(s=>s.id==='pilings-rise').start:16;
  const n=mode==='beach'?60:30;
  for(let i=0;i<n;i++){await frame(start+i/30,`frame-${String(i).padStart(4,'0')}`);if(i%15===0)console.log('range '+i+'/'+n);}
  const t=mode==='beach'?start+1:16.25;
  const a=await frame(t,'repeat-a');await frame(t+.5,'repeat-other');const b=await frame(t,'repeat-b');
  const evidence={mode,info,times,range:{start,frames:n,fps:30,sub:1},repeat:{t,a,b,identical:a===b},errors,blocked,requests:[...new Set(requests)],adaptation:'local fonts + engine imports; original drawing code unchanged; 960px capture; beach sub=1'};
  fs.writeFileSync(path.join(out,'capture-evidence.json'),JSON.stringify(evidence,null,2));console.log('evidence '+JSON.stringify({errors,blocked,repeatIdentical:a===b}));
  await browser.close();server.close();
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
