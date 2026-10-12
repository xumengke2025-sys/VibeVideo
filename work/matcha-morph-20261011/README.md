# 一片叶，变成一碗抹茶

当前阶段：35秒1080×1920竖屏正式片已导出并展示，审核未完成。独立角色尚未初始化、未返回全帧报告，实际听音与正常速度感知未完成。音乐与工序拟音为原创合成，无旁白。详见 `qa/full-r1/REVIEW.md`。

## 当前交付入口
- `out-full-r1/matcha-full.mp4`：35秒、1080×1920、30fps、1050帧，H.264/AAC立体声。完整音画解码通过，审核状态以 `qa/full-r1` 为准。
- `full.html`、`full-film.mjs`：整片播放器和可编辑绘制入口；`timeline-full.json` 为镜头/字幕与声音事件表。
- `render-full.mjs`、`audio-full.py`：正式片导出与原创声音重建。
- `out-preview-r3/matcha-steam-dry.mp4`：移动摄影版，540×960、30fps、5秒，有音乐和音效。原固定镜头r1保留。
- `representatives/leaf.png`、`mill.png`、`bowl.png`：1080×1920，实际绘制组件的形象代表帧。
- `index.html`：本地播放器，可拖动时间轴。启动服务后打开 http://127.0.0.1:4321/ 。
- `timeline.json`：35秒时间表，以及已实现5秒片段事件表。

## 重建（PowerShell，在本目录运行）
```powershell
& 'C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' audio-full.py
& 'C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe' render-full.mjs --out=out-full-new
& 'C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' audio.py
& 'C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe' render.mjs --stills
& 'C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe' render.mjs --out=out-preview-r4
& 'C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe' server.mjs
```
改动后选择新输出目录，避免复用过期帧。本机Chrome、应用Playwright、随Remotion的FFmpeg；不安装新依赖，不改全局配置。

## 小样审核状态
当前r3的独立报告已导入 `qa/performance-resume/aggregate/av-review.json`，实际覆盖150/150帧并补看7张原尺寸帧。当前媒体与证据哈希、覆盖声明通过一致性核验，见 `qa/performance-resume/aggregate/av-consistency.json`。未观察到blocker/major；2.433–3.633秒托盘右端短时裁切为minor，叶片完整，保留当前小样。正常速度观看与0–5秒实际听音未完成，完整视听结论为incomplete。可读报告见 `qa/performance-resume/reports/000000-000149-review.md`。2026-10-11已续接收尾并交付当前5秒小样；35秒整片按原阶段等待用户反馈后制作。

## 实现与边界
SVG轮廓240点，Canvas绘制并裁切生成纸纹；蒸汽带按82点中心线计算。气流、叶片、字幕及声音事件按绝对时间求值。`full.html` 中的 `renderAt(seconds)`、`stateAt(seconds)`覆盖整片0–35秒；旧小样入口覆盖0–5秒，保留历史版本。

图像不直接轮播；蒸汽→气流是视觉连接，茶叶本体持续存在。技术验证不代替审美和听音；独立审核结果在qa。事实与许可见SOURCES.md；内置imagegen提示词见assets/paper-prompt.txt。Windows字体仅供本机渲染，分享源码前应换成可分发字体。
