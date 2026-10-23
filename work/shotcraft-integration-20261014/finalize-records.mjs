import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
const task=path.resolve('work/shotcraft-integration-20261014');
const wb='D:/Codex/skills/video-shotcraft';
const installed='D:/Codex/skills/vibe-video',snapshot=path.resolve('skill/vibe-video');
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const manifest=JSON.parse(fs.readFileSync(task+'/installation.json'));
const differences=[];
for(const original of manifest.upstreamFiles){const target=path.join(wb,original.path);const st=fs.lstatSync(target);if(st.isSymbolicLink()){differences.push({path:original.path,kind:'local-link',target:fs.readlinkSync(target),upstream:original.sha256});continue;}const after=hash(target);if(after!==original.sha256)differences.push({path:original.path,kind:'modified',upstream:original.sha256,sha256:after});}
const adapter=['SKILL.md','LICENSE','references/upstream-skill.md','references/local-compatibility.md','workbench/package.json','workbench/package-lock.json','workbench/scripts/gen-index.mjs','workbench/scripts/open.mjs','workbench/scripts/local-platform.mjs','workbench/scripts/parity-local.mjs','workbench/vite.config.ts','workbench/remotion.config.ts'];
const files=[];
for(const relative of adapter){const target=path.join(task,'local-adapter',relative);fs.mkdirSync(path.dirname(target),{recursive:true});fs.copyFileSync(path.join(wb,relative),target);files.push({path:relative,sha256:hash(target)});}
fs.writeFileSync(task+'/local-adaptations.json',JSON.stringify({commit:manifest.commit,differences,adapterFiles:files,note:'Generated workbench indexes/project assets reflect the last linked internal sample; regenerate via open.mjs. Original upstream source and old install remain intact.'},null,2)+'\n');
const syncFiles=['SKILL.md','references/shotcraft-source.json','references/shotcraft-library.json','references/shotcraft-integration.md','scripts/shotcraft_library.mjs','assets/shotcraft/PageCamAdaptive.tsx','assets/shotcraft/LICENSE-shotcraft.txt'];
const synchronization=[];
for(const relative of syncFiles){const target=path.join(snapshot,relative);fs.mkdirSync(path.dirname(target),{recursive:true});fs.copyFileSync(path.join(installed,relative),target);const sha=hash(target);if(sha!==hash(path.join(installed,relative)))throw Error('Snapshot mismatch');synchronization.push({path:relative,sha256:sha});}
fs.writeFileSync(task+'/skill-sync.json',JSON.stringify({version:'0.16.0',installed,snapshot,files:synchronization},null,2)+'\n');
console.log(JSON.stringify({modifiedUpstreamFiles:differences.length,archivedAdapterFiles:files.length,synchronizedFiles:synchronization.length}));
