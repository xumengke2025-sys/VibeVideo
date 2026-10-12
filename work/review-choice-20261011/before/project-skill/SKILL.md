---
name: vibe-video
description: 制作科普、知识解释、自由动效和三维短片，吸收开源代码作品的导演、摄影、运镜、美术与着色器机制，提供可运行工程和实际审片。适用于 Vibe Video、动画制作、Opus 作品研究与复现或文章转视频；按题材组合素材，用户限定代码制作时使用可核查的代码渲染路线。普通原理问答、仅写脚本和单独调用视频生成模型不触发制作。
metadata:
  version: "0.14.0"
---

# Vibe Video

把创作请求完成为可编辑源码、预览和实际视频。默认追求专业科普片的视觉完成度：主体精细、构图明确、动作解释内容，第一眼有值得看的画面。渲染成功只说明工程可用；审美与动态必须看实际输出。用户指定极简、白板或其他风格时按其方向做。

新建完整影片或改善质量时，先读 [references/production-quality.md](references/production-quality.md)：在现有镜头表标明观众理解顺序，先完成关键动作的最终品质样段，再扩展整片；加入布局/锚点检查，独立审片先检查画面能否自明，修复时保护已有效的部分。公开 Opus 制作流程的来源、实际阅读范围和不采用的固定配额也记录在那里。

需要角色分工或双模型工作流时读 [references/role-orchestration.md](references/role-orchestration.md)：导演定稿、制作实施、独立审片顺序交接；仅使用用户授权的模型路由，调用预算不得减免全帧/完整音频审核。直接吸收 Functional Emotions、ClaudeAnimationBase 或连续变形经验时读 [references/reference-transfer.md](references/reference-transfer.md)，区分源码已研究、机制已验证和成片已采用。

## 先决定观众怎样理解

编码前读 [references/director-design.md](references/director-design.md)。先提出三个事件机制明显不同的候选（概念、关键事件、观众体验、核心镜头、难点/成本与适配理由），记录自主选择依据；简单工具动画可合并为简短判断。颜色或机位变化不算不同概念。确定开场承诺、关键因果动作、递进与结尾兑现，再写镜头关系。按视频类型选择目标，不强制反转或高潮。复杂作品先以简化几何/低分辨率动态预演检验这些判断，方向不成立先改构思。

把主动作写成建立→变化→结果，分别安排主体与相机。相机靠近是为了看细节，拉远是为了揭示关系，跟随是为了保持动作锚点；机制最难读的接触处可以停机。用景别、机位、遮挡与注意力变化检验镜头价值，不以均匀绕行或整页缩放充数。

主体在移动、用户要求灵动/电影感/复杂运镜，或旧片长期锁定中心时，编码前读 [references/subject-cinematography.md](references/subject-cinematography.md)。默认先设计一段伴随主体行动的镜头：主体位置、相机位置和看向点共享绝对时间，但各有任务；预留行进空间、前景视差与注意交接。固定中心环绕不能替代跟拍。主体原地完成机制动作时，可跟随活动零件、光路或因果前沿，关键接触保留有目的的停机。复杂度用揭示和体验衡量，不按每秒移动次数衡量。

## 再把画面做对

写主体代码前读 [references/art-direction.md](references/art-direction.md) 和 [references/motion-craft.md](references/motion-craft.md)。先确定观众应理解的一件事和一个能兑现的视觉惊喜，再选择画面。不要用孤立基础几何、小组件加大标题来代替精细主体；需要复杂有机形态、人物、器物、摄影质感时，优先真实素材、生图或成熟三维资产。

必要时生成代表性设定帧：开场、最难解释的机制、视觉高潮，再做包含主动作与结果的低成本预演。生成视频后先执行独立视听审核与有限修复，再展示当前版本，具体见下述闭环。漂亮图片的缓慢移动只验证素材与构图；需要变形、空间揭示或机制解释时，短片段应真实完成该动作。创作方向可以自主确定，不要求用户逐步审批。

批量精修前，以正式画幅、字体、素材和渲染路线完成最难动作及相邻转场的样段，按 production-quality 检查实际品质与理解时间。简化预演不能替代它；简单短片可直接用整片，不新增无必要阶段。

将画面拆成有共同光照、透视和材质的场景层，逐层选择最能做好它的工具。程序化几何、着色器和字体轮廓适合空间穿行、连续变形、精细线场与文字参与的动作；生图负责复杂形象与质感；真实资料负责证据；代码负责准确文字、数据、机制、遮罩、相机与时序。已授权生图、上网取材、裁切或审帧时直接使用。素材具体做法见 [references/asset-pipeline.md](references/asset-pipeline.md)。工具选择由需要发生的动作决定，不以素材数量或是否纯代码衡量画质。

## 决定路线

- 先检查现有工程、已安装运行时和当前素材，保留已有版本与入口。已有工程可在独立子目录注册新 composition，避免改坏旧视频。
- Remotion 有帧时间轴、素材同步、预览和 MP4 导出，适合已有工程中的完整短片；大量 GPU 线场、SDF 场景或定制采样可用独立 Three.js/WebGL 引擎。先沿用能完成目标动作的现有路线，再按瓶颈决定扩展。API 随版本变化；先看本地包版本，按需读取可用的 `remotion-best-practices` 对应规则或官方文档。
- 单 HTML / SVG / Canvas / Three.js 适合交互演示或快速动画研究。需要导出时提供 `renderAt(seconds)` 或等效可寻址时间轴，暂停所有独立计时动画。录屏是可选交付路线；精确逐帧输出不能依赖墙上时钟。
- 真正需要模型、灯光和空间遮挡时用 Three.js / Remotion Three；二维摄影机变换和解析三维投影足够时不额外引入引擎。不要把解析投影写成真实物理模拟。
- 产品截图宣传片可转到可用的 `video-shotcraft`；按用户已选的创作模式执行。白板、角色、旁白等专门任务按需使用对应可用技能，勿把所有视频套成同一模板。

## 默认自主完成

用户给出题材即可先用合理假设推进，画幅、时长和风格从用途与参考推断并说明。只有缺失信息会改变事实、授权素材或核心目标时才问。不要强制用户选背景、逐阶段审批或对每个镜头确认；用户希望共同创作时才采用确认节点。

先写简短 production brief 和镜头表：时间、新理解、建立/主动作/结果、景别与机位目的、声音事件、素材路线和风险状态。相邻镜头另写连接：保留哪个对象/方向/位置/动作/含义，为什么在这里切，以及切前、切中、切后的可读状态。擦拭/叠化可以适用，但不能被命名为几何连续变形。具体示例和可执行计划见 [references/director-design.md](references/director-design.md)。事实有依据，生成概念图与真实观测分开记载。

运动主体镜头补充 `subjectId`、主体世界路径、相机相对偏移、看向点/下一关注对象、速度响应和主体屏幕活动区；先验证主体真的穿过世界、相机真的伴随、背景真的有相对运动。选定摄影方法时读一个对应源码实现，记录保留的关系与本片改动；本地库没有合适方法再寻找其他可核查开源项目，不限定作者或引擎。摄影字段供设计和审片使用，现有 shot_contract 不自动判断其质量。

## 创作重点

在写主体代码前阅读 [references/motion-craft.md](references/motion-craft.md)。依据内容选择具体视觉机制：物体变形、因果传播、沿路径生长、空间揭示、字符形态变化、图表结构变化、角色动作等。清晰的主动作和连续的视觉关系优先于一连串标题卡。

用户提供参考作品时读 [references/reference-study.md](references/reference-study.md)：记录实际观看版本、具体时间段、动作中间态与源码对应，再把差距变成短片段验收项。用户指定日期时核实作品/文档的发布日期，不能把爬取时间或仓库近期活动当成新作品。提示词缺失、重制版本、原始作品与源码需区分。候选方法及 2026-09-30 之后的研究见 [references/sources.md](references/sources.md)。读外部技能用于研究时，不自动继承其纯代码限制、模型宣传或审批习惯。

提供一种符合题材的视觉方向，统一光照、轮廓、材质、色彩功能和文字角色。构图随镜头任务改变，风格统一不要求常驻章节栏或固定大标题。文字可以是投影标注、世界标牌或主动作，但须让主体先可读。不要把灯光、粒子、音效变成固定装饰清单。

## 风格与视听时间轴

用户选定风格、需要可复用样片或风格库时，读 [references/style-production.md](references/style-production.md)。风格包同时规定材质、文字、核心动作、摄影与声音；先从新题材构思，再借用样片实现。当前提供工程蓝图与数据叙事规范，以及 [assets/style-studio](assets/style-studio/) 中两个 10 秒能力片段和一个 32 秒原创时间轴。具体动作与验证状态按风格的 `DEMO.md` 和 `capabilities.json` 判断，不能把示例覆盖范围扩成整种风格已验证。

按本片选择旁白、音乐或动作驱动的主时钟；画面、声音和字幕共享事件数据，具体见 [references/event-timeline.md](references/event-timeline.md)。不强制音乐先行、运镜/静音数量或纯代码；重要接触、发现与结果有声音回应，阅读和理解时间先得到保证。有旁白时使用实际录音时长和重音。

新增或复用能力时，按 [references/capability-evidence.md](references/capability-evidence.md) 分别登记渲染、静帧、连续状态、播放、听音、改内容重建与寻址证据。时间轴检查不代替审美判断，音量分析不代替听音。

## 实现与复用

用户要求吸收完整工程、研究代码制作或提升空间摄影时，读 [references/code-cinema.md](references/code-cinema.md)。沿绘制入口、场景/着色器、时间接口和输出验证来源；提示词和图库技术标签不能单独证明代码制作。没有源码就继续搜索作者仓库和可核查的补充工程，区分原作与补充作品。用户限定代码时不调用生图或生成视频服务，也不以调用生成API的代码充数；普通制作仍按题材选素材。

本地源码优先：读 [references/opus-methodology.md](references/opus-methodology.md)，用 `scripts/opus_methodology.py recommend --query "需求" --code-only` 查方法，再用 `card <id>` 和 `source <id>` 取得源码绝对路径、行号与固定版本。37张方法卡记录导演目的、持续对象、实现、失败条件与审片重点；阅读对应实现再迁移，检索命中不代表质量验证。找不到原工程继续追查作者仓库，补充作品与原作关系保持明确。要求近期高完成度影片时读 [references/recent-film-selection.md](references/recent-film-selection.md)，可加 `--film-only` 排除组件参考；日期、绘制路径与动态质量分别取证，普通旧demo不充当影片标杆。

[assets/code-studies](assets/code-studies/) 保存十套固定commit、逐文件哈希及原许可的源码包，共688个上游文件；代码MIT与字体/音乐等第三方许可分别保留。两套完整绘制运行部分已做代表帧/连续窗回放，其余八套为选定文本源码参考，尚未运行且素材/依赖不完整；其中浅水、刚体、Clearwater归为技术组件。用 [scripts/capture_code_study.mjs](scripts/capture_code_study.mjs) 回放已有两套；[assets/cinematic-starter](assets/cinematic-starter/) 提供原创Three短片与位置/目标双轨迹摄影工具；[assets/sdf-glass-lab/index.html](assets/sdf-glass-lab/index.html) 提供单界面折射实验。按需要复制到任务目录，版本、阅读入口与缺口见方法论，运行命令见 code-cinema。研究素材不自动成为所有题材的固定风格。

研究 Opus 图库、需要酷炫机制或选 UI 连续变形、门户缩放、液态玻璃、文字/交互解释时，读 [references/opus-gallery.md](references/opus-gallery.md)。通过 `scripts/opus_gallery.py search --mechanism <机制> --limit 5` 检索513条来源记录，按 slug 读提示词与实际画面；`scripts/opus_methodology.py trace <slug>` 返回阅读范围、源码关联与混合来源。原作、公开提示词、Skillry 重制版与源码分开取证，技术标签属于重制版。明确使用生成视频或来源未知的案例不能作纯代码效果证明。已有明确方向的简单视频不必额外查图库。

将参考写成持续对象、状态交接与事件表；同一形状/图片/字形能跨镜头延续，比堆叠无关效果更有用。按动作需要选择机制，参考的固定风格、专属工具、付费服务和审批习惯不自动继承。只要求研究/升级技能时交付研究与更新；验证可做独立短测试，不自动扩成完整制作项目。

- 解析视觉状态由帧号/时间、固定数据和素材直接计算，随机初始化使用固定种子。有状态模拟采用预计算缓存，或固定步长、完整重置/检查点与历史重播；分别测试顺序、乱序与新进程，不仅声明支持任意帧。像素差和状态差分别记录。
- 摄影机与场景使用一致坐标系。运动由动作驱动：展示细节时靠近，揭示关系时拉开，转移注意时移动，理解关键状态时停留。
- 需要跟拍可复制 [assets/subject-camera.mjs](assets/subject-camera.mjs)：无引擎依赖的二维/三维主体跟拍、绝对时间平滑、速度前瞻、相对偏移与揭示姿态混合。Three 路线将 position/target 数组用 `fromArray` 写入相机，示例见摄影参考。它不自动避障、构图求解或模拟光学对焦；朝向相对跟拍默认使用水平切向，垂直/急停/反向动作按参考说明改用世界偏移或单独轨迹。实时逐帧 lerp 不能直接用于任意帧输出。
- 支持参数化重要内容和风格，避免重做整片才能改文字、数据或配色。沿用项目的 JSX/TSX 和依赖习惯。
- 可复制 [assets/motion.mjs](assets/motion.mjs)：时间进度、缓动、固定种子、二维相机和解析三维投影；函数只接收时间和参数，不读取浏览器时钟。
- 连续 UI 或门户路线可复制 [assets/continuity.mjs](assets/continuity.mjs)：支持多次改目标的解析弹簧、松手初速度、对数匀速缩放和有明确点对应的轮廓插值。乱序求值与重复时刻应相同；循环另检查导出末帧→首帧的位置和速度。SDF单界面折射已有独立实验；完整玻璃出口求交、焦散与任意字形 morph 仍需按题材实现并验证，不能凭工具名宣称已跑通。
- [assets/CodeMotionStudy.jsx](assets/CodeMotionStudy.jsx) 是帧时间轴与几何运动的运行参考，不能作为专业科普片的画质标杆或默认模板。默认 1920×1080、30fps、360 帧，设置 `soundSrc` 才加入音频。
- 用用户已有音乐、合法本地音效或原创合成声音。旁白和外部付费服务按现有授权使用。声音事件与动作接触点、切点和落定点对齐；无声需求不强行配乐。

## 生成后由第二角色审核，再交付

制作缓慢、长片审片或续接暂停任务时读 [references/review-performance.md](references/review-performance.md)：真实低清缓冲、分阶段计时、复用已导出的证据、连续帧小批审核与可续接覆盖记录；无进展交付边界不改变完整审核要求或用户选定模型。

默认流程为制作角色导出 → 第二审片角色实际逐帧看画面、按完整时间轴听音 → 制作角色修复 → 审片角色复核 → 展示可播放版本。预演、局部片段和正式片均适用，按各自 brief 判断完成度。开始审核前必读 [references/independent-av-review.md](references/independent-av-review.md)，优先使用独立 Codex 子代理并保持用户选定模型与推理设置；职责、派工文本、覆盖证据、音频能力边界与返工停止条件以该文为准。用户明确要求先看时直接展示并标明审核状态；不可把未审阅、仅技术通过或工具不可感知的音频写成视听验收通过。

## 制作与独立审片闭环

1. 先渲染代表帧，在实际观看尺寸看构图，再放大检查材质、轮廓、光照、裁切和遮挡。白模、占位符、发白顶面、重复木纹、贴纸式合成等可见问题先修，再扩展整片。
2. 实际渲染 MP4。记录 composition、入口、参数、版本与输出位置。浏览器加载失败或编解码器报错必须修复或明确报告，不能交付空文件当成片。
3. 有结构化镜头表时，先运行 `scripts/shot_contract.py plan.json --out review-schedule.json` 检查时间覆盖、动作状态与连接风险；它不评价审美。用 `scripts/video_evidence.py` 提取代表帧与媒体元数据，用 `scripts/frame_audit.py` 导出全部帧并分批实际查看；剪口和高风险连续帧另看大图。长片按连续区间分批完成全片覆盖，维护待审范围，不能以关键帧抽查代替逐帧审核。
4. 按 [references/visual-review.md](references/visual-review.md) 看图并登记具体缺陷；查看大图解决接触表看不清的地方。再检查动态与声音：播放或连续序列，准确记录检查方式和覆盖范围。机器帧差不是审美评分；导出全部帧也不等于已经看过全部帧。
   跟拍另看起步、转弯、最快段、遮挡重现和目标交接的连续窗；同时比较主体与背景，区分固定中心环绕、定点摇摄、真正伴随和整图平移。记录相机/看向点世界位移、主体投影与可见缺陷；主体保持相似屏幕位置可以是成功跟拍，不能仅因主体居中判为静态，也不能仅因相机数值变化判为灵动。
5. 按 visual-review 的类型权重和时间码证据比较，找出最重要的三个问题，区分创意/镜头/运动/渲染。优先修改核心事件，最多两轮主要创意返工；重新渲染受影响片段并记录前后证据。方向成立且无阻碍理解的缺陷即停止。改片后核对最终整片哈希与观察对象，分数只作辅助，不能证明审美通过。
6. 独立审片者按 independent-av-review 保存与当前成片哈希绑定的覆盖记录、缺陷和结论；主 Agent 核验覆盖与修复证据。最多两轮修复复核；通过后展示成片，到达上限或能力受限时展示标明未通过/未完成的当前版本并说明剩余问题，不无限返工。

命令示例（路径与入口按项目调整）：

```text
npx remotion still src/index.jsx MyVideo out/qa/open.png --frame=30
npx remotion render src/index.jsx MyVideo out/video.mp4
python scripts/video_evidence.py out/video.mp4 --out out/qa --duration 12 --fps 30 --size 1920x1080 --times 0.5,2.5,3.5,6.5,9.5,11.9 --require-audio
python scripts/frame_audit.py out/video.mp4 --out out/frame-audit --cuts 90,180
python scripts/frame_audit.py out/video.mp4 --out out/transition-audit --start-frame 82 --end-frame 106 --width 1920
```

脚本使用系统 FFmpeg/ffprobe 或项目中 Remotion 随包的二进制；也可显式提供 `--ffmpeg` 与 `--ffprobe`。`video_evidence.py` 的必需依赖只有 Python 标准库；有 Pillow 时生成 JPEG 接触表，否则生成 HTML 接触表。`frame_audit.py` 需要 Pillow。缺少运行时或 Pillow 时用已有视频/图像工具完成相同证据提取，不为本技能装一整套媒体工具。

脚本不依赖精简 FFmpeg 中可能缺失的 xstack、select 或 volumedetect 过滤器。音量检查采样前 60 秒内的音频，不能替代听音或全片音频验收。已验证的实现经验见 [references/verified-experience.md](references/verified-experience.md)。

Windows 出现 x264 分配内存失败时，先降低渲染并发；必要时在项目自己的 `renderMedia` 调用或配置中用 `ffmpegOverride` 指定输出编码 `-threads:v 1`，并可设置 `-x264-params threads=1:lookahead_threads=1`。只在证据支持的故障恢复时采用；不要改用户全局配置或把低线程固定成所有机器的默认。安装包版本一致性、内存和可执行路径都应从本机核实。

## 交付

可用 `scripts/creative_review.py prepare plan.json video.mp4 --out qa` 串联现有代表帧/连续窗提取，生成待填写日志；实际查看后运行 `check plan.json video.mp4 --review qa/review.json`。它核对成片哈希、逐镜状态、连续窗口、类型维度及返工证据，不能自动评价画面。用 `opus_methodology.py card <id>` 查看重要卡的输入输出、参数、组合、成本与最小验证命令；机械行程可复用 [assets/mechanical.mjs](assets/mechanical.mjs)，但它是准静态受限示意，非流体/动态力学求解。

提供可直接播放的实际视频、可编辑源码入口与简短制作说明，并附独立视听审核结论、覆盖范围和剩余限制；必要时附证据链接。说明有哪些手段被真实测试，哪些是未测试路线。保持用户源码、素材、证据和成片可对应；不借“只改几行”或“完全一键”夸大实际工作。

用户要求停止正在生成的片子时，停止其具体任务/渲染，保留工程与已有素材；流程改进测试在独立目录做，不能以验证技能为由续做已取消的交付。不要结束无关服务。
