# 检查点 — 《你的包裹，正在找路》

日期：2026-10-11 ｜ **delivery_mode: `user_feedback`**（用户选择①直接生成、由用户反馈修改）

## 交付物

| 项 | 值 |
|---|---|
| 成片 | `out/final-v1/video.mp4` |
| SHA256 | `3778ebbff300d4c964adb0f3a11835ebee6d62520ba208402cda70215016239f` |
| 规格 | 1080×1920（9:16）｜ 30fps ｜ 660 帧 ｜ 22.000s ｜ 12.9 MB ｜ H.264 + AAC 立体声 48kHz |
| 源码 | `index.html`、`js/timeline.js`、`js/main.js`、`audio.mjs`、`render.mjs` |
| 可编辑入口 | `node render.mjs --mode=preview`（540×960）／`node server.mjs` 交互预览 |
| 预览 | 需先运行 `node audio.mjs` 生成 `audio/mix.wav`，再 `node server.mjs` 开 http://127.0.0.1:4318 |

题材：环形交叉带分拣机；跟随一个包裹从扫码到被横向抛出落入"杭州"格口的全过程。
风格：2.5D 等距（正交相机、视线 (1,1,1)），Canvas 合成叠加文字层。

## 已完成的检查（与实测结果）

**工程检查（全部通过）**
- 全片 660 帧完整解码，`decoded:true`，页面运行时 `errors:[]`（零 pageerror）
- ffprobe 核对：1080×1920、30fps、nb_frames=660、时长 22.000s、视频流 H.264、音频流 AAC 立体声 48000Hz
- 三块画布原生缓冲经 `window.__renderBuffers()` 校验，均为 1080×1920（非"假低清"）
- 反向 seek 一致性：静帧模式对 4 个时刻反向重取，SHA256 逐一对齐（`out/stills-v4/checks.json`）
- 源码哈希护栏：`js/main.js`+`js/timeline.js`+`render.mjs`+`three.module.js`+`audio/mix.wav` 签名绑定
- 渲染分阶段计时：浏览器启动 2710ms ／ 捕获 33646ms ／ 编码 19115ms（`out/final-v1/phase-timings.json`）

**声音（仅客观测量，不是听过）**
- 原创合成，无旁白、无外部素材：机械底噪 + 每 1.045s 过车脉冲 + 11.30–13.82s 带面电机升速 + 14.21s 脱离声 + 14.47s 落槽撞击 + 15 个其他小车抛投
- 单遍 loudnorm 实测：输出 −14.05 LUFS、真峰值 −2.34 dBTP（`audio/loudness-normalization.log`）
- 近景段落（3.5–16.5s）把其他小车的抛投声压到 0.30，避免与主角的抛出抢注意力

**画面（实际看过，覆盖范围如下）**
- 迭代 4 轮静帧，每轮 19 个时刻全部实际查看（`out/stills-v1..v4/`）
- 成片本身另抽 13 个时刻的帧实际查看（`qa/final-framecheck/`），重点核查三处风险窗口
- 具体确认：抛出三帧连续性（t=12.4 居中 → t=14.0 越过带面边缘 → t=14.4 落到斜槽上）方向一致、指向"杭州"格口

## 明确未完成的检查

- **未正常速度播放观看**。本 Agent 无法感知连续播放，节奏、运动连贯性、转场观感没有验证。
  静态帧覆盖不能证明节奏与运动观感通过。
- **未听音**。无音频输入通道，响度与静音检测不等于听过。音画同步（抛出与撞击声是否对得上）未经听感确认。
- 未做全帧覆盖（mode ① 不要求，本片按用户反馈推进）。

## 自查发现的待观察项（交给用户反馈）

1. 扫码门深色门架在 t≈7 的中景里偏重，可能压住主体
2. 3.2–4.3s 由全貌推到跟随的机位移动较快，动态观感未验证
3. 15 个格口去向标签在全貌镜头里密度较高
4. 小车在"上线点"重新装载包裹时，带面肋条的偏移量会归零，可能存在一次微小跳变（静态帧看不出）

## 与项目既有成片的一致性

`pix_fmt` 为 `yuvj420p,pc`（全范围标记）。经核对，本项目既有成片（污水 `final-cats-45s-v3`、`sand-journey`、`one-way-portrait`）全部相同，属既有流水线特性，非本片引入。

## 复用与来源

渲染链路继承自 `work/wastewater-isometric-20261011` 的 `render.mjs`/`server.mjs` 与 `vendor/three.module.js`（THREE r169，MIT，许可文件同目录）。场景代码、时间轴、声音为本片新写。

## 下一步

等用户观看反馈，按反馈做针对性修改。用户可随时把 `delivery_mode` 切到 `ai_review_once`。
