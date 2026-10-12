# 已检查的方案与复用边界

检查日期：2026-10-07。以下是来源与候选方法，不是对全部样片做过对等质量评测。

## 技术基础

- [Remotion 官方技能](https://www.remotion.dev/docs/ai/skills)：API、帧时间轴、音频、字幕、素材、渲染。适合作为工程基础，不能单凭 API 正确性保证美术质量。
- [Remotion 官方 Codex 插件](https://www.remotion.dev/docs/ai/codex-plugin)：官方明确支持 Codex；当前本地已有 Remotion 工程和相关技能，不要求为同一功能重复安装插件。

## 创作方法

- [video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft)：产品宣传片的真实页面采集、镜头卡、2.5D 运镜、音效与终检；当前本地版本与上游数量不同，不覆盖本地修改做自动升级。
- [Remotion Motion Graphics Skills](https://github.com/Liamrjohnston/remotion-motion-graphics-skill)：带样片和参考源码的制作流程，cinematic-camera 强调共享世界、局部动作、揭示全局、落定。格式、背景、零霓虹等属于作者固定风格与流程，不能当成用户所有动画的普遍要求。本技能仅吸收概念，自行实现工具，不复制代码或样片。
- [MG-Skills](https://github.com/myceldigital/MG-Skills)：叙事、动作层级、预备与余动。宣传用语、所有视频必须加粒子/微动等不是已证明的质量标准；按题材选择。
- [Motion Graphics Skills / HyperFrames](https://github.com/imMamdouhaboammar/motion-graphics-skills)：包含多个专项技能、实际作品与源码，偏另一套运行时。可作为后续路线；当前无需为了验证基础能力安装全部专项技能或替换现有引擎。

## 案例参考

- [awesome-opus5-5-videos](https://github.com/yihui-dev/awesome-opus5-5-videos)：用于查主题、提示词与创作者原帖。原帖、提示词、原始源码、重制版本要区分；公开提示词不能保证一模一样的重现。

## 2026-09-30 及之后的重点研究

核查日期 2026-10-07，日期按来源说明区分：

| 来源 | 可核实日期 | 实际看过的证据与采用方式 |
|---|---|---|
| [huashu-art-motion](https://github.com/alchaincyf/huashu-art-motion) | 方法文档记录 10-04/05；本地源码提交 `26dba25b2b495c2138848c29a2c90df356a20325` 为 10-06 16:32 +08:00 | 读一帧先行、经验、分层路线与许可证；吸收按层选工具、代表帧先行、源坐标和连续审片。它的角色素材许可独立于 MIT，不挪用角色库。没有对全部作者成片做逐帧评测。 |
| [iArt 作者实测：Motion Graphics](https://www.iart.ai/blog/claude-motion-graphics) | 页面明确更新 10-03，首次发布日期未核实 | 同一主体跨镜头、一个核心想法、准确数据、手机尺寸可读性；作者也记录空画面、形变折叠等问题。这里只采用方法，不把其首次生成或传播数字当独立验证。 |
| [iArt 作者实测：Launch Videos](https://www.iart.ai/blog/opus-5-5-product-launch-videos) | 明确更新 10-03，首次发布日期未核实 | 研究开放创作 brief 与详细镜头表的差别：先留空间探索视觉承诺，再把已选方向写成时序；产品炫技节奏不直接套到知识解释。 |
| [iArt javascript-animation-skills](https://github.com/iart-ai/javascript-animation-skills) | 仓库创建 09-23；[0.4.1 合并提交](https://github.com/iart-ai/javascript-animation-skills/commit/f7d0882a313249cbd43f0e4e9e209b1622870253) 为 09-30 19:40 +08:00 | 检查 0.4.1 源码及 09-30 提交：时间确定性、分镜/布局自检，移除固定配乐菜单与每30秒镜头数量，避免成片被模板锚定。其零素材限制仅属于纯代码模式，本技能不继承。 |

[awesome-opus5-5-videos](https://github.com/yihui-dev/awesome-opus5-5-videos) README 最新更新标 09-29；属于此前背景线索，不假装符合用户指定的新资料窗口。未使用它证明新模型发布日期或跨模型优劣。

## 验证范围

0.2 的新增能力是代表画面、混合素材与逐帧证据流程。独立短测试片与检查记录保存在本次项目的 `work/skill-refinement-20261007/`，具体通过项以实际报告为准。下载影像的原始发布日期可以早于研究时间窗；研究文章的时间筛选不限制制作素材的年代。未完成 Claude 与 GPT 的同题、同素材、同预算比较；不能据此保证复现全部 Claude 案例或宣称模型能力等同。
