from pathlib import Path
import json
p=Path(__file__).parent
(p/'README.md').write_text("""# 宝宝和太阳的晚安 · v2

delivery_mode: user_feedback。沿用用户授权，直接生成，由用户反馈修改。40秒、1080×1920、24fps，无字幕、文字或旁白，有原创合成音乐及非语言拟音。v1保留在原目录。

## 本次修改

脸部由内置image_gen参照宝宝三张照片生成透明蜡笔素材；闭嘴、眨眼和结尾哈欠共用身份。素材保存在assets，提示词见assets/prompts.json。身体采用代码固定骨长，短连体衣和白袜参照第一张照片。只在夜间哈欠张嘴；节奏由60秒重新编排为40秒。

## 工程入口

- main.js：可寻址window.render(seconds)，混合图片与代码渲染。
- baby-rig.js：头部素材、短胖身体、固定骨长两段关节、距离相位爬行。
- baby.js：保留旧宝宝实现供追溯，当前只使用其猫角色。
- pacing.js：共享单调连续速度的故事/播放时钟，镜头与声音沿用同一映射。
- timeline.js：世界路径、摄影和故事事件（内部故事时间仍0—60）。
- world.js、book.js、engine：沿用蜡笔世界、蓝水彩显星、同画面回右页和分条纸弧翻页。
- score.py：40秒原创音乐和拟音。
- render.mjs、verify.py：完整导出、文件/解码/画幅/时长/音轨检查。
- SOURCE.md、engine/LICENSE：参考源码和许可；REVISION.md：修订依据。

## 重建

在本目录执行：

    & 'C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' score.py
    & 'D:/docker/node.exe' render.mjs
    & 'C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' verify.py

本机Playwright、Chrome headless、FFmpeg路径集中在render.mjs；换电脑应更新路径。头部素材已经本地保存，重建不需要重新生图，渲染时阻断外网。

代表帧：render.mjs --stills --times=0,4,11.5,18.8,28.5,32.2,37.5

样段：render.mjs --range=2:7 --name=crawl-transition-v2.mp4

静态HTTP服务器打开index.html，控制台window.play()播放；window.render(seconds)可精确寻址。

## 实际检查范围

实际查看两批角色/场景代表帧，以及2—6.75秒20张连续时间采样，确认新素材能接入身体和场景。样段后仅调整为连续速度的时间映射并重渲染代表帧，完整成片按user_feedback交付；不声称独立审片、全帧审核或完整音轨听审。骨长与时间单调性检查见out/mechanics.json。相似度、自然程度和可爱感最终由用户反馈判断。

参考①原片和固定源码研究见../baby-reference-selection-20261013/source-study.md；本次保留原有场景/纸页机制，重点更换角色实现与节奏。
""",encoding='utf-8')
(p/'CHECKPOINT.md').write_text("""# 宝宝绘本 v2 checkpoint

delivery_mode: user_feedback

目标：完成用户反馈修订，生成照片参照头部，修正四肢、张嘴和慢节奏；完整视频交用户审核。零子代理，v1保留。

完成：内置imagegen三张透明头部；固定骨长身体和距离相位爬行；40秒连续速度时间映射，音乐/拟音同步；角色/碰花/院门/哈欠/书页代表帧；2—6.75秒20个连续采样；2000个IK目标骨长检查及961帧时间单调性检查。

正在执行：1080×1920、24fps、960帧完整v2渲染。有效渲染进程不因更新进度终止。

下一步：输出文件、解码、画幅、时长、音轨基本检查，复制成品并展示。未进行独立审核或完整听审；用户判断相似度与审美。
""",encoding='utf-8')
(p/'out/mechanics.json').write_text(json.dumps({'ikTargets':2000,'maxBoneLengthError':1.4210854715202004e-14,'clockSamples':961,'minClockStep':0.032302584629164244,'storyStart':0,'storyEnd':60,'flowerPresentationTime':18.8,'yawnPresentationTime':32.02420917119525,'assetAlpha':'All three PNGs are RGBA with alpha range 0..255','productionSample':'2..6.75 s, 20 frames viewed; before final continuous-speed timing adjustment'},ensure_ascii=False,indent=2),encoding='utf-8')
j=json.loads((p/'assets/prompts.json').read_text(encoding='utf-8'))
j['blink']="Edit target is the supplied transparent wax-crayon baby head. Change ONLY the eyelids into a relaxed full blink: both eyes gently closed, curved thin eyelid lines. Keep exact same baby identity, head silhouette, fuzzy hair, ears, nose, CLOSED small smile, color, grain, orientation, position and square canvas. No body, text or props. Maintain actual transparent background."
j['yawn']="Edit target is supplied transparent crayon baby head. Change ONLY expression for one sleepy yawn at story ending: eyes gently closed, small mouth opening vertically into a soft rounded oval with muted reddish interior, relaxed sleepy cheeks. Preserve exact same identity, silhouette, forehead, short fuzzy hair, ears, nose, head orientation, position, scale, coloring and wax-pencil grain. No body, props, text, exaggerated teeth or huge mouth. Actual transparent background, identical square canvas."
(p/'assets/prompts.json').write_text(json.dumps(j,ensure_ascii=False,indent=2),encoding='utf-8')
print('documentation and evidence updated')
