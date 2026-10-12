# 埃及远征 · 水墨新版

60秒，1080×1920，9:16，24fps。十二镜覆盖登陆、行军、结阵与骑兵退却、锚泊舰队受袭、考察与石面记录、将军离去与空岸。暖灰纸底、黑灰水墨，仅少量低饱和身份色和暗赭火光。没有标题、字幕、旁白、地图或箭头。

在本目录打开PowerShell，使用本机已有运行时：

```powershell
$videoNode = 'C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe'
$videoPython = 'C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
& $videoNode ./render.mjs --serve --port=8766
# 浏览器打开 http://127.0.0.1:8766/，播放或拖动时间轴。
```

另一个终端重建：

```powershell
& $videoNode ./validate.mjs --sync-events
& $videoPython ./score.py
& $videoNode ./validate.mjs
& $videoNode ./render.mjs --range=0:60 --width=1080 --out=out/final-rebuild-01
```

每次改变输入后使用新输出目录；未改输入可接续已有帧。指纹覆盖源码、事件、素材、vendor与声轨。Chrome、Playwright和FFmpeg固定路径见render.mjs。主体原生1080×1920绘制，预演缩小输出。

`film.mjs`为总入口；`plan.json`存镜头、事件与步态/划桨时钟；`scenes/`、`actors/rig.mjs`、`actors/horse.mjs`、`camera/subject-camera.mjs`、`compositor/ink.mjs`分别负责场景、人物/骑兵、摄影和合成。11张静态源图存于assets/originals；assets/registry.json含31条登记，其中28个在用组件、3个保留的旧步兵组件。三张高清步兵有效高度约1742–1959px。

工程证据：out/engineering-full.json检查1440帧数值、代表时刻重复/倒序/独立进程哈希、104人中空方阵和旧版历史哈希；各输出目录render-evidence.json记录尺寸、时长、编解码、声轨及全文件解码。声音为原创合成。数值检查不证明构图、步态观感、完整碰撞或听音效果。

人物采用受限图像网格、路径触地与两段腿骨IK；骑兵为四条独立两段腿骨、颈部/骑手转动及缰绳端点绑定的2.5D图像网格，不是完整体积人体/马体或碰撞物理；断桅为解析铰接，水面为解析动画。生成后先展示，未自主观看/听音，视觉未验收。七组历史素材的精确提示词已从本任务记录找回并保存到assets/original-prompts.json；新增三张高清步兵精确提示词见assets/hires-infantry-prompts.json；只有初版infantry-atlas的精确提示词仍缺失，registry明确区分重构简述。

不同事件代表不同地点与时间；不是连续一天。石面清理/记录是艺术重构，刻痕不冒充真实可读碑文，解读不归功于拿破仑。离去仅表现将军离开；不采用轰毁狮身人面像鼻子的传说，金字塔战役不定位于金字塔脚下。旧源码、六张素材与旧影片保留在上级目录。

实际采用与许可见SOURCE-REUSE.md，完成状态与限制见IMPLEMENTATION-AUDIT.md。

最新已交付版本：out/final-20261011-03/current.mp4。60秒、1080×1920、24fps，H264 yuv420p有限范围/AAC 48kHz双声道，完整解码通过，已立即展示。delivery.json锁定成片SHA256、输入指纹和7份证据；前两版和五段预演保留。84个声音事件，53个脚步来自实际路径触地。逐帧接触证据验证骨长、足部网格顶点与目标误差、支撑期世界滑移；不代替审美和听音。第三版另外修正石面被石块倒角遮挡的问题、纸端按真实变形网格接触、桅端相对摇摆船体触水，并调整近景摄影倍率；源像素支持检查目前覆盖代表时刻。
