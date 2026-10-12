import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';
import {validate,reviewSchedule} from './timeline.mjs';
const root=path.dirname(fileURLToPath(import.meta.url));let fail=false;
for(const file of fs.readdirSync(path.join(root,'clips')).filter(f=>f.endsWith('.json'))){
 const p=JSON.parse(fs.readFileSync(path.join(root,'clips',file),'utf8')),errors=validate(p);
 fs.mkdirSync(path.join(root,'plans'),{recursive:true});fs.writeFileSync(path.join(root,'plans',p.id+'-review.json'),JSON.stringify(reviewSchedule(p),null,2));
 console.log(JSON.stringify({clip:p.id,events:p.events.length,shots:p.shots.length,errors}));fail||=!!errors.length;
}
process.exitCode=fail?1:0;
