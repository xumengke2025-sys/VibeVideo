# 妈妈与婴儿 · 二十时代 v21

40 秒，20 时代按历史顺序，竖屏 9:16、1080×1920、24fps。画面已移除时代名和年份。最新交付是带原创温馨配乐的 `out/mother-baby-20-eras-portrait-v21-40s-music.mp4`；无声母版另保留。

配乐为原创 F 大调小品，120 BPM，以钢琴、钟琴、尼龙吉他和轻拨弦构成，38 秒落到主和弦后自然淡出。乐器由 GeneralUser GS 音色库渲染，授权见 assets/audio-v21/LICENSE-GeneralUser.txt。40 秒 WAV、可编辑 MIDI、音符表、音色库和作曲脚本随源码提供；安装 numpy、tinysoundfont 后可运行 `python compose_music_v21.py` 重建。`python add_music_v21.py` 将配乐加入无声母版，复制视频流而不重新压缩画面。配乐已完成时长、解码、无削波和连续信号检查；当前工具不支持实际听音，未声称听音审核通过。

本版按每段实际可用时长重新烘焙人物姿态，消除旧版将 48 姿态取整压入较短时间段造成的交替跳帧。手和道具的局部透明拖影用相邻清晰绘画的运动对齐补色处理，面部、婴儿核心、双脚及固定坐垫受保护。新生成四幅换手图，补足结尾双手接杯、向右移杯、松手和放下的过程；仅替换妈妈躯干和手臂，沿用原人物头部、宝宝、腿和凳子。换手连接延长为 33 姿态，整片仍为 40 秒。新素材通过内置 image_gen 生成，原图和提示词为 assets/motion-v21/handover-generated.png 与 handover-prompt.txt。

宝宝尺寸沿用 v19/v20 的校准。小坐垫、大地毯固定；坐垫不跟随人物动作。背景继续保留窗外鸟蝶、云、太阳，以及局部叶片、藤蔓、流苏和帘边活动。背景、家具与画幅沿用 v20。

## 运行与编辑

安装 Node.js，在本目录执行 `npm install`，再执行 `npm run preview`，访问 http://127.0.0.1:8768/film/index-v21.html 。点击画面播放/暂停。

`npm run render` 顺序导出 8 个 5 秒小段，无损拼接为 40 秒母版，再加入配乐生成带 music 后缀的 MP4。可设置 `CHROME_EXECUTABLE` 指向已有 Chromium。源码包不含 node_modules、浏览器、原始家庭照片或成片。网页预览点击画面时同步播放配乐。

`npm run check` 检查 19 条人物连接、固定坐垫、逐帧时钟及寻址一致性。`npm run check:transitions` 检查背景转场端点。

入口为 film/index-v21.html；时间轴和合成为 film/sequences-v21.js；人物图集清单为 assets/motion-v21/manifest.json。背景细节和转场入口分别为 film/environment-life-v20.js、film/environment-stopmotion-v15.js、film/transitions-v16.js。

## 可选重建

播放、编辑和视频导出只需要已烘焙的 v21 素材，不依赖生成 API 或动作模型。源码包也附 v20 人物图集作为局部修复的输入；安装 numpy、Pillow、opencv-python 后执行 `python build_batched_v21.py` 可分批重建。脚本按已有 qa/v21/scene-*.json 和 bridge-*.json 断点跳过；要重建指定材料，直接调用 `build_motion_v21.py --scenes 16` 等参数。

`build_handover_v21.py` 将已生成的换手素材合成到原轨道。重新执行其补间步骤需要原工作区的 `.tools/rife/runtime`（rife-ncnn-vulkan、rife-v4.6 模型和可用 Vulkan GPU），该第三方运行时不随源码包分发；最终 33 幅换手图已烘焙并随包提供。模型无需重新生成图片。重建后执行 `python clean_matte_v21.py` 清除图块边缘断开的补间杂点，再执行 `python check_assets_v21.py` 核对素材。

本次是用户反馈后的主制作角色定向检查，没有新一轮独立审核。具体查看范围、剩余软边限制和当前成片哈希见 qa/v21/production-review.json。机械检查不代表所有姿态的解剖结构或全片正常速度审美已通过。v20 成片与源码保留。
