# 夜鹭的一天 · 彩皮影动画

最新版：`film/out/final-soundstage-v10/video.mp4`，36秒、1080×1920、24fps，含夜鹭实录与戏曲锣鼓音轨。

去掉解释性字幕，统一角色跨分镜的走位、姿态、步态和翻面时间线；动物园、企鹅桶及归巢景片渐次交接。只保留场内标牌。

可编辑入口：`film/film.js`；环境、材质和假山：`film/art.js`。启动 `node film/server.mjs` 后打开 http://127.0.0.1:8796/ 查看关节预览。完整使用说明见 `交付说明.md`。

最新工程位于 `delivery/soundstage-v10/`，含透明PNG、864帧关节数据、源码、音轨、成片及导出记录。

当前 `delivery_mode: user_feedback`。用户明确要求直接改、不再二次校验；未安排新版独立审片。上一轮及历史版本保留，不能当作当前新版审核。

当前优化：上半部增加雕刻垂柳、淡远山、云纹与渐变日月；保持连续动作和无解释字幕。使用film/timeline.js的分段时间映射：入园和返家加快，取鱼与喂食保留动作停顿。结尾约4秒大夜鹭和两只幼鸟用同一组节拍张嘴、伸缩颈与轻摆皮件，配真实夜鹭短叫的三组呼应，幼鸟轻度升调，伴奏在结尾减弱。

本版只换声音，H.264画面流与v9逐字节一致。film/audio-stems/提供打击乐、鸟声与环境动作三个分轨。night-heron声音署名Sharad Apte；戏曲采样署名ajaysm、Mi Tian、Ying Wan。音轨及同步改编影片按CC BY-SA 4.0交付，详情见film/audio-assets/ATTRIBUTION.md。未实际听音，按用户反馈继续修改。
