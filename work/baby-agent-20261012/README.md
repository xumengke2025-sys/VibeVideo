# 代号：小小读者

60秒，1080×1920竖屏，24fps。用户已认可的宝宝五官素材搭配原创剪纸身体；移动使用手掌、膝盖交替撑地的爬行，翻书、抱小鸭时坐姿。四肢肤色从已认可脸部素材取样统一为 `#f8c28b`。独立审核方式与当前覆盖见 `qa/`，交付版本见 `CHECKPOINT.md`。

## 绘制与预览入口

- `film.mjs`：七场绘制、宝宝坐姿/爬行rig、绝对时间运动、24fps摄影与12fps纸偶表演。
- `index.html`：播放与时间轴预览；需要通过本地HTTP服务加载。
- `brief.json` / `plan.json` / `events.json`：创作、镜头与音乐/拟音事件。
- `assets/head-atlas.png`：三个定稿表情；运行时按透明边界裁剪。
- `make_audio.py`：原创合成爵士配乐、翻页/点触/小鸭拟音，无旁白、无外部录音样本。
- `render.mjs`：逐帧JPEG到H.264/AAC MP4，工程检查与SHA256证据。新版本改源码后使用新版本号。

在工程目录执行：

```powershell
node server.mjs 8768
# 浏览器打开 http://127.0.0.1:8768
node render.mjs --mode=final --version=自选新版本号
```

当前渲染脚本使用本机Chrome、相邻项目的playwright-core及Remotion随包FFmpeg；路径在脚本开头。更换电脑时调整依赖路径。预演 `--mode=preview` 使用真实540×960缓冲、12fps；正式导出1080×1920、24fps。

## 来源与许可

风格参考：[lemomo-ai/lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar)，固定commit `e3cb16f63768c68693ff0e15171d6e755457cc32`。实际研究 `styles/spy-titles/demo/paper.js`、`story.js`、`film.js` 及 `chars.js` 相关片段；采用固定种子剪边、纸纹、按拍点的绝对时间、12fps纸偶与连续摄影、停时、圆形匹配及文字世界机制。原许可在 `assets/LICENSE-lemo.txt`。本片为原创剧情与布局，没有声称与原作逐像素相同。

宝宝素材依据用户提供的视频与已认可设定，通过内置imagegen生成，使用范围为本家庭短片。配乐/拟音由本工程合成；没有复用上游音乐、地图或字体文件。中文使用Windows系统Microsoft YaHei，英文使用系统Arial Black/Georgia，字体文件未随工程分发。

同页面乱序渲染已经检查。新页面存在少量Canvas边缘取整差异（每通道最大2），记录在输出 `checks.json`；不能称跨页面逐像素完全一致。
