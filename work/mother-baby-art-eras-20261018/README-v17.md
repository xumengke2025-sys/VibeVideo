# 宝宝与妈妈 · 20时代亲子互动 v17

40秒、竖屏9:16、1080×1920、24fps、二维卡通，有意无声。沿用已生成的20时代完整双人动作，婴儿与妈妈面对面近距离互动，保留窗外鸟蝶、云、太阳与夜景星点；室内家具与窗框固定。

Windows运行：`npm install`，`npm run preview`，打开 http://127.0.0.1:8768/film/index-v17.html 。点击画面播放/暂停。`npm run render` 导出四段并拼接40秒MP4。`npm run check` 检查图集边界与乱序/重载像素一致性；`npm run check:transitions` 检查19个转场端点像素及乱序寻址。

Node.js和Chromium为运行依赖。首次渲染可由Remotion准备浏览器；也可设置环境变量 `CHROME_EXECUTABLE` 为已有Chromium绝对路径。源码包不含node_modules、浏览器、用户原始家庭照片或视频。中文使用Microsoft YaHei，换机器需要可用中文字体。

本版改动：

- 整组重新注册坐姿，以首姿态锁住低位凳脚、坐垫和落脚区；不拆拼人物手臂，不叠加周期性全身摇摆。
- 每场完整原生姿态通过RIFE v4.6离线补为48幅烘焙动作，再按40秒共享时间线取样。模型不参与播放器；快速遮挡及服饰媒介转换处仍可能有局部软边或形变。
- 19处时代交接各增加完整双人连接姿态，末姿态是下一动作的起点，取消每场前后冻结。普通连接17幅、结尾放稳杯瓶连接25幅，均包含在40秒内。
- 结尾先降低杯子和奶瓶，放稳、松手后再碰掌；杯瓶保留在座位旁。结尾8幅完整碰掌姿态重新生成，动作不归零。
- 19次时代切换按媒介使用丝带、纸扇、马赛克、颜料和像素遮罩；遮罩只交接背景，完整人物在其后仅绘制一次，人物动作不会被背景擦断。
- 保留v15窗外逐格轻动画，无室内网格形变。

编辑入口：`film/sequences-v17.js`（时间轴与合成）、`film/transitions-v16.js`（背景转场）、`film/environment-stopmotion-v15.js`（外景）、`assets/motion-v17/manifest.json`（已烘焙动作位置）。`film/chase-scenes-v9.js`为历史文件名，当前采用坐姿版本。`render-v17.mjs`与`render-batched-v17.mjs`负责编码。

可选重建动作：安装 `requirements-build-v17.txt`；用 `fetch_rife_v16.py`准备`.tools/rife/runtime`，运行 `python build_continuity_v17.py --scenes 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19 --bridges 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19`。需兼容Vulkan的GPU；`RIFE_GPU`可指定设备，本机使用1号NVIDIA GPU。`build_motion_v16.py`为复用的注册工具。日常预览和导出不需要模型。生图已通过内置image_gen完成并随包保存，提示词见`assets/bridges-v17/prompt-*.txt`；拒用的多手草图不打包、不运行。

验证与观看范围见`qa/v17/production-review.json`和`qa/v17/final/engineering-check.json`。历史AI一轮审核预算已用完，此次为用户反馈后的定向制作检查，没有新一轮独立审核。抽帧和端点像素相等不代表解剖或正常速度全片审美通过。保留v16及以前全部历史视频。
