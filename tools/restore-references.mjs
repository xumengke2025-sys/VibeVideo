import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {Readable} from 'node:stream';
import {pipeline} from 'node:stream/promises';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=p=>JSON.parse(fs.readFileSync(p,'utf8').replace(/^\uFEFF/,''));
const catalog=read(path.join(root,'work/github-reference-expansion-20261011/catalog.json'));
const upstream=read(path.join(root,'reference-sources/upstream-videos/manifest.json'));
const ids=new Set(catalog.preview.mediaIds);
const films=catalog.media.filter(m=>ids.has(m.id));
const packageIds=new Set(films.map(m=>m.packageId));
const tasks=new Map();
function local(original){
  const normalized=original.replaceAll('\\','/'),marker='/VibeVideo项目/';
  const relative=/^[A-Za-z]:\//.test(normalized)&&normalized.includes(marker)?normalized.slice(normalized.indexOf(marker)+marker.length):normalized;
  const target=path.resolve(root,relative);
  if(!target.startsWith(root+path.sep))throw Error('Path outside project: '+original);
  return target;
}
function add(task){if(!/^[a-f0-9]{64}$/i.test(task.sha256))throw Error('Missing SHA256: '+task.relative);tasks.set(task.relative,task);}
for(const pkg of catalog.packages.filter(p=>packageIds.has(p.id))){
  const base=path.join(root,'reference-sources/github-expansion-20261011',pkg.id);
  const source=read(path.join(base,'SOURCE.json'));
  for(const f of source.files){
    const dest=path.resolve(base,f.path);
    if(!dest.startsWith(base+path.sep))throw Error('Unsafe source path');
    const relative=path.relative(root,dest).replaceAll('\\','/');
    add({relative,dest,bytes:f.bytes,sha256:f.sha256,url:`https://raw.githubusercontent.com/${pkg.repo}/${pkg.commit}/${f.path.split('/').map(encodeURIComponent).join('/')}`});
  }
}
for(const film of films.filter(m=>!m.newlyDownloaded)){
  const record=upstream.items.find(i=>i.status==='downloaded'&&i.sha256===film.sha256);
  if(!record?.url)throw Error('No author download URL: '+film.title);
  const dest=local(film.path),relative=path.relative(root,dest).replaceAll('\\','/');
  add({relative,dest,bytes:film.bytes,sha256:film.sha256,url:record.url});
}
const list=[...tasks.values()];
if(process.argv.includes('--dry-run')){
  const absent=list.filter(t=>!fs.existsSync(t.dest));
  console.log(JSON.stringify({previewFilms:films.length,sourcePackages:packageIds.size,files:list.length,totalBytes:list.reduce((n,t)=>n+t.bytes,0),missingFiles:absent.length,missingBytes:absent.reduce((n,t)=>n+t.bytes,0),note:'Dry run: no network requests or file writes. Existing files are hash-verified during restoration.'},null,2));
  process.exit(0);
}
async function sha(file){const h=crypto.createHash('sha256');for await(const chunk of fs.createReadStream(file))h.update(chunk);return h.digest('hex');}
let cursor=0,completed=0;const errors=[];
async function worker(){while(cursor<list.length){const t=list[cursor++];try{
  if(fs.existsSync(t.dest)&&fs.statSync(t.dest).size===t.bytes&&await sha(t.dest)===t.sha256){completed++;continue;}
  fs.mkdirSync(path.dirname(t.dest),{recursive:true});
  const response=await fetch(t.url,{signal:AbortSignal.timeout(15*60*1000)});
  if(!response.ok)throw Error('HTTP '+response.status);
  const temp=t.dest+'.download';
  await pipeline(Readable.fromWeb(response.body),fs.createWriteStream(temp));
  if(fs.statSync(temp).size!==t.bytes||await sha(temp)!==t.sha256)throw Error('Size/SHA256 mismatch');
  fs.renameSync(temp,t.dest);completed++;
  console.log(`Restored ${completed}/${list.length}: ${t.relative}`);
}catch(e){errors.push({path:t.relative,error:e.message});console.error(`Failed: ${t.relative}: ${e.message}`);}}}
await Promise.all(Array.from({length:4},worker));
const result={checkedAt:new Date().toISOString(),completed,total:list.length,errors,scope:'52 preview films and their five source packages; original author URLs and fixed commits; no upstream code executed'};
const evidence=path.join(root,'.codex/reference-restore-result.json');fs.mkdirSync(path.dirname(evidence),{recursive:true});fs.writeFileSync(evidence,JSON.stringify(result,null,2));
console.log(JSON.stringify({completed,total:list.length,failed:errors.length}));
if(errors.length)process.exitCode=1;
