# 从源码到可用的导演方法

适用于吸收 Opus 图库、寻找动画源码、提升导演/摄影/运镜/美术能力，或按用户需求选择类似效果。先查本地源码，再沿原帖和作者仓库补充。用户只要求研究和更新技能时，交付来源、方法与检索能力；不自动制作样片。

## 本地源码入口

`assets/code-studies/` 保存十套固定版本的源码参考包。每套保留原 LICENSE 和 `SOURCE.json`：原仓库、commit/提交时间、用途、质量证据、采用范围、逐文件 SHA256。源码保持上游原样；实际迁移在任务目录的副本里完成。代码MIT不自动覆盖字体轮廓、音乐和第三方素材。版本和行号通过检索脚本返回，不依赖临时下载目录。影片与组件的区分见 [recent-film-selection.md](recent-film-selection.md)。

|检索 ID / 本地目录|优先读取的代码|可以吸收什么|当前证据与缺口|
|---|---|---|---|
|`beach` / [particle-beach](../assets/code-studies/particle-beach/)|`js/trailer-shots.js`、`js/core.js`、`js/trailer.js`|远机位长焦、低位穿行、位置/目标双轨迹、世界光照、点云遮挡|图库原作者链接；保存完整绘制运行部分，已检查代表帧和连续窗口。字体替代、局部近黑和重复像素差详见 [code-cinema.md](code-cinema.md)|
|`reel` / [work-reel-26](../assets/code-studies/work-reel-26/)|`skills/kinetic-reel/examples/work-reel-26/reel.js`、`cues.js`|点身份对应、程序化材质、文字窗口、选中区域进入下一镜|补充作品，保存完整绘制运行部分；已检查代表帧和连续窗口，并核对重复时刻。不是 513 原作统一源码|
|`mg` / [mg-styles-15](../assets/code-studies/mg-styles-15/)|`demos/08-morph/index.html`、`07-liquid/js/shaders.js`、`05-cel-boil/js/engine.js`、`03-isometric/js/render.js`、`20-pixel/film.js`|轮廓/孔洞分离形变、连续场融合、稳定手绘、采样、语义色板|补充作品；154 个文本文件，本轮精读上述选定实现。未运行；媒体、字体、部分图片/mesh/音频及依赖未打包|
|`paper` / [papermotion](../assets/code-studies/papermotion/)|`examples/light/main.ts`、`examples/kite/main.ts`、`examples/cast/Child.ts`、`src/direction/Beats.ts`、`src/stage/Stage.ts`|角色意图与骨骼、接触驱动剧情/音效、纸片视差、相机跟随|补充引擎与影片；146 个文本文件，未运行。Stage 仅递增帧；素材/依赖未打包。作者将 light 标为 GPT 6 Astra，不统一归因 Opus|
|`water` / [water-opus](../assets/code-studies/water-opus/)|`runs/claude-code-opus-5-5/src/sim/water.ts`、`sim/world.ts`、`render/waterMesh.ts`|四邻通量、水量预算、模拟状态映射到几何和材质|图库原帖链接；26 个文件，仅保存该模型实现与根署名。关键源码已读，未运行；高度场浅水不适用于阀内三维流动，实时循环会丢积压时间|
|`rigid` / [three-avbd](../assets/code-studies/three-avbd/)|`examples/basic.ts`、`src/app3d/renderer3d.ts`，再沿引用读 solver|GPU 刚体、关节/断裂、模拟与绘制同步、接触层次|图库原帖链接；92 个文件，未运行。Math.random/Clock 要迁移为固定种子与离线模拟；依赖未打包|
|`songbie` / [songbie](../assets/code-studies/songbie/)|`score.js`、`render.js`|乐谱/琴键/手部共享事件、角色接棒、融化状态与表演|作者声明Opus 5.5代码绘制；8文本文件，选定实现已读，未运行/审片；钢琴样本不随包|
|`lemo` / [lemo-opuscar](../assets/code-studies/lemo-opuscar/)|`styles/art-deco/demo/timeline.js`、`blueprint/demo/machine.js`、`ink-wash/demo/ink.js`、`hologram-hud/demo/film.js`|追逐与静音接触、零件身份/剖切、干湿笔触、世界锚点标注|作者声明43种风格；仅归档4种选定风格与共享代码147文件，未审片；第三方素材独立许可|
|`lyric` / [i-like-ur-look-lyric-video](../assets/code-studies/i-like-ur-look-lyric-video/)|`app/src/engine/curl.ts`、`page.ts`、`scenes/magazine/focus.ts`、`view.ts`、`schedule.ts`|曲面纸页、阅读约束景深、弱手持、错时落定|近期代码影片候选，编码模型未确认；72文本文件，未运行/审片；歌曲、歌词/节拍数据与字体不随包|
|`clearwater` / [clearwater](../assets/code-studies/clearwater/)|`index.html`焦散297行、吸收508行、循环871行；`tools/make_pebbles.py`|折射网格光集中、水深吸收、互动涟漪|同期光学组件，不是完整导演影片；4文件，未运行，原帖/模型归属未核实；固定t不重建涟漪历史|

前阶段六包有457个文件；本次再加231个选定文本文件，十包共有688个带哈希的上游文件。文件数量不代表阅读或运行覆盖。只有 beach、water、rigid 的原帖到源码链接已核查；指定 commit 与发布录屏像素一致性尚未证实。无明确代码 LICENSE 的线索没有复制进技能，例如 Faraz 的 SDF 玻璃和 JohnHeibel/PDoomVideo；可以继续追查许可或独立实现公共原理，不能与其他重制工程混同。

## 按需求检索

从技能目录运行；可用已核实的 Python 绝对路径替代 `python`。脚本只读取本地资料，不联网、不执行第三方工程、不渲染视频。

```text
python scripts/opus_methodology.py stats
python scripts/opus_methodology.py recommend --query "竖屏 弹簧止回阀 剖面 流体" --limit 4
python scripts/opus_methodology.py recommend --query "点云 长焦 运镜" --code-only
python scripts/opus_methodology.py recommend --query "产品 全息 标注" --code-only --film-only
python scripts/opus_methodology.py card outline-morph
python scripts/opus_methodology.py source mg
python scripts/opus_methodology.py trace koldo2k-778767
python scripts/opus_methodology.py validate
```

`recommend` 返回方法候选、目的、证据状态及源码绝对路径/行号/固定版本链接；命中词的分值只用于检索排序。接着用 `card` 读取决策、实现、失败条件与验收窗，再阅读对应源码。没有匹配就从 brief 建立机制，不随机塞入热门案例。

`--code-only` 保留有绘制实现参考的方法卡，案例线索仅保留已关联源码的记录。它不证明原片全由该版本绘制，也不证明方法已在本机运行。`source glass` 只有远程来源，实际本地原理实现为 `assets/sdf-glass-lab/index.html`；其他本地工具来源为 `codex-tools`。机械剖面与文字建筑等无源码卡仍可作为独立设计，不能虚构原作者实现。

[opus-methods.json](opus-methods.json) 含37张方法卡（35张来源方法 + 两张原创的主体意图/受限阀门）；[opus-source-index.json](opus-source-index.json) 给出513条逐条阅读范围、重复文本、原文机制命中和来源状态。来源作品的9张卡来自选定源码观察，没有强行关联图库原作。自动命中只表示候选。图库较底层的提示词/slug 检索继续使用 [opus-gallery.md](opus-gallery.md) 中的脚本。

重要卡的 `operating` 给出技术栈、类型、输入输出、参数、组合、性能、不适用条件及最小验证方式。命令默认从技能目录执行；浏览器渲染先把资产复制到任务目录并沿该包package.json准备依赖，或显式传本机 `--playwright`/`--three` 路径。不要在没有依赖时把失败写成画质已验证。优先检索要解决的视觉问题，再读源码迁移持续对象/状态关系，不能整段复制参考故事。

## 把代码读成创作决策

按本片目标使用下面的关系，不必每次做齐所有技术。

1. **需求与视觉承诺。** 用一句话说明观众最后理解什么、画面如何兑现。机械片承诺“看见密封如何打开和复位”；门户片承诺“进入局部后发现更大关系”。先选一个主要机制，其他机制为它服务。
2. **持续对象。** 定义跨镜头保留的主体 ID、形状、材质、方向或语义。源码里查这些状态是否真的共享；两个对象叠化不能当形变，放大单张照片不能当空间穿行。
3. **状态与因果。** 建立起点→主动作→结果。几何、数值、字幕和声音从同一事件或模拟状态取值；检查触发条件、超时和预算。角色先有意图，再有步态、视线和余动。
4. **摄影与运镜。** 分别阅读 position、lookAt、FOV 和遮挡。远机位改变透视、窄 FOV 匹配景别；低位前景提供纵深；双轨迹让发现有次序；关键接触处停机。判断相机为什么动，比抄轨迹参数更有用。
5. **美术与材质。** 从共享世界光照、轮廓、法线、深度、色板和材质响应追查层次。先修大形和明暗，再增加纹理/粒子/高光。距离场融合、屏幕折射、matcap 和浅水都是有范围的近似。
6. **节奏与声音。** 让识别、动作、结果各有时间；接触、选择、揭示共同触发画面和声音。音乐节拍不能压缩机制理解；统计音轨不替代实际听音。
7. **迁移与比对。** 读取源码后明确保留的关系、需要改写的部分和未验证条件。普通制作按主 skill 做代表帧、最难连续窗和整片审看。研究任务在阅读/方法交付处结束；未经成片比对，不承诺已经达到原作质量。

制作时采用本片已选画幅：横屏 16:9、1920×1080，或竖屏 9:16、1080×1920；用户指定其他尺寸时按要求处理。跨画幅迁移需要重排主体、相机轨迹、标注与字幕；直接裁切会改变锚点、前景遮挡和景别。

## 质量如何落实

为需求选定实际对标作品、观看版本和时间窗，再逐项比较，不打虚构分数。

|比较维度|从源码提出的问题|成片需要证明的内容|
|---|---|---|
|形式和主体|持续 ID、轮廓与状态是否继承？|观众能跟住主对象，中间态没有混乱或突然换主体|
|动作解释|原因、接触和结果由同一状态决定吗？|动作先后可读，结果由动作造成，关键处有停留|
|摄影|轨迹、目标与 FOV 如何形成揭示？|锚点稳定，前中后景有层次，运动没有穿模或无意义绕行|
|美术|光照、法线、颜色与材质是否一致？|大形明确，轮廓/暗部/接触可信，文字在实际手机尺寸可读|
|连续性|配点、遮罩、孔洞与新镜如何交接？|入前、最拥挤中间态、交接与落定都干净，四角没有漏层|
|动态和声音|采样、模拟时间与事件 cue 如何对应？|无明显闪烁/鬼影，声音回应实际动作；真实播放/听音覆盖有记录|

如需精确导出，先将实时循环改成绝对时间或固定步长重播/缓存，分别检查顺序、乱序和新进程。代码能运行、源码被阅读、短窗被检查、整片达到对标是不同证据，分开登记。

## 研究覆盖与来源边界

本轮基于 2026-10-09 的 513 条固定快照：459 段不同公开文本中，420 段短文本全文阅读，39 段长文本按机制摘录阅读；234 条记录被图库标为部分提示词。全库有文本索引，不等于原片全部看过或复现过。

35张卡覆盖上述机制，并增加表演接棒、情绪共享状态、追逐静音、零件剖切、世界标注、水墨材料、阅读摄影、曲面纸页与焦散。带源码的卡是源码观察加迁移设计；无源码卡是公开需求或独立设计。方法卡并非35种效果全已实测。

混合来源明确保留：`koldo2k-778767` 的公开需求使用 Magnific/Seedream 图片及 Kling 动画；Seedance、Higgsfield、Runway/Veo 等线索也标在索引里。SDXL 图片+代码合成、Midjourney 角色+Remotion 属于混合素材；来源未知的背景 MP4 仍未知。可以独立实现其门户/遮罩关系，但这些原片不能证明纯代码画质。Two photos + radial mask 也不能证明内部三维结构。

这里的“吸收”是把来源、实现细节、设计决策和检查方法持久化到技能，供后续任务查阅与迁移；没有修改模型权重。继续找不到某部原作源码时，保留缺口，采用可核查的补充工程并说明同作关系，不假设代码制作必然已开源。
