# Risky 风险视角 · 文字与动作修订版

80秒，1920×1080，60fps，H264/AAC。正式交付是同目录的Risky-黄铜机械-完整版.mp4。index.html仅是内部绘制入口。

此次修正铭牌纹理拉伸，精简机构文字与字幕，改进相机连续速度、案匣弧长运行及转向，保留同一案件的完整业务过程。沿用原配乐和机械拟音，无旁白；公司与过程为合成示例，没有运行Risky业务引擎。

源码入口scene.js，支持window.renderAt(seconds)乱序寻址。captions.srt保存字幕文本，修改画面字幕需同步编辑scene.js内captions数组。素材随assets与vendor保留，继承原来源许可。

在本目录用PowerShell重渲：

```powershell
& 'D:/docker/node.exe' './render.cjs' --mode=stills --times=4.4,26.8,44,68.8
& 'D:/docker/node.exe' './render.cjs' --mode=render --fps=60 --duration=80 --output=risky-full-silent.mp4
& 'C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' './finalize.py'
```

工具路径在脚本顶部，可按实际安装修改。motion-audit.cjs是相机曲线数值诊断，不代表视听审片通过。实际检查范围见qa/independent-review；正常速度观看和实际听音能力受限时如实标明。
