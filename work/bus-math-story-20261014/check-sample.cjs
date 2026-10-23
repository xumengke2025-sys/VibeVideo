const fs=require('fs'),path=require('path'),cp=require('child_process');
const sharp=require('C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const {renderAt}=require('./scene.cjs');
const root=__dirname,plan=JSON.parse(fs.readFileSync(path.join(root,'timeline.json')));
const ff=path.resolve(root,'../../node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe');
async function main(){
 const frames=[];
 for(const t of [1,3,5,8]){
  const f=path.join(root,'stills',`sample-${t}.png`);
  cp.execFileSync(ff,['-v','error','-y','-ss',String(t),'-i',path.join(root,'out/sample-music-only.mp4'),'-frames:v','1',f],{windowsHide:true});
  frames.push(await sharp(f).resize(270,480).png().toBuffer());
 }
 for(const id of ['flag','mapbus','gap','ending']){
  const stage=plan.stages.find(s=>s.id===id),t=stage.end-1;
  frames.push(await sharp(Buffer.from(renderAt(t,plan))).resize(270,480).png().toBuffer());
 }
 await sharp({create:{width:1080,height:960,channels:3,background:'#f5ecd9'}}).composite(frames.map((input,i)=>({input,left:i%4*270,top:Math.floor(i/4)*480}))).png().toFile(path.join(root,'stills/music-only-check.png'));
 console.log('sample contact sheet complete');
}
main().catch(e=>{console.error(e);process.exitCode=1});
