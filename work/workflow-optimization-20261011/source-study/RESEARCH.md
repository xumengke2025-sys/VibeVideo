# 两个上游项目的直接源码研究

日期：2026-10-11。范围：公开、固定 commit 的文档和少量 JavaScript 源码。没有运行上游工程、查看视频、试听音乐、下载媒体资产或证明上游观感。研究结论是机制适配建议，不是影片质量验收。

## 固定来源与阅读范围

| 项目 | 固定 commit | 本地保存与直接阅读 |
|---|---|---|
| [Functional Emotions](https://github.com/ledbetterljoshua/functional-emotions-video/tree/b34c20a4f8f64ee87079a2ae2fdedf2cf1990a49) | `b34c20a4f8f64ee87079a2ae2fdedf2cf1990a49` | README、ANIMATION_GUIDE 全文；STORYBOARD 开头/第一章；check/render 脚本；lib 的关节/姿态/音乐/章节/遮光段；c1 的手机、发光线、升起、运镜段；cast 保存但不作为未读内容的证据 |
| [ClaudeAnimationBase](https://github.com/JohnHeibel/ClaudeAnimationBase/tree/0ac8bf2b31942376cb6b8c4074715595d512acd2) | `0ac8bf2b31942376cb6b8c4074715595d512acd2` | README 全文；ANIMATION_GUIDE 的叙事/reads/动作/工作流/审核段；core 的时间、运动、相机和 renderSheet；clawd 的情绪时间轴；timeline；render CLI；studio 入口保存 |

原始源码放在同名子目录。`*-metadata.json` 保存 GitHub API 返回的仓库、分支、commit 和路径树；`source-manifest.json` 保存下载文件的 SHA256 与固定 URL。本地源码仅供研究，不代表整仓可运行副本。

## Functional Emotions：可迁移机制

### 1. 创意目标能否成立，先于表面精致

证据：[README L14–20](https://github.com/ledbetterljoshua/functional-emotions-video/blob/b34c20a4f8f64ee87079a2ae2fdedf2cf1990a49/README.md#L14-L20) 记录首版精致歌词视频被否决，第二次明确要求故事和场景，第三次按节奏参考重剪第一章。这里是作者自述，不是本次独立重建的生产证据。

迁移：导演简报除了尺寸/画风，还应写作品形式、核心事件、观众最后理解的变化、不可接受的替代形式。独立审核可以判“技术正确、表达形式错误”；此类问题退回概念或分镜，不能只加光效、粒子和运镜。短机械片的否决理由应是关键原理读不出来、没有因果演示；不能以音乐视频的“不得是歌词片”标准否决知识字幕。

### 2. 分工靠具体契约，不靠人数

证据：[ANIMATION_GUIDE L18–37](https://github.com/ledbetterljoshua/functional-emotions-video/blob/b34c20a4f8f64ee87079a2ae2fdedf2cf1990a49/ANIMATION_GUIDE.md#L18-L37) 明确一章一文件、完整帧、纯时间函数、私有 helper、共享文件只报告缺陷、章节精确止于边界。[lib.js L224–228](https://github.com/ledbetterljoshua/functional-emotions-video/blob/b34c20a4f8f64ee87079a2ae2fdedf2cf1990a49/js/lib.js#L224-L228) 实际把章内时间表注册为 shot，下一项起点成为上一项终点。

迁移：镜头任务契约应明确时间范围、构图/相机入口出口、主体状态、共享资产接口和可改文件。主制作角色独占共享约束与最终集成。8 秒或15 秒作品不必用七名子代理；短片优先保留导演/制作/独立审片的清晰职责，只有相互独立的任务才并行。

### 3. 语义桥接有具体起点和落点

证据：[STORYBOARD L39–49](https://github.com/ledbetterljoshua/functional-emotions-video/blob/b34c20a4f8f64ee87079a2ae2fdedf2cf1990a49/STORYBOARD.md#L39-L49) 以手机发出的光线→城市多线→河流→瀑布→湖中主体组织意义。[c1.js L98–110](https://github.com/ledbetterljoshua/functional-emotions-video/blob/b34c20a4f8f64ee87079a2ae2fdedf2cf1990a49/js/ch/c1.js#L98-L110) 实际从手机返回的坐标发出 Bézier 光线，相机沿升起方向离开室内，末段 smear 处理快速移动。

迁移：为每次语义转换记录持续对象/形状、空间锚点、含义变化和下一镜头接收状态。飞行轨迹→路径图、流体方向→压力分布→阀瓣受力可以借鉴；“使用 whip”本身并不构成语义桥接，知识正确性仍需制作时检查。

### 4. 道具绑定与光层遮挡都有源码实现

证据：[lib.js L94–151](https://github.com/ledbetterljoshua/functional-emotions-video/blob/b34c20a4f8f64ee87079a2ae2fdedf2cf1990a49/js/lib.js#L94-L151) 由姿态角计算关节并返回，灯笼直接从 hdR/hdL 挂载；[c1.js L21–32](https://github.com/ledbetterljoshua/functional-emotions-video/blob/b34c20a4f8f64ee87079a2ae2fdedf2cf1990a49/js/ch/c1.js#L21-L32) 手机来自左右手平均位置。[lib.js L231–236](https://github.com/ledbetterljoshua/functional-emotions-video/blob/b34c20a4f8f64ee87079a2ae2fdedf2cf1990a49/js/lib.js#L231-L236) 在 additive light 层重画黑色轮廓避免背后发光穿过身体。

迁移：飞行器灯、尾焰、检测环，阀瓣、阀杆、弹簧连接点、受力箭头应共享主体状态和变换；不能各自独立补坐标。基于统一锚点进行位置检查后仍需实际查看接触和遮挡。此方法不是三维深度系统或物理求解器。

### 5. 音乐事件驱动，不是任意 sin(t)

证据：[lib.js L20–32](https://github.com/ledbetterljoshua/functional-emotions-video/blob/b34c20a4f8f64ee87079a2ae2fdedf2cf1990a49/js/lib.js#L20-L32) 有特征采样、二分搜索节拍和衰减 pulse；[ANIMATION_GUIDE L50–51](https://github.com/ledbetterljoshua/functional-emotions-video/blob/b34c20a4f8f64ee87079a2ae2fdedf2cf1990a49/ANIMATION_GUIDE.md#L50-L51) 给出节拍/歌词词级时间 API；README L31 的 Demucs/Whisper/对齐流程是文档描述，本次未重跑分析。

迁移：有音乐时把关键事件锚定实际 downbeat/onset，有旁白时先保证句意可读和事件跟随语义，再安排重音。85.7 BPM、固定 beat index、歌词工具链不能直接复制到新片。音频特征、波形、ASR 都不能替代真实听音。

## ClaudeAnimationBase：可迁移机制

### 1. 姿态表先成立，再插值

证据：[ANIMATION_GUIDE L115–148](https://github.com/JohnHeibel/ClaudeAnimationBase/blob/0ac8bf2b31942376cb6b8c4074715595d512acd2/ANIMATION_GUIDE.md#L115-L148) 给出事件、反应、reads 时间表，并要求先检查关键姿态再加中间运动。L99–108 包括预备、重量、跟随、避免 twinning 和眼睛先行。

迁移：飞行器建立发现障碍/减速/选择/通过/恢复的姿态节点，动作偏移应由事件、方向或曲率驱动；阀门建立闭合/临界开启/行程限制/逆压封闭关键状态，保持机械约束。夸张、squash/stretch、故意左右不对称是卡通角色技巧，不应让刚性阀件变形或破坏实际对称机构。

### 2. 情绪变化是短事件，不是切换字符串

证据：[clawd.js L584–615](https://github.com/JohnHeibel/ClaudeAnimationBase/blob/0ac8bf2b31942376cb6b8c4074715595d512acd2/src/clawd.js#L584-L615) 提前 squint、交换面部、take、body 的 backOut 过冲、颜色淡变、恢复和 emote pop；[core.js L56–77](https://github.com/JohnHeibel/ClaudeAnimationBase/blob/0ac8bf2b31942376cb6b8c4074715595d512acd2/src/core.js#L56-L77) 用纯时间 spring/jump/take 描述预备与落地恢复。

迁移：角色片可完整采用“注意→预备→反应→恢复”；飞行器可用灯/姿态/推进响应表达意图；机械片只用适用的阻尼响应和事件分段。`spring()` 是衰减正弦视觉 helper，`jump()` 是抛物线示意，不能当作实际力学模型。

### 3. 三层视觉审核与随锚点裁剪

证据：[ANIMATION_GUIDE L169–200](https://github.com/JohnHeibel/ClaudeAnimationBase/blob/0ac8bf2b31942376cb6b8c4074715595d512acd2/ANIMATION_GUIDE.md#L169-L200) 规定全片结构 sheet、重要动作/转场的逐帧 strip、接触/脸/道具的全分辨率 crop。[render.mjs L88–96](https://github.com/JohnHeibel/ClaudeAnimationBase/blob/0ac8bf2b31942376cb6b8c4074715595d512acd2/render.mjs#L88-L96) 枚举 strip 区间每个 frame；[core.js L302–316](https://github.com/JohnHeibel/ClaudeAnimationBase/blob/0ac8bf2b31942376cb6b8c4074715595d512acd2/src/core.js#L302-L316) 按每帧 LAST_CAM 将固定世界点转换到屏幕，中心裁剪同一区域，标时间码。

迁移：独立审片在全帧覆盖之外，对门框擦碰、阀瓣座面、弹簧固定端、流线穿透加锚点跟随 crop。缩略接触表不能证明细节可读，导出 strip 不能证明审核者已经看过，crop 也不能替代全局构图和实时节奏查看。工具原实现有页面表达式 eval；适配时优先数字/可信锚点 resolver，避免让外部数据作为任意 JS 执行。

## 不应机械照搬的规则

- 两项目主要是 1920×1080 横屏；本项目必须重新构图为 1080×1920 竖屏，不能简单缩放或裁切。
- “一秒无变化就是 bug”“相机始终运动”“每个切口都转场”“不得文字/3D”等是对应音乐/手绘角色风格约束。知识片需要读图停留、字幕和稳定的机械参照。
- Functional 的 1.4–4 秒镜头、固定 palette、约 60k brushstrokes 和 ClaudeAnimationBase 的纸纹/水彩不是质量提升的通用条件。先让事件与因果读出来，再选择表现媒介。
- 七章并行与多渲染 worker 是不同层面的并行：前者涉及创意/共享代码冲突，后者要求渲染纯函数且机器可承受；不能把两者合并成无条件多模型配置。
- Functional `check.mjs` 使用 `/tmp`、Chrome Metal 参数和文件 URL；不是 Windows 通用工具。本次只读，未尝试执行。
- 上游示例中的“看图直到漂亮”应适配现有最多两轮修复与复核；达到上限仍不通过就诚实交付当前状态，不无限返工。

## 建议接入优化计划的可验收项目

1. 导演卡明确作品形式和否决条件；关键样片若形式失败，回到分镜而非堆特效。
2. 制作/审片交接加入时间范围、入口出口、主体状态和共享接口；独立审核首遍仅获最低必要目标，避免剧透解释代替观感。
3. 用统一锚点做接触和局部观察，把关键姿态/事件/恢复写成纯时间状态；乱序 seek 与重复渲染验证确定性。
4. 在 8 秒飞行器和15 秒机械片中各验证一个具体机制，保持题目、画幅和时长便于比较；同时记录视觉覆盖和全音频实际听音，未执行就保持 pending。
5. 语义桥接必须能说明持续对象和含义，不以转场数量、粒子数量、模型数量代替内容质量。

