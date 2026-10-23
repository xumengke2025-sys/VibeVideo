# 夜鹭跨时代 · v9动物去重版

已完成31秒1080×1920/48fps新版。16场被抢动物各不重复，失鱼后相对岸边静止，惊讶并低头看原鱼所在空地，不追视、不回头。

成片：out/film-run-v9-unique-animals-final/video.mp4
SHA256：e9ae381507354ec76f072ff20137d1043d7c3e159a7c6c13913ef6a70e241491
16场总览：out/film-run-v9-unique-animals-final/styleboard.jpg
可编辑入口：run-v9.html / src/run-v9.js / src/run-v9-owners.js
计划：production-plan-run-v9.json
素材：assets/run-v9/manifest.json / prompts.json / provenance.json
资料：research/history-run-v9.md
检查：qa/film-run-v9-unique-animals-final/production-check.md

全片解码与媒体检查通过；354时刻岸边固定/姿势时序及三处乱序寻址检查通过。主制作已查看最终80个反应节点、16场总览和18处局部/转场/结尾帧；非独立审核，未完整连续播放或听音。沿用既有审核预算，由用户反馈继续。

渲染：node render-run-v9.mjs --mode=film --version=<新的输出名>
打包：python package-run-v9.py <输出名>
反应抽帧：python check-reactions-run-v9-resting.py <输出名>
