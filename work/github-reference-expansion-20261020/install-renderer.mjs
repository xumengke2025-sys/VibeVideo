import fs from'node:fs';import path from'node:path';import{fileURLToPath}from'node:url';
const work=path.dirname(fileURLToPath(import.meta.url)),target=path.resolve(work,'../video-film-expansion-20261014/catalog-extension.mjs');let text=fs.readFileSync(target,'utf8');
if(text.includes('loadMaintenance(root,catalog)')){console.log('Maintenance renderer already installed');process.exit(0);}
fs.writeFileSync(path.join(work,'renderer-before.mjs'),text);
function edit(a,b){if(text.split(a).length!==2)throw Error('Expected one renderer anchor '+a.slice(0,80));text=text.replace(a,b);}
text="import {loadMaintenance} from '../github-reference-expansion-20261020/catalog-maintenance.mjs';\n"+text;
edit(" const exclusions=new Set", " const maintenance=loadMaintenance(root,catalog),currentRound=maintenance.roundId||'film-2026-10-14';\n const exclusions=new Set");
edit("oldPreview.has(m.id)||manifest.media.some(x=>x.id===m.id)||m.kind==='案例原片'", "oldPreview.has(m.id)||manifest.media.some(x=>x.id===m.id)||maintenance.ids.has(m.id)||m.kind==='案例原片'");
edit("catalog.round={date:'2026-10-14',id:'film-2026-10-14',addedPreview:catalog.filmExpansion20261014.addedPreview};", "catalog.round=maintenance.active?{date:maintenance.roundDate,id:currentRound,addedPreview:maintenance.count}:{date:'2026-10-14',id:'film-2026-10-14',addedPreview:catalog.filmExpansion20261014.addedPreview};");
edit("const rank=m=>m.addedRound==='film-2026-10-14'?", "const rank=m=>m.addedRound===currentRound?");
edit("${catalog.filmExpansion20261014.addedPreview}</strong><small>本轮加入目录", "${catalog.round.addedPreview}</strong><small>本轮加入目录");
edit("<strong>12</strong><small>原片画风分类", "<strong>${groups.length}</strong><small>参考分类");
edit("本轮：原片与风格扩展", "本轮：${catalog.round.date} 影片与源码");
edit("c.dataset.round==='film-2026-10-14'", "c.dataset.round==='${currentRound}'");
edit("c.dataset.round!=='film-2026-10-14'", "c.dataset.round!=='${currentRound}'");
edit("${cards}</div><div class=\"pager\">", "${cards}</div><div class=\"pager\">");
// Keep the prior expansion's audit history, and prepend the current maintenance totals.
edit("const md=`# 原片、风格与源码参考\\n\\n", "const md=`# 原片、风格与源码参考\\n\\n${maintenance.active?`2026-10-20维护：新增${maintenance.count}个影片/样段与对应源码；累计${included.length}个可播放参考，${source.length}个有对应绘制源码。新增${catalog.maintenance20261020.films}个影片及${catalog.maintenance20261020.shortSamples}个短样段。复刻、非商业许可、混合模型与模型未证实分别标注。\\n\\n- [本轮检查点](../github-reference-expansion-20261020/CHECKPOINT.md)\\n- [本轮来源与源码映射](../../reference-sources/github-expansion-20261020/manifest.json)\\n- [本轮查重](../github-reference-expansion-20261020/duplicate-report.json)\\n\\n`:''}");
text=text.replace('2026-10-14原片扩展：累计${included.length}个可播放参考，${source.length}个有对应绘制源码。','历史批次（2026-10-14）：当时累计${included.length-(maintenance.count||0)}个可播放参考，${source.length-(maintenance.count||0)}个有对应绘制源码。');
edit('addedPreview:included.filter(x=>!oldPreview.has(x.id)).length','addedPreview:included.filter(x=>!oldPreview.has(x.id)&&!maintenance.ids.has(x.id)).length');
fs.writeFileSync(target,text);console.log('Installed optional source-paired maintenance in existing renderer');
