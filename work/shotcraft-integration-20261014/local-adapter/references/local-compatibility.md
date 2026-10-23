# VibeVideo本机适配 — 2026-10-14

固定来源：`Vincentwei1021/video-shotcraft@13c74a707786872a18e3317e48c5c94011027620`。上游代码和技能原件保留；本机入口优先于研究文档中的固定横屏、三种创作模式、强制独立审核和推广流程。

- Gallery：124张卡/150个变体；现行demos：150个组件。两种计数来自不同索引，不能互换。vibe-video目录中的 `scripts/shotcraft_library.mjs` 校正分类、组件别名与卡片参考实现；Gallery匹配149个现行demo与1个FlashCut组件。CrashZoom另附撞停实现，预览对应和动态质量另行核对。
- Windows：Git的 `workbench/demosrc` 文本占位转换为指向本库demos的junction；源码工程使用junction，public根文件复制并记录哈希，切换时只删除未修改的自有副本；遇冲突停止并保留文件。
- 渲染：Node解引用同步public到私有 `.render-public`，不依赖rsync；Node调用Remotion CLI；Windows帧并发和FFmpeg解码/过滤/编码线程为1，避免共享机器上自动分配大量线程。
- 同帧验证：`scripts/parity-local.mjs` 使用锁定的pngjs7.0.0，不需要Python/Pillow或完整版FFmpeg；复用一个Chrome，精确零像素差为默认阈值。`--out`保存PNG和comparison.json；无法比较返回2，有差异返回1。
- 浏览器：可设置 `SHOTCRAFT_BROWSER_EXECUTABLE`，parity也支持 `--browser`。`TEMP/TMP`可以仅为该启动进程设置到空间充足的任务目录。服务仅监听127.0.0.1。
- 画幅：原demo多为横屏，不自动变成竖屏。vibe-video提供PageCamAdaptive，实际布局与锚点需分别设计。工作台manifest记录真实尺寸/fps，原片与manifest共用时间数据。
- 本次不验证剪映导出、全部镜头的动态/听音质量、HTML/Canvas旧工程自动拆解。实际内部样段、失败记录、验证与安装差异见项目 `work/shotcraft-integration-20261014/`。

依赖锁定：Remotion4.0.484、React19.2.7、Vite6.4.3。执行 `npm ci --ignore-scripts --no-audit --no-fund`，勿混用项目根的另一套Remotion。基础制作/交付规则见本机SKILL.md；上游详细工作台协议仍读workbench.md。
