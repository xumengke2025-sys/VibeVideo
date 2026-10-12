# 当前可参考代码、风格与本地视频

盘点日期：2026-10-10。此清单整理现有文件，不新生成视频，也不启动自主审片。新制作默认1080×1920竖屏；原片与历史横版保留。

可播放目录：[index.html](<D:/ai项目/ai动画/VibeVideo项目/work/reference-catalog-20261010/index.html>)。共73个视频文件，含历史版、静音版、预演与技术验证，不等于73种风格。

## 10套固定版本参考源码

| 工程 | 可借鉴风格与机制 | 本地入口 | 当前边界 |
|---|---|---|---|
| 粒子海滩电影 / particle-beach | 点云世界、长焦、低位穿行、昼夜光照、双轨迹摄影 | [源码](<D:/Codex/skills/vibe-video/assets/code-studies/particle-beach/js/trailer-shots.js>) · [SOURCE.json](<D:/Codex/skills/vibe-video/assets/code-studies/particle-beach/SOURCE.json>) | 绘制运行部分已回放；没有本地作者原片 |
| 动效作品集 / work-reel-26 | 点云变形、程序化材质、文字窗口、局部放大交接 | [源码](<D:/Codex/skills/vibe-video/assets/code-studies/work-reel-26/skills/kinetic-reel/examples/work-reel-26/reel.js>) · [SOURCE.json](<D:/Codex/skills/vibe-video/assets/code-studies/work-reel-26/SOURCE.json>) | 绘制运行部分已回放；没有本地作者原片 |
| 15种MG风格 / mg-styles-15 | 完整名单见下表；SVG / Canvas / WebGL / Three.js / Blender | [源码](<D:/Codex/skills/vibe-video/assets/code-studies/mg-styles-15/README.md>) · [SOURCE.json](<D:/Codex/skills/vibe-video/assets/code-studies/mg-styles-15/SOURCE.json>) | 15种本地绘制源码；素材和依赖不完整，尚未逐片运行；无本地原片 |
| 4种已归档影片风格 / lemo-opuscar | 装饰艺术、工程蓝图、中国水墨、科幻全息HUD | [源码](<D:/Codex/skills/vibe-video/assets/code-studies/lemo-opuscar/README.md>) · [SOURCE.json](<D:/Codex/skills/vibe-video/assets/code-studies/lemo-opuscar/SOURCE.json>) | 只归档4种，未逐片运行；作者43种索引另列；无本地原片 |
| 纸片角色叙事 / papermotion | 纸片视差、角色骨骼、风雨、接触事件、相机跟随 | [源码](<D:/Codex/skills/vibe-video/assets/code-studies/papermotion/examples/light/main.ts>) · [SOURCE.json](<D:/Codex/skills/vibe-video/assets/code-studies/papermotion/SOURCE.json>) | 选定文本源码；未运行，素材和依赖不完整；无本地原片 |
| 蜡笔绘本与音乐表演 / songbie | 钢琴、角色接棒、融化、情绪与身体共享状态 | [源码](<D:/Codex/skills/vibe-video/assets/code-studies/songbie/render.js>) · [SOURCE.json](<D:/Codex/skills/vibe-video/assets/code-studies/songbie/SOURCE.json>) | 选定文本源码；未运行，钢琴音轨不随包；无本地原片 |
| 杂志排版歌词MV / i-like-ur-look-lyric-video | 曲面翻页、字体、景深、弱手持、阅读节奏 | [源码](<D:/Codex/skills/vibe-video/assets/code-studies/i-like-ur-look-lyric-video/app/src/engine/curl.ts>) · [SOURCE.json](<D:/Codex/skills/vibe-video/assets/code-studies/i-like-ur-look-lyric-video/SOURCE.json>) | 选定文本源码；未运行；歌曲、字体、节拍数据不随包；无本地原片 |
| 网格浅水模拟组件 / water-opus | 地形、水流、水量预算、水面材质 | [源码](<D:/Codex/skills/vibe-video/assets/code-studies/water-opus/runs/claude-code-opus-5-5/src/sim/water.ts>) · [SOURCE.json](<D:/Codex/skills/vibe-video/assets/code-studies/water-opus/SOURCE.json>) | 技术组件；未运行，不是完整影片，也不是阀内三维流体解算 |
| WebGPU刚体组件 / three-avbd | 碰撞、关节、堆叠、断裂、GPU模拟 | [源码](<D:/Codex/skills/vibe-video/assets/code-studies/three-avbd/examples/basic.ts>) · [SOURCE.json](<D:/Codex/skills/vibe-video/assets/code-studies/three-avbd/SOURCE.json>) | 技术组件；未运行，需固定随机和离线模拟 |
| 水面光学组件 / clearwater | 折射、水底焦散、吸收、互动涟漪 | [源码](<D:/Codex/skills/vibe-video/assets/code-studies/clearwater/index.html>) · [SOURCE.json](<D:/Codex/skills/vibe-video/assets/code-studies/clearwater/SOURCE.json>) | 技术组件；未运行，固定时间不自动重建涟漪历史 |

## 更早的研究代码与资料

- PDoom / AGI概念MV：线场、逐词卡拉OK、音乐节拍、后处理、三维空间。[本地入口](<D:/ai项目/ai动画/VibeVideo项目/reference-sources/pdoom-source-review/app/src/timeline.ts>)。有本地B站重渲转载，版本与当前代码有差异。
- OpenMontage / Remotion：钩子、流程图、工具演示、动效时间轴。[本地入口](<D:/ai项目/ai动画/VibeVideo项目/work/director-study-20261008/source-snapshots/Liamrjohnston/docs/prompt-threads.md>)。有3个上游MP4和方法资料；不承诺三个示例的完整绘制源码均已保存。
- Lugia / 配对估计科普：漫画式解释、关系建立、代码分镜。[本地入口](<D:/ai项目/ai动画/VibeVideo项目/work/director-study-20261008/source-snapshots/Lugia123/episodes/ep03-paired-estimate/index.html>)。有选定分镜源码与本地重渲片段；不是完整原片。
- huashu-art-motion：分层绘制、导演经验、代码与图像素材协作。[本地入口](<D:/ai项目/ai动画/VibeVideo项目/work/director-study-20261008/source-snapshots/alchaincyf/repo.json>)。保存来源和选定研究资料；不是已验证影片模板。

## MG的15种风格

以下15种均有本地代码，但作者成片没有归档；尚未逐片运行。在线链接来自作者README，本次没有联网复核。

| 风格 | 本地代码 | 作者影片 |
|---|---|---|
| 逐帧手绘 / 抖线 | [05-cel-boil](<D:/Codex/skills/vibe-video/assets/code-studies/mg-styles-15/demos/05-cel-boil/index.html>) | [在线原片](https://vincentwei1021.github.io/mg-styles-15/#05-cel-boil) |
| 等距2.5D | [03-isometric](<D:/Codex/skills/vibe-video/assets/code-studies/mg-styles-15/demos/03-isometric/index.html>) | [在线原片](https://vincentwei1021.github.io/mg-styles-15/#03-isometric) |
| 扁平矢量 | [01-flat-vector](<D:/Codex/skills/vibe-video/assets/code-studies/mg-styles-15/demos/01-flat-vector/index.html>) | [在线原片](https://vincentwei1021.github.io/mg-styles-15/#01-flat-vector) |
| 线条艺术 | [02-line-art](<D:/Codex/skills/vibe-video/assets/code-studies/mg-styles-15/demos/02-line-art/index.html>) | [在线原片](https://vincentwei1021.github.io/mg-styles-15/#02-line-art) |
| 三维软质渲染 | [04-3d-render](<D:/Codex/skills/vibe-video/assets/code-studies/mg-styles-15/demos/04-3d-render/index.html>) | [在线原片](https://vincentwei1021.github.io/mg-styles-15/#04-3d-render) |
| 形状变形 | [08-morph](<D:/Codex/skills/vibe-video/assets/code-studies/mg-styles-15/demos/08-morph/index.html>) | [在线原片](https://vincentwei1021.github.io/mg-styles-15/#08-morph) |
| 贴纸式科普 | [19-paperclip](<D:/Codex/skills/vibe-video/assets/code-studies/mg-styles-15/demos/19-paperclip/index.html>) | [在线原片](https://vincentwei1021.github.io/mg-styles-15/#19-paperclip) |
| 赛博HUD / FUI | [22-hud](<D:/Codex/skills/vibe-video/assets/code-studies/mg-styles-15/demos/22-hud/index.html>) | [在线原片](https://vincentwei1021.github.io/mg-styles-15/#22-hud) |
| 拼贴 / 剪纸 | [06-collage](<D:/Codex/skills/vibe-video/assets/code-studies/mg-styles-15/demos/06-collage/index.html>) | [在线原片](https://vincentwei1021.github.io/mg-styles-15/#06-collage) |
| 极光 / 玻璃质感 | [12-aurora-glass](<D:/Codex/skills/vibe-video/assets/code-studies/mg-styles-15/demos/12-aurora-glass/index.html>) | [在线原片](https://vincentwei1021.github.io/mg-styles-15/#12-aurora-glass) |
| 包豪斯几何 | [09-bauhaus](<D:/Codex/skills/vibe-video/assets/code-studies/mg-styles-15/demos/09-bauhaus/index.html>) | [在线原片](https://vincentwei1021.github.io/mg-styles-15/#09-bauhaus) |
| 80年代合成波 / VHS | [10-synthwave](<D:/Codex/skills/vibe-video/assets/code-studies/mg-styles-15/demos/10-synthwave/index.html>) | [在线原片](https://vincentwei1021.github.io/mg-styles-15/#10-synthwave) |
| 像素艺术 | [20-pixel](<D:/Codex/skills/vibe-video/assets/code-studies/mg-styles-15/demos/20-pixel/index.html>) | [在线原片](https://vincentwei1021.github.io/mg-styles-15/#20-pixel) |
| 液态动效 | [07-liquid](<D:/Codex/skills/vibe-video/assets/code-studies/mg-styles-15/demos/07-liquid/index.html>) | [在线原片](https://vincentwei1021.github.io/mg-styles-15/#07-liquid) |
| 综艺花字 / 竖屏字幕 | [18-hanazi](<D:/Codex/skills/vibe-video/assets/code-studies/mg-styles-15/demos/18-hanazi/index.html>) | [在线原片](https://vincentwei1021.github.io/mg-styles-15/#18-hanazi) |

## Lemo的43种上游风格索引

本地归档4种：装饰艺术、工程蓝图、中国水墨、科幻全息HUD。其余39种只保存了README中的索引，没有对应风格源码，不能当作已经掌握或复现。

| 风格 | 入口 | 本地状态 |
|---|---|---|
| 蜡笔绘本 | [上游指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/crayon-book/STYLE.md) | 仅上游索引；未归档此风格源码 |
| 水彩笔触 | [上游指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/watercolor/STYLE.md) | 仅上游索引；未归档此风格源码 |
| 中国水墨 | [ink-wash](<D:/Codex/skills/vibe-video/assets/code-studies/lemo-opuscar/styles/ink-wash/STYLE.md>) | 有本地源码；未运行 |
| 厚涂油画 | [上游指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/impasto/STYLE.md) | 仅上游索引；未归档此风格源码 |
| 一笔画 | [上游指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/one-line/STYLE.md) | 仅上游索引；未归档此风格源码 |
| 白板科普 | [上游指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/whiteboard/STYLE.md) | 仅上游索引；未归档此风格源码 |
| 城市钢笔淡彩 | [上游指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/urban-sketch/STYLE.md) | 仅上游索引；未归档此风格源码 |
| 皮影戏 | [上游指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/shadow-puppet/STYLE.md) | 仅上游索引；未归档此风格源码 |
| 浮世绘 | [上游指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/ukiyoe/STYLE.md) | 仅上游索引；未归档此风格源码 |
| 红色剪纸 | [上游指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/papercut-red/STYLE.md) | 仅上游索引；未归档此风格源码 |
| 剪纸灯箱 | [上游指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/paper-lantern/STYLE.md) | 仅上游索引；未归档此风格源码 |
| 孔版印刷 | [上游指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/risograph/STYLE.md) | 仅上游索引；未归档此风格源码 |
| 网点档案 | [上游指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/halftone-dossier/STYLE.md) | 仅上游索引；未归档此风格源码 |
| 木刻版画 | [上游指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/woodcut/STYLE.md) | 仅上游索引；未归档此风格源码 |
| 铜版雕刻 | [上游指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/engraving/STYLE.md) | 仅上游索引；未归档此风格源码 |
| 丝网旅行海报 | [上游指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/silkscreen-poster/STYLE.md) | 仅上游索引；未归档此风格源码 |
| 瑞士平面动效 | [上游指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/swiss-motion/STYLE.md) | 仅上游索引；未归档此风格源码 |
| 60年代间谍片头 | [上游指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/spy-titles/STYLE.md) | 仅上游索引；未归档此风格源码 |
| 装饰艺术 | [art-deco](<D:/Codex/skills/vibe-video/assets/code-studies/lemo-opuscar/styles/art-deco/STYLE.md>) | 有本地源码；未运行 |
| 工程蓝图 | [blueprint](<D:/Codex/skills/vibe-video/assets/code-studies/lemo-opuscar/styles/blueprint/STYLE.md>) | 有本地源码；未运行 |
| 彩色玻璃 | [上游指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/stained-glass/STYLE.md) | 仅上游索引；未归档此风格源码 |
| 象形图标动效 | [上游指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/pictogram-motion/STYLE.md) | 仅上游索引；未归档此风格源码 |
| ASCII / CRT终端 | [上游指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/ascii-crt/STYLE.md) | 仅上游索引；未归档此风格源码 |
| 数据叙事 | [上游指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/dataviz/STYLE.md) | 仅上游索引；未归档此风格源码 |
| 等距信息图 | [上游指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/iso-infographic/STYLE.md) | 仅上游索引；未归档此风格源码 |
| 暗色科技发布会 | [上游指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/dark-keynote/STYLE.md) | 仅上游索引；未归档此风格源码 |
| 动态录屏 | [上游指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/living-screencast/STYLE.md) | 仅上游索引；未归档此风格源码 |
| 科幻全息HUD | [hologram-hud](<D:/Codex/skills/vibe-video/assets/code-studies/lemo-opuscar/styles/hologram-hud/STYLE.md>) | 有本地源码；未运行 |
| 30年代橡皮管卡通 | [上游指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/rubber-hose/STYLE.md) | 仅上游索引；未归档此风格源码 |
| 80年代赛璐珞动画 | [上游指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/cel-anime-80s/STYLE.md) | 仅上游索引；未归档此风格源码 |
| 科幻情景喜剧卡通 | [上游指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/scifi-toon/STYLE.md) | 仅上游索引；未归档此风格源码 |
| 世纪中期卡通 | [上游指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/midcentury-toon/STYLE.md) | 仅上游索引；未归档此风格源码 |
| 16位像素RPG | [上游指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/pixel-rpg/STYLE.md) | 仅上游索引；未归档此风格源码 |
| HD-2D | [上游指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/hd-2d/STYLE.md) | 仅上游索引；未归档此风格源码 |
| 微游戏合集 | [上游指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/microgame/STYLE.md) | 仅上游索引；未归档此风格源码 |
| 平面游戏节目 | [上游指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/game-show/STYLE.md) | 仅上游索引；未归档此风格源码 |
| 20年代默片 | [上游指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/silent-film/STYLE.md) | 仅上游索引；未归档此风格源码 |
| 阈限空间 / 拾得影像 | [上游指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/backrooms/STYLE.md) | 仅上游索引；未归档此风格源码 |
| 积木玩具 | [上游指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/brick-toy/STYLE.md) | 仅上游索引；未归档此风格源码 |
| 纸艺立体书 | [上游指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/paper-popup/STYLE.md) | 仅上游索引；未归档此风格源码 |
| 移轴微缩 | [上游指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/tilt-shift/STYLE.md) | 仅上游索引；未归档此风格源码 |
| 低多边形等距岛屿 | [上游指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/lowpoly-island/STYLE.md) | 仅上游索引；未归档此风格源码 |
| 玻璃产品渲染 | [上游指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/glass-product/STYLE.md) | 仅上游索引；未归档此风格源码 |

## 外部原片与重制版

- AGI概念MV / 用户此前选定参考 [外部原片]：[播放文件](<D:/ai项目/ai动画/VibeVideo项目/reference-sources/bilibili-media/BV18ta86EEHb/reference.mp4>)。线场、三维空间、逐词字幕、音乐同步；B站参数重渲转载，与当前PDoom源码不是同一版本。[代码 / 资料](<D:/ai项目/ai动画/VibeVideo项目/reference-sources/pdoom-source-review/app/src/timeline.ts>)
- Opus5.5告诉你，它是怎么做视频的 [外部原片]：[播放文件](<D:/ai项目/ai动画/VibeVideo项目/reference-sources/bilibili-media/BV1vRHa63EYg/reference.mp4>)。代码动画制作过程与画面转换；未取得对应原工程。
- TwoClipping / UI连续变形 [外部原片]：[播放文件](<D:/ai项目/ai动画/VibeVideo项目/work/opus-gallery-study-20261009/twoclipping-original.mp4>)。按钮、播放器、滑杆、图表等UI状态交接；原工程未取得。
- Koldo2k / 复古拼贴无限缩放 [外部原片]：[播放文件](<D:/ai项目/ai动画/VibeVideo项目/work/opus-gallery-study-20261009/koldo2k-original.mp4>)。摄影景观、报纸剪贴、物件门户；公开提示词含生图与Kling动画，不能当纯代码证明。
- Ror_Fly / 鸡尾酒配方动效 [外部原片]：[播放文件](<D:/ai项目/ai动画/VibeVideo项目/work/opus-gallery-study-20261009/ror-fly-original.mp4>)。从空杯到成品的原料加入、剂量和步骤；原工程未取得。
- OpenMontage / Hook [外部原片]：[播放文件](<D:/ai项目/ai动画/VibeVideo项目/work/director-study-20261008/source-snapshots/Liamrjohnston/examples/openmontage-hook.mp4>)。Remotion开场钩子、文字与流程图动效。[代码 / 资料](<D:/ai项目/ai动画/VibeVideo项目/work/director-study-20261008/source-snapshots/Liamrjohnston/docs/prompt-threads.md>)
- OpenMontage / Tool Chaos [外部原片]：[播放文件](<D:/ai项目/ai动画/VibeVideo项目/work/director-study-20261008/source-snapshots/Liamrjohnston/examples/openmontage-tool-chaos.mp4>)。工具堆叠、信息组织、节奏化演示。[代码 / 资料](<D:/ai项目/ai动画/VibeVideo项目/work/director-study-20261008/source-snapshots/Liamrjohnston/docs/prompt-threads.md>)
- OpenMontage / Claude Pipeline [外部原片]：[播放文件](<D:/ai项目/ai动画/VibeVideo项目/work/director-study-20261008/source-snapshots/Liamrjohnston/examples/openmontage-claude-pipeline.mp4>)。流程叙事、节点连接、产品讲解。[代码 / 资料](<D:/ai项目/ai动画/VibeVideo项目/work/director-study-20261008/source-snapshots/Liamrjohnston/docs/prompt-threads.md>)
- TwoClipping / Skillry重制版 [外部重制]：[播放文件](<D:/ai项目/ai动画/VibeVideo项目/work/opus-gallery-study-20261009/twoclipping-remake.mp4>)。与原片分开登记；重制技术标签不能证明原片实现。

## 已有项目样片

- 飞行器 / 主体意图与跟拍：[播放样片](<D:/ai项目/ai动画/VibeVideo项目/work/creative-upgrade-20261010/flight/out-final/flight-director.mp4>) · [代码](<D:/ai项目/ai动画/VibeVideo项目/work/creative-upgrade-20261010/flight/film.js>)。三维场景、转弯、相机跟随；静音，等待用户反馈。
- 止回阀 / 受限机械行程：[播放样片](<D:/ai项目/ai动画/VibeVideo项目/work/creative-upgrade-20261010/valve/out-final/valve-director.mp4>) · [代码](<D:/ai项目/ai动画/VibeVideo项目/work/creative-upgrade-20261010/valve/film.js>)。工程剖面、弹簧、压差与行程；静音，等待用户反馈。
- 主体跟拍 / 竖屏研究：[播放样片](<D:/ai项目/ai动画/VibeVideo项目/work/camera-upgrade-20261010/out-r2/subject-follow-portrait.mp4>) · [代码](<D:/ai项目/ai动画/VibeVideo项目/work/camera-upgrade-20261010/demo/film.js>)。主体世界路径、前景视差、相机相对偏移。
- 工程蓝图 / 10秒能力片段：[播放样片](<D:/ai项目/ai动画/VibeVideo项目/work/style-production-20261009/studio/out-approved/blueprint-proof/blueprint-proof.mp4>) · [代码](<D:/ai项目/ai动画/VibeVideo项目/work/style-production-20261009/studio/film.mjs>)。外壳分离、剖切、零件与标注联动。
- 数据叙事 / 10秒能力片段：[播放样片](<D:/ai项目/ai动画/VibeVideo项目/work/style-production-20261009/studio/out-approved/dataviz-proof/dataviz-proof.mp4>) · [代码](<D:/ai项目/ai动画/VibeVideo项目/work/style-production-20261009/studio/film.mjs>)。同一组点从折线到零基线柱形。
- 只向一个方向 / 竖屏蓝图：[播放样片](<D:/ai项目/ai动画/VibeVideo项目/work/portrait-valve-20261009/out-final/one-way-portrait.mp4>) · [代码](<D:/ai项目/ai动画/VibeVideo项目/work/portrait-valve-20261009/film.js>)。机械因果、剖面、事件拟音。
- 淡墨远征 / 拿破仑在埃及：[播放样片](<D:/ai项目/ai动画/VibeVideo项目/work/napoleon-egypt-ink-20261009/out/napoleon-egypt-ink.mp4>) · [代码](<D:/ai项目/ai动画/VibeVideo项目/work/napoleon-egypt-ink-20261009/film.js>)。水墨叙事；生成的图像组件 + Canvas / WebGL显影与运镜，属于混合素材。
- 5厘米的噩梦 / 诙谐科普：[播放样片](<D:/ai项目/ai动画/VibeVideo项目/work/whale-20261009/out/final/whale.mp4>) · [代码](<D:/ai项目/ai动画/VibeVideo项目/work/whale-20261009/film.js>)。纯Canvas绘制、大小反差、事件拟音。
- 熵增 / 统计科普：[播放样片](<D:/ai项目/ai动画/VibeVideo项目/work/entropy-20261009/out/entropy-r3/entropy.mp4>) · [代码](<D:/ai项目/ai动画/VibeVideo项目/work/entropy-20261009/film.mjs>)。Canvas、组合枚举、粒子与统计、中文旁白；历史横版。
- 光庭 / 空间光学电影：[播放样片](<D:/ai项目/ai动画/VibeVideo项目/work/cinematic-assimilation-20261009/demo/out-durable/lumen-sound.mp4>) · [代码](<D:/ai项目/ai动画/VibeVideo项目/work/cinematic-assimilation-20261009/demo/film.js>)。Three.js、程序化器件、光束、低位穿行、升高揭示。
- SDF玻璃 / 局部实验：[播放样片](<D:/ai项目/ai动画/VibeVideo项目/work/cinematic-assimilation-20261009/sdf-lab/out/sdf-glass-window.mp4>) · [代码](<D:/ai项目/ai动画/VibeVideo项目/work/cinematic-assimilation-20261009/sdf-lab/index.html>)。WebGL2单界面折射近似；不代表完整物理折射或焦散。
- 一条线 / UI连续性实验：[播放样片](<D:/ai项目/ai动画/VibeVideo项目/work/opus-gallery-study-20261009/demo/out/continuity-study.mp4>) · [代码](<D:/ai项目/ai动画/VibeVideo项目/work/opus-gallery-study-20261009/demo/index.html>)。解析弹簧、点对应、滑杆到曲线到勾号。
- 蓝色的建筑 / 机制小样：[播放样片](<D:/ai项目/ai动画/VibeVideo项目/work/morpho-blue-20261008/out/mechanism-study.mp4>) · [代码](<D:/ai项目/ai动画/VibeVideo项目/work/morpho-blue-20261008/film.mjs>)。结构色、显微机制；只交付过27秒小样，52秒最终版未交付。
- 绕过黑暗 / 黑洞透镜：[播放样片](<D:/ai项目/ai动画/VibeVideo项目/work/black-hole-lensing-20261008/out/around-the-dark.mp4>) · [代码](<D:/ai项目/ai动画/VibeVideo项目/work/black-hole-lensing-20261008/film.mjs>)。光路、黑洞、科学机制与空间示意；历史横版。
- 冰下，宇宙亮了 / 历史样片：[播放样片](<D:/ai项目/ai动画/VibeVideo项目/work/hot-news-20261009/out-final/icecube-news-portrait.mp4>) · [代码](<D:/ai项目/ai动画/VibeVideo项目/work/hot-news-20261009/film.js>)。实景照片 + 艺术化三维示意；用户已否定此版，只作历史记录。

## 37张方法卡

- 单对象贯穿多种UI：`ui-identity`
- 轮廓、孔洞与附属笔画分别形变：`outline-morph`
- 从选中局部进入下一层世界：`portal-scale`
- 选择动作成为镜头连接：`select-transition`
- 文字作为运动材质窗口：`type-window`
- 文字搭建场景并兑现句意：`type-architecture`
- 同一材料在结尾变为标志：`semantic-finale`
- 让数值、图形和标签共享状态：`data-state`
- 先建立器件，再剖开关键接触：`mechanical-section`
- 共享世界光照塑造层次：`world-light`
- 远机位与窄视角压缩空间：`telephoto`
- 低位穿行，用遮挡证明纵深：`low-travel`
- 位置与目标双轨迹揭示主体：`reveal-path`
- 在因果点保持相机稳定：`hold-cause`
- 点云有实体深度与遮挡：`point-volume`
- 点身份持续，形态才能接续：`point-correspondence`
- 场的结构形成材质与地形：`procedural-surface`
- 玻璃轮廓、折射和内容分层：`glass-sdf`
- 液体用连续场融合并继承颜色：`liquid-union`
- 手绘感来自笔压与稳定线条变化：`hand-ink`
- 像素风用语义色板表达时间：`pixel-palette`
- 角色意图驱动骨骼与跟随动作：`paper-acting`
- 接触事件同时推进剧情与声音：`event-story`
- 地形、水量和材质形成因果：`water-cause`
- 受力、关节与断裂提供动作因果：`rigid-contact`
- 采样服务轮廓、阴影与高速动作：`sample-quality`
- 用同一乐谱完成角色表演接棒：`performance-handoff`
- 一个变化状态同时改变身体与表演：`emotion-shared-state`
- 追逐加速之后用静音突出接触：`chase-silence-catch`
- 零件身份贯穿绘制、爆炸与剖切：`blueprint-part-states`
- 相机、零件和产品标注共享世界锚点：`world-anchor-callout`
- 笔压、墨量和干湿分层形成水墨：`ink-material-layers`
- 阅读区域约束景深与手持摄影：`reading-constrained-lens`
- 曲面纸页与相机错时落定：`curved-page-handoff`
- 折射网格面积生成水底焦散：`refracted-caustic-grid`
- 主体判断、减速和预备转向：`subject-intent`
- 预载、压差与受限机械行程：`load-regulated-valve`

## 全部现有视频文件

- [外部原片] [reference-sources/bilibili-media/BV18ta86EEHb/reference.mp4](<D:/ai项目/ai动画/VibeVideo项目/reference-sources/bilibili-media/BV18ta86EEHb/reference.mp4>)（19.0 MB）
- [外部原片] [reference-sources/bilibili-media/BV1vRHa63EYg/reference.mp4](<D:/ai项目/ai动画/VibeVideo项目/reference-sources/bilibili-media/BV1vRHa63EYg/reference.mp4>)（6.9 MB）
- [外部原片] [work/opus-gallery-study-20261009/twoclipping-original.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/opus-gallery-study-20261009/twoclipping-original.mp4>)（0.8 MB）
- [外部原片] [work/opus-gallery-study-20261009/koldo2k-original.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/opus-gallery-study-20261009/koldo2k-original.mp4>)（4.6 MB）
- [外部原片] [work/opus-gallery-study-20261009/ror-fly-original.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/opus-gallery-study-20261009/ror-fly-original.mp4>)（2.2 MB）
- [外部原片] [work/director-study-20261008/source-snapshots/Liamrjohnston/examples/openmontage-hook.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/director-study-20261008/source-snapshots/Liamrjohnston/examples/openmontage-hook.mp4>)（1.4 MB）
- [外部原片] [work/director-study-20261008/source-snapshots/Liamrjohnston/examples/openmontage-tool-chaos.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/director-study-20261008/source-snapshots/Liamrjohnston/examples/openmontage-tool-chaos.mp4>)（1.2 MB）
- [外部原片] [work/director-study-20261008/source-snapshots/Liamrjohnston/examples/openmontage-claude-pipeline.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/director-study-20261008/source-snapshots/Liamrjohnston/examples/openmontage-claude-pipeline.mp4>)（2.7 MB）
- [外部重制] [work/opus-gallery-study-20261009/twoclipping-remake.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/opus-gallery-study-20261009/twoclipping-remake.mp4>)（0.3 MB）
- [项目样片] [work/creative-upgrade-20261010/flight/out-final/flight-director.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/creative-upgrade-20261010/flight/out-final/flight-director.mp4>)（2.3 MB）
- [项目样片] [work/creative-upgrade-20261010/valve/out-final/valve-director.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/creative-upgrade-20261010/valve/out-final/valve-director.mp4>)（1.7 MB）
- [项目样片] [work/camera-upgrade-20261010/out-r2/subject-follow-portrait.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/camera-upgrade-20261010/out-r2/subject-follow-portrait.mp4>)（2.5 MB）
- [项目样片] [work/style-production-20261009/studio/out-approved/blueprint-proof/blueprint-proof.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/style-production-20261009/studio/out-approved/blueprint-proof/blueprint-proof.mp4>)（1.7 MB）
- [项目样片] [work/style-production-20261009/studio/out-approved/dataviz-proof/dataviz-proof.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/style-production-20261009/studio/out-approved/dataviz-proof/dataviz-proof.mp4>)（0.2 MB）
- [项目样片] [work/portrait-valve-20261009/out-final/one-way-portrait.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/portrait-valve-20261009/out-final/one-way-portrait.mp4>)（1.4 MB）
- [项目样片] [work/napoleon-egypt-ink-20261009/out/napoleon-egypt-ink.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/napoleon-egypt-ink-20261009/out/napoleon-egypt-ink.mp4>)（21.7 MB）
- [项目样片] [work/whale-20261009/out/final/whale.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/whale-20261009/out/final/whale.mp4>)（6.2 MB）
- [项目样片] [work/entropy-20261009/out/entropy-r3/entropy.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/entropy-20261009/out/entropy-r3/entropy.mp4>)（5.0 MB）
- [项目样片] [work/cinematic-assimilation-20261009/demo/out-durable/lumen-sound.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/cinematic-assimilation-20261009/demo/out-durable/lumen-sound.mp4>)（11.4 MB）
- [项目样片] [work/cinematic-assimilation-20261009/sdf-lab/out/sdf-glass-window.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/cinematic-assimilation-20261009/sdf-lab/out/sdf-glass-window.mp4>)（0.2 MB）
- [项目样片] [work/opus-gallery-study-20261009/demo/out/continuity-study.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/opus-gallery-study-20261009/demo/out/continuity-study.mp4>)（0.2 MB）
- [项目样片] [work/morpho-blue-20261008/out/mechanism-study.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/morpho-blue-20261008/out/mechanism-study.mp4>)（6.3 MB）
- [项目样片] [work/black-hole-lensing-20261008/out/around-the-dark.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/black-hole-lensing-20261008/out/around-the-dark.mp4>)（26.9 MB）
- [项目样片] [work/hot-news-20261009/out-final/icecube-news-portrait.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/hot-news-20261009/out-final/icecube-news-portrait.mp4>)（12.6 MB）
- [历史 / 预演 / 验证] [work/black-hole-lensing-20261008/out/key-action-study-v2.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/black-hole-lensing-20261008/out/key-action-study-v2.mp4>)（5.8 MB）
- [历史 / 预演 / 验证] [work/black-hole-lensing-20261008/out/key-action-study.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/black-hole-lensing-20261008/out/key-action-study.mp4>)（5.8 MB）
- [历史 / 预演 / 验证] [work/camera-upgrade-20261010/out/subject-follow-portrait.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/camera-upgrade-20261010/out/subject-follow-portrait.mp4>)（2.5 MB）
- [历史 / 预演 / 验证] [work/cinematic-assimilation-20261009/demo/out-durable/lumen.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/cinematic-assimilation-20261009/demo/out-durable/lumen.mp4>)（11.1 MB）
- [历史 / 预演 / 验证] [work/cinematic-assimilation-20261009/demo/out-final/lumen.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/cinematic-assimilation-20261009/demo/out-final/lumen.mp4>)（2.0 MB）
- [历史 / 预演 / 验证] [work/creative-upgrade-20261010/flight/out-preview-r1/flight-preview.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/creative-upgrade-20261010/flight/out-preview-r1/flight-preview.mp4>)（0.7 MB）
- [历史 / 预演 / 验证] [work/creative-upgrade-20261010/flight/out-preview/flight-preview.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/creative-upgrade-20261010/flight/out-preview/flight-preview.mp4>)（0.7 MB）
- [历史 / 预演 / 验证] [work/creative-upgrade-20261010/forward-test/fixture.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/creative-upgrade-20261010/forward-test/fixture.mp4>)（0.1 MB）
- [历史 / 预演 / 验证] [work/creative-upgrade-20261010/other-regression/cache-fixture/out-cache/cache.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/creative-upgrade-20261010/other-regression/cache-fixture/out-cache/cache.mp4>)（0.0 MB）
- [历史 / 预演 / 验证] [work/creative-upgrade-20261010/valve/out-preview-r2/valve-preview.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/creative-upgrade-20261010/valve/out-preview-r2/valve-preview.mp4>)（0.6 MB）
- [历史 / 预演 / 验证] [work/director-study-20261008/reference-review/lugia-p4-fragment/normalized-fragment.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/director-study-20261008/reference-review/lugia-p4-fragment/normalized-fragment.mp4>)（0.6 MB）
- [历史 / 预演 / 验证] [work/entropy-20261009/out/entropy-r2/entropy-silent.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/entropy-20261009/out/entropy-r2/entropy-silent.mp4>)（3.5 MB）
- [历史 / 预演 / 验证] [work/entropy-20261009/out/entropy-r2/entropy.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/entropy-20261009/out/entropy-r2/entropy.mp4>)（4.9 MB）
- [历史 / 预演 / 验证] [work/entropy-20261009/out/entropy-r3/entropy-silent.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/entropy-20261009/out/entropy-r3/entropy-silent.mp4>)（3.5 MB）
- [历史 / 预演 / 验证] [work/entropy-20261009/out/entropy/entropy-silent.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/entropy-20261009/out/entropy/entropy-silent.mp4>)（3.4 MB）
- [历史 / 预演 / 验证] [work/entropy-20261009/out/members-5s-r2/members-5s-silent.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/entropy-20261009/out/members-5s-r2/members-5s-silent.mp4>)（0.3 MB）
- [历史 / 预演 / 验证] [work/entropy-20261009/out/members-5s/members-5s-silent.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/entropy-20261009/out/members-5s/members-5s-silent.mp4>)（0.3 MB）
- [历史 / 预演 / 验证] [work/hot-news-20261009/out-final/icecube-news-silent.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/hot-news-20261009/out-final/icecube-news-silent.mp4>)（12.2 MB）
- [历史 / 预演 / 验证] [work/light-to-lens-20261008/out/apparent-position-study.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/light-to-lens-20261008/out/apparent-position-study.mp4>)（0.7 MB）
- [历史 / 预演 / 验证] [work/light-to-lens-20261008/out/from-line-to-black-hole.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/light-to-lens-20261008/out/from-line-to-black-hole.mp4>)（38.5 MB）
- [历史 / 预演 / 验证] [work/napoleon-egypt-ink-20261009/out/final-render/picture.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/napoleon-egypt-ink-20261009/out/final-render/picture.mp4>)（20.3 MB）
- [历史 / 预演 / 验证] [work/portrait-valve-20261009/out-final/one-way-portrait-silent.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/portrait-valve-20261009/out-final/one-way-portrait-silent.mp4>)（1.2 MB）
- [历史 / 预演 / 验证] [work/reference-study-20261008/pdoom-native-loss-study.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/reference-study-20261008/pdoom-native-loss-study.mp4>)（12.6 MB）
- [历史 / 预演 / 验证] [work/skill-refinement-20261007/out/optical-study.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/skill-refinement-20261007/out/optical-study.mp4>)（12.2 MB）
- [历史 / 预演 / 验证] [work/style-production-20261009/studio/out-15sec/one-way-15/one-way-15-silent.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/style-production-20261009/studio/out-15sec/one-way-15/one-way-15-silent.mp4>)（1.9 MB）
- [历史 / 预演 / 验证] [work/style-production-20261009/studio/out-15sec/one-way-15/one-way-15.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/style-production-20261009/studio/out-15sec/one-way-15/one-way-15.mp4>)（2.0 MB）
- [历史 / 预演 / 验证] [work/style-production-20261009/studio/out-approved/blueprint-proof/blueprint-proof-silent.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/style-production-20261009/studio/out-approved/blueprint-proof/blueprint-proof-silent.mp4>)（1.6 MB）
- [历史 / 预演 / 验证] [work/style-production-20261009/studio/out-approved/dataviz-proof/dataviz-proof-silent.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/style-production-20261009/studio/out-approved/dataviz-proof/dataviz-proof-silent.mp4>)（0.1 MB）
- [历史 / 预演 / 验证] [work/style-production-20261009/studio/out-approved/dataviz-variant/dataviz-variant-silent.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/style-production-20261009/studio/out-approved/dataviz-variant/dataviz-variant-silent.mp4>)（0.1 MB）
- [历史 / 预演 / 验证] [work/style-production-20261009/studio/out-approved/dataviz-variant/dataviz-variant.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/style-production-20261009/studio/out-approved/dataviz-variant/dataviz-variant.mp4>)（0.2 MB）
- [历史 / 预演 / 验证] [work/style-production-20261009/studio/out-approved/one-way/one-way-silent.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/style-production-20261009/studio/out-approved/one-way/one-way-silent.mp4>)（3.0 MB）
- [历史 / 预演 / 验证] [work/style-production-20261009/studio/out-approved/one-way/one-way.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/style-production-20261009/studio/out-approved/one-way/one-way.mp4>)（3.3 MB）
- [历史 / 预演 / 验证] [work/style-production-20261009/studio/out-final/blueprint-proof/blueprint-proof-silent.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/style-production-20261009/studio/out-final/blueprint-proof/blueprint-proof-silent.mp4>)（1.6 MB）
- [历史 / 预演 / 验证] [work/style-production-20261009/studio/out-final/blueprint-proof/blueprint-proof.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/style-production-20261009/studio/out-final/blueprint-proof/blueprint-proof.mp4>)（1.7 MB）
- [历史 / 预演 / 验证] [work/style-production-20261009/studio/out-final/dataviz-proof/dataviz-proof-silent.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/style-production-20261009/studio/out-final/dataviz-proof/dataviz-proof-silent.mp4>)（0.1 MB）
- [历史 / 预演 / 验证] [work/style-production-20261009/studio/out-final/dataviz-proof/dataviz-proof.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/style-production-20261009/studio/out-final/dataviz-proof/dataviz-proof.mp4>)（0.2 MB）
- [历史 / 预演 / 验证] [work/style-production-20261009/studio/out-final/dataviz-variant/dataviz-variant-silent.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/style-production-20261009/studio/out-final/dataviz-variant/dataviz-variant-silent.mp4>)（0.1 MB）
- [历史 / 预演 / 验证] [work/style-production-20261009/studio/out-final/one-way/one-way-silent.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/style-production-20261009/studio/out-final/one-way/one-way-silent.mp4>)（3.0 MB）
- [历史 / 预演 / 验证] [work/style-production-20261009/studio/out-final/one-way/one-way.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/style-production-20261009/studio/out-final/one-way/one-way.mp4>)（3.3 MB）
- [历史 / 预演 / 验证] [work/style-production-20261009/studio/out-release/blueprint-proof/blueprint-proof-silent.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/style-production-20261009/studio/out-release/blueprint-proof/blueprint-proof-silent.mp4>)（1.6 MB）
- [历史 / 预演 / 验证] [work/style-production-20261009/studio/out-release/blueprint-proof/blueprint-proof.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/style-production-20261009/studio/out-release/blueprint-proof/blueprint-proof.mp4>)（1.7 MB）
- [历史 / 预演 / 验证] [work/style-production-20261009/studio/out-release/dataviz-proof/dataviz-proof-silent.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/style-production-20261009/studio/out-release/dataviz-proof/dataviz-proof-silent.mp4>)（0.1 MB）
- [历史 / 预演 / 验证] [work/style-production-20261009/studio/out-release/dataviz-proof/dataviz-proof.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/style-production-20261009/studio/out-release/dataviz-proof/dataviz-proof.mp4>)（0.2 MB）
- [历史 / 预演 / 验证] [work/style-production-20261009/studio/out-release/dataviz-variant/dataviz-variant-silent.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/style-production-20261009/studio/out-release/dataviz-variant/dataviz-variant-silent.mp4>)（0.1 MB）
- [历史 / 预演 / 验证] [work/style-production-20261009/studio/out-release/dataviz-variant/dataviz-variant.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/style-production-20261009/studio/out-release/dataviz-variant/dataviz-variant.mp4>)（0.2 MB）
- [历史 / 预演 / 验证] [work/style-production-20261009/studio/out-release/one-way/one-way-silent.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/style-production-20261009/studio/out-release/one-way/one-way-silent.mp4>)（3.0 MB）
- [历史 / 预演 / 验证] [work/style-production-20261009/studio/out-release/one-way/one-way.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/style-production-20261009/studio/out-release/one-way/one-way.mp4>)（3.3 MB）
- [历史 / 预演 / 验证] [work/vibe-video-proof/out/code-motion-study.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/vibe-video-proof/out/code-motion-study.mp4>)（6.2 MB）
- [历史 / 预演 / 验证] [work/whale-20261009/out/final/whale-silent.mp4](<D:/ai项目/ai动画/VibeVideo项目/work/whale-20261009/out/final/whale-silent.mp4>)（5.9 MB）

## 核对依据

[源码方法与证据](<D:/Codex/skills/vibe-video/references/opus-methodology.md>)
[参考来源与版本](<D:/Codex/skills/vibe-video/references/sources.md>)
[风格生产规范](<D:/Codex/skills/vibe-video/references/style-production.md>)
[项目检查点](<D:/ai项目/ai动画/VibeVideo项目/CHECKPOINT.md>)

渲染成功、查看静帧、连续帧取样、实时播放、听音、用户接受是不同状态；此盘点没有新增视觉验收。