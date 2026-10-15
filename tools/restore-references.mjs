import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {Readable} from 'node:stream';
import {pipeline} from 'node:stream/promises';
import {spawn} from 'node:child_process';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const manifest=JSON.parse(fs.readFileSync(path.join(root,'tools/reference-restore-manifest.json'),'utf8'));
const args=process.argv.slice(2),onlyIndex=args.indexOf('--only');
if(onlyIndex>=0&&!args[onlyIndex+1])throw Error('--only requires an exact project-relative path');
const only=onlyIndex>=0?args[onlyIndex+1]:null;
const list=manifest.files.filter(t=>!only||t.relative===only).map(t=>{
  const dest=path.resolve(root,t.relative);
  if(path.isAbsolute(t.relative)||/^[A-Za-z]:|\\/.test(t.relative)||!dest.startsWith(root+path.sep))throw Error('Path outside project: '+t.relative);
  if(!/^[a-f0-9]{64}$/i.test(t.sha256)||!Number.isSafeInteger(t.bytes)||t.bytes<0||new URL(t.url).protocol!=='https:')throw Error('Invalid restore record: '+t.relative);
  if(t.transform&&(t.transform!=='lf-to-crlf'||!Number.isSafeInteger(t.downloadBytes)||!Number.isSafeInteger(t.bytes)||!/^[a-f0-9]{64}$/i.test(t.downloadSha256)))throw Error('Invalid text transform: '+t.relative);
  return {...t,dest};
});
if(only&&!list.length)throw Error('Unknown restore path: '+only);
if(args.includes('--dry-run')){
  const absent=list.filter(t=>!fs.existsSync(t.dest));
  console.log(JSON.stringify({previewFilms:manifest.previewFilms,sourcePackages:manifest.sourcePackages,files:list.length,totalBytes:list.reduce((n,t)=>n+t.bytes,0),missingFiles:absent.length,missingBytes:absent.reduce((n,t)=>n+t.bytes,0),note:'No network requests or file writes. Restoration verifies size and SHA256; optional local posters are not included.'},null,2));
  process.exit(0);
}
async function sha(file){const h=crypto.createHash('sha256');for await(const chunk of fs.createReadStream(file))h.update(chunk);return h.digest('hex');}
// Node 20 fetch does not honor HTTP(S)_PROXY; system curl follows those settings.
const useCurl=args.includes('--curl')||Boolean(process.env.HTTPS_PROXY||process.env.https_proxy||process.env.HTTP_PROXY||process.env.http_proxy||process.env.ALL_PROXY||process.env.all_proxy);
async function download(url,temp){
  if(useCurl){
    fs.closeSync(fs.openSync(temp,'wx'));
    await new Promise((resolve,reject)=>{const child=spawn(process.platform==='win32'?'curl.exe':'curl',['--fail','--location','--silent','--show-error','--connect-timeout','30','--max-time','900','--proto','=https','--proto-redir','=https','--output',temp,'--url',url],{windowsHide:true,stdio:['ignore','ignore','pipe']});let detail='';child.stderr.on('data',chunk=>{detail=(detail+chunk).slice(-1000);});child.on('error',e=>reject(Error('System curl required for proxy downloads: '+e.code)));child.on('close',code=>code===0?resolve():reject(Error('curl exit '+code+': '+detail.trim())));});
  }else{
    const response=await fetch(url,{signal:AbortSignal.timeout(15*60*1000)});
    if(!response.ok)throw Error('HTTP '+response.status);
    await pipeline(Readable.fromWeb(response.body),fs.createWriteStream(temp,{flags:'wx'}));
  }
}
// Reject directory symlinks/junctions that could redirect a restored file outside root.
function assertContained(dest){for(let p=dest;p!==root;p=path.dirname(p)){if(fs.existsSync(p)&&fs.lstatSync(p).isSymbolicLink()){const real=fs.realpathSync(p),realRoot=fs.realpathSync(root);if(real!==realRoot&&!real.startsWith(realRoot+path.sep))throw Error('Restore path redirects outside project: '+p);}}}
let cursor=0,completed=0;const errors=[];
async function worker(){while(cursor<list.length){const t=list[cursor++];let temp;try{
  assertContained(t.dest);
  if(fs.existsSync(t.dest)&&fs.statSync(t.dest).size===t.bytes&&await sha(t.dest)===t.sha256){completed++;continue;}
  if(args.includes('--verify-only'))throw Error('Missing file or size/SHA256 mismatch');
  fs.mkdirSync(path.dirname(t.dest),{recursive:true});
  temp=t.dest+'.'+crypto.randomUUID()+'.download';
  await download(t.url,temp);
  if(t.transform==='lf-to-crlf'){
    if(fs.statSync(temp).size!==t.downloadBytes||await sha(temp)!==t.downloadSha256)throw Error('Upstream size/SHA256 mismatch');
    fs.writeFileSync(temp,fs.readFileSync(temp,'utf8').replace(/\r?\n/g,'\r\n'));
  }
  if(fs.statSync(temp).size!==t.bytes||await sha(temp)!==t.sha256)throw Error('Size/SHA256 mismatch');
  fs.renameSync(temp,t.dest);temp=null;completed++;
  console.log(`Restored ${completed}/${list.length}: ${t.relative}`);
}catch(e){errors.push({path:t.relative,error:e.message});console.error(`Failed: ${t.relative}: ${e.message}`);}finally{if(temp)fs.rmSync(temp,{force:true});}}}
await Promise.all(Array.from({length:4},worker));
const result={checkedAt:new Date().toISOString(),completed,total:list.length,errors,scope:`${manifest.previewFilms} preview films and ${manifest.sourcePackages} source packages; original URLs and fixed commits; no upstream code executed`};
const evidence=path.join(root,'.codex/reference-restore-result.json');fs.mkdirSync(path.dirname(evidence),{recursive:true});fs.writeFileSync(evidence,JSON.stringify(result,null,2));
console.log(JSON.stringify({completed,total:list.length,failed:errors.length}));
if(errors.length)process.exitCode=1;
