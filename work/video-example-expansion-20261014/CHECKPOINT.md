# 视频与源码混合扩展

用户选择：产品运镜、连续变形、三维场景、数据叙事混合补充。

用户追加偏好：优先已有开源项目，直接取得作者效果视频及实际绘制源码。

已完成：

- 保存20段Shotcraft作者Gallery MP4，连接已有固定版本完整源码、精确TSX及镜头卡。产品摄影4段、连续布局/状态交接6段、CSS空间镜头4段、数据叙事6段。匹配光圈切与几何变形分开，CSS透视与真实三维分开。
- 保存《The Claude Glass》59.6秒作者解释片和Chaoqi31/opus-paints完整257文件固定仓库快照（65fba0d92cf5cfbb821c67e1734acbc55801a8ca）。含逐帧timeline.py、score.py、60幅程序画作与原许可；全部Git blob SHA1核对通过，SHA256存入SOURCE.json。
- 将已有60秒Particle Beach作者预告与完整cinematic runtime接入统一目录；未重复下载。没有再次下载已连续404的PaperMotion附件。
- 本轮22个预览条目，实际新增下载21个视频；目录从76增至98，旧76个预览ID保留，无本轮重复下载。新增20个镜头样段，影片类条目由76增至78。
- 视频、准确源码、来源与许可可直接点击。统一目录支持影片/镜头样段分类、关键词、来源及本次新增筛选；同时修正目录旧的固定竖屏说明。
- vibe-video更新为0.16.1，安装与项目副本同步。新增video_examples.mjs及video-examples.json，可按需求/类别检索并直接取MP4和源码。

验证：22个视频（含1个复用片）SHA256/元数据/完整音视频解码通过；22组HTTP视频范围请求206、源码HEAD200。新旧目录入口无缺失，6段数据筛选、2个影片类型筛选、精确MosaicReframe.tsx映射通过。浏览器实际播放mosaic-reframe，观察到时间推进、readyState4、无媒体错误；影片筛选显示2个本轮条目，全类型显示22/98。技能两份official quick_validate通过（Windows用Python -X utf8）；4个技能文件逐字节同步。

证据：[verification.json](verification.json)、[media-verification.json](media-verification.json)、[目录截图](gallery.png)、[索引](../../skill/vibe-video/references/video-examples.json)。本次来源在reference-sources/video-examples-20261014/，筛除原因存于manifest.json；此前文件快照位于before/。

验证边界：未批量重渲、未完整动态观看或听音。Shotcraft部署视频未提供固定Git版本，固定Gallery映射不证明同源码逐像素重建。Claude Glass影片及画作CC BY 4.0、代码MIT；重建所用macOS字体需合法取得或替换。Shotcraft音频许可与品牌素材独立。没有发布GitHub，没有恢复暂停项目或改动其他片子。

状态：本轮参考扩展完成。可在本地目录直接挑选视频和源码，后续制作按用户画幅与交付选择迁移。
