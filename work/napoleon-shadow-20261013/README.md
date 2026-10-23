# 《一顶皇冠之前》

64秒，1080×1920竖屏，24fps；讲1796—1804年拿破仑从将军到皇帝的阶段。delivery_mode: user_feedback，由用户反馈修改；零子代理。

当前成片：`film/out/final-v2/video.mp4`；原版保留在`film/out/final-v1/video.mp4`。

v2针对用户反馈的人物变形重建四景骨架：修正重复手臂、错误裁切、肩颈拼接和分件叠层，大小腿与双臂保持固定骨长；手与旗、剑、皇冠绑定同一可达端点。动作改为准备、发力、停留与回收。白马采用新透明分件图集，从站立抬前蹄再落地，后蹄固定，骑手随马鞍变化；调整竖屏构图保留完整后腿。加冕两臂区分前后层，保护约瑟芬脸部轮廓。

四幅原型依次为格罗《阿尔科莱桥上的波拿巴》《波拿巴探访雅法疫病患者》、大卫《跨越阿尔卑斯山》《拿破仑加冕礼》。中间补入1799回国、雾月政变与第一执政。事件年份与作品年份分别标注；翻山采用白马红披风的构图，旁白说明现实骑骡；英雄化绘画不作为现场实录。

人物和景片使用内置image_gen生成透明PNG；源码把头、身体、手臂、旗帜、白马和皇冠组装为关节皮影。沿用夜鹭的透射背光、乘色叠层、景片与锣鼓事件流程。160个持续ID的Boids皮片采用邻域分离/对齐/聚合，在转场时聚散；红幕覆盖时切换场景，再交给下一角色动作。Boids固定1/60秒模拟、12fps缓存，24fps导出插值。

## 编辑与重建

在`film`目录执行（本机Node为`D:\docker\node.exe`）：

```powershell
node server.mjs
# 浏览 http://127.0.0.1:8803/，可以播放、暂停和拖动时间
node precompute.mjs
node audio.mjs
node render.mjs --mode=stills --version=edited --times=7,24,38,56,60.8
node render.mjs --mode=final --version=v2
```

使用已安装的playwright-core、Chrome及Remotion随包的FFmpeg/ffprobe。`render.mjs`支持`CHROME_PATH`、`FFMPEG_PATH`和`FFPROBE_PATH`环境变量。编辑后用新版本名，避免复用旧帧。

- `film/film.js`：镜头编排、字幕、作品标注与可寻址时间接口。
- `film/rig-v2.js`：当前人物/马骨架、两骨IK、脚底和道具接触；`rig.js`、`film-v1.js`保留旧版实现。
- `film/art.js`、`film/math.js`：景片、幕片、摄影与时间曲线。
- `film/simulation.js`：真实邻域Boids规则；缓存和验证记录同目录。
- `film/narration.json`：中文稿、声音窗口和实际合成时长；本机Microsoft Huihui Desktop合成。`make_narration.ps1`重建旁白后再运行`audio.mjs`。
- `film/audio.mjs`、`film/sound-events.json`：64秒锣鼓、风、皮片和空间声场。移除抬蹄停留期间的连续木板节奏，准备与落地对应35.15/45.85秒木板声；v1音轨另行保留。
- `assets`：正式透明图集、保留的旧版和生成提示词。翻山正式素材为`alps-v2.png`，王室百合花已换成几何金点。

## 检查与来源

实际检查过代表静帧的构图、关节裁切及皇冠接触；查看47—53.75秒每0.25秒画面序列，确认幕片覆盖换景。相同时刻重复乱序取帧哈希一致；Boids重复模拟一致，关闭邻域规则会改变轨迹，状态有限。正式导出脚本保存`evidence.json`、`ffprobe.json`、源码签名、视频SHA256并做完整解码、画幅、帧数、时长和音轨检查。没有安排独立视听审核，不将音量分析或静帧查看写成完整听音。

v2机械检查：`node verify-rig.mjs`覆盖1536个时刻，骨长/手目标/接触/脚底误差均小于0.001px，结果在`film/out/motion-v2-verification/constraints.json`。这个检查不评价外观；实际渲染图在`stills-motion-v2-layout2`、`stills-motion-v2-crown`，10秒加冕样段在`sample-human-v2`。

原画及历史来源见`research/SOURCES.md`，研究摄影不进入成片。生图是原创皮影转译，不是原画扫描。上游皮影WebGL源码沿用MIT，见`film/vendor/LICENSE`。五项戏曲采样来自Ajay Srinivasamurthy/QMUL-BeijingOperaPercussion，CC BY 4.0；署名、演奏/录音及链接见`film/audio-assets/ATTRIBUTION.md`。采样已重新编排、改变音量/声像并加空间处理。
