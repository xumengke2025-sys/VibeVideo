import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';
const work=path.dirname(fileURLToPath(import.meta.url)),root=path.resolve(work,'../..'),skill=path.join(root,'skill/vibe-video'),installed='D:/Codex/skills/vibe-video',read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const catalog=read(path.join(root,'work/github-reference-expansion-20261011/catalog.json')),ids=new Set(catalog.preview.mediaIds),items=catalog.media.filter(x=>ids.has(x.id)),stats=catalog.filmExpansion20261014;
const fields=['id','title','group','kind','tags','author','authorUrl','repo','repository','packageId','commit','path','entry','researchEntry','card','guide','sourceRecord','poster','sha256','metadata','license','sourceStatus','representation','decodePassed','addedRound','newlyDownloaded','newlySurfaced','related'];
fs.writeFileSync(path.join(skill,'references/video-examples.json'),JSON.stringify({checked:'2026-10-14',projectRoot:root.replaceAll('\\','/'),galleryPath:'work/github-reference-expansion-20261011/index.html',scope:'统一参考目录；源码齐备影片、镜头样段、原片、作者改编、节选与模板输入缺口分别标注。哈希/完整解码不等于动态审阅、听音或重渲。',items:items.map(m=>Object.fromEntries(fields.filter(f=>m[f]!==undefined).map(f=>[f,m[f]])))},null,2)+'\n');
const md=`# 原片、风格影片与对应源码

本机2026-10-14累计${items.length}个可播放参考，${catalog.preview.sourceCount}个有对应绘制源码（含镜头样段）。本轮接入${stats.addedPreview}条；其中${stats.existingOriginalsSurfaced}条为此前已保存的作者原片，不计新下载。视频保存在项目reference-sources，技能只保存检索索引；作者原片保持原画幅，新制作按用户选择横屏或竖屏分别布局。

\`\`\`text
node scripts/video_examples.mjs search --query "产品 运镜" --source present --limit 5
node scripts/video_examples.mjs search --query "纸艺 手绘" --source missing
node scripts/video_examples.mjs search --kind "影片与源码"
node scripts/video_examples.mjs card kimi-manim/MeltingSpace
node scripts/video_examples.mjs card shotcraft/mosaic-reframe
node scripts/video_examples.mjs verify
\`\`\`

结果返回本地视频、实际绘制入口或来源记录、固定版本、许可、元数据与验证范围。统一播放目录为项目 \`work/github-reference-expansion-20261011/index.html\`，用 \`npm run preview:references\` 启动。网页按画风、作品类型、源码状态和批次筛选并分页；搬迁项目时用 \`--root\` 或 \`VIBE_VIDEO_REFERENCE_ROOT\` 重定位项目内路径。

|参考用途|优先入口|实际公开范围|
|---|---|---|
|纸艺、瑞士排版、工程蓝图、连续UI变形与数据叙事|crawfordxx/xiaoma-studio，8部短片|examples/*/index.html、engine/runtime.js、音频/cues与成片|
|三维数学、曲面与证明|HarleyCoops/KimiK3Manim|Melting Space与Reverse Reasoning有README精确对应场景；Euler成片未找到具体绘制场景|
|35种艺术画风|alchaincyf/huashu-art-motion|scripts/engine及35个scenes；已有成片是对Tak原作的代码重绘，release片与源码版本不同；夜访博物馆完整影片工程未取得|
|口播、纸面、分屏、纵深与形变|adunext/adu-motion-video，12个样片|公开模板与授权预览；私人原输入缺失，不能算原片可重建工程|
|原片画风与跨模型摄影参考|作者帖视频、motionpromptgallery作者节选|保留原帖、提示词、索引版本、媒体与节选说明；画廊代码不算影片绘制源码|
|产品、数据与2.5D摄影|20个Shotcraft镜头样段|实际TSX配方入口；CSS投影与真实Three三维分开|
|真实三维场景与绘制叙事|Particle Beach、The Claude Glass|cinematic runtime与Python timeline/score；前者真实Three空间，后者逐帧程序绘画|
|更多风格完整工程|43种Lemo与15种MG|对应style/demo目录、时间轴和作者影片；字体、音乐许可另核|

先选一部作品，实际观看关键动作窗口，再读绘制入口和共享依赖，记录持续对象、动作中间态、机位/看向点、时序和本片改动。无源码原片用于视觉研究，不能写成已读实现或代码效果证明。原片、作者改编、节选、模板示意分别标注；输入不完整的模板不能冒称原片完整工程。尚未运行的源码只表示已归档，不宣称可以在本机逐像素重建。

扩库前先查本索引及旧catalog，再按作者帖status ID、媒体SHA256、近似时长和20/50/80%三帧指纹查重。近似候选人工核对，同一作品重编码通常只展示一条；横竖版、不同剪辑或原作/改编保留价值时注明关联，不当成独立的新风格。三帧不能保证发现所有片段/变速/重剪重复。本轮处理记录在项目 \`work/video-film-expansion-20261014/duplicate-decisions.json\`。

新增媒体已核对哈希、元数据、入口存在与完整音视频解码；旧媒体本轮仅新增指纹，历史解码记录仍按原批次。没有全库动态审美、听音或源码批量重渲验收。固定Git blob和逐文件SHA256验证不等于运行测试。

代码MIT、Apache或索引CC BY不自动覆盖影片、歌曲、字体及第三方素材。xiaoma、Kimi、花叔与阿杜按各仓库LICENSE和第三方说明；公开作者影片未取得开放素材许可时仅按视觉参考标注。Shotcraft声音许可见原assets/audio/ATTRIBUTION.md；Claude Glass代码MIT、绘画与影片CC BY4.0；Particle Beach代码MIT。来源与失败记录见项目 \`reference-sources/video-films-20261014/manifest.json\` 和本轮CHECKPOINT。
`;
fs.writeFileSync(path.join(skill,'references/video-example-library.md'),md);
const skillFile=path.join(skill,'SKILL.md');let text=fs.readFileSync(skillFile,'utf8');text=text.replace('version: "0.16.1"','version: "0.16.2"');text=text.replace(/^需要直接观看效果视频并读取配套源码时，.*$/m,'需要选原片、风格影片或读取配套源码时，读 [references/video-example-library.md](references/video-example-library.md)，用 `node scripts/video_examples.mjs search --query "需求" --source present` 找实际绘制工程，或 `--source missing` 找视觉参考。统一目录区分影片与源码、镜头样段、作者原片、改编、节选及输入不完整的模板；提示词或索引代码不算影片源码。扩库先按原帖、哈希与近似帧查重，有价值的版本注明关联。');fs.writeFileSync(skillFile,text);
for(const f of ['SKILL.md','scripts/video_examples.mjs','references/video-examples.json','references/video-example-library.md']){fs.mkdirSync(path.dirname(path.join(installed,f)),{recursive:true});fs.copyFileSync(path.join(skill,f),path.join(installed,f));}
console.log(JSON.stringify({version:'0.16.2',indexed:items.length,withSource:catalog.preview.sourceCount,synced:4}));
