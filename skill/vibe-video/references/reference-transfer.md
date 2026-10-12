# 三项重点参考怎样迁移

用于连续变形、角色/主体表演、语义连接或创意返工的改进。2026-10-11 直接核对两个开源工程的固定版本文档和选定源码；没有运行或观看这些上游影片，不宣称它们已在本机复现。

## 1. Functional Emotions：表达形式与事件串联

固定来源：[b34c20a4](https://github.com/ledbetterljoshua/functional-emotions-video/tree/b34c20a4f8f64ee87079a2ae2fdedf2cf1990a49)。它采用自定义 GPU 笔触渲染器，不是 ClaudeAnimationBase 的 p5.brush 工程。代码许可与音乐/歌词权利分开处理；本技能不随附上游音乐。

| 解决的视觉问题 | 已直接读取的入口 | 迁移与验证 |
|---|---|---|
| 精致但创意形式错误 | [README 14–20](https://github.com/ledbetterljoshua/functional-emotions-video/blob/b34c20a4f8f64ee87079a2ae2fdedf2cf1990a49/README.md#L14-L20) 的首版否决记录 | brief 写形式与创意否决条件；独立首次理解观察检查核心事件是否实际成立。作者自述不是本机实测 |
| 分镜任务互相破坏 | [指南18–37](https://github.com/ledbetterljoshua/functional-emotions-video/blob/b34c20a4f8f64ee87079a2ae2fdedf2cf1990a49/ANIMATION_GUIDE.md#L18-L37)、`js/lib.js:224–228` | 精确时间边界、每镜完整帧、共享接口、可写文件约束；短片不照搬七个制作代理 |
| 转场只有效果，没有含义 | [STORYBOARD 39–49](https://github.com/ledbetterljoshua/functional-emotions-video/blob/b34c20a4f8f64ee87079a2ae2fdedf2cf1990a49/STORYBOARD.md#L39-L49)、`js/ch/c1.js:98–110` | 手机锚点发出的线被镜头追随进入下一空间；迁移时记录持续对象、含义变化、下一镜接收状态，检查完整中间态 |
| 道具脱手或发光穿透 | [lib.js 94–151](https://github.com/ledbetterljoshua/functional-emotions-video/blob/b34c20a4f8f64ee87079a2ae2fdedf2cf1990a49/js/lib.js#L94-L151)、`js/ch/c1.js:21–32`、`js/lib.js:231–236` | 姿态返回关节，手机/灯笼共用手部坐标；加光层重绘遮挡轮廓。机械零件和标注共用行程/变换，实际检查接触 |
| 动作与音乐脱节 | `js/lib.js:20–32`、`ANIMATION_GUIDE.md:50–51` | 对实际曲目提取拍点/词级时刻，用共同时间轴驱动事件；本次未重跑其音乐分析，特征数据不能替代听音 |

迁移前先确定适用媒介：夜色、笔触、每秒持续变化、固定拍速属于原作音乐片。科普可停镜读图，可有字幕；机械固定端不能随笔触漂移。语义线→流路→受力关系要以正确知识为边界。

## 2. ClaudeAnimationBase：关键姿态与细节观察

固定来源：[0ac8bf2b](https://github.com/JohnHeibel/ClaudeAnimationBase/tree/0ac8bf2b31942376cb6b8c4074715595d512acd2)。它是 p5.js/p5.brush 角色动画基础工程；此前通过衍生 painted-animation 文档间接接触，本次才直接读选定源码。

- **关键姿态先成立**：[指南99–148](https://github.com/JohnHeibel/ClaudeAnimationBase/blob/0ac8bf2b31942376cb6b8c4074715595d512acd2/ANIMATION_GUIDE.md#L99-L148) 将事件、反应和 reads 分开安排。先验证剪影和意图，再插值；关键动作窗口检查预备、反应、过冲与恢复，不给全部部件同一延迟。
- **表情变化是事件**：[clawd.js:584–615](https://github.com/JohnHeibel/ClaudeAnimationBase/blob/0ac8bf2b31942376cb6b8c4074715595d512acd2/src/clawd.js#L584-L615) 和 `core.js:56–77` 用纯时间状态安排眯眼、交换、take、身体过冲和恢复。可以借给角色或自主飞行主体；衰减正弦/抛物线 helper 是表演示意，不是实际受力求解。
- **局部观察跟着锚点走**：[core.js:302–316](https://github.com/JohnHeibel/ClaudeAnimationBase/blob/0ac8bf2b31942376cb6b8c4074715595d512acd2/src/core.js#L302-L316) 将世界锚点经当前相机投到屏幕，再裁剪每一帧的同一部位；`render.mjs:88–96` 枚举条带每帧。适合阀座接触、弹簧固定端、门框擦碰。用可信数字/锚点 resolver，不从外部数据执行任意 JS 表达式。

验证组合：全帧分页观察确保全局覆盖；关键动作连续窗检查顺序；原尺寸/跟随裁剪检查细节；整体播放检查节奏。局部裁剪不能取代全局审核，生成条带不等于实际看过。角色夸张、无文字、纸纹和永不静止不作为机械/科学视频规则。

## 3. twoclipping：已有研究需要进入作品

[14秒连续UI案例](https://skillry.dev/ai-videos/opus-5-5/twoclipping-402193) 的原作与重制版已在2026-10-09分别取样查看并完整解码；本机8秒无声机制测试240帧接触表已实际查看，见 [opus-gallery.md](opus-gallery.md)。没有原作完整源码，不认证原作全部实现或音乐同步。

可复用 [continuity.mjs](../assets/continuity.mjs) 的对应轮廓、解析弹簧和缩放；迁移目标是同一对象在新语义下继续行动。为转场规定锚点/点对应、进入退出状态、有意义的中间态和理解停留。UI测试通过不证明任意字形 morph、机械流场转换或飞行片结尾有效，需在题材样段验证。

## 把研究状态写清

采用记录分四级：仅提示词/展示、已读固定源码、本机机制已运行并观察、实际作品已采用并审核。登记解决的问题、不适用的条件、与前后镜头的组合方式和最小验证输出。不要因为新增本文，把未执行的两条基准片或上游工程标为通过；也不要把三项参考各做成一套新渲染框架。
