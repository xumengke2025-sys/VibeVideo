import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
const root=path.dirname(fileURLToPath(import.meta.url));
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const put=(p,s)=>fs.writeFileSync(path.join(root,p),s);
const archive='production-plan-v2-historical.json';
if(!fs.existsSync(path.join(root,archive)))fs.copyFileSync(path.join(root,'production-plan.json'),path.join(root,archive));
const specs=read('assets/rebuild-v3/prompts.json').specs;
const keys=['01_cave','02_egypt','03_greek','04_roman','34_shadowpuppet','05_gothic','06_renaissance','32_rembrandt','17_ink','08_impressionism','09_postimp','11_cubism','33_rubberhose','23_dali','13_pop','14_8bit'];
const dates=['约公元前16000年','约公元前1350年','约公元前530年','公元79年','约1050年','约1290年','1503年','1642年','约1690年','1874年','1889年','1912年','1930年','1931年','1962年','1985年'];
const action='初始缩颈→伸颈到旁边动物脚边→叼走地上的鱼→抬头吞咽→收颈归位';
const reaction='同一相位：发现鱼被取走后轻微后仰抬头，再俯身查看原位置；无争抢、追逐或对抗。';
const evidence=read('out/film-v3/evidence.json');
const plan={title:'夜鹭偷鱼艺术史',version:'rebuild-v3-generated-all-eras',date:'2026-10-15',status:'playable_engineering_verified',
 brief:{aspect_ratio:'9:16',width:1080,height:1920,fps:24,duration:40,eraCount:16,delivery_mode:'ai_review_once',onscreenText:'仅时代与年份，无片名、说明、动作旁白或画风名',audio:'沿用原创合成配乐，无旁白'},
 requirements:['16时代分别生图，夜鹭、鱼和其他动物均采用对应画风','实际移植花叔背景和材质源码并重排为竖屏','同一偷鱼动作和同一动物反应','多关节缩颈—伸颈—收颈；全程无对抗','地点/年代/动物相容，证据强度见历史台账'],
 direction:{promise:'同一只夜鹭、同一偷鱼节拍跨越16时代与画风',action,reaction,rig:'肩根、上颈、下颈、头部连接四控制关节；共享解析时间；各时代生成羽毛纹理随颈部轮廓伸展连接。',camera:'固定竖屏正侧面，保留取鱼接触点；主体锚点与动作相位跨时代保持。',concept:'out/rebuild-concept-final/styleboard.jpg',sample:'out/rebuild-sample-v2/video.mp4'},
 timeline:{opening:{start:0,end:2,action:'缩颈静候，鱼在旁边动物脚边'},shots:specs.map((s,i)=>({id:'era_'+s.id,start:2+i*2.25,end:4.25+i*2.25,date:dates[i],style:s.style,owner:s.owner,atlas:'assets/rebuild-v3/era-'+s.id+'.png',referenceScene:keys[i],action,reaction,phases:{reach:[.15,.43],grab:.44,lift:[.52,.69],swallow:[.67,.77],reset:[.74,.91]},connectionToNext:'半秒平滑叠化；保持脚底、取鱼点和头部相位；不宣称几何变形。'})),outro:{start:38,end:40,action:'最后一时代缩颈停留，无标题'}},
 source:{upstream:'alchaincyf/huashu-art-motion',commit:'64cb27271ee0ad3375298e2890b33cbec36d4051',license:'MIT',vendor:'vendor/huashu',provenance:'vendor/huashu/provenance.json',adaptation:'运行原生背景、材质和装饰；移除原叙事角色、文字及部分家具；竖屏裁取与局部同源材质铺底。'},
 assets:{generation:'内置image_gen，16次分别生成各时代5拆件，原PNG保留',prompts:'assets/rebuild-v3/prompts.json',manifest:'assets/rebuild-v3/atlas-manifest.json',history:'research/history-v3.md'},
 review:{mode:'ai_review_once',budget:'既有一轮与一次修复已使用，不另派新审片者，不重开全面审核。',currentStatus:'主制作查看样段与代表帧，非独立；未完成完整听音或实时视听审核。',oldReports:'qa/film-v1/report.md 与 qa/film-v2/delivery-report.md，不覆盖新版。'},
 deliverables:{video:'out/film-v3/video.mp4',sha256:evidence.sha256,entry:'rebuild-v3.html',source:'src/film-v3.js',sourceSnapshot:'out/film-v3/source',legacy:'旧入口、源码与历史影片保留'}};
put('production-plan.json',JSON.stringify(plan,null,2));
const readme=`# 夜鹭偷鱼艺术史 · v3

16时代，1080×1920竖屏，24fps，40秒。全部分别使用内置 image_gen 生成夜鹭、其他动物与鱼，画风贯穿全部要素。实际移植花叔源码背景与材质，再作竖屏构图。只显示时代与年份，原创合成配乐，无旁白。

动作：${action}。颈部使用四个控制关节及对应时代羽毛纹理。其他动物反应：${reaction}

## 预览和输出

本目录运行 node serve.mjs，打开 http://127.0.0.1:8146/rebuild-v3.html 。网页可播放音频、拖动时间轴。

命令：
node build-source-v3.mjs
python prepare-atlases.py
node render.mjs --mode=concepts --version=新的概念图版本名 --entry=rebuild-v3.html
node render.mjs --mode=video --version=新的成片版本名 --entry=rebuild-v3.html


依赖本机Chrome、工作区Playwright和Remotion附带FFmpeg。换电脑需更新render.mjs中的三处路径。Python仅用于测量alpha和制作检查联系表，不用于重绘原始生图。

- rebuild-v3.html / src/film-v3.js：新版入口、四关节颈部、统一反应、鱼绑定、标签和时间轴。
- assets/rebuild-v3/era-01.png至era-16.png：16套独立生成原素材；prompts.json为完整提示词；atlas-manifest.json为裁切。
- vendor/huashu/：MIT许可、移植源码、逐文件来源与改编哈希。
- research/history-v3.md：16时代、地点、动物、事实来源和证据强度。
- production-plan.json / CHECKPOINT.md：当前计划与完成范围；v2历史计划单独保留。
- out/film-v3/video.mp4：新版成片；out/rebuild-concept-final/styleboard.jpg：16画风总览。

0–2秒建立；2–38秒16时代、每段2.25秒；38–40秒收尾。半秒平滑叠化保留动作相位与取鱼锚点。这是匹配动作的材质转换，不是几何连续变形。

## 来源与实际范围

花叔alchaincyf/huashu-art-motion固定提交64cb27271ee0ad3375298e2890b33cbec36d4051，MIT。新版运行其背景/材质函数，移除了原片人物、叙事文字及部分家具；竖屏采用裁取、重排和同源材质铺底。改编关系见vendor/huashu/provenance.json。未将原片抽帧当背景，未重渲完整上游影片。

这是虚构夜鹭穿越艺术时代的喜剧。动物选择追求地域/年代相容，生成画面不是考古重建或物种出现年代证明，依据及局限见历史台账。

旧入口index.html、旧源码和历史影片全部保留。既有审核预算不重置。新版工程检查和实际制作查看与本版媒体哈希绑定；主制作查看不等于独立审核，解码与音量检查不代表听过完整音轨。
`;
put('README.md',readme);
const snapshot=path.join(root,'out/film-v3/source'),frozen=[];
for(const file of [...evidence.sourceFiles,'build-source-v3.mjs','prepare-atlases.py','render.mjs','production-plan.json','README.md','research/history-v3.md']){
 const src=path.join(root,file),dst=path.join(snapshot,file);fs.mkdirSync(path.dirname(dst),{recursive:true});fs.copyFileSync(src,dst);frozen.push({file,sha256:createHash('sha256').update(fs.readFileSync(dst)).digest('hex')});
}
put('out/film-v3/source-manifest.json',JSON.stringify({signature:evidence.signature,videoSha256:evidence.sha256,files:frozen},null,2));
console.log(JSON.stringify({video:evidence.video,sha256:evidence.sha256,decoded:evidence.decoded,sourceFiles:frozen.length}));
