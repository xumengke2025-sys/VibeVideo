# 夜鹭的一天 · 彩皮影小戏

成片为50秒、1080×1920、24fps竖屏动画，带原创合成音乐与动作音效。打开包内 `夜鹭的一天.mp4` 即可播放。

故事包含晨起、进动物园、直立缩颈模仿企鹅、停步翻面张望、探桶夹鱼、携鱼返家、喂两只幼鸟。夜鹭伪装时仍保留黑帽、红眼、长嘴和后颈白羽；体量接近企鹅，后景有镂空假山。

## 编辑与预览

需要Node.js 20或更新版本，以及支持WebGL的Chrome。进入解压目录执行：

```powershell
node film/server.mjs
```

浏览器打开 `http://127.0.0.1:8796/`。可播放、暂停和拖动时间线；这个关节预览播放器仅播放画面。带声成片使用包内MP4。

- `film/film.js`：时间线、刚性皮件裁切、两段颈腿IK、下颌、脚步和翻面。
- `film/art.js`：树、动物园假山、地条、字幕牌、舞台框及灯光。
- `film/vendor/`：参考项目的透射、刻皮与景片模块，附原MIT许可和来源说明。
- `assets/`：10张高清透明PNG。正式视频复用同一夜鹭皮件，早期姿态图集供素材参考。
- `film/frame-rig-1200.json`：1200帧的夜鹭关节状态、嘴鱼锚点及鱼归属。坐标基于1080×1920舞台，生成元数据使用270×480低清缓冲，不影响坐标数值。
- `film/audio.mjs`、`audio.wav`、`sound-events.json`：原创合成音轨与事件表，无旁白。
- `film/production-brief.md`：实际镜头、风格实现与参考阅读范围。

动作由绝对帧时间计算。翻面使用同一皮件绕竖轴的余弦侧缘投影，参考源码的 `mir` 本身是幕后镜像。没有声称直接照搬现成的物理翻面动画。

## 重新输出

安装渲染依赖，并提供FFmpeg、ffprobe和Chrome路径：

```powershell
npm install
$env:FFMPEG_PATH = '你的ffmpeg.exe绝对路径'
$env:FFPROBE_PATH = '你的ffprobe.exe绝对路径'
$env:CHROME_PATH = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
node film/render.mjs --mode=final --version=my-edit
```

修改后使用新的 `--version` 名称，避免误用旧帧缓存。默认完整输出50秒、1080×1920、24fps，存入 `film/out/final-my-edit/`。静帧可使用 `--mode=stills --version=my-edit --times=18,28.3334,43.6`。音轨修改后执行 `node film/audio.mjs` 再渲染。

## 验证与审核范围

`verification/` 保存实际成片的文件哈希、媒体参数与完整解码结果。`review/` 保存本轮审片记录，证据大图保留在原项目qa目录；交付包不携带数千张中间帧。

用户选择AI审核一轮。实际画面覆盖及修复以最终报告为准。当前工具无法让模型感知正常速度播放或听音，不能据此声称完整视听审核通过。音频编码、完整解码和峰值等工程检查不代替听感。

工程入口与片中画面一致；包内 `manifest.json` 保存交付文件哈希。原始计划及历史版本保留在工作区。
