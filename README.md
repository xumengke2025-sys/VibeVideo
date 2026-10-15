# Vibe Video 项目

本目录集中保存参考研究、旧作品、导演方法改进和原创验证片。整理日期：2026-10-09。

GitHub公开版本的上传范围、参考恢复及启动方法见 [PUBLICATION.md](PUBLICATION.md)。项目源码和本项目制作的预览影片随仓库保存；第三方原片从作者原址恢复，原许可证和固定版本索引保留。运行 `npm run preview:references` 可打开本地参考选择目录。

参考入口（2026-10-15发布更新）：[原片、风格与源码目录](work/github-reference-expansion-20261011/index.html)，共319条参考，109条有对应绘制源码（89部影片、20段镜头样段），其余按作者原片、改编、节选及输入不完整的模板标注。支持搜索、画风、作品类型、源码状态、批次筛选和分页。[本轮来源与查重](work/video-film-expansion-20261014/README.md)、[仓库清单与说明](work/github-reference-expansion-20261011/CATALOG.md)。公开仓库提供索引、来源与恢复清单；第三方原片从作者地址恢复，下载范围和许可见 [PUBLICATION.md](PUBLICATION.md)。

当前视频支持 **16:9 横屏**（1920×1080）与 **9:16 竖屏**（1080×1920），新片启动时提供选项；已指定画幅和后续修改沿用该片选择。以下为历史15秒成片：

- [热点片《冰下，宇宙亮了》](work/hot-news-20261009/out-final/icecube-news-portrait.mp4)：南极历史实景、冰下光迹与2026诺贝尔物理学奖，含原创氛围配乐与事件音。
- [弹簧止回阀《只向一个方向》竖屏版](work/portrait-valve-20261009/out-final/one-way-portrait.mp4)：重新纵向绘制的15秒机制片，含机械音效。

两支片的源码、来源与审片证据均保存在各自目录。下列横版为历史版本。

制作流程见 [PRODUCTION.md](PRODUCTION.md)。技能当前版本0.16.3，入口在 [skill/vibe-video/SKILL.md](skill/vibe-video/SKILL.md)。[成套视频与源码检索](skill/vibe-video/references/video-example-library.md)返回视频和准确源码入口；仅有媒体的作品可用于视觉研究，不能冒称已研究实现。新片与大幅改造默认先做可动画化的整体效果图，落实反馈后制作关键动作样段与整片；已有认可方案和局部修改直接复用，细则见 [效果图先行](skill/vibe-video/references/concept-first.md)。交付沿用用户所选“直接生成，由用户反馈”或“AI 审核一轮”。

镜头库与Motion Workbench接入见 [shotcraft-integration.md](skill/vibe-video/references/shotcraft-integration.md)：固定2026-10-13上游版本，124张卡/150个Gallery变体，新增准确源码检索、Windows工作台与横竖PageCam适配。安装 `D:/Codex/skills/video-shotcraft` 的旧版完整保存在本次任务目录；[接入检查点](work/shotcraft-integration-20261014/CHECKPOINT.md)记录实际验证与限制。工作台需要Remotion组件清单，旧HTML/Canvas片不自动转换。

三项暂停任务的性能改动、验证与续接入口见 [实施说明](work/performance-optimization-20261011/实施说明.md)。暂停聊天没有自动恢复；继续时先读取各项目PERFORMANCE-HANDOFF.md。

本轮参考研究、已落实改动与验收边界见 [完整优化计划](work/workflow-optimization-20261011/优化计划.md)。按用户最新要求，已撤回项目双模型配置；制作、按需导演和独立审片继承用户当前模型与推理选择。三个参考的迁移方法、动作与镜头改进及审核校验继续使用，旧双模型资料仅归档。

本轮验证片：[8秒飞行器](work/creative-upgrade-20261010/flight/out-final/flight-director.mp4)、[15秒弹簧止回阀](work/creative-upgrade-20261010/valve/out-final/valve-director.mp4)，均为1080×1920、24fps静音版；当前等待用户观看反馈。

本轮升级交付、要求对照与验证边界见 [DELIVERY.md](work/creative-upgrade-20261010/DELIVERY.md)。

- `work/style-production-20261009`：本轮风格与视听体系改进、来源文档、备份、原创验证和审片记录。
- `work/style-production-20261009/studio/out-approved/one-way/one-way.mp4`：32 秒原创蓝图《只向一个方向》。
- 同级 `blueprint-proof`、`dataviz-proof`：两个 10 秒能力片段；`dataviz-variant`：更换演示数据后的重建验证。

- `work/director-study-20261008`：本次参考研究、审片证据、skill 旧版备份。
- `work/morpho-blue-20261008`：原创验证片《蓝色的建筑》的源码、生成素材、声音和阶段渲染。
- `work/black-hole-lensing-20261008`、`work/light-to-lens-20261008`：保留的旧作品及工程。
- `work/reference-study-20261008`、`work/skill-refinement-20261007`、`work/vibe-video-proof`：此前研究、改进和验证资料。
- `reference-sources`：公开参考媒体与源码的本地副本；不包含 Git 历史和第三方依赖。
- `skill/vibe-video`：当前已安装 skill 的整理时快照；实际安装位置仍为 `D:/Codex/skills/vibe-video`。
- `goal-objective.md`：完整目标；`CHECKPOINT.md`：当前进度；`organization-manifest.json`：整理映射和文件哈希。

原 work 路径保留目录联接，已有绝对路径仍可使用。此目录的 node_modules 联接复用上级共享依赖；本项目尚不是可脱离本机直接运行的独立归档。临时来源保留原件，以维持现有源码和工具引用。

此前长期目标的 52 秒《蓝色的建筑》及其综合研究交付另见 CHECKPOINT.md；本轮 32 秒蓝图验证片不替代该目标。当前新风格体系的完成情况与验证边界见本轮检查点。

按节奏反馈新增15秒版：《只向一个方向》见 [15秒版](work/style-production-20261009/studio/out-15sec/one-way-15/one-way-15.mp4)，原32秒版保留。
