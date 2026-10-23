# 新增影片与源码参考

objective: 继续查找 Opus 5.5 编写绘制代码的作品，必须同时有作者影片与对应源码，保存到项目并加入现有预览。
status: complete
checked: 2026-10-13
delivery_mode: reference_archive（资料归档，不新建视频项目）

- 已完成：新增6个仓库的9段作者影片，补齐MG15种既有影片的完整源码与资产。本轮24条进入预览，52→76条，合计12个源码包；原52条均保留，原39个GIF、历史版及无对应源码条目仍不进入预览。
- 新归档：../../reference-sources/github-expansion-20261013/。来源、固定提交、许可与作者模型声明保存在各包SOURCE.json及research/；源码入口、绘制、时间轴、导出关系见source-mapping.json，7个映射均具备文本证据。
- 来源：az9713/opus-5.5-musical-cartoon、bilaldemirerr/opus-video-recipes、c5inco/motion-showreel、DDChen666/civilization-film、JakeB-5/motion-graphic-skill、toankhontech/pelican-test-opus55，以及Vincentwei1021/mg-styles-15的完整源码补档。
- 版本对应：文明简体中文影片源码固定v1.0标签e33ad33757ab196c7349b9008a2205f572b5a3b6；Android源码与v1.0发布一致。两段发布影片SHA256与GitHub资产摘要一致。
- 完整性验证：verification.json记录632个原文件、1101755830字节（含复用MG影片），SHA256与Git blob SHA1检查通过，零错误。
- 媒体验证：media-verification.json记录24/24影片完整解码通过及元数据、海报；http-verification.json记录318个本地链接和24个MP4范围请求通过。
- 浏览器验证：咖啡、文明史、MG像素动画实际播放无媒体错误；关键词、来源、全部及本轮筛选通过。browser-verification.json保存观察，属于播放器工程检查，不是完整视听审片。
- 恢复工具：tools/restore-references.mjs支持新归档、复用媒体和发布资产；dry-run统计76影片、12源码包、2837文件，缺失文件及字节均为0。
- 预览：http://127.0.0.1:8176/work/github-reference-expansion-20261011/index.html#watch；默认显示本轮24条。服务进程32084，日志与PID在.codex/reference-server.*。
- 排除：remotion-director宣传片无对应绘制源码；App Store条目仅brief；aadil6971仓库未明确5.5；Jake的Sonnet/Codex案例不入选。
- 边界：模型版本来自作者声明；已核查影片与源码关系，但未批量安装依赖、执行下载代码或重渲，不承诺逐像素复现。原许可证保留，代码许可不扩大至音乐、字体和影像；无明确许可内容仅本地保存。原作保留上游画幅，项目未来新片仍1080×1920。
- 发布状态：本轮没有commit/push，保留其他聊天的进行中修改；GitHub已发布快照仍为0f4dc07654388a562d828e9596b1b095f4d19237。README及PUBLICATION明确区分本地新增与已发布快照。
- 下一步：本轮无剩余必需工作；用户选择参考后再检查相应运行依赖与复用范围。
