# Waterloo · 纸雕灯箱 v4

60秒、1080×1920、24fps，无文字/旁白/歌词。delivery_mode: user_feedback，零子代理。

当前成片：out/final-v4d/video.mp4。对应源码入口index-v4.html、main-v4.js、timeline-v4.js；旧index.html/build3e保留。

## 重建
在项目根目录执行：

```powershell
node work/waterloo-20261012/studio/render.mjs --entry=index-v4.html --audio=audio-v4.wav --mode=final --width=1080 --version=your-new-version
```

可预览index-v4.html，控件只在工作台显示，成片不含文字。音频需重建时使用现有Python运行时执行score-v4.py；GeneralUser GS许可及音源沿用audio-assets中的原文件。

## 实际采用
内置生图生成同源纸雕近/远景，Canvas2D处理2.5D分层、整形骑兵短程推进、摄影、剪影队列、三次短闪与纸烟。不是多人AI视频、全三维战场或逐腿奔跑。铜版感仅在纸面纹理与局部刻线中体现。

母图/前层/背景的原始提示词见assets-v4/prompts.json；其他规格及尚未返回的结尾候选见prompt-specs-v4.md；五个已使用素材及alpha/锚点/来源见asset-manifest-v4.json。历史地形与布阵为艺术演绎。

正式样段20–28秒完成后实际看过连续状态、开火附近状态和全尺寸图，并修正中景悬浮及平板烟幕。完整版本基本工程检查见out/final-v4d/evidence.json及ffprobe.json。乱序像素一致性见out/stills-v4d/checks.json及结尾更新检查。没有独立视听审核或完整听音；由用户反馈修改。
