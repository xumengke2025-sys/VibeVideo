# 绘制来源与改写

Lemo crayon-book，commit e3cb16f63768c68693ff0e15171d6e755457cc32，MIT（engine/LICENSE保留）。

engine/crayon.js、gl.js、rig.js、pal.js、lib.js来自固定版本；尺寸改为1080×1920，绝对导入改为同目录。引擎原文字辅助函数保留但本片无调用。所有画面无外部影像或字体请求。

timeline.js、baby.js、world.js、main.js、score.py、render.mjs为本片新增。book.js依照上游end.js的64条曲面、纸背、投影和桌面接管机制为竖屏改写，不复制来源的书页句子/片尾。

v2按用户最新要求，将三张宝宝照片作为身份参考提供给内置image_gen，生成透明蜡笔头部及眨眼/哈欠变体；头部并非代码生成。素材及完整提示词保存在assets。身体由新增baby-rig.js控制，衣服参照照片；院子/花园照片仍仅作代码场景的布局特征参考。连接门位为动画设计。未调用视频生成模型，原片音轨、女孩/月亮/羊角色和文字不复用。

v2新增pacing.js，将内部0—60秒故事映射为40秒可播放版本，单调Hermite保证速度连续；score.py使用同一映射求声音事件时间。旧baby.js的宝宝代码保留追溯，当前仅使用drawCat。
