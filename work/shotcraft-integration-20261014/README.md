# video-shotcraft镜头库与工作台接入

本机较早版本已完整备份，更新到固定上游 `13c74a707786872a18e3317e48c5c94011027620`（2026-10-13），并接入vibe-video0.16.0。详细制作入口见 [shotcraft-integration.md](../../skill/vibe-video/references/shotcraft-integration.md)，实际结果与限制见 [CHECKPOINT.md](CHECKPOINT.md) / [verification.json](verification.json)。

## 当前可以使用

- 124张镜头配方卡、150个Gallery变体：搜索卡片，取得准确源码与备选实现，迁移动作/摄影/声音机制；检索结果不代表全部动态质量通过。
- Motion Workbench：已有Remotion影片按共用时间表的manifest拆为镜头/字幕/音轨；提供schema的组件可以编辑内容、颜色、字号；可导出MP4和工程JSON。
- 横屏16:9与竖屏9:16：每次新片提供画幅选择，与交付方式一起询问，明确选择和续接项目不重复问。PageCamAdaptive读取实际composition尺寸，页面、主体与相机锚点分别布局。
- 原先效果图先行、直接生成由用户反馈或AI审核一轮流程继续有效。外部技能的三种模式、固定横屏、强制审片及推广要求没有成为本项目制作规则。

## 使用入口

在项目根目录执行检索：

```powershell
node skill/vibe-video/scripts/shotcraft_library.mjs search --category camera --limit 5
node skill/vibe-video/scripts/shotcraft_library.mjs card mask-wipe
```

当前工作台：[localhost:5198](http://localhost:5198/)，链接本次内部竖屏测试。重新启动或切换影片：

```powershell
node D:/Codex/skills/video-shotcraft/workbench/scripts/open.mjs <带src/workbench.ts的工程目录> --no-open
```

工作台仅监听127.0.0.1。大部分上游demo的内部内容仍由常量驱动；工作台能裁剪、变速、图层移动，内部文字等需提为props/schema再编辑。现有HTML/Canvas工程不自动拆解。上游demo固定横屏时按本片重排，不以改尺寸代替竖版设计。

## 验证与保留

两个90帧内部测试共享事件数据，分别左右与上下排列，覆盖平面/透视PageCam；浏览器修改后导出：

- [横屏MP4](verification/landscape-edited.mp4)，[像素对照](verification/landscape/comparison.json)。
- [竖屏MP4](verification/portrait-edited.mp4)，[像素对照](verification/portrait/comparison.json)。

每版6个采样帧均为精确0像素差；两版解码、尺寸、90帧、3秒视频和预期AAC测试音轨均通过。实际观察导出首帧，确认修改文本与竖版颜色/字号。没有做全库动态质量或实际听音/独立审核，不将内部技术样段作为正式创作样片。

`before/video-shotcraft`保存旧安装；`installation.json`保存上游和旧版文件指纹；`local-adapter`保存已验证的本机适配文件，覆盖固定源码后还需将demosrc建立为本库demos的junction，再生成索引。早期install-upstream/adapt-local脚本仅为实施记录，后者不包含后续全部修复，重建须以local-adapter为准。Apache-2.0和音频ATTRIBUTION分别保留，原源码checkout未改tracked文件。
