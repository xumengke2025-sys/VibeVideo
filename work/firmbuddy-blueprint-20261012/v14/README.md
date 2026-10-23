# FirmBuddy V14 · 90秒业务减负之旅

1920×1080横屏 / 30fps / 90秒 / H264 + AAC / 纯音乐无配音。

基于V13原视频增加贯穿全片的业务人员、六次机械卸载、商机判断逻辑与来源工位。原有抽卡、蓝图纸面、专家阶梯会场、九业务分类、六知识槽与人工审核保留。

六项减负：资料分散→客户线索归集；判断费力→来源与判断逻辑；专家难找→多专业协作；依据难找→知识检索；准备重复→跟进材料；记录难接续→经营记录。AI为辅助解读、会商、查证与整理，业务价值是主线。包裹与文字是工作负担的示意，不是实测效率数据。

新增工位依据当前产品统一规则及商机文档，展示融资、并购、股东服务、风险与跨境的来源→判断要点→服务方向，并展示融资阶段筛选。事实与边界见 `opportunity-logic-evidence.json`。公开信号支持线索研判，不代表已确认需求或成交概率；授权客户资料与人工判断仍是业务过程的一部分。

`journey.js`：90秒时序、人物独立世界轨迹、六次卸载、判断工位、新相机连接；`scene-body.js`：原世界与业务机构；`intro.js`：原抽卡和业务说明；`film.js`：最终合并入口；`plan.json`：时间映射、卸载落点及声音事件；`make_audio.py`：沿用原配乐合成音色重写90秒节奏。

从源码包根目录运行（需要 Node、Chrome、playwright-core、Python、numpy；验证接触表需要 Pillow；音频合成需要 imageio-ffmpeg）：

```powershell
python v14/setup.py
python v14/make_audio.py
$env:FIRMBUDDY_PLAYWRIGHT='C:/absolute/path/to/playwright-core/index.mjs'
$env:FIRMBUDDY_FFMPEG='C:/absolute/path/to/ffmpeg.exe'
$env:FIRMBUDDY_FFPROBE='C:/absolute/path/to/ffprobe.exe'
node v14/render.mjs --mode=final --version=my-v14 --duration=90 --width=1920 --fps=30
```

已附混音，可跳过音频重建。运行 `node server.mjs --serve` 后在 `http://127.0.0.1:8768/v14/index.html` 预览。环境变量覆盖现有本机默认依赖路径。

本版先输出实际代码效果图，查看六次卸载的前/中/后状态，再渲染19.6–27.6秒正式样段验证首次卸载至新增工位的过渡，最后渲染90秒成片。工程证据及实际观察范围见交付目录。历史AI审核预算已用，本次用户反馈修改未新增独立审片；完整实际听音与完整正常速度观看未完成，不声称独立视听验收。

原绘图及纸纹参考的来源、固定版本与许可见 `source-transfer.json`、`vendor`。所有版本保留，FirmBuddy产品工程只读。
