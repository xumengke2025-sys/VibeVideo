# 宝宝与妈妈 · 20时代亲子互动 v16

40秒、竖屏9:16、1080×1920、24fps、二维卡通，有意无声。沿用已生成的20时代完整双人动作，婴儿与妈妈面对面近距离互动，保留窗外鸟蝶、云、太阳与夜景星点；室内家具与窗框固定。

Windows运行：`npm install`，`npm run preview`，打开 http://127.0.0.1:8768/film/index-v16.html 。点击画面播放/暂停。`npm run render` 导出四段并拼接40秒MP4。`npm run check` 检查图集边界与乱序/重载像素一致性；`npm run check:transitions` 检查19个转场端点像素及乱序寻址。

Node.js和Chromium为运行依赖。首次渲染可由Remotion准备浏览器；也可设置环境变量 `CHROME_EXECUTABLE` 为已有Chromium绝对路径。源码包不含node_modules、浏览器、用户原始家庭照片或视频。中文使用Microsoft YaHei，换机器需要可用中文字体。

本版改动：

- 整组重新注册坐姿，以首姿态锁住低位凳脚、坐垫和落脚区；不拆拼人物手臂，不叠加周期性全身摇摆。
- 原12姿态图集先用RIFE v4.6离线补为每场48帧，再以不可变室内底图合成。模型不参与播放器；动作不是48张全新生图，快速遮挡处仍可能有局部软边或形变。
- 每场前后各1/3秒保持端点，中央4/3秒完成一次完整互动；转场中两侧人物停稳。
- 19次时代切换按媒介使用流金丝带、纸扇旋开、马赛克接力、颜料晕开和像素阶梯。每次2/3秒，遮罩交接两张完整场景，窄色边随前沿移动；不拉伸、旋转整个人物，不加入曝光闪白。
- 保留v15窗外逐格轻动画，无室内网格形变。

编辑入口：`film/sequences-v16.js`（时间轴与合成）、`film/transitions-v16.js`（转场）、`film/environment-stopmotion-v15.js`（外景）、`assets/motion-v16/manifest.json`（已烘焙动作位置）。`film/chase-scenes-v9.js`为历史文件名，当前采用坐姿版本。`render-v16.mjs`与`render-batched-v16.mjs`负责编码。

可选重建动作：安装 `requirements-build-v16.txt`；用 `fetch_rife_v16.py`准备本项目`.tools/rife/runtime`，运行`node export_backgrounds_v16.mjs`导出室内底片，再运行`python build_neural_motion_v16.py`。该步骤需兼容Vulkan的GPU；可设置`RIFE_GPU`，本机使用1号NVIDIA GPU。构建工具及来源见THIRD_PARTY_NOTICES；日常预览和导出不需要模型。原姿态、提示词和注册证据随包保留。

验证与观看范围见`qa/v16/production-review.json`和`qa/v16/final/engineering-check.json`。历史AI一轮审核预算已用完，此次是用户反馈后的定向制作修改，没有新一轮独立审核；没有以抽帧或帧差宣称正常速度全片审美通过。保留v15及以前的历史视频。
