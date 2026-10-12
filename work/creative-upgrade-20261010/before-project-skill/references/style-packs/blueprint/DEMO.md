# 原创蓝图样片

入口：[style-studio](../../../assets/style-studio/)。共享 Canvas 引擎中 `blueprintState(t)` 定义阀瓣、弹簧、剖切与相机状态；`blueprint(t)` 绘制。`clips/blueprint-proof.json` 是 10 秒能力片段；`clips/one-way.json` 是 32 秒原创《只向一个方向》。

故事：阀体出现 → 剖切揭示 → 外壳拆解展示部件关系 → 正向压差打开阀瓣 → 压差降低弹簧复位 → 回到主体与结论。对象位置保持连续，字幕是图纸说明，无旁白，声音为原创合成拟音。

边界：弹簧式轴向止回阀的简化二维原理，不是流体求解、工程尺寸或可制造图纸。示意粒子用于表达通路，流速没有物理含义。没有用 lemo-opuscar 样片源码，不宣称复现其画质。

## 重建

复制整个 `assets/style-studio` 到工作目录；安装其 package.json 依赖，使用已有 Python+numpy、Chrome 和支持 x264/AAC/loudnorm 的 FFmpeg。环境已有依赖时通过参数指定，勿改全局配置。

```text
node check.mjs
node render.mjs --clip=blueprint-proof --out=out/blueprint-proof --chrome=/path/to/chrome --ffmpeg=/path/to/ffmpeg
python score.py --clip=blueprint-proof --out=out/blueprint-proof --ffmpeg=/path/to/ffmpeg
node render.mjs --clip=one-way --out=out/one-way --chrome=/path/to/chrome --ffmpeg=/path/to/ffmpeg
python score.py --clip=one-way --out=out/one-way --ffmpeg=/path/to/ffmpeg
```

外部 Node 模块可加 `--playwright=/absolute/path/to/playwright-core/index.js`。先 `--stills-only` 看图；改源码或输入后用新输出目录，旧帧不会混入新版本。实际验证状态见 `capabilities.json`；完整证据留在制作项目。
