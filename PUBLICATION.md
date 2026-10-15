# 公开仓库范围与本地使用

本项目于2026-10-12按所有者要求公开发布到[GitHub VibeVideo](https://github.com/xumengke2025-sys/VibeVideo)。它包含代码视频实验、制作流程、技能快照、参考影片索引与来源记录。

## 发布内容

- 项目源码、配置、文档、分镜和工程记录。
- 本项目制作的预览影片；历史版本和未交付版本保持各工程原有状态记录，不统一标为已通过审核。
- 五个有明确代码/内容许可的第三方参考包：Lemo、Makefx、Opus导演课程、opus-js-animations模板与makevoid制作工具。各包保留原LICENSE及额外的字体、内容和素材说明。
- 其余参考资料的来源、固定commit、文件哈希和媒体对应索引。未明确许可或注明仅供本地研究的源码/原片不直接复制到公开仓库。

依赖联接、环境凭据、浏览器缓存、下载临时文件、逐帧渲染目录和工具二进制不上传。第三方音视频原片从作者原始地址恢复，不把代码MIT/Apache许可扩大为歌曲、影像或字体的许可。

本仓库没有授予整个项目统一的开源许可证。公开可见不代表所有内容可任意使用；原有第三方许可各自有效。使用、修改或再分发具体内容时查看该目录的许可证和来源说明。

## 参考预览

需要Node.js 20或以上。根目录的参考服务与恢复工具不需要安装npm依赖。

```sh
npm run references:plan
npm run restore:references
npm run preview:references
```

第一条只列出恢复规模，不访问网络。第二条按 `tools/reference-restore-manifest.json` 中的原作者地址及固定commit恢复工程与媒体，逐文件校验大小和SHA256；不会执行上游源码、技能或安装第三方插件。2026-10-15更新包含319条参考、20个关联源码/资料包的恢复任务，共6478个文件、约6.14 GB（包含部分历史影片及工程素材）。网络中断或原作者移除资源时会记录失败，重新运行复用已通过哈希检查的文件；原地址长期可用性无法保证。

可用 `node tools/restore-references.mjs --only <项目内相对路径>` 恢复清单中的单个文件；`--verify-only` 只校验本地文件，不下载。新目录下载的抽帧海报是可选本地缓存，不随公开包分发，不影响视频播放。319条为索引规模，首次克隆尚未恢复时不代表媒体已在本机。

若环境配置了 `HTTPS_PROXY`、`HTTP_PROXY` 或 `ALL_PROXY`，恢复工具自动使用系统curl遵循代理设置（Windows自带curl；其他系统需安装）；也可用 `--curl` 显式选择。未设置代理时使用Node原生下载。两条路线均校验同一份大小和SHA256，不降低TLS校验。

Shotcraft的原Windows源码快照包含CRLF换行。恢复清单对这些文本文件分别固定上游原始字节和归档字节的哈希：先校验下载内容，再按明确规则转换换行并校验最终文件，其余文件不转换。

第三条启动只监听127.0.0.1的本地服务。打开：

`http://127.0.0.1:8176/work/github-reference-expansion-20261011/index.html#watch`

影片保持作者原画幅。新制作可选择16:9横屏（1920×1080）或9:16竖屏（1080×1920），分别布局。目录包含109条对应绘制源码的影片/镜头样段，以及210条视觉参考或输入不完整的作品；默认显示本轮加入的221条，每页24条。有源码不等于已验证可直接重渲原片；无源码的原片可研究画风、动作、运镜和节奏，不能当作代码实现证据。模型归属按作者声明标注。

技能版本为0.16.3。将 `skill/vibe-video` 复制到自己的技能目录即可使用；完整参考视频仍需克隆本仓库并恢复，单独安装时设置 `VIBE_VIDEO_REFERENCE_ROOT` 为该仓库路径。Shotcraft检索会寻找相邻的 `video-shotcraft` 安装或本仓库恢复的固定上游源码，也可用 `VIDEO_SHOTCRAFT_ROOT` 指定。Motion Workbench的本机Windows适配验证记录见 `work/shotcraft-integration-20261014`；此处不把原作者源码快照冒称已安装适配版。

## 制作项目

每个`work/项目名`保留各自源码、依赖描述、brief和CHECKPOINT。历史脚本中有原Windows机器的FFmpeg、Chrome、Python与技能绝对路径；换机器时按各工程入口配置工具路径。根目录`runtime-package.json`是原机器共享运行时的快照，不是包含全部项目的统一构建命令。

参考源码在`reference-sources/github-expansion-20261011`；项目技能快照在`skill/vibe-video`。完整参考登记见`work/github-reference-expansion-20261011/catalog.json`和`CATALOG.md`。
