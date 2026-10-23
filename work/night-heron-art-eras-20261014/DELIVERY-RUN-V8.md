# 夜鹭跨时代 · 看向失鱼处

按2026-10-16用户反馈，取消动物跟随夜鹭、转向正面或回头的动作。鱼离地后，动物先短暂停顿，再低头看原来放鱼的空地，保持惊讶的姿势至出画。动物与近岸共用摄影位移，脚底不随夜鹭行进。

- 成片：`out/film-run-v8-empty-ground-final/video.mp4`。
- 16时代、31秒、1080×1920竖屏、48fps、原配乐及夜鹭奔跑/仰头吞鱼保留。
- 动画入口：`run-v8.html`；源码：`src/run-v8.js`与`src/run-v8-owners.js`；背景沿用`src/run-v7-backgrounds.js`。
- 素材：复用v6各时代独立生图的中性、惊讶和低头姿势，仅使用0/1/3/4；不再使用左右追踪姿势，不新增生图。刚性脚底注册与固定下缘见`prepare-run-v8.py`，来源哈希见`assets/run-v8/provenance.json`。
- 新行为以`production-plan-run-v8.json`的`revision_run_v8`和本说明为准；计划中保留的旧追踪描述为继承历史，v8源码已移除该驱动。
- 最终哈希、媒体检查、源码快照和实际查看范围见`qa/film-run-v8-empty-ground-final/production-check.md`及输出的`evidence.json`、`source-manifest.json`。

原一轮审核预算不重开。本次为主制作按用户反馈修订和生产检查；未新增独立审片。完整连续播放及完整听音未完成，不声明全片独立视听通过。小动物的反应可能被前景夜鹭短暂遮挡。旧v7及历史版本保留。
