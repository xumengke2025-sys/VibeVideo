const path=require('path'),cp=require('child_process');
const sharp=require('C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const root=__dirname,ff=path.resolve(root,'../../node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe');
(async()=>{
 const images=[];
 for(const t of [3,9.5,12.5,16.5,22,27.5]){
  const file=path.join(root,'stills',`short-${t}.png`);
  cp.execFileSync(ff,['-v','error','-y','-ss',String(t),'-i',path.join(root,'out/bus-math-story-30s.mp4'),'-frames:v','1',file],{windowsHide:true});
  images.push(await sharp(file).resize(360,640).png().toBuffer());
 }
 await sharp({create:{width:1080,height:1280,channels:3,background:'#f5ecd9'}}).composite(images.map((input,i)=>({input,left:i%3*360,top:Math.floor(i/3)*640}))).png().toFile(path.join(root,'stills/short-check.png'));
 console.log('six decoded frames saved');
})().catch(e=>{console.error(e);process.exitCode=1});
