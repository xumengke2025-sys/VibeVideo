# AI 驱动审计非现场监测：30 秒参考选择

Updated: 2026-10-18 (Asia/Shanghai)

## Objective and authorized scope

精读用户提供的25页PDF，研究参考视频与源码。最新任务转为：查阅用户AI机械图项目的聊天、偏好与现有实现，为审计项目制定约30秒的具体制作计划。当前交付计划，不启动成片或恢复其他聊天工作。

- aspect_ratio: 16:9
- width: 1920
- height: 1080
- duration_target_seconds: 30
- delivery_mode: ai_review_once
- Reference choice: 提出AI机械图精密仪器方向建议，尚未经用户确认；不再重复通用参考筛选。
- Concept image: 待本片方向确定后制作；AI机械图已认可概念图是参考，不是本片效果图。
- Subagents used: 0

## Source and completed research

原始 PDF：D:/腾讯电脑管家文件搬家/WXWork/1688855784827722/Cache/File/2026-07/AI 驱动・审计非现场智能监测体系建设.pdf

- 全文提取保存在 source-text.txt，25 页。页面概览保存在 pdf-pages-01/07/13/19.jpg；页面图用于结构核对，正文以全文与必要大图为准。
- p2-10：建设方案、六类痛点与价值、分阶段演进；p10 为成效预期，不是实测量化收益。
- p12-16：统筹、数据、规则、预警、可视化及核查反馈闭环。
- p14：试点自然语言转可执行代码草稿，供审核；不要表现为未经审核直接生产执行。
- p15：MVP 线索台账与人工真实性判定；静态试点看板与后续动态画像需要分层。
- p18-23：客户风险测评异常 MVP。开户与问卷信息差异、跨级修改（季度内两次差值≥2）、后续交易关联、分级核查、客户/经理/营业部画像。
- p19：沿用月度跑批；不是已部署实时自主监测。
- p20：区分客户自主修改与疑似诱导，结合设备线索、交易与销售留痕核查；单项异常不证明动因或违规。
- p22：客户行为特征矩阵与机构异常人数阈值为不同口径，30 秒片不混成同一风险刻度。
- p24：人工最终定性与处罚、最小必要采集、脱敏、可解释性；多 Agent 端到端属后续阶段。

## Reference selection

精读技能 references/video-example-library.md、opus-methodology.md、recent-film-selection.md。查统一索引，初筛六部，各提取六张时间点概览，查看实际画面。六部完整索引保存 reference-candidates.json。

拟向用户展示四部：

1. Lemo / 网点档案，原片 30s。编号、网点纸张、证据卡汇总、印章与归档。原片为胖橘幽默故事，审计改编需重新制作专业叙事及道具，不继承预先定罪措辞。源码：reference-sources/github-expansion-20261011/lemomo-ai--lemo-opuscar/styles/halftone-dossier/demo/index.html。阅读舞台/场景注册、标题与档案、归档、HUD、网点擦拭、render 主循环（约349-430、884-989、1037-1084）。属于二维 SVG/Canvas 分镜与擦拭，不是连续三维穿行。
2. Lemo / 等距信息图，原片约58.79s（咖啡豆从产地到杯中）。共享世界、持续对象、运输跟随、向货舱/箱/袋内层层推进、结尾拉远。源码 demo/main.js → film.js（路径/状态、camAt 61-97、render 429起）与 engine.js（等距投影P、深度排序、世界锚点）。Canvas 等距投影，不冒称 Three/物理三维。改编为一份审计线索穿过数据、规则、人工核查与反馈站，30秒减少站点。
3. 小马 / 一形贯穿九个UI状态，原片12.5s、1:1。单一形状从点/按钮/加载/卡片/协作提示/图表/导出状态连续改变，光标操作驱动，轻微过冲。源码 examples/launch-morph/index.html（全文136行）、engine/runtime.js（镜头与render接口）。改编为业务需求→规则草稿审核→线索→复核归档的概念演示，标注方案示意，不冒充真实产品录屏。横屏需重排布局。
4. Lemo / 瑞士平面动效，原片44s（Five Rules for a Poster）。黑白红、网格、数字、字块重排、红圆越界、海报旋转与拉远。源码 demo/main.js → film.js（文字揭示45起、CAM 231-240、RULES245起、renderFilm395起）。改编为问题→证据→分级→人工复核的精炼图解；数字可作步骤编号，不虚构提升率。

未列入最终四选：小马研究结论演示（27.2s，无音轨，偏演示页）与 Lemo 数据叙事（50s，铅笔画百年气温曲线；原材料没有可直接替换的实测时间序列）。保留研究缓存。

## Verification and limits

已核对本地成片、绘制入口与实际关键实现，并查看四个关键动作窗口的顺序抽帧：网点档案19.7-22.1s（网点擦拭、证据卡依次进入）；等距信息图27.4-29.8s（跟船、向箱内推进）；UI变形3.0-5.4s（加载形状扩展为卡片、文字与按钮操作）；瑞士24.3-26.7s（红圆离开网格并引起版面变化）。各窗口12张帧、约0.218s采样间隔，保存为各候选子目录 motion-window.jpg；不是实时整片播放或全帧审核。尚未在本任务重渲上游项目，Lemo 发布媒体与固定源码逐像素一致性未确认。参考筛选不是成片独立视听审核；没有声称完整听音或全帧覆盖。

## Next action

用户最新标准：适合正式项目介绍、专业化程度高。应以业务问题、体系运转与专业价值筛选完整项目/系统介绍片，不再以艺术画风或单项动效为中心。

本轮增看 Makefx工作原理、Lemo暗色科技发布会、Lemo全息HUD各6个时间点。以 Makefx工作原理（40s,1920×1080,24fps）作为新的单支推荐：同一资产从需求到处理、结果、复用、全局关系，图解和局部界面直接解释系统行为。实际绘制入口 reference-sources/github-expansion-20261011/makefx--animation-video-test/index.html；已阅读 SCENES.md 的叙事/视觉约定、s06-workflow.html 的卡片沿步骤推进/标签状态联动、s18-finale.html 的关系链汇总与拉远。参考片的开发者代码、定价和计费等不迁入审计片；不照搬原片每2秒一镜/每拍一事件的配额。

本轮各自概览在 makefx/contact.jpg、dark-keynote/contact.jpg、hologram-hud/contact.jpg。未重渲、未完整播放/听音，不写独立视听审核通过。向用户展示Makefx原片、实际效果与30秒业务转译建议，继续等其选择；不立即生成概念图或成片。

选择后据30秒理解预算设计横屏整体概念图，记录反馈/保护项；之后制作最难动作与相邻转场样段，再展开成片。AI审核仅在正式待交付版本启用一个继承当前模型/推理的审片者，最多一次修复及必要复核。


## Expanded professional reference selection (2026-10-18)

用户尚未认可视觉方向，当前只交付更多可播放参考供选择，不能代选并开始制作。
新增检索并查看10支参考，各6个时间点：deedydas、davidmarcus、kaolti、moritzkremb、dale_vaz、gouthamjay8、howdevelop、alex_prompter、ann_nnng，以及 Lemo living-screencast。完整元数据保存在 reference-expanded.json，各目录 contact.jpg。
本轮准备展示7支（全为横屏）：
1. original/moritzkremb-466494（46.06s）：以Notion为内容的产品发布参考，痛点→统一平台界面→会议/搜索/Agent能力→价值。非已核实官方品牌宣传片；无绘制源码。
2. original/dale_vaz-879074（47.07s）：深色金融交易终端，多窗组装、图表与数字特写、拉远及手机落版；用于参考专业数据画面，审计改编不用交易K线冒充审计事实。无绘制源码，原片无音轨。
3. lemo/living-screencast（59.4s）：界面操作演示，输入→计划→改动审阅→运行预览，聚光/镜头跟随操作，原片含像素角色。改编可突出自然语言规则草稿→人工审核→线索台账→核查反馈，正式方向去掉角色。有同风格绘制源码，但原片是代码绘制示意界面，不称真实审计录屏。
4. original/deedydas-252537（26.05s）：Muda推理产品，等待问题→计算块矩阵→彩色文本流→结论；明亮、技术解释。审计只借图解逻辑，不迁入原片效率数字。无绘制源码。
5. lemo/dark-keynote（42s）：Tidy文件产品，文件通知混乱→收束整齐网格→产品界面与价值；深色、绿色强调。有同风格绘制源码。
6. original/howdevelop-733090（30.10s）：TanStack AI主题技术发布参考，信号线、节点分支、任务状态、结果面板。审计可借数据→规则→线索→人工复核关系；不照搬Agent自动执行叙述。无绘制源码。
7. original/kaolti-092204（39.5s）：Cosmos主题产品参考，图片材料墙→搜索筛选→收藏/聚合→球形收束。审计可转为多源材料与关联证据，删减图片球形装饰。无绘制源码，原片无音轨。
上述7支另查看9帧顺序时间窗：Notion 5.5–10s、交易5–12s、动态录屏25–33s、Muda3–10s、暗色12–22s、TanStack12–19s、Cosmos29–36s；各目录 expanded-window.jpg。此为稀疏动态研究，不是完整播放、听音或成片审核。
源码阅读范围：dark-keynote/demo/main.js全部15行，确认Canvas renderFilm入口；film.js检索排序波/主render/事件入口。living-screencast/demo/main.js前65行，确认DOM界面、锚点、camera transform、聚光遮罩/运动模糊与角色层；film.js检索camAt/build/frame入口。没有重渲原工程，不能宣称逐像素复刻已验证。
下一步：展示7部原片和各自适用重点，等待用户选编号或组合；继承16:9、1920×1080、30秒、ai_review_once。选定后才按concept-first做整体效果图。

## AI机械图跨聊天研究与最新计划（取代上述历史下一步）

用户要求查其AI机械图聊天并针对审计项目制定计划。已读“回复问候”(01a14950-a8d2-7982-a28b-965a0dfc34cb)、“整理AI应用周报”(01a144a8-96d9-7863-90da-7dda9d0118d9)、“完善转正答辩视频”(01a146e4-423e-7de2-aac1-7e83d9dea495)、“查看 anatomy skill 用途”(01a13dbc-34bf-7981-93f0-e2b0d09f1191)。未发消息、创建聊天或恢复其他片。

最新偏好：全屏机械，用机械讲述业务原理；文字随机关出现，无底部字幕；更精妙的因果机构，避免大面板加简单机械；关键案例深入，运镜不重复推近拉远。认可温润黄铜、深木、古典科学仪器气质。

源码阅读：D:/ai项目/ai机械图/output/probation-film/ 的BRIEF、CHECKPOINT、PRINCIPLES-CHECKPOINT、principle-instruments.mjs（审计121–143行）和timeline.mjs审计段。已看five-machines-v1概念图与current-contact旧接触表。最新量规/联锁还未生成本轮样段，不能宣称效果已验证；概念与旧实际画面有完成度差距，没有完整播放或听音。

本片计划保存于“机械视频制作计划.txt”：审计线索检核机，0–4s资料与规则审核，4–13s双维初筛/等级差量规，13–19s交易时序联查，19–26s人工核实，26–30s整机及反馈揭示。重点纠偏：两个初筛维度独立，交易只加强核查关注，缺交易不丢弃初筛线索，归属不等于定责。

从2026-10-16周报补充现状：原表下线，已替换DW.DWD_CLIENTPREFERJOUR_D_I并同步Doris，FinBI待重配；计划不展示动态看板已全量上线。

下一步：向用户交付具体计划。方向确认后按整体效果图→6–8秒关键机构样段→全片→既定一轮AI审核推进。当前无效果图、无新渲染、无审核、无子代理；延续16:9、1920×1080、30秒、ai_review_once。
