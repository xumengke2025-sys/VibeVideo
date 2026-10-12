# 制作检查点

日期：2026-10-08（Asia/Shanghai）。制作与交付文件验证已完成，渲染 session 89842 已正常退出；没有渲染进程待继续。成片、源码包、说明与审片证据均已就绪。不要重新渲染或重复已经完成的审片。

## 目标

原创黑洞引力透镜科普短片「绕过黑暗」，32 秒、16:9、1920×1080、30fps。交付 MP4、可编辑源码和真实审片证据。用户要求精细画面、连续光路和空间运镜；已取消的榫卯项目不能继续。

## 已完成

- 成片：out/around-the-dark.mp4，28,255,324 字节，H.264/AAC，960 帧。
- 源码：film.mjs、lens.frag、render.mjs、index.html、make_soundtrack.py、verify_orbits.py、package.json；说明：README.md、production.md。
- 原创 32 秒合成电子氛围音轨 soundtrack.wav，无旁白。
- 两轮关键动作研究与修正已完成。修复盘面接缝、光点出画、观察标签挤占、上拱像标注和叠化双重轮廓。
- 完整解码通过；音频检查覆盖 32 秒，峰值 −4.33 dBFS、RMS −19.26 dBFS；浏览器错误和资源加载失败均为空。
- 已实际查看最终 24 帧接触表、开场转场 114–172 帧的两张连续帧表、成像重建 408–474 帧的三张连续帧表，以及 0、11.5、23、31.966 秒的四张 1920×1080 图片。覆盖范围内没有未解决的重大视觉缺陷。
- 独立 RK4 轨道检查通过；NASA 两篇事实依据与示意边界已写入 production.md。
- review-evidence.json 已记录最终 SHA256、实际审阅范围、修复问题与限制。

## 验证限制

没有全片实时播放或实际听音；机器音量检查不能替代听音。连续帧表宽度为 960px，不能声称全片每帧都做了原尺寸检查。科学模型为非旋转黑洞示意，颜色与运动经过美术化，未验证 GPU 积分误差或完整辐射转移。

## 交付验证与下一步

- 最终视频 SHA256：484f0ada1a27ff139763e074b5b9cc7de6bbf790af6288bcdd48bb1b005d03e0，与两个最终 frame-audit.json 一致。
- 已生成 out/delivery-inventory.json；所有证据引用与源码文件存在。
- 已生成 out/around-the-dark-source.zip，13,216,849 字节、27 个条目；ZIP CRC 与打包文件哈希全部通过。源码包含声音、说明、报告、实际查看的最终接触表和四张原尺寸图片，排除成片、旧样片、大量单帧及 node_modules。
- 制作要求已完成；登记 goal complete 并交付成片与源码。后续只按用户反馈修改，不继续循环审查。

## 运行入口

本机 Node：C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe。
Python：C:/Users/67236/AppData/Local/Programs/Python/Python312/python.exe。
在项目目录执行 node render.mjs 重渲，node render.mjs --serve 启动预览，端口 8926。其余依赖与迁移说明见 README.md。
