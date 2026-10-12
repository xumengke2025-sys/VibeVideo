# 冲完马桶后，水去了哪里？

当前版本：45秒等距2.5D科普，竖屏1080×1920、30fps。直接处理标题、原创音乐与合成音效，无旁白。新增家庭排水管道行程和7只拟人小猫。视频：out/final-cats-45s-v2/video.mp4。按用户要求暂停独立审片，新版未宣称视听验收通过。

## 本机运行
```
node server.mjs
```
打开 http://127.0.0.1:4318 ，按钮播放，时间滑块可直接寻址。
```
node audio.mjs
node render.mjs --mode=stills --version=自定义版本
node render.mjs --mode=preview --version=自定义版本
node render.mjs --mode=sample --version=自定义版本
node render.mjs --mode=final --version=自定义版本
```
预演540×960/15fps，样段为25—36秒，正式片45秒。历史75秒预演保留；修改源码后用新版本名。

## 编辑位置
- js/main.js：程序化建模、材质、设备动作、固定等距相机及字幕绘制。
- js/timeline.js：镜头分段、字幕、音效事件、时长及视频规格。
- audio.mjs：原创96BPM器乐与合成音效，输出audio/mix.wav。
- vendor/three.module.js：已包含本任务使用的Three.js，不从CDN加载。

渲染依赖本机Chrome、上级动画项目的FFmpeg，以及相邻sand-journey工程的playwright-core；具体绝对路径见render.mjs。迁移时修改这三个路径即可。中文使用系统Microsoft YaHei，字体不随工程分发。

## 证据
BRIEF.md记录事实边界、来源和审核条件；CREDITS.md记录素材许可。qa内审核报告必须与实际视频哈希对应；未完成的听音不得标为通过。CHECKPOINT.md记录当前进度与两轮修复预算。

画面是解释性示意：时空压缩、流向标记、可见剖面与微观窗口均非真实流体、生化或工程设计模拟。不同污水厂的处理流程并不相同。
