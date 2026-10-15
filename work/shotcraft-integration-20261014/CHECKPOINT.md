# video-shotcraft 接入 — 2026-10-14

- objective：更新本机较早的 video-shotcraft，将整理后的镜头库与工作台接入 vibe-video，保留本项目画幅选择、效果图先行与两种交付方式。
- upstream：Vincentwei1021/video-shotcraft，固定 commit `13c74a707786872a18e3317e48c5c94011027620`（2026-10-13）。
- completed：固定源码已存reference-sources/video-shotcraft-20261014；旧技能660文件完整备份before/video-shotcraft；1358个上游文件已安装；Windows junction、索引路径、素材复制、Node CLI与localhost绑定已适配；项目兼容入口、vibe-video检索与集成文档已建立。
- verification：官方quick_validate三处技能通过；工作台TypeScript与Vite生产构建通过（305 modules，已有大chunk提示）；124卡/150变体准确解析为149个现行demo和1个组件，缺失/未解析均0；横竖样段分别6个采样帧导入前后均0像素差；实际浏览器导入与文字参数修改，竖版另改颜色/字号；工作台MP4导出、两版完整解码、90帧/30fps/3秒视频与48kHz AAC音轨检查通过；实际查看两版导出首帧，确认修改生效。总证据见verification.json。
- samples：verification/landscape-edited.mp4（1920×1080）与portrait-edited.mp4（1080×1920）；共享事件表，横版左右/竖版上下布局，PageCamAdaptive覆盖平面与透视路径；测试音为原创合成纯音，非创意样片。容器3.050667秒包含AAC填充，视频恰为3秒。
- source/rollback：原固定commit checkout的tracked文件未改；旧安装660文件逐文件哈希验证；local-adapter/与local-adaptations.json保存本机改动，skill-sync.json保存安装与项目副本7文件一致的SHA256；vibe-video0.16.0。
- failures/resolution：首次Chrome资源/超时、随后FFmpeg编码失败；改为单浏览器、D盘进程临时目录、Windows帧并发1和FFmpeg线程1后导出成功。打包FFmpeg功能裁剪，像素对照改pngjs7.0.0，解码显式指定codec，音量从解码PCM计算；官方validator依赖只安装在本任务validation-deps，未改全局Python环境。
- limitations：未对全库150变体逐一做动态/视听审美验收；未实际听音或独立审片；未验剪映导出；HTML/Canvas旧工程需另做清单适配；没有自动恢复暂停项目。初次索引没有在线预览MP4本地缓存，工作台直接实时渲染demo。
- next：本次接入完成。后续新片从镜头叙事用途检索并读准确实现，按画幅分别设计布局，沿用效果图先行与用户所选交付模式；不追加审核轮次。
- workbench：http://localhost:5198/，当前链接内部竖屏验证工程，服务监听127.0.0.1；scripts/open.mjs可切换到用户的带workbench.ts工程。Windows使用记录且核实身份的PID停止，不能泛停其他node/Chrome。
- scope：本次是技能升级与内部能力验证，不恢复暂停的视频项目，不派导演/审片子代理。
