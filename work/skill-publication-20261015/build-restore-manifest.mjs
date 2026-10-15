import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const read=p=>JSON.parse(fs.readFileSync(path.resolve(root,p),'utf8').replace(/^\uFEFF/,''));
const relative=p=>{const s=p.replaceAll('\\','/'), marker='/VibeVideo项目/';const r=s.includes(marker)?s.slice(s.indexOf(marker)+marker.length):s;const dest=path.resolve(root,r);if(!dest.startsWith(root+path.sep))throw Error('Outside project: '+p);return path.relative(root,dest).replaceAll('\\','/');};
const catalog=read('work/github-reference-expansion-20261011/catalog.json');
const ids=new Set(catalog.preview.mediaIds),films=catalog.media.filter(m=>ids.has(m.id));
const packageIds=new Set(films.map(m=>m.packageId).filter(Boolean));
const upstream=read('reference-sources/upstream-videos/manifest.json');
const tasks=new Map(), records=new Set();
function add(t){if(!/^[a-f0-9]{64}$/i.test(t.sha256)||!Number.isSafeInteger(t.bytes)||t.bytes<0)throw Error('Invalid hash/size '+t.relative);const u=new URL(t.url);if(u.protocol!=='https:')throw Error('Invalid URL '+t.relative);tasks.set(t.relative,t);}
for(const pkg of catalog.packages.filter(p=>packageIds.has(p.id))){
  records.add(relative(pkg.sourceRecord));
  const source=read(pkg.sourceRecord);
  const files=source.files??(pkg.id==='video-shotcraft'?read('work/shotcraft-integration-20261014/installation.json').upstreamFiles:null);
  const transforms=pkg.id==='video-shotcraft'?read('work/skill-publication-20261015/shotcraft-restore-transforms.json'):{};
  if(!Array.isArray(files))throw Error('Missing file inventory '+pkg.id);
  for(const f of files){const r=f.localPath?relative(f.localPath):relative(path.join(path.dirname(pkg.sourceRecord),f.path));
    add({relative:r,bytes:f.bytes,sha256:f.sha256,url:f.url||`https://raw.githubusercontent.com/${pkg.repo}/${pkg.commit}/${f.path.split('/').map(encodeURIComponent).join('/')}`,...transforms[f.path]});}
}
for(const film of films){
  const r=relative(film.path),existing=tasks.get(r);
  if(film.sourceRecord)records.add(relative(film.sourceRecord));
  if(film.researchEntry?.endsWith('.json'))records.add(relative(film.researchEntry));
  if(existing?.sha256===film.sha256)continue;
  const record=upstream.items.find(i=>i.status==='downloaded'&&i.sha256===film.sha256);
  const url=film.remoteUrl||record?.url;
  if(!url)throw Error('No exact media URL: '+film.id);
  add({relative:r,bytes:film.bytes,sha256:film.sha256,url});
}
// Posters are optional local extracts; playback does not depend on them.
const manifest={schemaVersion:1,previewFilms:films.length,sourcePackages:packageIds.size,files:[...tasks.values()].sort((a,b)=>a.relative.localeCompare(b.relative))};
fs.writeFileSync(path.join(root,'tools/reference-restore-manifest.json'),JSON.stringify(manifest,null,2)+'\n');
fs.writeFileSync(path.join(root,'work/skill-publication-20261015/provenance-files.json'),JSON.stringify([...records].sort(),null,2)+'\n');
console.log(JSON.stringify({films:films.length,packages:packageIds.size,files:tasks.size,bytes:manifest.files.reduce((n,t)=>n+t.bytes,0),provenance:records.size}));
