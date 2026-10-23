import fs from'node:fs';import path from'node:path';
export function loadMaintenance(root,catalog){
 const file=path.join(root,'reference-sources/github-expansion-20261020/manifest.json');if(!fs.existsSync(file))return {ids:new Set(),active:false};
 const m=JSON.parse(fs.readFileSync(file,'utf8'));if(m.media.some(x=>!x.decodePassed))throw Error('Maintenance media must pass decoding before preview');
 const duplicates=JSON.parse(fs.readFileSync(path.join(root,'work/github-reference-expansion-20261020/duplicate-report.json'),'utf8')),excluded=new Set(duplicates.excludePreviewIds||[]),media=m.media.filter(x=>!excluded.has(x.id));
 for(const p of m.packages)if(!catalog.packages.some(x=>x.id===p.id))catalog.packages.push(p);
 for(const item of media){const prior=catalog.media.find(x=>x.id===item.id);if(prior)Object.assign(prior,item);else catalog.media.push(item);}
 catalog.checked=m.checked;
 catalog.maintenance20261020={checked:m.checked,addedPreview:media.length,films:media.filter(x=>x.kind==='影片与源码').length,shortSamples:media.filter(x=>x.kind==='镜头样段与源码').length,sourcePackages:m.packages.length,excluded:excluded.size,scope:m.policy};
 return {active:true,ids:new Set(media.map(x=>x.id)),roundId:'source-2026-10-20',roundDate:'2026-10-20',count:media.length};
}
