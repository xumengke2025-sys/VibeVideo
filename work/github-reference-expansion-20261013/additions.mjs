export const definitions={
 'DDChen666/civilization-film':{title:'人类大历史：文明长镜头',kind:'完整影片工程',tags:'历史 文明 地图 地球 一镜到底 长镜头 科普 程序化音乐 中文',license:'代码 MIT；影片/配乐/文档图像 CC BY 4.0；字体 OFL；地图公有领域',entries:['stage.html','src/film.js','src/engine.js','score.py','render.mjs'],note:'149秒从洞穴手印持续拉远到地球；176个历史节点与代码配乐同步。保存简体中文作者发布片。'},
 'az9713/opus-5.5-musical-cartoon':{title:'Clawd 水彩音乐短片',kind:'完整影片工程',tags:'手绘 水彩 卡通 Clawd 角色 喜剧 音乐 节拍 p5 brush',license:'未发现明确许可，仅本地研究',entries:['clawd-prose/index.html','clawd-prose/scene.js','clawd-prose/score.mjs','clawd-prose/render.mjs'],note:'15秒水彩角色短片：语言机器、角色动作和原创合成音效/配乐；绘制与渲染源码对应。'},
 'bilaldemirerr/opus-video-recipes':{title:'HyperFrames 排版与竖屏解说',kind:'完整示例工程',tags:'动态图形 排版 字幕 竖屏 科普 解说 旁白 HTML GSAP HyperFrames',license:'代码/提示词 MIT；媒体与品牌权利独立，仅本地参考',entries:['kinetic-typography-explainer/index.html','captioned-vertical-clip/index.html'],note:'2段同目录成片与HTML/GSAP时间轴源码。App Store条目只有brief与影片链接，没有绘制代码，未收录。'},
 'c5inco/motion-showreel':{title:'Android 原生动效与 AGSL',kind:'完整影片工程',tags:'动态图形 字体 三维 粒子 流体 着色器 Android Kotlin AGSL 循环',license:'代码 MIT；字体 OFL；发布录屏未见单独媒体授权，仅本地参考',entries:['app/src/main/java/com/example/showreel/Reel.kt','app/src/main/java/com/example/showreel/Shaders.kt','app/src/main/java/com/example/showreel/Particles.kt','app/src/main/java/com/example/showreel/MainActivity.kt'],note:'15秒Kotlin/Compose展演，流体着色器、形状变换与3600粒子；保存同v1.0发布的模拟器录屏及源码，不是MP4播放器源码。'},
 'toankhontech/pelican-test-opus55':{title:'海滨骑车鹈鹕：SVG角色运动',kind:'完整动画示例',tags:'卡通 角色 鹈鹕 自行车 SVG SMIL 关节 几何 海滨 循环',license:'未发现明确许可，仅本地研究',entries:['pelican-bicycle-animated.svg','index.html'],note:'7.2秒作者MP4和自包含SVG/SMIL动画；可参考车轮、腿部关节与循环运动。没有模型会话记录。'},
 'JakeB-5/motion-graphic-skill':{title:'韦伯望远镜、咖啡与扁平动效',kind:'完整示例工程',tags:'科普 韦伯 太空 望远镜 手冲 咖啡 V60 扁平 插画 卡通 节拍 音乐',license:'MIT；示例事实出处保留，外部资料权利独立',entries:['samples/webb-telescope/opus/index.html','samples/pour-over/opus/index.html','samples/skill-intro/opus/index.html','skills/motion-graphic/scripts/record.js'],note:'只收作者明确标注的3段Opus 5.5影片：韦伯望远镜45秒、手冲咖啡30秒、技能介绍30秒。Sonnet和Codex影片未归档。'},
 'Vincentwei1021/mg-styles-15':{title:'MG 15种完整风格源码',kind:'风格工程合集',tags:'扁平 线条 等距 三维 逐帧 拼贴 液体 变形 包豪斯 合成波 玻璃 像素 HUD 综艺 字幕',license:'作者代码/提示词/影片 MIT；第三方CC0/公有领域/OFL/BSD分别保留；字体文件未包含',entries:['demos/01-flat-vector/index.html','demos/04-3d-render/blender/scene.py','harness/render.mjs','assets/fonts/README.md'],note:'补齐已有15段作者原片的全部绘制目录、音频脚本、时间表与渲染器；含Blender三维及9:16综艺字幕。未另算为新发现影片。'}
};
const mgTitles={'01-flat-vector':'扁平矢量','02-line-art':'线条艺术','03-isometric':'等距空间','04-3d-render':'Blender 三维字体','05-cel-boil':'逐帧手绘抖动','06-collage':'纸艺拼贴','07-liquid':'液体变形','08-morph':'字体形变','09-bauhaus':'包豪斯几何','10-synthwave':'合成波','12-aurora-glass':'极光玻璃','18-hanazi':'综艺字幕／9:16','19-paperclip':'线条回形针','20-pixel':'像素动画','22-hud':'HUD 信息图'};
export function association(p,f,abs){
 const repo=p.repo,b=p.path;let entry,title,guide;
 if(repo==='DDChen666/civilization-film'){entry='stage.html';title='人类大历史／简体中文／149秒文明长镜头';}
 else if(repo==='az9713/opus-5.5-musical-cartoon'){entry='clawd-prose/index.html';title='Clawd：Mannered Prose／水彩音乐短片';}
 else if(repo==='bilaldemirerr/opus-video-recipes'){entry=f.path.split('/')[0]+'/index.html';title=f.path.startsWith('captioned')?'竖屏字幕解说／本地 TTS':'Opus 5.5 新功能／动态排版解释片';}
 else if(repo==='c5inco/motion-showreel'){entry='app/src/main/java/com/example/showreel/Reel.kt';title='Android 原生动效展演／流体与粒子';}
 else if(repo==='toankhontech/pelican-test-opus55'){entry='pelican-bicycle-animated.svg';title='海滨骑车鹈鹕／SVG 动画';}
 else if(repo==='JakeB-5/motion-graphic-skill'){entry=f.path.slice(0,f.path.lastIndexOf('/'))+'/index.html';title=f.path.includes('webb-')?'韦伯太空望远镜／45秒科普':f.path.includes('pour-over')?'V60 手冲咖啡／温暖插画指南':'贴纸笔记本／扁平卡通技能介绍';}
 else if(repo==='Vincentwei1021/mg-styles-15'){const style=f.path.split('/').at(-1).replace('.mp4','');entry=style==='04-3d-render'?`demos/${style}/blender/scene.py`:`demos/${style}/index.html`;title='MG / '+mgTitles[style];guide=abs(b+'/prompts/'+style+'.md');}
 else return null;
 return {title,tags:/^(JakeB|Vincent)/.test(repo)?title+' '+entry:p.tags,entry:abs(b+'/'+entry),guide,kind:'影片与源码',sourceStatus:'作者影片与同项目绘制源码；已核对入口与时间轴，未验证重渲',representation:repo.startsWith('c5inco')?'作者发布的模拟器录屏':repo.startsWith('Vincent')?'已有作者原片（本次补齐完整源码）':'作者仓库／发布影片',addedRound:'2026-10-13',newlyDownloaded:!f.reusedExistingMedia};
}
