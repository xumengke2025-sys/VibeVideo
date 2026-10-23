# 宝宝与妈妈 · 跨时代同动作

二维卡通竖屏短片：1080×1920，24fps，41.25秒，35种时代画风，有意无声。
妈妈在右侧重复端杯喝一口，宝宝在左下方重复捡起星星。角色保持小比例，跨时代共享动作相位。

## 编辑

- `film/eras.js`：时代名称、年份、画风、配色与切换时刻。
- `film/film.js`：分层二维路径、服饰、背景、二骨IK、杯子与玩具动作、转场。
- `film/index.html`：预览入口。单击画面播放/暂停；浏览器控制台可调用 `renderAt(seconds)` 精确寻址。
- `render.mjs`：逐帧渲染、H.264编码与机械检查。
- `brief.json`：用户约束和制作参数；`CHECKPOINT.md`：进度和剩余工作。

## 重建

需 Node.js、现有 `@remotion/renderer` 与配套 FFmpeg。此工程使用本机 `D:/ai项目/ai动画/node_modules`，跨机器时修改 `render.mjs` 第8、10行的依赖与FFmpeg路径。

```powershell
node render.mjs stills
node render.mjs sample
node render.mjs check
node render.mjs full
node validate.mjs
```

正式输出为 `out/mother-baby-35-eras-portrait-v1.mp4`。`stills`输出35个时代代表帧；`sample`输出6.4秒动作样段；`check`检查全部990帧的锚点、越界与乱序寻址状态。

`validate.mjs`还核对990帧手臂可达距离、喝杯阶段杯口接嘴，以及乱序和新浏览器进程的像素一致性。已验证运行时：Node.js 24.15.0、Remotion renderer 4.0.506。所有动作由绝对时间解析计算，不依赖导出速度。

参考研究和许可见 `research/REFERENCE-TRANSFER.md`、`THIRD_PARTY_NOTICES.md`、`REFERENCE-LICENSE.txt`。AI审核证据位于 `qa/`，以具体成片哈希绑定；仅工程检查不等于视觉审核通过。
