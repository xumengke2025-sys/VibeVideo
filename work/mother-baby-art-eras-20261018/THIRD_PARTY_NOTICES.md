# 来源与采用范围

参考工程：alchaincyf/huashu-art-motion，固定 commit `64cb27271ee0ad3375298e2890b33cbec36d4051`。
本地来源：`../../reference-sources/video-films-20261014/alchaincyf--huashu-art-motion/scripts/engine`。
原许可为 MIT，完整许可见同目录 `REFERENCE-LICENSE.txt`。

时代顺序和年份参考 `eras_gallery.js`，本版选取20个时代，环境、竖屏构图与渲染入口沿用本项目制作代码。历史版本曾参考 `lib/rig.js` 的二骨 IK 与杯子锚点机制；当前v15沿用v13共同生成的完整母婴动作图集和v14放大22%的构图，不使用IK、代码身体、四肢切片或头身拼装，由绝对帧时间控制姿态停留和整组刚性注册。v15保持室内原画，只在外景开口内加入鸟蝶逐格姿态、缓移云与太阳旋转，环境与人物共用姿态停留时钟；新增小动物图集由本任务通过内置image_gen生成。人物及道具为本任务AI生成素材，不是参考影片的逐帧裁切。

参考媒体为 `art-motion-35-styles.mp4`（41.25秒、24fps、1920×1080、无音轨）。媒体与所存源码版本存在差异，不能宣称逐像素重现。研究记录见 `research/REFERENCE-TRANSFER.md`。

用户照片仅作为本任务人物辨识参考；AI生成的身份图和概念图是制作参考，并未作为成片的摄影脸部素材。无需外部字体下载，片中中文使用本机 Microsoft YaHei；跨机器需安装可用中文字体或替换字体名称。

v16离线动作补帧使用 nihui/rife-ncnn-vulkan 的20221029 Windows发行版和其中rife-v4.6模型：https://github.com/nihui/rife-ncnn-vulkan/releases/tag/20221029 。本机模型、可执行程序只在构建阶段使用，不随源码素材包分发；包内提供获取脚本及已烘焙PNG。新转场为本项目编写的确定性二维空间遮罩。RIFE输出属于既有生成动作的中间态，不宣称逐帧新生成或几何无误。

v17沿用该离线补帧工具，以内置image_gen生成完整双人连接姿态、现代碰掌动作及杯瓶放下过程；提示词与使用的透明图保存在assets/bridges-v17。人物使用独立连续轨道，背景单独转场。身份参考、原始家庭照片和拒用的多手草图不随源码包分发。

v21新增本项目编写的40秒器乐配乐，乐谱、MIDI及WAV保存在assets/audio-v21。乐器音色采用Chris Collins的GeneralUser GS v2.0.3，随包保留LICENSE-GeneralUser.txt；其许可允许音乐创作及音乐录音的商业使用。音色库随源码包提供，乐谱渲染依赖numpy与tinysoundfont（需另行安装）。当前成片没有文字叠加，无需中文字体。
