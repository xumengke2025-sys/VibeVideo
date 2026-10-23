# 夜鹭的一天 · 彩皮影小戏

成片为36秒、1080×1920、24fps竖屏动画，带真实戏曲打击乐、夜鹭录音与原创动作音效。打开包内 `夜鹭的一天.mp4` 即可播放。

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
- `film/frame-rig-864.json`：864帧的夜鹭关节状态、嘴鱼锚点及鱼归属。坐标基于1080×1920舞台，生成元数据使用270×480低清缓冲，不影响坐标数值。
- `film/audio.mjs`、`audio.wav`、`sound-events.json`：采样混音与事件表，无旁白；素材许可见film/audio-assets/ATTRIBUTION.md。
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

修改后使用新的 `--version` 名称，避免误用旧帧缓存。默认完整输出36秒、1080×1920、24fps，存入 `film/out/final-my-edit/`。静帧可使用 `--mode=stills --version=my-edit --times=12,18,30`。音轨修改后执行 `node film/audio.mjs` 再渲染。

## 当前交付方式

用户已改为 `user_feedback`：直接修改并交付，不再安排第二次审片。此次去掉解释性字幕，统一角色跨镜头的位置、姿态与步态时间线，企鹅、鱼桶和场景渐次交接；仅保留动物园与企鹅的场内标牌。

`verification/` 保存导出参数、文件哈希与完整解码结果。当前版本为 `soundstage-v10`；`film/frame-rig-864.json` 与此版本相对应。工程包不包含大量中间帧。

上一轮审核及旧版本保留在原工作区，不能当作本版审核。源码、透明素材、逐帧关节数据、音轨与当前成片均在包内。

当前优化：上半部增加雕刻垂柳、淡远山、云纹与渐变日月；保持连续动作和无解释字幕。使用film/timeline.js的分段时间映射：入园和返家加快，取鱼与喂食保留动作停顿。结尾约4秒大夜鹭和两只幼鸟用同一组节拍张嘴、伸缩颈与轻摆皮件，配真实夜鹭短叫的三组呼应，幼鸟轻度升调，伴奏在结尾减弱。

本版只换声音，H.264画面流与v9逐字节一致。film/audio-stems/提供打击乐、鸟声与环境动作三个分轨。night-heron声音署名Sharad Apte；戏曲采样署名ajaysm、Mi Tian、Ying Wan。音轨及同步改编影片按CC BY-SA 4.0交付，详情见film/audio-assets/ATTRIBUTION.md。未实际听音，按用户反馈继续修改。
