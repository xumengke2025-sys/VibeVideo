# 从代码作品学习导演、摄影和美术

适用：用户要求吸收开源代码作品、研究代码动画，或需要空间摄影、遮挡揭示、粒子世界、文字与着色器混合。这里的研究对象有实际绘制源码；图库中的技术标签、成片链接和提示词不能单独证明代码来源。

## 先确认画面是谁画出来的

沿 `入口 → 场景/几何/绘制/着色器 → 时间接口 → 逐帧输出` 取证。检查所采用文件的依赖、网络调用和素材输入，再在阻断外部网络的浏览器中出图。字体、引擎包、本地传帧 POST、TTS 都不等于模型生视频；同样，代码只是调用 Sora/Runway 等生成端点，也不能据此称为代码绘制。混合工程要具体到采用的分支，不能给整个仓库统一贴标签。

2026-10-09 固定的研究对象：

|来源|绘制与时间证据|本轮实际验证|采用范围|
|---|---|---|---|
|[particle-beach](https://github.com/ishuagrawal/particle-beach/tree/92db82255b962acf2930f19bf6e5e7790174a790)|`js/main.js` 创建 Three 世界；`trailer-shots.js` 镜头表；`trailer.js` 的 `__trailer.frame`|20 镜头各一帧，19.2–21.2 秒共 60 连续帧，960px、sub=1；本地字体与引擎，外网零请求|图库原作者公开链接的完整电影运行源码，MIT，已随 skill 保存|
|[opus-video-skills / work-reel-26](https://github.com/tuzhechen2005/opus-video-skills/tree/59744a69c7b916cfbe4c4ec84006b0c2f5e2fde1)|`reel.js` Canvas+Three+GLSL 全场景；`cues.js` 84秒时间轴；`renderAt(t)`|11代表帧，16–17秒30连续帧；重复时刻JPEG一致，外网零请求|补充搜索找到的完整作品运行源码，MIT，已随 skill 保存；不是图库原作的同一工程|
|[opus-js-animations](https://github.com/klsoen/opus-js-animations/tree/be8d5792ffff563c9dc62933bbe5627ac41a89e0)|`assets/film-template.html` Canvas `__film.seek(t)`；`scripts/render.mjs` 本地渲染|本轮读取模板与导演资料，没有复现其示例影片|导演方法与分层绘制原则；不称展示页每部影片都有公开源码|
|[raymarched-liquid-glass](https://github.com/Faraz-Portfolio/demo-2025-raymarched-liquid-glass/tree/a1a3b134ef82e7ace42273b40d8c20616aefe4b0)|`RayMarchingMaterial.tsx` SDF；`RaymarchedStandardMaterial.ts` 光线步进/法线接入物理材质|读取核心；没有运行原工程|未发现明确 LICENSE，只研究公开原理。独立实现的 SDF 小实验另见下文|

更早已经复现的 PDoom 工程、曲线到峡谷和扫描揭示见 [reference-study.md](reference-study.md)。这些对象是有边界的实作经验，不代表 513 部作品全部复现，也不是模型训练或永久改变模型权重。

## 把惊艳归因到具体决策

以下源码锚点在随附的固定版本中也可直接搜索。先学它为什么这样拍，再决定是否迁移。

|观众所得与机制|实际实现锚点|迁移时的决策与风险|
|---|---|---|
|太阳与轮廓巨大、空间被压紧|[beach 镜头 49–71](https://github.com/ishuagrawal/particle-beach/blob/92db82255b962acf2930f19bf6e5e7790174a790/js/trailer-shots.js#L49)：距轮约205m，竖直FOV8.2→7°，横移12m|长焦配远机位才改变透视关系。单独缩FOV只改变取景；用主体屏幕占比检查，不能机械套一个焦段|
|观众进入世界，前景掠过强化纵深|[beach 75–90](https://github.com/ishuagrawal/particle-beach/blob/92db82255b962acf2930f19bf6e5e7790174a790/js/trailer-shots.js#L75)：1→1.35m低位，穿行人群，FOV38°|要有真实前中后景、遮挡和运动视差；移动整张图不提供同样空间。检查主体短暂被挡后的重新出现，以及相机实体碰撞|
|从局部障碍中发现完整主体|[beach 133–159](https://github.com/ishuagrawal/particle-beach/blob/92db82255b962acf2930f19bf6e5e7790174a790/js/trailer-shots.js#L133)：位置、look-at各自centripetal样条，从柱间升高|位置和看向目标分别编排，不用一直绕原点。开始先保留一个锚点，揭示结果后停止；样条可能穿实体，必须实际审帧|
|关键动作保持可读|[beach 162–180](https://github.com/ishuagrawal/particle-beach/blob/92db82255b962acf2930f19bf6e5e7790174a790/js/trailer-shots.js#L162)：相机近乎固定，look-at逐渐跟过山车|主体动时相机不必同时炫技。接触、变形、选择等因果点先读得懂，随后再移动|
|同一世界呈现时间变化|[beach 241–277](https://github.com/ishuagrawal/particle-beach/blob/92db82255b962acf2930f19bf6e5e7790174a790/js/trailer-shots.js#L241)：天文时间、车轮灯、曝光、机位分别随镜头变化|光必须改写场景层关系，不能只在最上层变色。共享世界光照，曝光按镜头目的调整；真实时间公式不保证画面每帧都正确|
|粒子画面仍有实体结构|`beach/js/core.js` 的 occluder、`stippled` 与共享 uniforms|透明点云往往需要不可见实体写深度或遮挡，避免穿墙。独立检查 depthWrite、排序和逆光层次|
|地形的密度和材质来自结构|[reel 40–119](https://github.com/tuzhechen2005/opus-video-skills/blob/59744a69c7b916cfbe4c4ec84006b0c2f5e2fde1/skills/kinetic-reel/examples/work-reel-26/reel.js#L40)：粒子顶点波、domain-warp fbm、程序化matcap+背面外壳描边|不是一张背景图做缩放。纹理与主体动作联系，点大小随深度，远场衰减；matcap是外观近似，不宣称真实金属环境反射|
|点云承接身份并成为有意义形状|`reel.js:122–194` 的 A/B 点对应、固定随机与 `cloud.project`|配对点必须共享身份。二维标注用最终世界位置投影，匹配相机和shader偏移；不要忽略wobble后称完美贴合|
|选择元素后钻入其含义|[reel 1045–1118](https://github.com/tuzhechen2005/opus-video-skills/blob/59744a69c7b916cfbe4c4ec84006b0c2f5e2fde1/skills/kinetic-reel/examples/work-reel-26/reel.js#L1045)：旧镜末帧冻结，选中矩形按对数比例放大，新镜通过裁切进入|这是冻结帧变换+遮罩交接，不是任意字形/物体morph。旧对象身份与下一镜意义要连续，入镜内容同时完成自己的动作|
|文字既是信息，也是可见材质窗口|`reel.js` 的 `texWindow`、`sSg1` 和后处理|字体先ready；按字形mask裁切运动材质，再用清晰字形承担信息。RGB分离/故障只在动作风险点使用，不遮挡正文|
|绘画有生命而不全帧乱抖|`opus-video-skills/skills/painted-animation/template/src/core.js:21–26,61–62,284–302`，`clawd.js:34–42,65–67`|对象/身体部位拥有稳定随机流；绘画动作可以12fps，相机连续。调用次序不是稳定身份；按元素ID+绘画时刻重置种子，避免某只手动导致背景重抖。本轮只读源码，未渲染此分支|
|玻璃轮廓融合、背景位移可见|`RayMarchingMaterial.tsx` 的SDF组合，`RaymarchedStandardMaterial.ts:92–137` 的法线与marching|先区分mesh transmission、SDF轮廓和屏幕折射。背景要有可读结构才能验折射。一次界面近似、无出口求交的实现不能称完整折射或焦散|

## 可直接用的资源

### 原工程代码练习库

[assets/code-studies](../assets/code-studies/) 保存上述两部作品的完整绘制运行部分，约635KB，不包含无关网站文档或远程成片。每部的 `SOURCE.json` 列出原相对路径与逐文件SHA256；源文件保持原样，MIT署名在各自 LICENSE。海滩另保留作者 `record.mjs` 供研究；它含macOS默认设置，Windows用本技能回放器。字体不随库分发，默认系统字体替代，不能据此称字排像素级一致。

`scripts/capture_code_study.mjs` 在本地服务器中只改引擎/字体路径，阻断全部外网，保存代表帧、连续JPEG和取证JSON。它不把本地POST当作AI端点，不静默下载视频。先复用已有Playwright和对应Three版本；也可在 `assets/code-studies` 中安装 package.json 的依赖。

```text
node scripts/capture_code_study.mjs --study=beach --three=<three0.169包目录> --playwright=<playwright-core目录> --out=<任务输出> --times=2.7,7.8,22.2,53.4 --range=19.2:21.2
node scripts/capture_code_study.mjs --study=reel --three=<three0.160包目录> --playwright=<playwright-core目录> --out=<任务输出> --times=2.5,48.5,50.25 --range=16:17
```

可设置 `--chrome=<浏览器可执行文件>`、`--width=960`、`--sub=2`（海滩）。`--font-dir` 支持本地化的 `beach.html/reel.html` 与字体缓存；研究输出说明是否替代字体。窗口中每帧真实求值，不以截图缩放冒充原场景运动。未经监听音轨，本回放只证明画面。

### 原创摄影工具与完整短片起点

[assets/cinematic-starter](../assets/cinematic-starter/) 是「光庭」的可编辑完整工程：程序化结构、细节刻度、玻璃、世界遮挡、同一光束的事件、低位穿行与升高揭示。复制到用户任务目录，再改 brief、几何和时序；不要把金色光学装置变成所有题材的固定美术。无远程影像、无生成API，文字使用系统字体。

`camera-kit.mjs` 提供位置/目标双轨迹、弧长采样、五次平滑起停、真实相机应用、竖直FOV与焦段换算、匹配景别的FOV和屏幕投影。弧长采样均匀化的是路径距离，外层ease仍改变速度；目标轨迹有自己的参数，仍须审构图。工具不包含自动避障、景深或物理摄影模拟。

`render.mjs` 通过 `renderAt(t)` 捕获，可加时间采样抗闪烁，先把JPEG落盘再编码；同输出目录只在源码哈希、区间与采样配置一致时续跑。进度、失败诊断、时间寻址哈希、相机边界与成片哈希保存到输出，避免中断后交付缺moov的MP4。完成后仍需decode和审片。`score.py` 可选择生成原创合成音床与接触钟声；不强制Python、配乐或旁白。

```text
npm install
node render.mjs --chrome=<Chrome路径> --ffmpeg=<FFmpeg路径> --out=out --sub=2
python score.py
ffmpeg -i out/lumen.mp4 -i score.wav -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -shortest out/lumen-sound.mp4
```

renderer可通过 `--playwright`、`--three` 复用本机包，支持 `--stills-only`、`--stills=...`、`--range=起点:终点`、`--name=...`。重复像素不同会保留false结果并警告；要求字节一致时加 `--strict-pixels`。Unix需给已有浏览器路径，或为Playwright安装可用浏览器。SDF目录没有package.json依赖，调用时显式给上述两个包路径。这里的源码库不预先占用用户的项目目录或启动后台服务。

### 独立 SDF 玻璃实验

[assets/sdf-glass-lab/index.html](../assets/sdf-glass-lab/index.html) 是原生WebGL2的自包含实验；有 `renderAt(t)` 与 `__film`，可用上述renderer的 `--project` 捕获。SDF轮廓、法线、折射与Fresnel均为代码；无引擎CDN、图像或视频资产。它只作单界面背景折射近似，未求出口、体内多次反射或焦散。

## 不盲目继承原工程的缺陷

海滩同页进入镜头会预跑3秒、补跑历史帧，但重复捕获的JPEG仍有约0.016–0.019/255的RGB平均绝对差；已验证的文字作品则一致。解析动画全部由t求值；有状态世界要用固定步长、完整重置或检查点+历史重播，分别测顺序、乱序和新进程，不只抄一句“纯函数”。本轮也观察到海滩17.1/17.7秒代表帧近全黑，尚未定位原因，不能把这个局部作为复现质量标杆。

默认只在题材需要时采用方法。做一张设定帧确认材质，再做最难的连续窗；看片后把发现写为可执行修正：前景挡住锚点→改变轨迹/遮挡时长，光路常亮→改为事件分发，极细线闪烁→增厚/加采样，玻璃发白→调整反射环境与曝光。源码阅读、实际渲染和迁移成功分别记录，不能互相替代。
