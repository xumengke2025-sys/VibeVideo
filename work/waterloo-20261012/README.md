# 滑铁卢 · 剪纸灯箱

约60秒，1080×1920，24fps，器乐和战场拟音，无文字和语音。delivery_mode: user_feedback。

本次按用户反馈重组已有工程：取消风景重复贴图与人物写实明暗，使用共同纸色、纸纤维、曲线地形层和暖背光；减少近景人数，远列用剪影；骑兵受阻后停顿并后退，卫队退却分时传播。原始生图和build2源码均保留。

## 文件
- PLAN.md：修订计划v3，动态调整与史实来源。
- studio/main.js：场景、分层、镜头、绝对时间动画和预览控制。
- studio/art.js：素材轮廓重着色、关节与裁纸队列。
- studio/timeline.js：60秒镜头和共用音效事件。
- studio/assets/manifest.json：原始生成图、alpha裁切与来源映射。
- studio/score.py：原创采样管弦和拟音制作，audio.wav为混音。
- studio/out/sample-build3d/video.mp4：18–26秒正式分辨率动作样段，已完成解码检查。
- studio/out/final-build3e/video.mp4：完整修订版；evidence.json、ffprobe.json为工程检查记录。
- studio/history/build2：修改前源码；PLAN-v2-production.md为旧计划备份。

## 本地预览与导出
在项目根目录运行：
```powershell
node work/waterloo-20261012/studio/server.mjs
```
浏览器访问 http://127.0.0.1:8802/ 。入口已修复为重定向真实页面。控件只用于预览，不进入成片。

```powershell
node work/waterloo-20261012/studio/render.mjs --mode=final --width=1080 --version=new-version
```
每次修改源码或音频后更换version，防止复用旧帧。导出需要本机Three.js依赖、sand-journey工程的playwright-core、Chrome及项目Remotion所带FFmpeg，路径写在render.mjs和index.html中；不是独立免安装包。

## 范围与许可
背景、角色动作与摄影由代码制作，没有使用AI生成多人运动视频。AI原图仅复用裁切alpha轮廓；纸色、旗面、枪刺刀和远列由代码统一。画面是戏剧化纸舞台，不是完整战场复原；旗手为复合角色。

Lemo paper.js/lib.js源码固定commit e3cb16f63768c68693ff0e15171d6e755457cc32，MIT许可见studio/LICENSE-Lemo-MIT.txt。GeneralUser GS音源许可和来源保存在studio/audio-assets，允许私用/商用音乐制作。未使用参考片音乐。

本次直接生成，未进行独立审片。制作时查看了代表静帧和冲突窗口的选定连续状态，不能写成完整逐帧审核或完整听音验收。
