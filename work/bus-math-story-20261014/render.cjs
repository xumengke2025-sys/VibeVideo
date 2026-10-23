const fs=require('fs'),path=require('path'),cp=require('child_process');
const sharp=require('C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const sceneArg=process.argv.indexOf('--scene');
const {renderAt}=require(sceneArg<0?'./scene.cjs':'./'+process.argv[sceneArg+1]);const ROOT=__dirname;
const planArg=process.argv.indexOf('--plan');
const plan=JSON.parse(fs.readFileSync(path.join(ROOT,planArg<0?'timeline.json':process.argv[planArg+1]),'utf8'));
const ff=path.resolve(ROOT,'../../node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe');
sharp.concurrency(1);sharp.cache({memory:48,items:24});
function arg(k,def){const i=process.argv.indexOf(k);return i<0?def:process.argv[i+1];}
const width=Number(arg('--width',1080)),fps=Number(arg('--fps',plan.fps)),start=Number(arg('--start',0)),duration=Number(arg('--duration',plan.duration));
const output=path.resolve(ROOT,arg('--out','out/bus-math-story-portrait-v1.mp4'));
async function main(){
 fs.mkdirSync(path.dirname(output),{recursive:true});
 if(process.argv.includes('--stills')){
  const frames=plan.stages.map(s=>({id:s.id,t:s.start+Math.min(8,(s.end-s.start)*.65)}));
  fs.mkdirSync(path.join(ROOT,'stills'),{recursive:true});
  for(const f of frames){await sharp(Buffer.from(renderAt(f.t,plan))).resize(width).png().toFile(path.join(ROOT,'stills',`${f.id}.png`));}
  console.log(JSON.stringify({stills:frames.length,width}));return;
 }
 const frames=Math.round(duration*fps),height=Math.round(width*16/9),args=['-v','warning','-y','-f','image2pipe','-c:v','png','-framerate',String(fps),'-i','pipe:0','-ss',String(start),'-i',path.join(ROOT,plan.audio||'audio/music-only.wav'),'-t',String(frames/fps),'-c:v','libx264','-threads:v','1','-preset','fast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart',output];
 const proc=cp.spawn(ff,args,{windowsHide:true,stdio:['pipe','ignore','pipe']});let err='';proc.stderr.on('data',d=>{err=(err+d).slice(-6000)});const completion=new Promise((resolve,reject)=>proc.on('close',code=>code===0?resolve():reject(new Error(err))));proc.stdin.on('error',()=>{});
 const begin=Date.now();
 for(let f=0;f<frames;f++){
  const svg=renderAt(start+f/fps,plan),data=await sharp(Buffer.from(svg)).resize(width,height).png({compressionLevel:1}).toBuffer();
  if(!proc.stdin.write(data))await new Promise(r=>proc.stdin.once('drain',r));
  if(f%(fps*5)===0){const info={frame:f,total:frames,percent:+(100*f/frames).toFixed(1),elapsedSeconds:Math.round((Date.now()-begin)/1000)};console.log(JSON.stringify(info));fs.writeFileSync(path.join(ROOT,'render-progress.json'),JSON.stringify(info));}
 }
 proc.stdin.end();await completion;
 fs.writeFileSync(path.join(ROOT,'render-record.json'),JSON.stringify({output,width,height,fps,start,duration:frames/fps,frames,engine:'SVG from explicit time, Sharp rasterization, FFmpeg H.264/AAC',elapsedSeconds:Math.round((Date.now()-begin)/1000)},null,2));
 console.log('completed',output);
}
main().catch(e=>{console.error(e.message);process.exitCode=1});
