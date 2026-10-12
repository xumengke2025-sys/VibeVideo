# 来源与采用

|来源|实际使用|版本/许可|边界|
|---|---|---|---|
|Three.js|vendor/three.module.js、three.core.js；世界、相机、网格与WebGL|0.186.1；vendor/THREE-LICENSE|无完整物理/自动摄影|
|Lemo ink-wash|vendor/ink.js、lib.js；common.mjs用mk/draw生成湿墨与飞白纹理|4d7014aa7ba7d22c00513052dd996a4f200d5102；vendor/LICENSE-lemo.txt|局部纹理，不是真实墨水扩散或完整demo移植|
|Vibe Video原创工具|camera/subject-camera.mjs；S02绝对时间跟拍|复制D:/Codex/skills/vibe-video/assets/subject-camera.mjs|无避障、自动构图、光学对焦|
|旧版项目|renderAt接口和离线捕获路线；旧vendor副本|旧文件保持，哈希见engineering-full.json|未搬旧声轨，不以旧船/画像充当全部镜头|
|Codex静态生图|11张源图；31条登记含28个在用组件与3个旧步兵组件|registry.json记录来源、裁切、哈希、视角及关节；original-prompts.json与hires-infantry-prompts.json保存精确提示词|艺术重构；初版infantry-atlas的精确提示词仍缺失，保留明确标注的重构简述；无生成视频|
|本轮原创|角色两段腿骨IK、四腿马局部骨架、方阵、船体/断桅、岸场、记录、合成与声音|revision-v2源码|受限2.5D动作，不是史料级复原、体积人体/马体或全场物理|

particle-beach、papermotion、mg-styles和lyric仅作机制阅读参考，没有打包其完整工程、字体、模型或音乐。阅读范围与固定版本沿用上级REVISION-PLAN-20261010.md第六节，不把阅读或历史回放算成本片视觉验证。
