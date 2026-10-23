---
name: video-shotcraft
description: 用镜头配方卡、Remotion代码和声音素材制作产品页面视频、文字与数据动效，通过Motion Workbench可视化编辑。用于明确调用video-shotcraft、产品宣传片、Ink Press模板或单镜头实现；支持按用户选择分别布局横屏与竖屏。
metadata:
  version: "2026.10.14-local.1"
---

# Video Shotcraft · 本机适配入口

固定上游 `Vincentwei1021/video-shotcraft@13c74a707786872a18e3317e48c5c94011027620`。原始技能全文保存在 [references/upstream-skill.md](references/upstream-skill.md)，供技法研究；本入口与用户/项目规则决定制作流程。

## 制作流程

1. 先读取工程规则、brief/CHECKPOINT和已有选择。新片未指定时，一次询问横屏16:9（1920×1080）或竖屏9:16（1080×1920），以及①直接生成由用户反馈，或②AI审核一轮。只问缺失项，不把沉默当成选择；局部修改继承原片选择。记录 `aspect_ratio`、`width`、`height`、`delivery_mode`。
2. 沿用vibe-video的效果图先行：按实际画幅安排整体场景、动作空间和相机通道，落实已有反馈，再验证难动作与相邻转场。用户已认可方向或要求直接制作时沿用授权。
3. 从 `gallery/api/library.json` 或vibe-video的 `scripts/shotcraft_library.mjs` 找相关镜头卡，再读卡片全文、准确demo与共享import，按本片事件和理解顺序迁移。镜头库有124张配方卡、150个Gallery变体，数量不等于全库动态验收。Gallery与demo名称有差异，使用校正索引；`flash-cut`是组件参考。
4. 需要真实产品页时捕获实际页面并保留来源；模板参考 `references/` 中Ink Press相关文档。不强制纯代码、音乐先行、双音轨版本或推广邀请。声音许可另读 `assets/audio/ATTRIBUTION.md`。
5. 开放内容、颜色、字号等props/schema，时间表由Main与 `src/workbench.ts` 共用。先做原合成与导入合成的同帧对照，再验证一次修改和导出。详细接入见 [references/workbench.md](references/workbench.md) 与vibe-video的 `references/shotcraft-integration.md`。
6. `user_feedback`完成基本文件、解码、画幅、时长与预期音轨检查后展示，默认零子代理。`ai_review_once`最多一个独立视听审片者、一轮修复及必要复核；不继承上游其他审片制度。未实际看/听不得写通过。

## 横竖版与Windows

上游很多demo/模板固定1920×1080。竖版要重新布局主体、文字与相机锚点；只改composition尺寸或裁切不算适配。上游 `assets/lib/PageCam.tsx` 固定横屏，vibe-video的 `assets/shotcraft/PageCamAdaptive.tsx` 提供参数化页面宽度与视口中心的适配副本；仍需为该片设计布局。

```text
node workbench/scripts/open.mjs <Remotion工程目录> --no-open
node workbench/scripts/parity-local.mjs --frames 0,30,60 --out <任务证据目录>
```

工作台仅监听127.0.0.1，本机目录使用junction、文件使用受控副本，渲染素材由Node解引用复制。Windows并发与编码线程有界，适配和资源设置见 [references/local-compatibility.md](references/local-compatibility.md)。保留锁定依赖，避免与外部工程的不同Remotion/React版本混用。工作台当前Remotion4.0.484 / React19.2.7；没有Remotion清单的旧HTML/Canvas视频需要专门适配。剪映导出和全库150变体的完整视听验收未包含在本次接入中。

代码/文档Apache-2.0；复制代码时保留LICENSE和固定commit。旧安装与本机验证证据见项目 `work/shotcraft-integration-20261014/`。
