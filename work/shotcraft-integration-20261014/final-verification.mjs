import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {spawnSync} from 'node:child_process';
const task=path.resolve('work/shotcraft-integration-20261014');
const installation=JSON.parse(fs.readFileSync(task+'/installation.json'));
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
for(const f of installation.backupFiles)if(sha(path.join(installation.backup,f.path))!==f.sha256)throw Error('Backup hash mismatch: '+f.path);
const python='C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';
const validators=[];
for(const skill of ['D:/Codex/skills/vibe-video','D:/Codex/skills/video-shotcraft',path.resolve('skill/vibe-video')]){
 const r=spawnSync(python,['D:/Codex/skills/.system/skill-creator/scripts/quick_validate.py',skill],{encoding:'utf8',windowsHide:true,env:{...process.env,PYTHONPATH:task+'/validation-deps',PYTHONUTF8:'1'}});
 if(r.status!==0)throw Error(r.stdout+r.stderr);validators.push({skill,passed:true,result:r.stdout.trim()});
}
const scripts=['D:/Codex/skills/vibe-video/scripts/shotcraft_library.mjs',...['gen-index','open','local-platform','parity-local'].map(s=>'D:/Codex/skills/video-shotcraft/workbench/scripts/'+s+'.mjs')];
for(const script of scripts){const r=spawnSync(process.execPath,['--check',script],{encoding:'utf8',windowsHide:true});if(r.status!==0)throw Error(r.stderr);}
const catalog=JSON.parse(fs.readFileSync('D:/Codex/skills/vibe-video/references/shotcraft-library.json'));
if(catalog.summary.missing.length||catalog.summary.unresolved.length)throw Error('Catalog references unresolved');
const samples={};
for(const aspect of ['landscape','portrait']){
 const comparison=JSON.parse(fs.readFileSync(`${task}/verification/${aspect}/comparison.json`));
 const media=JSON.parse(fs.readFileSync(`${task}/verification/${aspect}-media.json`));
 if(comparison.status!=='passed'||comparison.frames.length!==6||comparison.frames.some(f=>f.badPixels!==0)||!media.fullDecodePassed)throw Error('Sample check incomplete');
 const caption=media.editedProps.project.tracks.flatMap(t=>t.clips).find(c=>c.cardId==='proj:caption:caption');
 if(caption.props.text!==aspect.toUpperCase()+' · EDIT VERIFIED')throw Error('Edited text missing');
 if(aspect==='portrait'&&(caption.props.color!=='#bf5328'||caption.props.fontSize!==52))throw Error('Edited style missing');
 samples[aspect]={comparison,media,exportedFirstFrameObserved:true,workbenchScreenshot:`verification/workbench-${aspect}.png`};
}
const result={date:'2026-10-14',status:'completed',version:'0.16.0',upstream:{repository:installation.repository,commit:installation.commit,files:installation.upstreamFiles.length,originalCheckout:'Unchanged tracked source; only SOURCE.json added.'},backup:{path:installation.backup,files:installation.backupFiles.length,allHashesVerified:true},catalog:catalog.summary,skillValidation:validators,syntaxChecks:scripts,productionBuild:{passed:true,modules:305,warning:'Existing large all-card bundle warning; approximately 1.97 MB minified.'},samples,scope:{browserImportAndParameterEditing:true,fullDecode:true,independentAvAudit:false,actualListening:false,allGalleryDynamicAudit:false,jianyingExport:false,pausedProjectResumption:false},failureHistory:['First landscape attempt: Chrome reported memory/disk limit and parity browser setup timeout.','Bounded renderer attempt: FFmpeg automatic encoder threading failed. Fixed with explicit decoder/filter/encoder thread limits.','Bundled FFmpeg lacks rawvideo muxer, wrapped_avframe null default and volumedetect. Comparison uses pngjs; media decode uses explicit rawvideo/PCM codecs; test-tone levels calculated from decoded PCM.'],synchronization:JSON.parse(fs.readFileSync(task+'/skill-sync.json')),adaptations:'local-adaptations.json',workbenchUrl:'http://localhost:5198/'};
fs.writeFileSync(task+'/verification.json',JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({status:result.status,backupHashes:installation.backupFiles.length,skillValidators:validators.length,pixelComparisons:12,mediaDecodeChecks:2}));
