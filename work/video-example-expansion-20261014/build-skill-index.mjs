import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';
const work=path.dirname(fileURLToPath(import.meta.url)),root=path.resolve(work,'../..'),read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const manifest=read(path.join(root,'reference-sources/video-examples-20261014/manifest.json')),verified=new Map(read(path.join(work,'media-verification.json')).items.map(m=>[m.id,m]));
const index={checked:'2026-10-14',projectRoot:root.replaceAll('\\','/'),catalog:'work/github-reference-expansion-20261011/catalog.json',galleryPath:'work/github-reference-expansion-20261011/index.html',scope:'新增成套参考；原片及源码已保存，未批量重渲/完整动态审片或听音',items:manifest.media.map(m=>({...m,...verified.get(m.id)}))};
for(const skill of [path.join(root,'skill/vibe-video'),'D:/Codex/skills/vibe-video'])fs.writeFileSync(path.join(skill,'references/video-examples.json'),JSON.stringify(index,null,2)+'\n');
console.log('Indexed '+index.items.length+' source-linked examples');
