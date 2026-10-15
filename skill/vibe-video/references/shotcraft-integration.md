# 镜头库与工作台接入

用于需要可复用镜头、产品页面宣传、文字/数据动效、2.5D 分层摄影，或用户希望在浏览器里修改已交付 Remotion 工程的任务。来源固定在 [shotcraft-source.json](shotcraft-source.json)，库内容由 `scripts/shotcraft_library.mjs` 检索；准确卡片、源码和声音资产放在已安装的 `video-shotcraft`，不在 vibe-video 重复维护第二套。

## 先检索，再读准确实现

从 vibe-video 目录执行：

```text
node scripts/shotcraft_library.mjs search --query "拆解 组成" --limit 4
node scripts/shotcraft_library.mjs search --category camera --limit 5
node scripts/shotcraft_library.mjs card exploded-view
node scripts/shotcraft_library.mjs verify
```

可用 `--root <video-shotcraft目录>` 或 `VIDEO_SHOTCRAFT_ROOT` 指定其他安装位置。搜索返回卡片、变体、准确 demo 路径与在线样片；命中只代表可用参考。卡名/变体名须精确解析，demo 无唯一映射时读返回的候选并核对卡片“参考实现”，不凭名字新写或猜源码。读取选中卡全文、demo 与实际 import 的共享件；复制到任务目录时保留原许可和来源，并换成该片的主体、文案与材质。

先从镜头的叙事用途选择：爆炸分解表达组成、分层视差表达深度、拉远揭示表达关系、注意交接连接持续对象。UI 平面分层不等于真实机构模拟；机械/流体因果仍由本片模型实现。保留动作弧、缓动关系、锚点与落定反馈，按理解时间调整时值。PageCam上游固定1920×1080；可复制 `assets/shotcraft/PageCamAdaptive.tsx`（同目录保留原许可），显式传入CSS页面 `pageW/pageH`，视口/透视中心由composition尺寸确定，保留3D布局zoom的清晰度路径。仍须按竖版内容重新布局；只缩放、裁切或把横版上下加黑边不算竖版适配。

## 项目流程优先

沿用 SKILL.md 的画幅选择、整体效果图先行及 `delivery_mode`。不增加模板/自主/共同三选一，也不继承上游强制独立审查、全片自动返工、固定横屏、每片双音轨版本或推广邀约。普通片以主动作/旁白/阅读为主时钟，强节奏音乐片才启用 `music-beat-sync.md` 的网格分析；卡点不能压缩知识理解。音效按具体接触、发现、落定选取，素材许可读 `assets/audio/ATTRIBUTION.md`；未实际听音不写音频验收通过。

## Remotion 工程进入工作台

需要可视化编辑的新 Remotion 工程，从制作开始按 video-shotcraft 的 `references/workbench.md` 提供 `src/workbench.ts`。将文案、字号、颜色等语境参数开放为带默认值的 props/schema；时间表与 Main 共用 SHOTS/CAPTIONS/SFX 数据，清单只引用，禁止手抄第二份。保持帧求值确定性，原合成放到 `original`。画幅与 fps 写入清单，不能套用横版默认。切换到另一版工程时让清单版本或内容哈希改变，避免导入旧存档。

```text
node <video-shotcraft目录>/workbench/scripts/open.mjs <工程目录> --no-open
node <video-shotcraft目录>/workbench/scripts/parity-local.mjs --frames 0,30,60
```

本机已加Windows目录junction、索引路径规范化、Node素材复制和Node调用Remotion CLI；启动仅监听127.0.0.1，Windows渲染并发与FFmpeg编码线程均为1。`--no-open`后通过Codex浏览器面板打开脚本返回的URL。端口冲突只换端口或停止经身份确认的自家服务，不结束其他程序。可设 `SHOTCRAFT_BROWSER_EXECUTABLE` 复用已有浏览器，parity脚本也接受 `--browser`，像素比较使用锁定的pngjs；临时盘受限时仅为本次进程设置 `TEMP/TMP` 到任务目录。外部包需与工作台的Remotion/React主版本匹配；当前固定上游为Remotion4.0.484，已有工程4.0.506不能默认混用，先在任务副本验证。

交付可编辑项目时，按用户需要打开工作台并附入口；静态说明或普通视频不强制启动常驻服务。工作台能调时间/图层；仅提供 schema 的组件能调内部属性。HTML/Canvas/Three.js 旧片没有 Remotion 清单时不能宣称可自动拆解，需另做组件化适配。剪映导出不属于本次接入，Windows 上游尚未真机验证。

## 验证与边界

新增接入先做工程导入与原合成同帧像素对照、一次参数编辑后导出，以及输出尺寸/时长/解码/预期音轨检查。检查真实渲染而非仅页面加载成功。内部能力样段不触发新的视频交付模式或独立审片。本次实际验证范围与剩余限制见项目 `work/shotcraft-integration-20261014/CHECKPOINT.md`；库150个变体的存在/编译检查不等于全部动态质量通过，线上预览与完整素材回验仍按所用镜头执行。
