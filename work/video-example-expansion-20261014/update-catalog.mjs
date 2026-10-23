import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';
const work=path.dirname(fileURLToPath(import.meta.url)),root=path.resolve(work,'../..'),file=path.join(root,'work/github-reference-expansion-20261011/build-catalog.mjs');
fs.mkdirSync(path.join(work,'before'),{recursive:true});for(const f of ['build-catalog.mjs','catalog.json','index.html','CATALOG.md']){const p=path.join(root,'work/github-reference-expansion-20261011',f),backup=path.join(work,'before',f);if(!fs.existsSync(backup))fs.copyFileSync(p,backup);}
let text=fs.readFileSync(file,'utf8');const change=(from,to)=>{if(!text.includes(from))throw Error('Cannot locate '+from.slice(0,100));text=text.replace(from,to);};
change("import {definitions as extraDefinitions", "import {loadAdditions} from '../video-example-expansion-20261014/additions.mjs';\nimport {definitions as extraDefinitions");
change('const hashGroups=new Map();', 'const latest=loadAdditions(root,work);packages.push(...latest.packages);media.push(...latest.media);\nconst hashGroups=new Map();');
change("const catalog={checked:'2026-10-13'", "const catalog={checked:'2026-10-14'");
change("const previewMedia=media.filter(m=>m.kind==='影片与源码'&&m.entry&&!m.path.endsWith('.gif'));", "const previewMedia=media.filter(m=>['影片与源码','镜头样段与源码'].includes(m.kind)&&m.entry&&!m.path.endsWith('.gif'));\ncatalog.additions20261014={entries:latest.media.length,newVideos:latest.media.filter(m=>m.newlyDownloaded).length,shots:latest.media.filter(m=>m.kind==='镜头样段与源码').length,films:latest.media.filter(m=>m.kind==='影片与源码').length,failures:latest.failures,excluded:latest.excluded};");
change("catalog.round={date:'2026-10-13',addedPreview:media.filter(m=>m.addedRound==='2026-10-13').length,newFilms:media.filter(m=>m.addedRound==='2026-10-13'&&m.newlyDownloaded).length,existingFilmsWithNewSource:media.filter(m=>m.addedRound==='2026-10-13'&&!m.newlyDownloaded).length};", "catalog.round={date:'2026-10-14',addedPreview:latest.media.length,newFilms:latest.media.filter(m=>m.newlyDownloaded&&m.kind==='影片与源码').length,newShots:latest.media.filter(m=>m.kind==='镜头样段与源码').length,existingFilmsWithNewSource:latest.media.filter(m=>!m.newlyDownloaded).length};");
change("policy:'只展示同时具备本地影片与对应源码入口的影片'", "policy:'只展示同时具备本地视频与对应源码的条目，完整影片和镜头样段分别标注'");
change('<h1>具备影片和源码的参考</h1><p>只展示已保存本地影片和对应绘制源码的例子。</p>', '<h1>具备视频和源码的参考</h1><p>已保存作者效果视频和对应绘制源码，完整影片与镜头样段分别标注。</p>');
change('<small>影片与源码</small>', '<small>视频与源码</small>');
change('原片保持上游画幅；本项目后续新制作仍使用9:16竖屏。', '原片保持上游画幅；新制作可选横屏16:9或竖屏9:16，分别安排布局。镜头样段用于机制参考，不能当作完整影片标杆。');
change('<select id="kind" hidden aria-hidden="true"><option value="">影片与源码</option></select>', '<select id="kind" aria-label="按作品类型筛选"><option value="">全部视频与源码</option><option value="影片与源码">完整影片与源码</option><option value="镜头样段与源码">镜头样段与源码</option></select>');
change('本次新增（2026-10-13）','本次新增（2026-10-14）');
change("c.dataset.round==='2026-10-13'","c.dataset.round==='2026-10-14'");
change('本轮已归档 **${catalog.summary.repositories}', '2026-10-14新增 **${catalog.additions20261014.entries} 个可播放条目**：${catalog.additions20261014.shots} 段Shotcraft镜头样段、1部新找到的程序绘画影片，以及1段已有三维海滩预告。新增下载${catalog.additions20261014.newVideos}个视频；完整影片与镜头样段可分别筛选。来源、排除原因和验证见 [本次检查点](../video-example-expansion-20261014/CHECKPOINT.md)。\\n\\n累计已归档 **${catalog.summary.repositories}');
// Preserve the previous round's record as history rather than silently changing its date.
change('2026-10-13本次加入 **${catalog.round.addedPreview} 段参考**：新找到并保存 ${catalog.round.newFilms} 段影片，另补齐 ${catalog.round.existingFilmsWithNewSource} 段已有 MG 影片的源码。', '2026-10-13历史批次新增9段影片，另补齐15段已有MG影片的源码。');
fs.writeFileSync(file,text);console.log('Updated catalog builder');
