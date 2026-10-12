# Vibe Video 创意导演能力升级交付

2026-10-10。安装版与项目副本均为 **0.10.1**。本轮完成现有 Skill、技法索引和工程验证机制升级，保留原入口与历史作品；两条正式验证片已先提供给用户。最终审美反馈待用户，不宣称两片已获用户认可或完成全片自主视觉验收。

## 最新工作方式

按用户2026-10-10后续指令：每次视频生成后直接展示，让用户先看；展示前仅做必要工程检查，不自行预先观看、审美校准、评分或返工。用户反馈后按问题修改并展示新版。自主审片工具继续保留，仅在用户明确委托时启用。此规则已进入安装技能、项目副本、AGENTS.md、PRODUCTION.md与两个导演/审片引用文档。编码前创意选择、事实核实和机械约束继续执行。

## 原瓶颈与保留能力

原安装版0.9.0已有绝对时间运动、解析弹簧、跟拍、事件契约、代表帧与连续帧提取，以及35张可追溯方法卡；项目副本停留在0.7.0。主要缺口是没有编码前三个不同事件机制的选择记录、类型化评价与时间码证据、连续窗口观察核对和可执行返工记录。缓存只覆盖少数入口文件，会漏掉导入模块/事件数据变化。完整能力审计和修改前链路见 [baseline.md](baseline.md)。

保留 motion/continuity/subject-camera、现有 Canvas/Three/Remotion 路线、shot_contract、video_evidence、frame_audit、风格时间轴、上游归档与许可。没有新建统一渲染框架或大型依赖；没有把醒城、粒子、反转、发光或固定三段式写成通用模板。

## 实质变化与修改文件

|文件|变化|
|---|---|
|SKILL.md|三种差异创意与选择依据；按题材路由；生成后用户先看；按授权启用观察返工|
|references/director-design.md|创意决策记录、七种视频类型边界、动态预演与镜头目的|
|references/motion-craft.md|意图/约束/响应/恢复、主次动作、跨对象因果与机械事实|
|references/visual-review.md|类型权重、时间码、前三问题、最多两轮主要返工、哈希与观察范围|
|references/opus-methods.json|9张既有重要卡补操作元数据，新增2张原创卡；总37卡|
|scripts/opus_methodology.py|操作字段检查；继续兼容检索、source、trace、code-only与film-only|
|assets/mechanical.mjs（新增）|准静态预载/压差/受限行程状态、显式速度节点的Hermite路径|
|assets/test-motion.mjs（新增）|行程/固定端、路径接续/乱序、旧连续工具回归|
|scripts/creative_review.py（新增）|串联原提取器，生成pending日志；核对成片哈希、逐镜状态、主动作/风险连续窗、已看页、类型维度、返工证据|
|assets/cinematic-starter/render.mjs|输入模块/JSON/素材指纹；渲染器与工具链身份；缓存检查前移；局部范围/低成本比例；初始化错误及时报告|
|项目AGENTS.md、PRODUCTION.md、README.md|9:16规则保留；最新用户先看流程；版本、入口与同步记录|

技能文件路径均相对于 `D:/Codex/skills/vibe-video`；项目副本位于 `skill/vibe-video`。安装旧版备份在 `before-skill`，项目旧副本备份在 `before-project-skill`。逐文件差异与当前哈希见 [delivery-audit.json](delivery-audit.json)、[skill-sync-manifest.json](skill-sync-manifest.json)。索引仍使用既有JSON结构；11张重要卡具备完整操作字段，其余26张保留原导演目的、实现、失败条件、审片重点与源码锚点，未宣称全部扩展或运行验证。

## 原/新验证片

两个案例沿原源码隔离改造，选择记录见 [creative-direction.md](creative-direction.md)。均为1080×1920、24fps、H.264、无音频；历史带声片保留。

|案例|原片可验证问题|当前版本实际变化|证据与限制|
|---|---|---|---|
|8秒飞行器|连续穿行，环境初始化后不响应|0–2.4s接近闭门并减速；2.5s附近请求环出现；3.1–4.3s门退让；4.4–6.5s穿越；6.5–8s升高回收通道|原片 [画面](before-flight/contact-sheet.jpg)，新版 [视频](flight/out-final/flight-director.mp4)/[画面](flight/out-final/qa/media/contact-sheet.jpg)。新指令前实际看过代表表、3.3/7.85s大图与4窗7页连续序列；反馈事件可见。结尾主体较小且门仅局部入画，不能把自评分当改善证明|
|15秒止回阀|开场先给结论；运动区域小；相机仅轻微整页缩放|0–2.5s先给流动现象；2.5–5s剖面/接触揭示；5–10.5s近景读开度与弹簧压缩/复位；10.5–15s逆压关闭后收束|原片 [画面](before-valve/contact-sheet.jpg)，新版 [视频](valve/out-final/valve-director.mp4)/[画面](valve/out-final/qa/media/contact-sheet.jpg)。预演已按观察修过HUD侵入、接触宽度、箭头及阅读时长；正式代表表已看，6窗12页仅提取未看；不宣称全片自主视觉通过|

预演证据在 `flight/out-preview-r1`、`valve/out-preview-r2`；正式片与源码在各案例目录。阀门为准静态原理示意，非CAD、动态碰撞或流体求解。阀座孔405–555、阀瓣390–570有闭合重叠，弹簧固定下端1245，行程上限128；这些是本例绘制参数，不是通用机械设计尺寸。新指令之后没有继续自主校准或重渲两片。

## 实际工程验证

|验证|结果与证据|
|---|---|
|技能读取与引用|quick_validate通过；核心入口及本轮四份引用文档的43个本地链接有效；见delivery-audit.json|
|技法/来源|37卡、513来源记录、688源码哈希通过；锚点/固定commit/原文摘录检查有效。上游十套归档未全部执行，两套已有回放，其余保留source-read-only边界|
|审片执行器|独立测试发现并复现路径分隔符、无动态证据、缺正确性维度三个缺口；已修复。最新脚本10项正反例再次通过；见forward-test/FORWARD-TEST.md及review-test-results.json。最新逐镜fallback与合并窗也在两条正式片prepare中实跑|
|机械/寻址|独立8项约束检查通过；两个新Node进程状态哈希一致；新运动3项通过；见forward-test/mechanical-checks.json、fresh-process-check.json及delivery-audit.json|
|既有路线|style-studio事件/阅读/接触契约通过；旧数据片代表帧实际重建，无页面错误，新页面像素一致；见other-regression/dataviz/render-evidence.json。既有camera-upgrade检查通过；未声称覆盖所有视频类型|
|正式导出|飞行器8.0s/192帧，阀15.0s/360帧；完整解码通过，无技术失败，乱序重复像素一致；媒体、最终文件与render-evidence哈希匹配；见各out-final/qa/media/media-evidence.json及delivery-audit.json|
|缓存|7项实跑：基础导出、相同输入复用、导入模块改动、事件JSON改动、渲染器改动、比例改动、工具链记录不一致；变更均拒绝旧缓存，旧截图/JPEG/视频不被覆盖。见other-regression/cache-test-results.json；0.25s工程测试片已直接提供，不评价画质|
|项目同步|769文件与安装版哈希一致；无覆盖用户全局配置，无删除历史作品|

复测命令（从项目根）：

```powershell
& 'C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 work/creative-upgrade-20261010/audit_delivery.py
```

审片工具命令仍为 `creative_review.py prepare plan.json video.mp4 --out qa` 和 `check plan.json video.mp4 --review qa/review.json`；在本机显式传入捆绑FFmpeg/ffprobe。它检查证据一致性，不证明审美、真实观看行为或科学仿真正确性。正式两片的review.json保持pending，不能为了脚本绿色结果填造观察。重新渲染使用新输出目录，避免与原版本缓存配置冲突。

## 原要求对照

|原需求章节/验收项|当前对应依据|
|---|---|
|一、升级现有能力体系|0.10.1 Skill/参考/工具；保留引擎，不重建|
|二、先扫描、10项能力审计、基线|baseline.md、修改前备份与manifest|
|三、两种失败案例与通用原则|原片提取、creative-direction.md、原源码隔离改造；director-design的类型表|
|四、创意/巧思/运动/相机/节奏|核心入口及director-design、motion-craft、既有subject-cinematography/event-timeline；三个差异方案与选择记录|
|五、重要方法元数据、12类主题、反模板化|原35卡保留，9卡增强+2新卡，11张操作元数据；既有timeline/camera/continuity/text/audio/determinism机制按题材组合，不重复新建|
|六、预演、真实证据、类型评价、有限返工|两例预演与此前实际观察/修正；creative_review正反例。按后续用户指令，自主审片不再是展示前门槛；先给用户看，反馈后定向改片|
|七、兼容、异常、参数化、效率|原入口、许可和目录保留；轻量mechanical工具、状态/错误测试；局部range、scale及安全缓存|
|八、工程与创意回归、前后对照|上述实际测试、两片完整导出、原/新画面及时间码对照；至少飞行器已有实际连续观察支持因果变化；最终审美由用户先看|
|九、A Skill完整性|入口/创意/类型/动态/审片/引用关系均有文件与执行证据|
|九、B 视频创作能力|两例三个不同方案、自主选择、事件/镜头表及保留风格；不以源码复杂度认证美感|
|九、C 工程质量|读取/链接/索引/运动/事件/导出/缓存/其他类型与同步实跑|
|九、D 创作质量边界|真实画面证明事件与揭示发生变化；不宣称普遍审美提升、用户认可或未看的动态完成验收|
|十、实施顺序|baseline→指导/索引→执行器→预演/观察修正→正式导出→测试→本报告；后续用户优先规则已应用|
|十一、8项交付物及7个最终问题|Skill、引用、索引/代码、可执行审片、两例、对照、测试、残余限制均列于本报告|
|十二/十三、禁止事项与四原则|保留旧能力，创意先行、因果运动、事实边界、实际证据；不堆效、不强制模板、不以分数/渲染代替视觉结论|
|项目画幅与最新规则|两片1080×1920；AGENTS/Skill/PRODUCTION中用户先看；历史横片保留|

## 剩余边界与下一步投入

静音两片未做实时播放或听音验收；最终用户观看反馈待定。新机械模块只验证准静态约束，没有动态碰撞/迟滞/流体惯性。缓存指纹覆盖项目内输入和工具链身份，主动跳过符号链接及node_modules；外置自定义素材须复制入任务目录或另行加入指纹，不能假设全部外部文件自动覆盖。未证明任意字体变形、所有上游作品本机可跑或所有视频类型均已验证。

下一步最值得投入的是根据用户实际观看反馈集中修正关键事件的可读性与镜头完成感，积累不同题材的前后对照证据。需要声音时再加入动作对应的事件音并实际听音；继续增加技法前先检查已有方法能否完成目标。当前无需自动扩成新特效框架或继续自评返工。
