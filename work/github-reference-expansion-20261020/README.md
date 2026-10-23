# 2026-10-20 影片与对应绘制源码维护

本次只将本地样例影片与实际绘制源码成对的资源加入预览。沿用已有目录，完整影片与短样段分开，复刻不冒充原作，作者模型声明不当作独立证明。

|来源|选入范围|对应代码与注意事项|
|---|---|---|
|[Claude Imagine模板](https://github.com/lumian2015/opus-5-5-video-templates)|30种15–46秒动效模板样片|templates/*/index.html、同目录素材/时间轴/变量与template.json；作者重写的复刻，部分含生成照片；MIT及第三方许可分别使用|
|[Kiteva](https://github.com/delexw/kiteva)|139个风格短样段|assets/style-previews/sources/style-*/完整目录，与同名影片对应（136个MP4、3个WEBM）；多数约3秒；模型未逐例证实；Kiteva非商业许可|
|[Lemo Opuscar](https://github.com/lemomo-ai/lemo-opuscar)|新增8种Evidence Films|styles/<风格>/demo/index.html及完整目录、共享core/字体/导出工具；不覆盖旧43种风格快照；采用作者web发布的MP4，保留发布SHA256|
|[Myriad Worlds](https://github.com/holooooo/myriad-worlds)|70秒4K风景巡游|影片v1.0.2标签源码；src场景/天气/相机与tools录制导出代码、同版本影片镜头JSON；作者声明Opus奠基、GLM继续开发；MIT|
|[Argon vs Opus](https://github.com/krisuuu2/argon-vs-opus)|销售报告动画并排对照|claude-opus-5.5.html、gemini对应HTML、提示词、同一虚拟时钟录屏；未发现明确许可，仅本地研究|

固定版本和逐文件大小、SHA256、Git blob在各来源包SOURCE.json；视频逐条映射在项目reference-sources/github-expansion-20261020/manifest.json。源代码只归档和阅读，未批量安装、运行或重渲。媒体下载、完整解码及三时刻指纹不是全片视听审核。

## 本轮结果

实际新增179条，全部具备本地样例视频与对应绘制源码：40个影片/模板样片/对照及139个短风格样段。保留旧库后累计498条，其中288条有对应源码。全部179条完整解码通过；507条记录哈希比较，502条三时刻指纹比较，无重复候选；6条复刻与既有原帖另标关联。5条旧记录没有有效缓存帧，未计入画面指纹覆盖。

目录与双份技能检索索引、恢复清单已更新；1626个HTTP资源检查全部通过。浏览器抽查MP4实际播放与WEBM播放至结束，记录见browser-verification.json；工程与源文件检查见verification.json、media-verification.json、http-verification.json。没有执行上游工程或重渲，也未做全片视听审核。

## 候选筛选

- `Vishnu-tppr/motionloom-studio`：有制作引擎，当前固定提交没有发布成对MP4，不加入本轮预览。
- `Neeraj138/navratri-opus-5.5-anim`：有实际场景源码，当前仓库和release未发现成片，不加入。
- `inematds/google-carbon-video`：有release影片，但当前仓库只有README，没有绘制源码，不加入。
- `zhenghuiyu06/deepseek-v41-flash-video-materials`：素材包和第三方截取，不作为对应动画绘制工程加入。
- `MugaSofer/claude-music-videos`：源码值得后续研究，发布影片目前只发现YouTube入口，本轮未取得本地媒体，不加入本轮预览。
- `ghywel/ai-storyboard`：工具与demo源码存在，未发现本地成片或直接发布媒体，不加入。
- `pythoninoffice/tasty-opus5-5-videos`：当前提交无MP4或release样片，不加入。
- `tuzhechen2005/opus-video-skills`：公开GIF与技能模板，未将其计为MP4完整影片及对应源码。
- 各awesome索引只作为发现线索，提示词、网页播放器及画廊源码不算影片绘制源码。
- Lemo的OPUSCAR 98及里程碑影片不因同仓库有视频便算源码齐备；本轮只选入8种新增完整demo工程。

## 维护与验证

研究记录保留在research目录；源码下载用固定提交/Blob API，归档后与Git blob SHA1核对并记录SHA256；release媒体按作者发布摘要核对。网络中断可复用已验证文件和分块。整片下载与2MiB分块曾出现超时；最终用finish-release-ranges.mjs续传缺失的小分块，并核对完整发布SHA256。不要并行启动多个下载脚本写同一目标。

按顺序完成：`make-manifest.mjs` → `verify-media.mjs` → 核对duplicate-report.json → 项目目录生成器 → `update-index.mjs` → 现有恢复清单生成器 → `verify-library.mjs`、`verify-http.mjs`。新增缩略图是本地可选提取，不替代原片。

只维护本地内容；没有提交或推送本轮变更到GitHub。
