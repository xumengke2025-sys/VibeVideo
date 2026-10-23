# FirmBuddy V15 · 从客户任务出发的机械蓝图

1920×1080，16:9，30fps，90秒；纯音乐，无配音。用户反馈修改，既有AI审核预算已用，本版未新增独立审片。

## 本版行为
低对比抽象剪影携同一客户档案，在同一世界中完成任务选择、线索归集、业务研判、专家协作、依据查阅、沟通准备和客户沟通。人物用分段路径与关节求解绘制，依靠姿态表达意图。相机跟随独立人物世界轨迹，并在档案交接与阅读时停留。机械表现为齿轮、轴、曲柄滑块、滚轴导轨和压合装置；为叙事性机械示意，不作物理仿真声明。

AI作用以辅助归集/解读/匹配协作/检索引用/材料记录整理呈现，业务痛点与业务人员的结果为主。专家为产品九业务类，知识仓为六类知识槽，减持仅为例子。事实依据沿用../v14/opportunity-logic-evidence.json，产品工程未改。

## 制作与参考
- film.js：原创V15场景、角色、相机和档案所有权。
- plan.json：准确镜头与150BPM声音事件数据。
- vendor/draw.js、paper.js：保留Lemo固定版本绘图接口和蓝晒纸纹合成机制，见LICENSE-Lemo；原工程研究记录见../v14/source-transfer.json。
- 概念图仅用于审美/空间参考，成片不调用图片生成模型，也不以图像平移代替机构动作。人物进一步简化依据用户反馈，具体人物设定已停止采用。

## 重建
1. 用已有Python运行setup.py准备vendor、渲染入口与plan；已有film.js不会被覆盖。
2. Python运行make_audio.py生成原创合成音乐与拟音；依赖numpy和../tools/python中的imageio_ffmpeg。
3. Node运行render.mjs --mode=final --version=v15-human-mechanism --duration=90。需要本项目已有playwright-core与Chrome。渲染器支持帧缓存续接和同源码样段复用。
4. check_motion.mjs检查24个交接边界和主体投影；render.mjs检查文件规格和完整解码。prepare_delivery.py生成成片音频对齐/抽帧检查工具。

## 验证边界
工程检查、抽帧或连续接触表不能代替完整实际听音/正常速度观片。最终完成范围以out/final-v15-human-mechanism/delivery-checks.json和observations.json为准。
