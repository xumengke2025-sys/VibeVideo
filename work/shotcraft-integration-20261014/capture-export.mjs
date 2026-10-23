import fs from 'node:fs';
import path from 'node:path';
const aspect=process.argv[2];if(!['landscape','portrait'].includes(aspect))throw Error('Choose an aspect');
const wb='D:/Codex/skills/video-shotcraft/workbench';
const task=path.resolve('work/shotcraft-integration-20261014/verification');
const reportFile=`${task}/${aspect}-export-job.json`;
let id;
const propsFile=fs.readdirSync(wb+'/exports').find(f=>f.startsWith('.props-'));
if(propsFile){id=propsFile.slice(7,-5);fs.copyFileSync(`${wb}/exports/${propsFile}`,`${task}/${aspect}-edited-props.json`);}
else if(fs.existsSync(reportFile))id=JSON.parse(fs.readFileSync(reportFile)).id;
else {const files=fs.readdirSync(wb+'/exports').filter(f=>f.startsWith('.job-')).map(f=>JSON.parse(fs.readFileSync(wb+'/exports/'+f))).filter(j=>j.output.includes(aspect)).sort((a,b)=>b.id.localeCompare(a.id));id=files[0]?.id;}
if(!id)throw Error('No export job found');
const response=await fetch(`http://localhost:5198/api/export/${id}`);
if(!response.ok)throw Error('Export status unavailable');
const job=await response.json();fs.writeFileSync(reportFile,JSON.stringify({id,...job},null,2)+'\n');
console.log(JSON.stringify({id,status:job.status,progress:job.progress,lastLine:job.lastLine}));
