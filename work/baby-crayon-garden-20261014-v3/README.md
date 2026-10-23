# 宝宝和太阳的晚安 · v3

delivery_mode: user_feedback。沿用用户授权，直接生成，由用户反馈修改。40秒、1080×1920、24fps，无字幕、文字或旁白，有原创合成音乐及非语言拟音。v1/v2保留在原目录。

## 本次修改

脸部由内置image_gen参照宝宝照片与原片蜡笔画风生成，简化为粗蜡笔平涂和少量五官线条；正面、右转、右侧面与夜间哈欠共用身份。素材保存在assets，完整提示词与保存路径见assets/prompts.json。身体采用代码固定骨长，坐姿左右肩分开，手掌随前臂旋转，袖口接各自肩。短连体衣和白袜参照第一张照片。只在夜间哈欠张嘴；沿用v2的40秒节奏与音乐。

## 工程入口

- main.js：可寻址window.render(seconds)，混合图片与代码渲染。
- baby-rig.js：头部素材、短胖身体、固定骨长两段关节、距离相位爬行。
- baby.js：保留旧宝宝实现供追溯，当前只使用其猫角色。
- pacing.js：共享单调连续速度的故事/播放时钟，镜头与声音沿用同一映射。
- timeline.js：世界路径、摄影和故事事件（内部故事时间仍0—60）。
- world.js、book.js、engine：沿用蜡笔世界、蓝水彩显星、同画面回右页和分条纸弧翻页。
- score.py：40秒原创音乐和拟音。
- render.mjs、verify.py：完整导出、文件/解码/画幅/时长/音轨检查。
- SOURCE.md、engine/LICENSE：参考源码和许可；REVISION-v3.md：当前修订依据；REVISION.md保留v2历史依据。

## 重建

在本目录执行：

    & 'C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' score.py
    & 'D:/docker/node.exe' render-safe.mjs
    & 'C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' verify.py

本机Playwright、Chrome headless、FFmpeg路径集中在render.mjs；换电脑应更新路径。头部素材已经本地保存，重建不需要重新生图，渲染时阻断外网。

本次整段渲染遇到浏览器Target crashed，故采用render-safe.mjs：四段10秒顺序渲染，每120帧重载页面；视频按绝对时间连续拼接，音乐从原始score.wav一次编码。保留各段render.json，最终verify.py记录整片哈希与检查。

代表帧：render.mjs --stills --times=0,4,11.5,18.8,28.5,32.2,37.5

样段：render.mjs --range=2:7 --name=crawl-transition-v3.mp4

静态HTTP服务器打开index.html，控制台window.play()播放；window.render(seconds)可精确寻址。

## 实际检查范围

实际查看正式竖屏坐姿、爬行、夜间哈欠代表帧，以及2—6.75秒20张连续时间采样。坐姿效果帧已展示，沿用连续执行授权。完整成片按user_feedback完成基本工程检查后交付；不声称独立审片、全帧审核或完整音轨听审。相似度、自然程度和可爱感由用户反馈判断。

参考①原片和固定源码研究见../baby-reference-selection-20261013/source-study.md；本次保留原有场景/纸页机制，重点更换角色实现与节奏。
