# Digital OPUS 对照检查 — 2026-10-10

- 目标：研究 liuzhaowei1/Digital-OPUS-VIDEO-SKILL，比较现有工程可借鉴部分并核验本机依赖；不安装、不修改现有源码、不生成视频。
- 来源：upstream 为只读研究副本，固定 commit 86ab700d890b3d6ce4ec0a6c26d84ae800179a8c。
- 已完成：读取 upstream README/SKILL/SETUP/AUDIO/CRAFT 及依赖清单；读取本地 README/PRODUCTION/运行时清单；确认 Node 24.15.0、Three 0.186.1、Remotion 4.0.506、React 19.2.8，Playwright Core 1.62.1 在应用运行时。
- 当前发现：上游独立引擎缺 opentype.js、Vite、TypeScript、类型包；Playwright 包版本低于其声明下限，且不在项目解析路径。Python/FFmpeg 不在 PATH 不等于未安装。机器有 RTX 4070 Laptop，尚未核验浏览器实际 GPU。
- 已完成依赖核验：两个 Python 环境的包清单与实际导入证据保存在 python-app.json / python-system.json；系统 Torch/Numba 已安装但 DLL 导入失败，SciPy/SoundFile 导入通过。应用 NumPy/Pillow 基础运行通过。
- FFmpeg：随包 n7.1 可执行，缺上游使用的 setparams、ebur128、silenceremove/areverse。过滤器完整证据见 ffmpeg-filters.txt。
- GPU：gpu.json 记录上游 GL 参数无法创建 WebGL2，Windows D3D11 可创建但使用 Intel UHD；RTX 4070 实际渲染未就绪，未修改系统 GPU 设置。
- 比较完成：旁白内容指纹缓存、逐镜头依赖状态、音乐/事件双时钟、变化抽帧与参考索引、字体/自适应采样为候选增量；原工作流的竖屏、用户先看和现有证据流程应保留。
- 综合证据与建议：audit-summary.json，包含具体代码锚点和迁移限制。
- 状态：检查完成；下一步由用户决定是否采用改进。这次没有安装、下载模型、调用付费接口、改现有源码或生成视频。
