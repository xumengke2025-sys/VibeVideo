import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
const root=path.dirname(fileURLToPath(import.meta.url));
const version=process.argv[2]||'reference-v5';
const deliveryMode=process.argv[3]||'ai_review_once';
const config=JSON.parse(fs.readFileSync(path.join(root,'film/out/final-'+version+'/config.json')));
const dst=path.join(root,'delivery',version);
fs.mkdirSync(dst,{recursive:true});
const copy=(relative)=>{const target=path.join(dst,relative);fs.mkdirSync(path.dirname(target),{recursive:true});fs.copyFileSync(path.join(root,relative),target)};
for(const name of ['film.js','art.js','upper-scenery.js','timeline.js','audio.mjs','audio.wav','sound-events.json','index.html','server.mjs','production-brief.md','frame-rig-'+config.count+'.json'])copy('film/'+name);
for(const name of fs.readdirSync(path.join(root,'film/vendor')))copy('film/vendor/'+name);
if(fs.existsSync(path.join(root,'film/audio-assets/ATTRIBUTION.md'))){
  for(const name of ['ATTRIBUTION.md','sources.json','heron-Sangli.wav','heron-Sangli-48k.wav','222184.mp3','222168.mp3','205974.mp3','222190.mp3','222255.mp3','222184-48k.wav','222168-48k.wav','205974-48k.wav','222190-48k.wav','222255-48k.wav'])copy('film/audio-assets/'+name);
  for(const name of fs.readdirSync(path.join(root,'film/audio-stems')))copy('film/audio-stems/'+name);
}
for(const name of fs.readdirSync(path.join(root,'assets')).filter(f=>f.endsWith('.png')))copy('assets/'+name);
let renderer=fs.readFileSync(path.join(root,'film/render.mjs'),'utf8');
renderer=renderer.replace("from'../../sand-journey-20261010/node_modules/playwright-core/index.mjs'","from'playwright-core'");
renderer=renderer.replace("const FF='D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe',FP=FF.replace('ffmpeg.exe','ffprobe.exe');", "const FF=process.env.FFMPEG_PATH||'ffmpeg',FP=process.env.FFPROBE_PATH||'ffprobe';");
renderer=renderer.replace("executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'","executablePath:process.env.CHROME_PATH||'C:/Program Files/Google/Chrome/Application/chrome.exe'");
fs.writeFileSync(path.join(dst,'film/render.mjs'),renderer);
fs.writeFileSync(path.join(dst,'package.json'),JSON.stringify({name:'night-heron-shadow-puppet',private:true,type:'module',scripts:{preview:'node film/server.mjs',audio:'node film/audio.mjs',render:'node film/render.mjs --mode=final --version=custom',stills:'node film/render.mjs --mode=stills --version=custom'},dependencies:{'playwright-core':'1.62.1'}},null,2));
const video=path.join(root,'film/out/final-'+version+'/video.mp4');
fs.copyFileSync(video,path.join(dst,'夜鹭的一天.mp4'));
for(const name of ['evidence.json','ffprobe.json','config.json']){fs.mkdirSync(path.join(dst,'verification'),{recursive:true});fs.copyFileSync(path.join(path.dirname(video),name),path.join(dst,'verification',name))}
const qa=path.join(root,'qa',version);
if(deliveryMode==='ai_review_once'&&fs.existsSync(qa)){for(const name of fs.readdirSync(qa).filter(f=>/\.(json|md)$/.test(f))) {fs.mkdirSync(path.join(dst,'review'),{recursive:true});fs.copyFileSync(path.join(qa,name),path.join(dst,'review',name))}}
if(deliveryMode==='ai_review_once'&&version!=='reference-v5'){for(const name of ['av-review.json','review.md','blind-understanding.md']){fs.mkdirSync(path.join(dst,'review','reference-v5'),{recursive:true});fs.copyFileSync(path.join(root,'qa','reference-v5',name),path.join(dst,'review','reference-v5',name))}}
fs.writeFileSync(path.join(dst,'delivery-mode.json'),JSON.stringify({delivery_mode:deliveryMode,version},null,2));
if(fs.existsSync(path.join(root,'交付说明.md')))fs.copyFileSync(path.join(root,'交付说明.md'),path.join(dst,'README.md'));
const manifest=[];
function scan(folder){for(const d of fs.readdirSync(folder,{withFileTypes:true})){const p=path.join(folder,d.name);if(p===path.join(dst,'manifest.json'))continue;if(d.isDirectory())scan(p);else manifest.push({file:path.relative(dst,p).replaceAll('\\','/'),bytes:fs.statSync(p).size,sha256:createHash('sha256').update(fs.readFileSync(p)).digest('hex')})}}
scan(dst);fs.writeFileSync(path.join(dst,'manifest.json'),JSON.stringify({version,files:manifest},null,2));
console.log(JSON.stringify({directory:dst,files:manifest.length,bytes:manifest.reduce((n,f)=>n+f.bytes,0)}));
