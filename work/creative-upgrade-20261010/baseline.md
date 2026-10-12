# 修改前基线

2026-10-10。真实安装入口 `D:/Codex/skills/vibe-video/SKILL.md` 0.9.0；项目快照0.7.0。Node D:/docker/node.exe、捆绑Python3.12/Pillow、Chrome、playwright-core、Three.js、Remotion compositor FFmpeg/ffprobe均有本机路径；后续运行取证，不以文件存在代替通过。

## 生产链路和职责

Brief → director-design镜头表 → art-direction/motion-craft → 按内容选Canvas/Three/Remotion → renderAt绝对时间 → render.mjs浏览器逐帧/JPEG缓存/FFmpeg → video_evidence媒体及代表帧 → frame_audit连续帧 → shot_contract日志匹配 → 交付。

- `references/opus-methods.json`/`opus-source-index.json` + `scripts/opus_methodology.py`：35方法卡、513来源条目、固定commit/源码锚点及参考角色。
- `assets/motion.mjs`、`continuity.mjs`、`subject-camera.mjs`、`cinematic-starter/camera-kit.mjs`：缓动/种子/投影、解析弹簧/缩放/形变、绝对时间伴随摄影、位置目标双路径。
- `assets/style-studio/{timeline,film,render}.mjs`：事件驱动蓝图/数据片段，视听契约和导出。
- `work/camera-upgrade-20261010/demo/film.js`：8秒金色飞行器/蓝黑柱阵；有主体伴随与结尾拉远，环境不响应。
- `work/portrait-valve-20261009/film.js` + `clips/one-way-portrait.json`：15秒纵向Canvas剖面，阀瓣下移94px、弹簧下端固定、回座后停止正向箭头；标题从首帧给出结论，相机缩放只有3.5%。
- 相关技能：remotion、video-shotcraft、白板mask/stream、SRT白板、视频脚本/开头、imagegen。它们负责特定制作路线；本轮不修改其调用边界。源资料多栈混合，不能统一成一个新引擎。

## 能力审计

|能力|现状|最小补足|
|---|---|---|
|创意构思|有观众路径与视觉惊喜要求；没有差异候选/选择产物|三个事件机制不同的候选，选择与删减依据|
|艺术指导|已有材质、光照、字形、代表帧流程|保留，增加按视频类型的目标/禁用条件|
|分镜/镜头|已有intent、states、连接、主体相机|将期望与实际屏幕动作区对应|
|运动|已实现解析弹簧、确定性跟拍、曲线|缺受限机械行程与场景因果调用样例|
|编排|已有事件表、音画共享与阅读约束|保留，不引入新时间轴|
|变形|已有显式点对应、门户/连续对象卡|补组合、输入输出、成本和不适用条件|
|参考库|35卡已有purpose、relation、implementation、failure、review、source_refs|沿用JSON和检索入口补重要卡操作元数据|
|自动审片|真实帧提取/技术解码已实现；观察由Agent完成|执行器串联现有工具；连续窗口/哈希核对|
|自主返工|文档要求修具体问题|记录前三问题、修改窗口、前后证据及停止条件|
|质量验收|技术/视觉分开；无类型维度/权重对比|类型权重、时间码证据；评分只能辅助|

## 可验证瓶颈与最小文件集合

原飞行器subject(t)是正弦曲线，环境由初始化后静止对象构成，8秒唯一变化来自路径/镜头。阀首帧标题“只向一个方向”及字幕“单向通行”先给答案；94px行程相对1920高画面很小；镜头表写靠近/跟随，但实现仅整图1.035倍缩放。渲染器sourceHash只算index.html/film.js/camera-kit.mjs，修改timeline/导入模块/JSON不会失效已有JPEG缓存。

修改：入口；director-design/motion-craft/visual-review三个已有参考；既有方法JSON与检索；必要的机械/事件薄函数；复用render.mjs补完整缓存指纹；一个串联既有提取工具的审片执行器。新增指导按需加载，不把全部内容塞进入口。源案例拷贝到本轮独立目录，旧版原封保存。

验证：技能frontmatter/全部本地链接/源码卡锚点；寻址及机械受限状态测试；两例低成本动态预演、1080×1920完整MP4、全解码、代表帧和连续动作窗实际查看；前三缺陷→局部返工→新版核对。蓝图/数据旧片段运行回归，避免只验证两个样片。保留原/改进帧、哈希、命令与剩余边界。
