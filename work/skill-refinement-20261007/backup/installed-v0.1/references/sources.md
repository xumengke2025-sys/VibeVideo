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

## 当前验证范围

本技能是新整合的 0.1 版本；复用成熟工具和已存在的创作方法。代码样片验证的是本地帧渲染、解析三维投影、空间到字形变化和证据提取。没有完成与 Opus 同提示词、同预算的对等评测，也不将新技能称为经过大量项目验证的成熟产品。
