import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createRequire} from 'node:module';
import {createHash} from 'node:crypto';
const root=path.dirname(fileURLToPath(import.meta.url));
const require=createRequire('D:/ai项目/ai动画/package.json');
const {openBrowser}=require('@remotion/renderer');
async function run(all=false){
 const browser=await openBrowser('chrome',{logLevel:'error'});
 try{
  const page=await browser.newPage({context:()=>null,logLevel:'error',indent:false,pageIndex:0,onBrowserLog:null,onLog:()=>{}});
  await page.setViewport({width:1080,height:1920,deviceScaleFactor:1});
  await page.goto({url:pathToFileURL(path.join(root,'film/index.html')).href,timeout:60000});
  return await page.evaluate(all=>{
   const at=t=>{window.renderAt(t);return document.getElementById('film').toDataURL('image/png')};
   const initial=at(2.3);at(38.1);const repeat=at(2.3);
   const issues=[],dist=(p,q)=>Math.hypot(p[0]-q[0],p[1]-q[1]);let momMax=0,babyMax=0,mouthMax=0;
   if(all)for(let f=0;f<990;f++){
    const t=f/24,s=window.renderAt(t),momD=dist([791,1193],s.mom.wrist),babyD=dist([385+(1-s.a.lift)*5,1419],s.kid.wrist);
    momMax=Math.max(momMax,momD);babyMax=Math.max(babyMax,babyD);
    if(momD>179||babyD>108)issues.push({f,momD,babyD});
    if(s.a.lift===1){const c=s.mom.cup;const rim=[c.x+22*Math.cos(c.tilt),c.y+22*Math.sin(c.tilt)];mouthMax=Math.max(mouthMax,dist(rim,c.mouth));}
    if(!s.a.held&&s.a.lift!==0)issues.push({f,issue:'moving prop without grasp'});
   }
   return{initial,repeat,pixel_repeat_equal:initial===repeat,frames_checked:all?990:0,reach_issues:issues,max_mother_reach:momMax,max_baby_reach:babyMax,max_sip_contact_error:mouthMax};
  },all);
 }finally{await browser.close({silent:true})}
}
const a=await run(true),b=await run(false),hash=s=>createHash('sha256').update(s).digest('hex');
const report={...a,initial:undefined,repeat:undefined,pixel_png_sha256:hash(a.initial),fresh_browser_pixel_equal:a.initial===b.initial,fresh_browser_pixel_png_sha256:hash(b.initial)};
fs.writeFileSync(path.join(root,'out/determinism-and-reach.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report));
