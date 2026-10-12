# 已检查的方案与复用边界

检查日期：2026-10-07/08，Opus 图库补查 2026-10-09。以下是来源与候选方法，不是对全部样片做过对等质量评测。

## 技术基础

- [Remotion 官方技能](https://www.remotion.dev/docs/ai/skills)：API、帧时间轴、音频、字幕、素材、渲染。适合作为工程基础，不能单凭 API 正确性保证美术质量。
- [Remotion 官方 Codex 插件](https://www.remotion.dev/docs/ai/codex-plugin)：官方明确支持 Codex；当前本地已有 Remotion 工程和相关技能，不要求为同一功能重复安装插件。

## 创作方法

- [video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft)：产品宣传片的真实页面采集、镜头卡、2.5D 运镜、音效与终检；当前本地版本与上游数量不同，不覆盖本地修改做自动升级。
- [Remotion Motion Graphics Skills](https://github.com/Liamrjohnston/remotion-motion-graphics-skill)：带样片和参考源码的制作流程，cinematic-camera 强调共享世界、局部动作、揭示全局、落定。格式、背景、零霓虹等属于作者固定风格与流程，不能当成用户所有动画的普遍要求。本技能仅吸收概念，自行实现工具，不复制代码或样片。
- [MG-Skills](https://github.com/myceldigital/MG-Skills)：叙事、动作层级、预备与余动。宣传用语、所有视频必须加粒子/微动等不是已证明的质量标准；按题材选择。
- [Motion Graphics Skills / HyperFrames](https://github.com/imMamdouhaboammar/motion-graphics-skills)：包含多个专项技能、实际作品与源码，偏另一套运行时。可作为后续路线；当前无需为了验证基础能力安装全部专项技能或替换现有引擎。

## 案例参考

- [awesome-opus5-5-videos](https://github.com/yihui-dev/awesome-opus5-5-videos)：0.5 已加入固定快照的 513 条离线检索、来源/残缺标记、连续 UI/门户/玻璃等制作配方及解析工具。实际读取三部 Original 与一部 Remake 的媒体取样，未取得原作者完整源码。技术标签属于 Skillry 重制；提示词不是完整创作会话。详见 [opus-gallery.md](opus-gallery.md)。

## 2026-09-30 及之后的重点研究

核查日期 2026-10-07，日期按来源说明区分：

| 来源 | 可核实日期 | 实际看过的证据与采用方式 |
|---|---|---|
| [huashu-art-motion](https://github.com/alchaincyf/huashu-art-motion) | 方法文档记录 10-04/05；本地源码提交 `26dba25b2b495c2138848c29a2c90df356a20325` 为 10-06 16:32 +08:00 | 读一帧先行、经验、分层路线与许可证；吸收按层选工具、代表帧先行、源坐标和连续审片。它的角色素材许可独立于 MIT，不挪用角色库。没有对全部作者成片做逐帧评测。 |
| [iArt 作者实测：Motion Graphics](https://www.iart.ai/blog/claude-motion-graphics) | 页面明确更新 10-03，首次发布日期未核实 | 同一主体跨镜头、一个核心想法、准确数据、手机尺寸可读性；作者也记录空画面、形变折叠等问题。这里只采用方法，不把其首次生成或传播数字当独立验证。 |
| [iArt 作者实测：Launch Videos](https://www.iart.ai/blog/opus-5-5-product-launch-videos) | 明确更新 10-03，首次发布日期未核实 | 研究开放创作 brief 与详细镜头表的差别：先留空间探索视觉承诺，再把已选方向写成时序；产品炫技节奏不直接套到知识解释。 |
| [iArt javascript-animation-skills](https://github.com/iart-ai/javascript-animation-skills) | 仓库创建 09-23；[0.4.1 合并提交](https://github.com/iart-ai/javascript-animation-skills/commit/f7d0882a313249cbd43f0e4e9e209b1622870253) 为 09-30 19:40 +08:00 | 检查 0.4.1 源码及 09-30 提交：时间确定性、分镜/布局自检，移除固定配乐菜单与每30秒镜头数量，避免成片被模板锚定。其零素材限制仅属于纯代码模式，本技能不继承。 |

10-07 研究时该图库 README 标注更新 09-29；10-09 重查快照 `756290289742535eb0ac3817548f152e9759cc70` 已标注 10-08 更新、加入38条，513条总计。这里区分两次快照；入库日期不证明作品首发日期，也不用于证明模型发布日期或跨模型优劣。

## 验证范围

0.2 的新增能力是代表画面、混合素材与逐帧证据流程。独立短测试片与检查记录保存在本次项目的 `work/skill-refinement-20261007/`，具体通过项以实际报告为准。下载影像的原始发布日期可以早于研究时间窗；研究文章的时间筛选不限制制作素材的年代。未完成 Claude 与 GPT 的同题、同素材、同预算比较；不能据此保证复现全部 Claude 案例或宣称模型能力等同。

## 用户明确选择的成片（2026-10-08）

- [Opus5.5告诉你，它是怎么做视频的](https://www.bilibili.com/video/BV1vRHa63EYg/)：发布于 10-03 20:05 +08:00。实际读取约 147 秒、852×480、30fps 的匿名可用版本；整片每 4 秒抽帧，并加密检查 54–64 秒的代码/场景转换。没有取得其原工程或匿名字幕，不从宣传文案推断提示词之外的真实工作量。
- [吓哭了Opus5.5 AGI概念MV](https://www.bilibili.com/video/BV18ta86EEHb/)：发布于 09-27 17:47:56 +08:00，用户后续明确选为最喜欢的参考。描述说明是 4K 参数重渲版；实际读取约 156.67 秒、852×480、30fps 的匿名版本，不能用它证明原片的 4K 细节。整片每 4 秒抽帧，另看 10–15.5、29–33.4、82–87 秒的加密序列。
- [mexicat/pdoom-video](https://github.com/mexicat/pdoom-video)：已读 README、许可证、treatment、engine、timeline、逐词/音频数据及代表场景/字体/后处理源码。当前 commit `fa164b74fd0b26a99375715b619c55b4a0fb3d05` 的作者时间为 10-06 05:24:56 +08:00（原记录 10-05 22:24:56 +01:00），晚于上述转载；不能把当前代码与转载画面当完全同一版。代码 MIT；歌曲/歌词不在其许可内。

具体可迁移机制与验证范围见 [reference-study.md](reference-study.md)。0.3 改进重点是连续语义变化、空间与文字共同叙事、声音事件锚点及细线/时间采样的条件检查；原作者代码复现与新的原创制作能力须分别记载。
