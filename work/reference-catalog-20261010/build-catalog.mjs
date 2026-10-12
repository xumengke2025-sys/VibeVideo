import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {execFileSync} from 'node:child_process';

const out = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(out, '../..');
const skill = 'D:/Codex/skills/vibe-video';
const archive = `${skill}/assets/code-studies`;
const slash = p => p.replaceAll('\\', '/');
const escape = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const local = p => pathToFileURL(p).href;
const json = p => JSON.parse(fs.readFileSync(p, 'utf8').replace(/^\uFEFF/, ''));
const link = (label, p) => `<a href="${escape(local(p))}">${escape(label)}</a>`;
const mdLink = (label, p) => `[${label}](<${slash(p)}>)`;
const upstreamPath = path.join(root,'reference-sources/upstream-videos/manifest.json');
const upstream = fs.existsSync(upstreamPath) ? json(upstreamPath) : {items:[],summary:{downloaded:0,bytes:0}};
const downloaded = upstream.items.filter(i=>i.status==='downloaded'&&fs.existsSync(i.path));
const videoFor = (packageId,styleId) => downloaded.find(i=>i.packageId===packageId&&i.styleId===styleId&&!i.path.endsWith('.gif'));

const specs = [
 ['particle-beach','粒子海滩电影','点云世界、长焦、低位穿行、昼夜光照、双轨迹摄影','js/trailer-shots.js','绘制运行部分已回放；没有本地作者原片'],
 ['work-reel-26','动效作品集','点云变形、程序化材质、文字窗口、局部放大交接','skills/kinetic-reel/examples/work-reel-26/reel.js','绘制运行部分已回放；没有本地作者原片'],
 ['mg-styles-15','15种MG风格','完整名单见下表；SVG / Canvas / WebGL / Three.js / Blender','README.md','15种本地绘制源码；素材和依赖不完整，尚未逐片运行；无本地原片'],
 ['lemo-opuscar','4种已归档影片风格','装饰艺术、工程蓝图、中国水墨、科幻全息HUD','README.md','只归档4种，未逐片运行；作者43种索引另列；无本地原片'],
 ['papermotion','纸片角色叙事','纸片视差、角色骨骼、风雨、接触事件、相机跟随','examples/light/main.ts','选定文本源码；未运行，素材和依赖不完整；无本地原片'],
 ['songbie','蜡笔绘本与音乐表演','钢琴、角色接棒、融化、情绪与身体共享状态','render.js','选定文本源码；未运行，钢琴音轨不随包；无本地原片'],
 ['i-like-ur-look-lyric-video','杂志排版歌词MV','曲面翻页、字体、景深、弱手持、阅读节奏','app/src/engine/curl.ts','选定文本源码；未运行；歌曲、字体、节拍数据不随包；无本地原片'],
 ['water-opus','网格浅水模拟组件','地形、水流、水量预算、水面材质','runs/claude-code-opus-5-5/src/sim/water.ts','技术组件；未运行，不是完整影片，也不是阀内三维流体解算'],
 ['three-avbd','WebGPU刚体组件','碰撞、关节、堆叠、断裂、GPU模拟','examples/basic.ts','技术组件；未运行，需固定随机和离线模拟'],
 ['clearwater','水面光学组件','折射、水底焦散、吸收、互动涟漪','index.html','技术组件；未运行，固定时间不自动重建涟漪历史'],
];
const packages = specs.map(([id,title,styles,entry,status]) => {
 const base = `${archive}/${id}`;
 const source = json(`${base}/SOURCE.json`);
 const filename = `${base}/${entry}`;
 if (!fs.existsSync(filename)) throw new Error(`Missing source: ${filename}`);
 const media=downloaded.filter(i=>i.packageId===id);
 const movies=media.filter(i=>!i.path.endsWith('.gif')).length;
 const gifs=media.length-movies;
 if(media.length)status=status.replace(/；没有本地作者原片|；无本地原片/g,'')+`；已保存上游视频${movies}份、GIF演示${gifs}份`;
 return {id,title,styles,entry:filename,status,repository:source.repository || source.repo,commit:source.commit,source:`${base}/SOURCE.json`,localMovies:movies,localGifs:gifs};
});

const mgDefs = [
 ['05-cel-boil','逐帧手绘 / 抖线'],['03-isometric','等距2.5D'],['01-flat-vector','扁平矢量'],['02-line-art','线条艺术'],['04-3d-render','三维软质渲染'],['08-morph','形状变形'],['19-paperclip','贴纸式科普'],['22-hud','赛博HUD / FUI'],['06-collage','拼贴 / 剪纸'],['12-aurora-glass','极光 / 玻璃质感'],['09-bauhaus','包豪斯几何'],['10-synthwave','80年代合成波 / VHS'],['20-pixel','像素艺术'],['07-liquid','液态动效'],['18-hanazi','综艺花字 / 竖屏字幕'],
];
const mg = mgDefs.map(([id,title]) => ({id,title,entry:`${archive}/mg-styles-15/demos/${id}/index.html`,watch:`https://vincentwei1021.github.io/mg-styles-15/#${id}`,localVideo:videoFor('mg-styles-15',id)?.path||null}));
for (const s of mg) if (!fs.existsSync(s.entry)) throw new Error(`Missing style: ${s.entry}`);

const lemoNames = ['蜡笔绘本','水彩笔触','中国水墨','厚涂油画','一笔画','白板科普','城市钢笔淡彩','皮影戏','浮世绘','红色剪纸','剪纸灯箱','孔版印刷','网点档案','木刻版画','铜版雕刻','丝网旅行海报','瑞士平面动效','60年代间谍片头','装饰艺术','工程蓝图','彩色玻璃','象形图标动效','ASCII / CRT终端','数据叙事','等距信息图','暗色科技发布会','动态录屏','科幻全息HUD','30年代橡皮管卡通','80年代赛璐珞动画','科幻情景喜剧卡通','世纪中期卡通','16位像素RPG','HD-2D','微游戏合集','平面游戏节目','20年代默片','阈限空间 / 拾得影像','积木玩具','纸艺立体书','移轴微缩','低多边形等距岛屿','玻璃产品渲染'];
const lemoReadme = fs.readFileSync(`${archive}/lemo-opuscar/README.md`, 'utf8');
const lemo = [...lemoReadme.matchAll(/href="styles\/([^/]+)\/STYLE.md"[^>]*>.*?<b>(.*?)<\/b>/g)].map((m,i) => {
 const entry = `${archive}/lemo-opuscar/styles/${m[1]}/STYLE.md`;
 return {id:m[1],title:lemoNames[i] || m[2],entry:fs.existsSync(entry)?entry:null,watch:`https://lemomo-ai.github.io/lemo-opuscar/`,guide:`https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/${m[1]}/STYLE.md`,localVideo:videoFor('lemo-opuscar',m[1])?.path||null};
});
if (lemo.length !== 43) throw new Error('Unexpected Lemo style count');

const refs = [
 ['reference-sources/bilibili-media/BV18ta86EEHb/reference.mp4','AGI概念MV / 用户此前选定参考','外部原片','线场、三维空间、逐词字幕、音乐同步；B站参数重渲转载，与当前PDoom源码不是同一版本','reference-sources/pdoom-source-review/app/src/timeline.ts'],
 ['reference-sources/bilibili-media/BV1vRHa63EYg/reference.mp4','Opus5.5告诉你，它是怎么做视频的','外部原片','代码动画制作过程与画面转换；未取得对应原工程',null],
 ['work/opus-gallery-study-20261009/twoclipping-original.mp4','TwoClipping / UI连续变形','外部原片','按钮、播放器、滑杆、图表等UI状态交接；原工程未取得',null],
 ['work/opus-gallery-study-20261009/koldo2k-original.mp4','Koldo2k / 复古拼贴无限缩放','外部原片','摄影景观、报纸剪贴、物件门户；公开提示词含生图与Kling动画，不能当纯代码证明',null],
 ['work/opus-gallery-study-20261009/ror-fly-original.mp4','Ror_Fly / 鸡尾酒配方动效','外部原片','从空杯到成品的原料加入、剂量和步骤；原工程未取得',null],
 ['work/director-study-20261008/source-snapshots/Liamrjohnston/examples/openmontage-hook.mp4','OpenMontage / Hook','外部原片','Remotion开场钩子、文字与流程图动效','work/director-study-20261008/source-snapshots/Liamrjohnston/docs/prompt-threads.md'],
 ['work/director-study-20261008/source-snapshots/Liamrjohnston/examples/openmontage-tool-chaos.mp4','OpenMontage / Tool Chaos','外部原片','工具堆叠、信息组织、节奏化演示','work/director-study-20261008/source-snapshots/Liamrjohnston/docs/prompt-threads.md'],
 ['work/director-study-20261008/source-snapshots/Liamrjohnston/examples/openmontage-claude-pipeline.mp4','OpenMontage / Claude Pipeline','外部原片','流程叙事、节点连接、产品讲解','work/director-study-20261008/source-snapshots/Liamrjohnston/docs/prompt-threads.md'],
 ['work/opus-gallery-study-20261009/twoclipping-remake.mp4','TwoClipping / Skillry重制版','外部重制','与原片分开登记；重制技术标签不能证明原片实现',null],
];
const examples = [
 ['work/creative-upgrade-20261010/flight/out-final/flight-director.mp4','飞行器 / 主体意图与跟拍','三维场景、转弯、相机跟随；静音，等待用户反馈','work/creative-upgrade-20261010/flight/film.js'],
 ['work/creative-upgrade-20261010/valve/out-final/valve-director.mp4','止回阀 / 受限机械行程','工程剖面、弹簧、压差与行程；静音，等待用户反馈','work/creative-upgrade-20261010/valve/film.js'],
 ['work/camera-upgrade-20261010/out-r2/subject-follow-portrait.mp4','主体跟拍 / 竖屏研究','主体世界路径、前景视差、相机相对偏移','work/camera-upgrade-20261010/demo/film.js'],
 ['work/style-production-20261009/studio/out-approved/blueprint-proof/blueprint-proof.mp4','工程蓝图 / 10秒能力片段','外壳分离、剖切、零件与标注联动','work/style-production-20261009/studio/film.mjs'],
 ['work/style-production-20261009/studio/out-approved/dataviz-proof/dataviz-proof.mp4','数据叙事 / 10秒能力片段','同一组点从折线到零基线柱形','work/style-production-20261009/studio/film.mjs'],
 ['work/portrait-valve-20261009/out-final/one-way-portrait.mp4','只向一个方向 / 竖屏蓝图','机械因果、剖面、事件拟音','work/portrait-valve-20261009/film.js'],
 ['work/napoleon-egypt-ink-20261009/out/napoleon-egypt-ink.mp4','淡墨远征 / 拿破仑在埃及','水墨叙事；生成的图像组件 + Canvas / WebGL显影与运镜，属于混合素材','work/napoleon-egypt-ink-20261009/film.js'],
 ['work/whale-20261009/out/final/whale.mp4','5厘米的噩梦 / 诙谐科普','纯Canvas绘制、大小反差、事件拟音','work/whale-20261009/film.js'],
 ['work/entropy-20261009/out/entropy-r3/entropy.mp4','熵增 / 统计科普','Canvas、组合枚举、粒子与统计、中文旁白；历史横版','work/entropy-20261009/film.mjs'],
 ['work/cinematic-assimilation-20261009/demo/out-durable/lumen-sound.mp4','光庭 / 空间光学电影','Three.js、程序化器件、光束、低位穿行、升高揭示','work/cinematic-assimilation-20261009/demo/film.js'],
 ['work/cinematic-assimilation-20261009/sdf-lab/out/sdf-glass-window.mp4','SDF玻璃 / 局部实验','WebGL2单界面折射近似；不代表完整物理折射或焦散','work/cinematic-assimilation-20261009/sdf-lab/index.html'],
 ['work/opus-gallery-study-20261009/demo/out/continuity-study.mp4','一条线 / UI连续性实验','解析弹簧、点对应、滑杆到曲线到勾号','work/opus-gallery-study-20261009/demo/index.html'],
 ['work/morpho-blue-20261008/out/mechanism-study.mp4','蓝色的建筑 / 机制小样','结构色、显微机制；只交付过27秒小样，52秒最终版未交付','work/morpho-blue-20261008/film.mjs'],
 ['work/black-hole-lensing-20261008/out/around-the-dark.mp4','绕过黑暗 / 黑洞透镜','光路、黑洞、科学机制与空间示意；历史横版','work/black-hole-lensing-20261008/film.mjs'],
 ['work/hot-news-20261009/out-final/icecube-news-portrait.mp4','冰下，宇宙亮了 / 历史样片','实景照片 + 艺术化三维示意；用户已否定此版，只作历史记录','work/hot-news-20261009/film.js'],
];

const known = new Map();
for(const item of downloaded){const relative=slash(path.relative(root,item.path));known.set(relative,{title:item.title,kind:item.path.endsWith('.gif')?'上游GIF演示':'上游原片',note:item.note,entry:item.entry,packageId:item.packageId,sourceUrl:item.url,sourceRecord:item.path+'.source.json',metadata:item.metadata,remoteCode:item.remoteCode||null})}
for (const [relative,title,kind,note,entry] of refs) known.set(relative,{title,kind,note,entry:entry?slash(path.join(root,entry)):null});
for (const [relative,title,note,entry] of examples) known.set(relative,{title,kind:'项目样片',note,entry:slash(path.join(root,entry))});
const paths = [...new Set([...execFileSync('rg',['--files','-uuu','-g','!reference-sources/github-expansion-20261011/**','-g','*.mp4','-g','*.webm','-g','*.mov','-g','*.mkv'],{cwd:root,encoding:'utf8',maxBuffer:2*1024*1024}).trim().split(/\r?\n/).map(slash).filter(Boolean),...downloaded.filter(i=>i.path.endsWith('.gif')).map(i=>slash(path.relative(root,i.path)))])];
const media = paths.map(relative => {
 const absolute = slash(path.join(root,relative));
 const record = known.get(relative) || {title:path.basename(relative),kind:'历史 / 预演 / 验证',note:'保留文件；依据路径查看版本与用途',entry:null};
 return {...record,path:absolute,relative,bytes:fs.statSync(absolute).size,url:encodeURI(slash(path.relative(out,absolute)))};
}).sort((a,b) => [...known.keys()].indexOf(a.relative) < 0 ? ([...known.keys()].indexOf(b.relative)<0?a.relative.localeCompare(b.relative):1) : [...known.keys()].indexOf(b.relative)<0?-1:[...known.keys()].indexOf(a.relative)-[...known.keys()].indexOf(b.relative));
for (const relative of known.keys()) if (!paths.includes(relative)) throw new Error(`Missing video: ${relative}`);
for (const item of media) if (item.entry && !fs.existsSync(item.entry)) throw new Error(`Missing entry: ${item.entry}`);
const methods = json(`${skill}/references/opus-methods.json`).cards.map(c=>({id:c.id,title:c.title}));

const legacy = [
 ['PDoom / AGI概念MV','线场、逐词卡拉OK、音乐节拍、后处理、三维空间',`${root}/reference-sources/pdoom-source-review/app/src/timeline.ts`,'有本地B站重渲转载，版本与当前代码有差异'],
 ['OpenMontage / Remotion','钩子、流程图、工具演示、动效时间轴',`${root}/work/director-study-20261008/source-snapshots/Liamrjohnston/docs/prompt-threads.md`,'有3个上游MP4和方法资料；不承诺三个示例的完整绘制源码均已保存'],
 ['Lugia / 配对估计科普','漫画式解释、关系建立、代码分镜',`${root}/work/director-study-20261008/source-snapshots/Lugia123/episodes/ep03-paired-estimate/index.html`,'有选定分镜源码与本地重渲片段；不是完整原片'],
 ['huashu-art-motion','分层绘制、导演经验、代码与图像素材协作',`${root}/work/director-study-20261008/source-snapshots/alchaincyf/repo.json`,'保存来源和选定研究资料；不是已验证影片模板'],
];
const rows = packages.map(p=>`<tr><td>${escape(p.title)}<small>${escape(p.id)}</small></td><td>${escape(p.styles)}</td><td>${link('源码入口',p.entry)}<br>${link('来源与固定版本',p.source)}</td><td>${escape(p.status)}</td></tr>`).join('');
const mgRows = mg.map(s=>`<tr><td>${escape(s.title)}</td><td>${link(s.id,s.entry)}</td><td>${s.localVideo?link('播放本地原片',s.localVideo):`<a href="${s.watch}">作者在线影片</a>`}</td><td>本地代码；${s.localVideo?'原片已归档':'原片未归档'}</td></tr>`).join('');
const lemoRows = lemo.map(s=>`<tr><td>${escape(s.title)}</td><td>${s.entry?link(s.id,s.entry):`<a href="${s.guide}">${escape(s.id)} / 上游指南</a>`}</td><td>${s.localVideo?link('播放本地原片',s.localVideo):'原片未归档'}</td><td>${s.entry?'已归档此风格源码；未运行':'上游代码入口已登记；未归档此风格源码'}</td></tr>`).join('');
const cards = media.map(v=>`<article class="clip" data-kind="${escape(v.kind)}" data-package="${escape(v.packageId||'')}"><div class="caption"><h3>${escape(v.title)}</h3><span>${escape(v.kind)}${v.metadata?` · ${v.metadata.width}×${v.metadata.height} · ${Math.round(v.metadata.duration||0)}秒`:''}</span></div>${v.path.endsWith('.gif')?`<img class="gif" loading="lazy" src="${escape(v.url)}" alt="${escape(v.title)}">`:`<video controls playsinline preload="none" src="${escape(v.url)}"></video>`}<p>${escape(v.note)}</p><p>${link('视频文件',v.path)}${v.entry?` · ${link('对应代码 / 资料',v.entry)}`:v.remoteCode?` · <a href="${escape(v.remoteCode)}">上游代码</a>`:''}${v.sourceUrl?` · <a href="${escape(v.sourceUrl)}">作者发布入口</a> · ${link('来源记录',v.sourceRecord)}`:''} · ${(v.bytes/1048576).toFixed(1)} MB</p><details><summary>本地路径</summary><code>${escape(v.path)}</code></details></article>`).join('');
const table = (heads,body)=>`<div class="table-wrap"><table><thead><tr>${heads.map(h=>`<th>${escape(h)}</th>`).join('')}</tr></thead><tbody>${body}</tbody></table></div>`;
const missing=upstream.items.filter(i=>i.status==='failed');
const archiveSummary=`上游已归档${downloaded.filter(i=>!i.path.endsWith('.gif')).length}个视频、${downloaded.filter(i=>i.path.endsWith('.gif')).length}个GIF，${(downloaded.reduce((sum,i)=>sum+i.bytes,0)/1073741824).toFixed(2)} GB`;
const packageOptions=[...new Set(downloaded.map(i=>i.packageId))].map(id=>`<option value="${escape(id)}">${escape(packages.find(p=>p.id===id)?.title||id)}</option>`).join('');
const missingHtml=missing.length?`<details><summary>尚未取得的附件（${missing.length}个）</summary><ul>${missing.map(i=>`<li>${escape(i.title)} · <a href="${escape(i.url)}">作者附件入口</a> · ${escape(i.error?.includes('404')?'上游返回404':'下载失败，详见来源记录')}</li>`).join('')}</ul></details>`:'';
const html = `<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>VibeVideo 代码、风格与原片目录</title><style>
:root{color-scheme:light;font-family:"Microsoft YaHei",system-ui,sans-serif;color:#222;background:#f7f8fa}*{box-sizing:border-box}body{margin:0}header,main{max-width:1280px;margin:auto;padding:24px}header{border-bottom:1px solid #dce1e6}h1{font-size:28px;line-height:1.35;margin:0 0 12px}h2{font-size:22px;margin:32px 0 16px}h3{font-size:17px;margin:0;line-height:1.5}p{line-height:1.7;font-size:14px}a{color:#146e60;text-underline-offset:3px}nav{display:flex;gap:20px;flex-wrap:wrap;margin-top:18px}.filters{display:flex;gap:12px;flex-wrap:wrap;margin:18px 0}input,select{font:inherit;font-size:14px;padding:10px;border:1px solid #aeb9c2;border-radius:4px;background:white}input{width:340px;max-width:100%}#videos{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:28px}.clip{min-width:0;background:#fff;border:1px solid #dce1e6;border-radius:6px;padding:16px}.caption{min-height:68px}.caption span{font-size:12px;color:#6a466f}video{width:100%;height:320px;object-fit:contain;background:#111;display:block;border-radius:3px}.clip p{margin:12px 0 0}.table-wrap{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:14px;line-height:1.65;background:white}th,td{text-align:left;padding:12px;border-bottom:1px solid #dce1e6;vertical-align:top}th{background:#edf1f3}small{display:block;color:#626b74}code{font-size:12px;overflow-wrap:anywhere}details{margin-top:12px;font-size:13px}summary{cursor:pointer}.clip[hidden]{display:none}.methods{columns:2;line-height:1.8;font-size:14px}footer{margin:36px 0;color:#626b74;font-size:13px}@media(max-width:700px){header,main{padding:16px}h1{font-size:23px}#videos{grid-template-columns:1fr}video{height:360px}.methods{columns:1}td,th{padding:9px}}
</style><style>.gif{display:block;width:100%;height:320px;object-fit:contain;background:#111}@media(max-width:700px){.gif{height:360px}}</style>
<header><h1>代码、风格与原片目录</h1><p>2026-10-10 · ${archiveSummary} · 含历史版本共${media.length}份媒体</p><nav><a href="../github-reference-expansion-20261011/index.html">新增GitHub视频与完整源码</a><a href="#watch">本地视频</a><a href="#code">参考代码</a><a href="#mg">MG 15种</a><a href="#lemo">Lemo 43种</a><a href="#methods">37种方法</a></nav></header>
<main><section id="watch"><h2>本地视频</h2><p>作者原片按发布文件原样保存；GIF演示、转载、重制和项目样片分别标注。既有横版保持原样；新制作遵循1080×1920竖屏。${link('归档来源与文件哈希',upstreamPath)}</p>${missingHtml}<div class="filters"><input id="search" type="search" placeholder="搜索片名、风格或文件路径" aria-label="搜索视频"><select id="kind" aria-label="视频来源"><option value="">全部视频</option>${[...new Set(media.map(m=>m.kind))].map(k=>`<option${downloaded.length&&k==='上游原片'?' selected':''}>${escape(k)}</option>`).join('')}</select><select id="package" aria-label="参考工程"><option value="">全部工程</option>${packageOptions}</select><span id="count" aria-live="polite"></span></div><div id="videos">${cards}</div></section>
<section id="code"><h2>固定版本参考代码</h2>${table(['工程','可借鉴的画面与机制','本地代码','实际状态'],rows)}<h2>更早的研究代码与资料</h2>${table(['来源','风格 / 方法','本地入口','边界'],legacy.map(([name,style,entry,status])=>`<tr><td>${escape(name)}</td><td>${escape(style)}</td><td>${link('代码 / 资料',entry)}</td><td>${escape(status)}</td></tr>`).join(''))}</section>
<section id="mg"><h2>MG：15种风格</h2><p>${mg.filter(s=>s.localVideo).length}/15支作者原片已保存在本地，绘制源码保持原来的固定版本。三维软质渲染分支使用Blender；原片归档不改变代码运行的验证状态。</p>${table(['风格','本地绘制入口','原片','归档状态'],mgRows)}</section>
<section id="lemo"><h2>Lemo：43种风格</h2><p>${lemo.filter(s=>s.localVideo).length}/43支风格原片已保存在本地，另含OPUSCAR 98长片。绘制源码本地归档4套：装饰艺术、工程蓝图、中国水墨、科幻全息HUD；其余39种提供上游代码入口。${link('本地README',`${archive}/lemo-opuscar/README.md`)} · <a href="https://lemomo-ai.github.io/lemo-opuscar/">作者在线图库</a></p>${table(['风格','代码入口','本地原片','源码状态'],lemoRows)}</section>
<section id="methods"><h2>37张导演与实现方法卡</h2><p>方法卡覆盖程度不同，不等同于37种效果全部运行。${link('方法与证据原始数据',`${skill}/references/opus-methods.json`)}</p><ol class="methods">${methods.map(m=>`<li>${escape(m.title)} <code>${escape(m.id)}</code></li>`).join('')}</ol></section><footer>保留作者、来源、版本、尺寸、时长和哈希。不新生成或审阅视频；制作参考与代码复现证据分开记录。</footer></main><script>
const clips=[...document.querySelectorAll('.clip')],search=document.querySelector('#search'),kind=document.querySelector('#kind'),source=document.querySelector('#package');
function filter(){const q=search.value.trim().toLowerCase();let shown=0;for(const clip of clips){clip.hidden=!!((kind.value&&clip.dataset.kind!==kind.value)||(source.value&&clip.dataset.package!==source.value)||(q&&!clip.textContent.toLowerCase().includes(q)));if(!clip.hidden)shown++;else clip.querySelector('video')?.pause()}document.querySelector('#count').textContent=shown+' / '+clips.length}
search.addEventListener('input',filter);kind.addEventListener('change',filter);source.addEventListener('change',filter);filter();
for(const video of document.querySelectorAll('video'))video.addEventListener('play',()=>{for(const other of document.querySelectorAll('video'))if(other!==video)other.pause()});
</script></html>`;

const lines = [
 '# 当前可参考代码、风格与本地视频', '', '盘点日期：2026-10-10。此清单整理现有文件，不新生成视频，也不启动自主审片。新制作默认1080×1920竖屏；原片与历史横版保留。', '',
 `可播放目录：${mdLink('index.html',`${out}/index.html`)}。共${media.length}个视频文件，含历史版、静音版、预演与技术验证，不等于${media.length}种风格。`, '',
 '## 10套固定版本参考源码', '', '| 工程 | 可借鉴风格与机制 | 本地入口 | 当前边界 |','|---|---|---|---|',
 ...packages.map(p=>`| ${p.title} / ${p.id} | ${p.styles} | ${mdLink('源码',p.entry)} · ${mdLink('SOURCE.json',p.source)} | ${p.status} |`), '',
 '## 更早的研究代码与资料', '', ...legacy.map(([name,style,entry,status])=>`- ${name}：${style}。${mdLink('本地入口',entry)}。${status}。`), '',
 '## 上游原片归档', '', archiveSummary+'。文件按作者发布版本原样下载，未自行重渲或转码。', '', mdLink('来源、哈希与媒体元数据',upstreamPath), '', ...downloaded.map(i=>`- ${i.title}：${mdLink('本地播放',i.path)} · [作者发布入口](${i.url}) · ${i.metadata.width}×${i.metadata.height} · ${i.metadata.duration||'时长未知'}秒。${i.note}`), '',
 '## MG的15种风格', '', `以下15种均有本地代码，原片已归档${mg.filter(s=>s.localVideo).length}支；代码尚未逐片运行。`, '', '| 风格 | 本地代码 | 作者影片 |','|---|---|---|',
 ...mg.map(s=>`| ${s.title} | ${mdLink(s.id,s.entry)} | ${s.localVideo?mdLink('本地原片',s.localVideo):`[在线原片](${s.watch})`} |`), '',
 '## Lemo的43种上游风格索引', '', '本地归档4种：装饰艺术、工程蓝图、中国水墨、科幻全息HUD。其余39种只保存了README中的索引，没有对应风格源码，不能当作已经掌握或复现。', '', '| 风格 | 入口 | 本地状态 |','|---|---|---|',
 ...lemo.map(s=>`| ${s.title} | ${s.entry?mdLink(s.id,s.entry):`[上游指南](${s.guide})`} ${s.localVideo?' · '+mdLink('本地原片',s.localVideo):''} | ${s.entry?'有本地源码；未运行':'未归档此风格源码'} |`), '',
 '## 尚未取得的上游原片', '', ...missing.map(i=>`- ${i.title}：[作者入口](${i.url})。${i.error?.includes('404')?'上游附件持续返回404，未找到作者替代发布':'下载失败，详情见manifest.json'}。`), '', 'I Like Ur Look：当前作者README仍为link coming soon；无发布附件。Clearwater：仓库和发布页没有原片，保留互动演示源码。Work Reel：已保存作者GIF演示，84秒完整MP4未公开。Lugia：仓库和发布页没有成片，已有的本地重渲片段保持原标识。', '',
 '## 外部原片与重制版', '', ...refs.map(([relative,title,kind,note,entry])=>`- ${title} [${kind}]：${mdLink('播放文件',path.join(root,relative))}。${note}。${entry?mdLink('代码 / 资料',path.join(root,entry)):''}`), '',
 '## 已有项目样片', '', ...examples.map(([relative,title,note,entry])=>`- ${title}：${mdLink('播放样片',path.join(root,relative))} · ${mdLink('代码',path.join(root,entry))}。${note}。`), '',
 '## 37张方法卡', '', ...methods.map(m=>`- ${m.title}：\`${m.id}\``), '',
 '## 全部现有视频文件', '', ...media.map(m=>`- [${m.kind}] ${mdLink(m.relative,m.path)}（${(m.bytes/1048576).toFixed(1)} MB）`), '',
 '## 核对依据', '', mdLink('源码方法与证据',`${skill}/references/opus-methodology.md`),mdLink('参考来源与版本',`${skill}/references/sources.md`),mdLink('风格生产规范',`${skill}/references/style-production.md`),mdLink('项目检查点',`${root}/CHECKPOINT.md`), '',
 '渲染成功、查看静帧、连续帧取样、实时播放、听音、用户接受是不同状态；此盘点没有新增视觉验收。'
];
fs.writeFileSync(`${out}/index.html`,html);
fs.writeFileSync(`${out}/CATALOG.md`,lines.join('\n'));
fs.writeFileSync(`${out}/catalog.json`,JSON.stringify({checked:'2026-10-10',packages,mg,lemo,legacy,methods,media,upstreamSummary:upstream.summary,missing},null,2));
console.log(JSON.stringify({packages:packages.length,mg:mg.length,lemoLocal:lemo.filter(s=>s.entry).length,lemoIndex:lemo.length,methods:methods.length,media:media.length,externalOriginal:media.filter(m=>m.kind==='外部原片').length,output:slash(out)}));
