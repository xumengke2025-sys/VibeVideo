# 风起，群鸟散

红隼尝试捕猎珠颈斑鸠群的30秒皮影片。交付方式为 `user_feedback`，1080×1920、24fps；无旁白、无解释字幕，配锣鼓、风声与扑翼拟音。故事为伏枝观察、俯冲、惊飞、林间追击、扑空归枝。追捕成年斑鸠属于本片戏剧设定，不作为典型红隼捕食行为的纪录。

## 文件

- 成片：`film/out/final-v1/video.mp4`。
- 渲染参数、哈希、完整解码结果：同目录 `config.json`、`evidence.json`、`ffprobe.json`。
- 创意与镜头：`production-brief.md`。
- 三张生成素材：`assets/`；生成设计摘要见 `assets/GENERATION-NOTES.md`。
- 绘制入口：`film/film.js`；角色装配：`film/rig.js`；景片与透射：`film/art.js`。
- 鸟群规则：`film/simulation.js`；路径和时序：`film/math.js`；预计算：`film/precompute.mjs`。
- 音轨编排：`film/audio.mjs`、`film/sound-events.json`；来源和许可：`film/audio-assets/ATTRIBUTION.md`。

## 运行和修改

在 `film` 目录运行 `npm install` 安装playwright-core，已有依赖可跳过。预览命令 `node server.mjs`，打开 http://127.0.0.1:8803/ 。预览页面支持播放及定位时间，导出通过 `window.renderAt(seconds)` 精确寻址。

修改鸟群规则或路径后执行 `node precompute.mjs`；修改声音后执行 `node audio.mjs`。正式导出：`node render.mjs --mode=final --version=v2`。每次内容修改使用新版本号，旧成片保留。渲染脚本依赖Chrome、FFmpeg和ffprobe，可用 `CHROME_PATH`、`FFMPEG_PATH`、`FFPROBE_PATH`指定本机路径；默认路径为当前工作站配置。相机、关节动画及绘制都按绝对时间求值；Boids使用1/120秒固定步长，渲染插值读取缓存。

## 验证范围

鸟群包含14个独立ID，采用邻域分离、对齐、向心，加捕食者逃逸、预测避障与较弱的剧情目标。`film/simulation-checks.json`确认重复模拟和缓存乱序读取一致，关闭威胁会改变轨迹；这些参数是动画制作设定，不是珠颈斑鸠实测数据。

已查看全片代表帧和10.8–16.3秒每0.5秒追击接触表，正式品质6秒样段已解码。修复Chrome加速2D画布差异后，4个重复寻址时刻的PNG哈希一致，见 `film/out/stills-seekdiag3/checks.json`。正式片完成后记录画幅、帧数、时长、音轨和完整解码。此交付方式不含独立视听审核；未声称完整听音或逐帧审片。

## 参考与许可

继承夜鹭v10的透明PNG分件、刚性关节、连续世界、WebGL透射和事件音效流程，夜鹭历史工程保持独立。皮影风格源码来自 lemomo-ai/lemo-opuscar 的shadow-puppet，复制部分的MIT许可在 `film/vendor/` 保存。锣鼓采样使用CC BY 4.0，详见署名文件；风声、梆子和扑翼为原创合成，不使用夜鹭叫声，也不标作野生鸟类实录。

参考片54.4秒，实际参考阅读为0、6、12、18、24、30、36、42、50秒抽帧；没有宣称完整播放或听音。摄影关系参考particle-beach的主体驱动相机实现。原理资料：[Craig Reynolds Boids](https://red3d.com/cwr/boids/)；[红隼行为资料](https://animaldiversity.org/accounts/Falco_tinnunculus/)。
