# 原片、风格影片与对应源码

<!-- source-maintenance-20261020 -->
2026-10-20维护后累计498个参考，288个有对应源码。本次新增40个影片/对照和139个短样段，均有本地视频（MP4／WEBM）与绘制入口。新增Lemo实证影像、产品动效复刻、Kiteva风格样段、WebGL风景及模型对照；复刻、混合模型与非商业许可须按每条记录使用。可搜索“显微镜”“激光点云”“奔跑猫”“粒子流网络”。检查点：项目 work/github-reference-expansion-20261020/CHECKPOINT.md。

本机2026-10-14累计319个可播放参考，109个有对应绘制源码（含镜头样段）。本轮接入221条；其中30条为此前已保存的作者原片，不计新下载。视频保存在项目reference-sources，技能只保存检索索引；作者原片保持原画幅，新制作按用户选择横屏或竖屏分别布局。

```text
node scripts/video_examples.mjs search --query "产品 运镜" --source present --limit 5
node scripts/video_examples.mjs search --query "纸艺 手绘" --source missing
node scripts/video_examples.mjs search --kind "影片与源码"
node scripts/video_examples.mjs card kimi-manim/MeltingSpace
node scripts/video_examples.mjs card shotcraft/mosaic-reframe
node scripts/video_examples.mjs verify
```

结果返回本地视频、实际绘制入口或来源记录、固定版本、许可、元数据与验证范围。统一播放目录为项目 `work/github-reference-expansion-20261011/index.html`，用 `npm run preview:references` 启动。网页按画风、作品类型、源码状态和批次筛选并分页。GitHub仓库保存索引和来源；先运行 `npm run references:plan` 查看规模，再按需用 `npm run restore:references` 从原作者地址恢复约6.14 GB资料，校验大小和SHA256，不执行上游代码。仓库内技能自动识别项目根目录；单独安装技能时用 `--root` 或 `VIBE_VIDEO_REFERENCE_ROOT` 指向克隆并恢复后的项目。抽帧海报为可选本地缓存，不随公开包上传。

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

扩库前先查本索引及旧catalog，再按作者帖status ID、媒体SHA256、近似时长和20/50/80%三帧指纹查重。近似候选人工核对，同一作品重编码通常只展示一条；横竖版、不同剪辑或原作/改编保留价值时注明关联，不当成独立的新风格。三帧不能保证发现所有片段/变速/重剪重复。本轮处理记录在项目 `work/video-film-expansion-20261014/duplicate-decisions.json`。

新增媒体已核对哈希、元数据、入口存在与完整音视频解码；旧媒体本轮仅新增指纹，历史解码记录仍按原批次。没有全库动态审美、听音或源码批量重渲验收。固定Git blob和逐文件SHA256验证不等于运行测试。

代码MIT、Apache或索引CC BY不自动覆盖影片、歌曲、字体及第三方素材。xiaoma、Kimi、花叔与阿杜按各仓库LICENSE和第三方说明；公开作者影片未取得开放素材许可时仅按视觉参考标注。Shotcraft声音许可见原assets/audio/ATTRIBUTION.md；Claude Glass代码MIT、绘画与影片CC BY4.0；Particle Beach代码MIT。来源与失败记录见项目 `reference-sources/video-films-20261014/manifest.json` 和本轮CHECKPOINT。
