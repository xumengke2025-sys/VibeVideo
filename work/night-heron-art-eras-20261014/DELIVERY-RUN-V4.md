# 夜鹭跨时代狂奔 · run-v4

完整成片：[video.mp4](out/film-run-v4-final/video.mp4)。31秒，1080×1920，24fps，16时代；夜鹭持续向右加速，重复偷鱼、仰头吞下、收颈动作；原持有动物轻微低头反应，无对抗。画面只保留时代和年份。

16套分别生成的姿势图集见assets/run-v4；背景实际调用固定MIT参考源码的纸纹、笔触、马赛克、切面、网点和像素算法。最终总览见out/film-run-v4-final/styleboard.jpg；历史版本保留。

## 编辑与重建

工程入口run-v4.html，主体/时间寻址见src/run-v4.js，背景见src/run-v4-backgrounds.js，参数/事件见production-plan-run-v4.json，切口约定见transitions-run-v4.json。需通过HTTP打开，不能直接file协议访问。

在本工程目录运行Python的`-m http.server 8080`，访问`http://localhost:8080/run-v4.html`查看无声实时画面；MP4含原创配乐。浏览器支持`window.renderAt(seconds)`寻址。

本机重建：`node audio-run-v4.mjs`生成原创音轨，然后`node render-run-v4.mjs --mode=video --version=新的输出名 --duration=31 --width=1080`。渲染器使用已安装Chrome、邻接sand-journey工程的playwright-core和项目Remotion内置FFmpeg，换机器时需调整路径。输出保存在out，不覆盖旧版。

## 证据

全片渲染与解码通过，浏览器错误0。最终SHA256：`99d89e1662a802cc11a7e349e2d602a9831a5ad34438c6460ff7c15749ebae55`。源码快照及逐文件哈希在out/film-run-v4-final/source和source-manifest.json；素材许可和来源随vendor保存。

实际查看范围、修复及局限见qa/run-v4-final/production-check.md。既有独立审核预算沿用；本版没有完整独立视听通过结论，全音轨听音未完成，足部接触仍为近似。
