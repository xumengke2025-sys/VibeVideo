# 宝宝和太阳的晚安 · 第一版

delivery_mode: user_feedback。2026-10-13用户授权先生成视频，再由用户审核。无字幕、画内文字或旁白；原创合成配乐和材质拟音。60秒、1080×1920、24fps。

## 文件

- `out/宝宝和太阳的晚安-v1.mp4`：完整成片。
- `main.js`：WebGL合成与可寻址入口；`window.render(seconds)`。
- `timeline.js`：宝宝世界路径、摄影轨迹和事件。
- `baby.js`：按照片重新设计的宝宝及新增橘猫。
- `world.js`：家、院子、院门、院外花园、太阳及夜色。
- `book.js`：同画面回右页和分条纸弧翻页。
- `score.py`：原创合成配乐与非语言拟音。
- `SOURCE.md`、`engine/LICENSE`：源码迁移范围和许可。
- `PLAN.md`、`CHECKPOINT.md`：计划与实际进度。
- `out/verification.json`：输出哈希及基本工程检查结果。

## 重建

在本目录运行：

```powershell
& 'C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' score.py
node render.mjs
```

渲染脚本使用本机已有Playwright、Chrome headless及FFmpeg，路径集中在 `render.mjs`；跨电脑时修改这三个路径。不调用生图/视频生成服务，导出时阻断外网。

代表帧：`node render.mjs --stills --times=0,8.8,20.8,30.2,36.9,43.5,49.5,55,57.8,58.5,59.5`。

局部样段：`node render.mjs --range=17:25 --name=跨院门关键样段.mp4`。

通过任意本地HTTP静态服务器打开 `index.html`，控制台运行 `window.play()` 可预览；导出独立调用绝对时间，不依赖播放时钟。

## 制作检查范围

已实际查看角色、跨门、摸花、日落、刷痕夜色、书页接管和翻页的代表帧，以及17–24.5秒16个连续取样；修正跨门裁切、太阳过早遮挡及月牙轮廓。这里记录制作判断，未进行独立审片、全帧审核或完整音轨听审。最终按用户选择，以基本工程检查后交付的第一版为准，由用户反馈修改。

人物仍是蜡笔绘本改编形象，院门连接位置为动画设计。原片的源码研究和取样观察见 `../baby-reference-selection-20261013/source-study.md`。研究与本片实际输出分开记录。
