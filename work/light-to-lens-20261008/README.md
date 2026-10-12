# 从一条直线，到黑洞的亮弧

90 秒、1920×1080、30fps 的六段科普短片。先用二维光路解释直线传播、引力偏折和视位置，再用点质量薄透镜的逐点映射生成亮弧，最后进入三维吸积盘与黑洞成像。新增中文 AI 合成旁白与原创合成氛围音轨。

成片：`out/from-line-to-black-hole.mp4`。源码包：`out/from-line-to-black-hole-source.zip`。最终检查：`review-evidence.json`。

## 六个段落

| 时间 | 内容 |
|---|---|
| 00:00–00:12 | 直线传播与到达方向 |
| 00:12–00:25 | 掠过距离与引力偏折 |
| 00:25–00:40 | 真实光源、反向延长线和视位置 |
| 00:40–00:54 | 点光源铺开，逐点成像为亮弧 |
| 00:54–01:02 | 二维图解切换到三维吸积盘 |
| 01:02–01:30 | 背面光路、上拱像、观察角度与结论 |

## 可编辑入口

- `lesson.mjs`：全片时间轴、二维图解、虚实光路、扩展光源的薄透镜映射、三维镜头重排、文字与章节。
- `film.mjs`、`lens.frag`：上一版原创 Three.js 非旋转黑洞场景的改编，加入相机覆盖和独立排版接口。未复用参考 MV 的场景代码。
- `make_narration.py`：完整中文文案与分段合成。`narration/` 是已生成的公开中文合成声音，`narration.json` 记录文本和时段；声线不是任何真实人的克隆。
- `make_soundtrack.py`：环境音乐、分段提示声和旁白混音。`audio-evidence.json` 记录语音实际时长与混音幅度。`narration.srt` 可另行导入剪辑软件。
- `render.mjs`：本地预览、代表帧、关键动作样片和完整 MP4 导出。
- `production.md`：六段分镜、事实来源与科学范围。

声音已随源码提供，普通预览/重渲无需访问语音服务。全片由可寻址帧时间计算，任意跳帧不依赖前一帧状态。三维采用 1.5 倍空间超采样和 MSAA；二维文字/图解按输出尺寸绘制。编码为 x264 CRF17，音轨 AAC 256k。

## 当前工作区运行

```powershell
& 'C:\Users\67236\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe' render.mjs --serve
```

浏览器打开 `http://127.0.0.1:8936`，播放与拖动时间条。使用 `window.__film.renderAt(seconds)` 直接寻址。

```powershell
# 完整成片
& 'C:\Users\67236\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe' render.mjs
# 代表帧
& 'C:\Users\67236\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe' render.mjs --stills
# 25–40 秒机制片段，1280×720
& 'C:\Users\67236\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe' render.mjs --study
```

迁移到其他机器：安装 `package.json` 中的依赖，设置 `CHROME` 和 `FFMPEG` 为本机程序路径；`PLAYWRIGHT_PATH` 可指定已有 playwright-core，`PORT` 可修改预览端口。混音脚本需 Python/numpy；重新合成旁白另需 edge-tts 和可用网络。默认混音 FFmpeg 路径沿用此工作区的 Remotion 二进制，可编辑脚本顶部变量。中文使用本机微软雅黑/可替代中文字体，字体文件不随包分发。

## 科学范围与审阅限制

二维成像是点质量薄透镜模型，弱场公式解释偏折趋势；它不能预测黑洞附近的强场。三维部分是非旋转 Schwarzschild 示意，有限数值积分、初始相机映射和盘面外观经过近似或美术化，未做完整辐射转移或 Kerr 自旋模拟。二维和三维之间明确提示模型切换，最后画面不是望远镜观测。

技术检查、实际看过的图片/连续帧、修复问题和没有完成的检查分别记录在 `review-evidence.json`；机器解码或幅度检查不能代替实际听音，不声称全片每帧均看过。
