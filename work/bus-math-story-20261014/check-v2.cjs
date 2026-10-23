const fs=require('fs'),path=require('path'),cp=require('child_process');
const sharp=require('C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const root=__dirname,ff=path.resolve(root,'../../node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe');
const groups={run:[2.1,2.3,2.5,2.7,2.9,3.1],transition:[13.9,14.1,14.2,14.3,14.45,14.65],highfive:[27,27.2,27.4,27.6,27.8,28],overview:[1,5.8,9.5,16.5,22,28.5]};
(async()=>{
 for(const [name,times] of Object.entries(groups)){
  const images=[];const full=name==='overview',height=full?640:380;
  for(const t of times){
   const file=path.join(root,'stills',`v2-${name}-${t}.png`);
   cp.execFileSync(ff,['-v','error','-y','-ss',String(t),'-i',path.join(root,'out/bus-math-story-30s-v2.mp4'),'-frames:v','1',file],{windowsHide:true});
   const base=sharp(file);if(!full)base.extract({left:48,top:326,width:984,height:958});
   images.push(await base.resize(360,full?640:350).extend(full?{}:{bottom:30,background:'#f5ecd9'}).composite(full?[]:[{input:Buffer.from(`<svg width="360" height="30"><text x="180" y="23" text-anchor="middle" font-family="Arial" font-size="20">${t.toFixed(2)} s</text></svg>`),left:0,top:350}]).png().toBuffer());
  }
  await sharp({create:{width:1080,height:height*2,channels:3,background:'#f5ecd9'}}).composite(images.map((input,i)=>({input,left:i%3*360,top:Math.floor(i/3)*height}))).png().toFile(path.join(root,`stills/v2-${name}-check.png`));
 }
 console.log('24 decoded frames in 4 contact sheets');
})().catch(e=>{console.error(e.message);process.exitCode=1});
