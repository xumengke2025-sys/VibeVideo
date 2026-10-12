# 淡墨远征：拿破仑在埃及

60秒 · 1080×1920 · 24fps · 水墨/书写叙事。无标题、字幕、旁白；古代刻痕仅为艺术纹理。

## 工程

- `timeline.js`：镜头、因果动作、转场和声音事件。
- `film.js`：可寻址 Canvas 组件与 WebGL 墨晕合成。人物/沙漠/舰船/石碑/学者/军队是独立图像组件；代码控制时序、位置、景别、显影、墨线、浓烟、火光、碎片和运镜。不是视频生成模型的输出。
- `assets/prompts*.json`：内置 image_gen 图像生成提示词，图像为艺术重构。
- `vendor/ink.js`、`lib.js`：Lemo / lemo-opuscar 的 MIT 笔触实现，保留许可。`film.js` 的墨晕前沿参考原 `comp.js` 的噪声距离/积墨边机制，扩展为RGB组件合成。源码阅读与原作观看区分记录。
- `score.py`：原创合成器乐、环境音、拟音，无真人旁白，无外部音乐采样。

## 本机运行

```powershell
cd 'D:/ai项目/ai动画/VibeVideo项目/work/napoleon-egypt-ink-20261009'
& 'D:/docker/node.exe' render.mjs --serve --port=8788
# 打开 http://127.0.0.1:8788/，播放/拖动时间轴。
& 'D:/docker/node.exe' render.mjs --out=out/rebuild
& 'C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 score.py
```

渲染器参数支持 `--range=25:38`、`--stills-only`、`--stills=27,28,29`、`--fps=24`、`--chrome=...`、`--playwright=...` 和 `--ffmpeg=...`。改变源码后使用新的输出目录，防止旧帧混入。依赖本机 Chrome、playwright-core、FFmpeg；声音脚本需要 numpy。

## 历史边界

本片把跨海、军队推进、海战受挫、学术记录、离去组织为诗意叙事。空间重叠是视觉表达，不表示海战发生在金字塔脚下。舰船、学者、军队、石碑为艺术重构；雕文不是碑文转录。金字塔战役在开罗附近，金字塔在远处。未使用狮身人面像鼻子被拿破仑轰毁的传说，未把石碑解读归功于拿破仑。

事实核查：1798年远征及7月21日金字塔战役、8月1日阿布基尔海战，1799年拿破仑离开埃及，1801年法军撤离，参见 [Fondation Napoléon](https://www.napoleon.org/en/history-of-the-two-empires/articles/the-campaign-in-egypt/) 和 [timeline](https://www.napoleon.org/en/history-of-the-two-empires/timelines/the-egyptian-campaign)。1799年法军发现罗塞塔石碑，参见 [British Museum](https://www.britishmuseum.org/collection/egypt/explore-rosetta-stone)。这些日期没有作为画面文字。

## 验证

首轮找到首次水波缓存引入的时间依赖，修复为固定几何+解析运动，并区分日/夜笔触缓存。第二轮顺序/乱序像素一致、新页面重建一致、0加载/脚本错误。实际静帧已查看，最终媒体核验及动态观察记录见 `REVIEW.md`。
