# 妈妈与宝宝 · 35种时代画风 · v5

9:16，1080×1920，24fps，41.25秒，有意无声。妈妈举杯喝咖啡，宝宝双手抱奶瓶喝奶。二维卡通、小人物与大环境，35时代同步改变人物与环境的平面画法。

本版改动：生成素材拆成稳定躯干与独立手臂，由两骨IK驱动；不再对整个人物做网格形变。背景、人物和枝叶分层合成；场界两侧共14帧环境过渡，约5帧整体人物叠化。背景使用宽羽化颜料扩散、纸张方向或普通叠化，不再将人物切成瓦片。相机、举杯/喝奶和枝叶摆动沿用绝对时间，不在场界清零。此为动作匹配和叠化，不宣称拓扑连续变形。

## 可编辑入口

- `film/index-v5.html`：预览画面；加载后点击画面播放/暂停，控制台`renderAt(seconds)`精确定位。浏览器预览播放不参与离线渲染。
- `film/rig-v5.js`：人物关节、动作、分层、环境运动与转场。
- `film/eras.js`：35时代名称、年份、配色和场界时间。
- `film/rig-anchors-v4.js`：逐时代口部锚点；`film/rig-manifest-v4.js`：素材路径。v5继承这两份已经提取的素材配置。
- `assets/rig-v4/`：图层、生成原始部件图、提取记录和提示词。有效角色不含旧的整身网格动作。
- `assets/generated-v2/layers/*/background.jpg`：35时代生成背景。
- `render-v5.mjs`：逐帧视频输出。
- `qa_transitions_v5.py`：完整解码、转场连续帧、接触表与基本媒体检查；输出不是自动审美判断。
- `research/transition-study-v5.md`：本次资料、实际观察、方案选择及边界。

## 运行

在本目录安装package.json依赖后：

```powershell
node render-v5.mjs sample
node render-v5.mjs check
node render-v5.mjs full
```

渲染器临时开启只监听127.0.0.1的HTTP服务，结束后关闭。浏览器预览也须通过本地HTTP服务加载素材，不能直接用file协议。点击播放仅为人工预览；离线导出全部通过renderAt(frame/24)生成，不依赖播放时钟。

Python证据脚本需要Pillow。使用`python qa_transitions_v5.py full`提取成片；FFmpeg路径位于脚本开头，换机器需修改。渲染器按本机Windows Remotion compositor包解析FFmpeg，其他系统需换为相应二进制。无需生图API即可用现有素材重渲染。

## 实际验证与限制

已完成的检查和真实审核范围以`qa/v5/`与CHECKPOINT为准。新版本不继承旧版全片通过结论。整个人物短叠化可能出现不同服装、发型的几帧重影；这是当前素材之间的换画边界，不能声称已做到连续形体变换。正常速度观感未被模型实际感知时，连续帧观察也不等于正常速度审片。

参考来源和许可沿用`THIRD_PARTY_NOTICES.md`与`REFERENCE-LICENSE.txt`。参考发布视频与研究的源码版本不同，不宣称逐像素复刻。
