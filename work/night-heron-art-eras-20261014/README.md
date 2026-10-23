# 夜鹭偷鱼艺术史 · v3

当前正在重设计持续奔跑版 run-v4：16时代、计划31秒，加入边跑边仰头吞鱼和按物种统一世界尺度。完整方案见 [REDESIGN-RUN-V4.md](REDESIGN-RUN-V4.md)，可执行时间表见 production-plan-run-v4.json，四张效果图见 concepts/run-v4/concept-board.jpg。当前仅完成重设计与静态概念；新版MP4尚未生成。以下为保留的v3可播放版本记录。

16时代，1080×1920竖屏，24fps，40秒。全部分别使用内置 image_gen 生成夜鹭、其他动物与鱼，画风贯穿全部要素。实际移植花叔源码背景与材质，再作竖屏构图。只显示时代与年份，原创合成配乐，无旁白。

动作：初始缩颈→伸颈到旁边动物脚边→叼走地上的鱼→抬头吞咽→收颈归位。颈部使用四个控制关节及对应时代羽毛纹理。其他动物反应：同一相位：发现鱼被取走后轻微后仰抬头，再俯身查看原位置；无争抢、追逐或对抗。

## 预览和输出

本目录运行 node serve.mjs，打开 http://127.0.0.1:8146/rebuild-v3.html 。网页可播放音频、拖动时间轴。

命令：
node build-source-v3.mjs
python prepare-atlases.py
node render.mjs --mode=concepts --version=新的概念图版本名 --entry=rebuild-v3.html
node render.mjs --mode=video --version=新的成片版本名 --entry=rebuild-v3.html


依赖本机Chrome、工作区Playwright和Remotion附带FFmpeg。换电脑需更新render.mjs中的三处路径。Python仅用于测量alpha和制作检查联系表，不用于重绘原始生图。

- rebuild-v3.html / src/film-v3.js：新版入口、四关节颈部、统一反应、鱼绑定、标签和时间轴。
- assets/rebuild-v3/era-01.png至era-16.png：16套独立生成原素材；prompts.json为完整提示词；atlas-manifest.json为裁切。
- vendor/huashu/：MIT许可、移植源码、逐文件来源与改编哈希。
- research/history-v3.md：16时代、地点、动物、事实来源和证据强度。
- production-plan.json / CHECKPOINT.md：当前计划与完成范围；v2历史计划单独保留。
- out/film-v3/video.mp4：新版成片；out/rebuild-concept-final/styleboard.jpg：16画风总览。

0–2秒建立；2–38秒16时代、每段2.25秒；38–40秒收尾。半秒平滑叠化保留动作相位与取鱼锚点。这是匹配动作的材质转换，不是几何连续变形。

## 来源与实际范围

花叔alchaincyf/huashu-art-motion固定提交64cb27271ee0ad3375298e2890b33cbec36d4051，MIT。新版运行其背景/材质函数，移除了原片人物、叙事文字及部分家具；竖屏采用裁取、重排和同源材质铺底。改编关系见vendor/huashu/provenance.json。未将原片抽帧当背景，未重渲完整上游影片。

这是虚构夜鹭穿越艺术时代的喜剧。动物选择追求地域/年代相容，生成画面不是考古重建或物种出现年代证明，依据及局限见历史台账。

旧入口index.html、旧源码和历史影片全部保留。既有审核预算不重置。新版工程检查和实际制作查看与本版媒体哈希绑定；主制作查看不等于独立审核，解码与音量检查不代表听过完整音轨。
