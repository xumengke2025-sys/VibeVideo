# 雪山钟城：第一篮面包

制作中。目标为 90 秒、1080×1920、24fps 的完整 MP4 与可编辑三维工程；当前尚未完成整片，不把样帧或数值检查当成交付成片。

## 当前入口

- `run-film.ps1`：构建、样帧、43–60 秒连续样段、完整渲染、工程验证与状态查询，详细命令见 `PIPELINE.md`。
- `src/film_world.py`：共享雪山城镇、坡地、建筑、道路、站台、照明。
- `src/film_animation.py`：统一绝对时间的货篮、唯一面包箱、人物、马车、钟楼与摄影。
- `src/film_render.py`：EEVEE/Cycles 与场景深度、倾斜清晰带合成；当前正式渲染使用 EEVEE 64 samples。
- `src/architecture_assets.py`、`craft.py`：新设计的阿尔卑斯建筑与烘焙坊。
- `src/freight_assets.py`、`actors.py`、`carriage_assets.py`：可编辑索道、人物骨架、马车。
- `src/alpine_environment.py`：山谷与雪山，树木采用许可留存的 CC0 资产。
- `src/score.py`、`audio/first-bread-original.mid`：独立原创室内乐编配和合成环境声。

当前生产模型为 `model/clock-city-production-v5.blend`，保留网格、打包材质、人物骨架与机构层级。原始高精度 v2 模型保留；v5 对远景树木采用共享细节层级，缓存静态倒角，并封闭前景雪坡。动画由 `src/film_animation.py` 中的 `at(seconds)` 求值，渲染入口可按帧寻址；直接打开模型不会自动播放程序动画，须由渲染入口调用时间函数。原版模型和本地建模样板仍保留，不覆盖巴比伦工程。

## 验证边界

`render/grounding-report.json` 为道路、楼宇、平台和居民的数值包络检查；`render/actor-transfer-audit.json` 为两位工人的真实骨架接触检查。它们不代表全网格碰撞证明或画面验收。当前未完成全片实际观看或实际听音，独立 AI 审核一轮尚未开始。

正式渲染按版本冻结源码、模型与音轨哈希；工程检查随 MP4 保存尺寸、帧数、时长、音轨、完整解码和成片哈希。只有同一冻结版本的帧才能续渲或复用。

## 素材与运行环境

Blender 4.5.3；本机 RTX 4070 Laptop 8GB、16GB RAM。项目使用全机 Blender 等待队列，避免同时启动多个重型场景；不会结束其他影片的工作。

建筑、机构、道路、服装与配乐为本片重新设计。外部几何/纹理/采样库的来源及许可保存在 `assets/models/CREDITS.md`、`assets/pbr/CREDITS.md`、相应素材目录与 GeneralUser GS 许可文件。仅复用巴比伦的共享世界、绝对时间、移轴合成、分层动作和断点渲染方法，不使用它的建筑几何或音乐。
