# 宝宝与妈妈 · 20时代亲子互动 v20

40秒，20时代按历史顺序，竖屏9:16，1080×1920，24fps，有意无声。

本版把婴儿身下坐垫从原动作图集中分离，改成独立固定底层。20款完整空坐垫通过内置image_gen生成，提示词为assets/motion-v20/cushion-prompt.txt。坐垫在所有时代使用相同绘制矩形，只在时代交接时混合材质，位置不跟随宝宝。大地毯也保持固定。沿用v19婴儿尺寸，人物不做任何新增坐标变换；仅在下方遮挡区域调整透明度，并保护脚、妈妈鞋尖、积木和奶瓶。

背景保留窗外鸟蝶、云、太阳和星点活动；19个适用场景增加轻微叶片/藤蔓、流苏或帘边活动。动区按实物位置和颜色登记，有固定根部，最大位移7像素；花盆、家具、窗框和墙面主体固定。洞穴沿用窗外运动，不强行移动壁画。背景运动与人物共用确定性时间轴，保持原片逐格风格。

运行：安装Node.js，在本目录执行npm install，然后npm run preview，访问 http://127.0.0.1:8768/film/index-v20.html 。点击画面播放或暂停。npm run render 顺序渲染8个5秒小段，先合成四个10秒分段，再拼接成40秒MP4，以降低浏览器峰值负担。npm run check 检查19条动作连接、坐垫静止和寻址一致性；npm run check:transitions 检查背景转场；npm run check:environment 检查室内动区边界。

依赖：Node.js、Chromium、可用中文字体。可设置CHROME_EXECUTABLE指向已有Chromium。源码包不含node_modules、浏览器、原始家庭照片或成片。解包验证复用本机依赖，不代表新电脑安装验证。

编辑入口：film/sequences-v20.js（时间轴/固定坐垫合成）、film/environment-life-v20.js（室内局部活动）、film/environment-stopmotion-v15.js（窗外活动）、film/transitions-v16.js（背景转场）、assets/motion-v20/manifest.json（人物图集）。历史命名chase-scenes-v9.js仅作为20场静态配置，本版采用坐姿互动。

可选重建：pip install -r requirements-build-v20.txt。python prepare_cushion_atlas_v20.py 从本次生成素材裁切透明图集；python build_batched_v20.py 从随包v19图集重新分离人物与坐垫。逐场子进程运行以限制内存；这些是素材处理进程，不是AI子代理。mask的人工接触轮廓和道具保护见build_cushions_v20.py。无需重新生成人物或下载动作模型。日常播放及导出只需要已烘焙v20图集。

本次为用户反馈后的定向制作检查，历史AI一轮审核已经结束，没有新一轮独立审核。实际检查范围与限制见qa/v20/production-review.json；全片解码信息见qa/v20/final/engineering-check.json。原有跨画风补间仍有局部软边，不能把机械检查或抽帧等同于全片审美通过。v19交付文件保留。
