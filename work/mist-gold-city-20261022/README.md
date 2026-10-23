# 雾金之城

原创十八世纪奇幻山城移轴短片工程。竖屏 1080×1920、24 fps、90 秒；城市、桥、车辆、居民、船只均为可编辑三维几何。历史版本位于 `history/`，巴比伦旧工程未被修改。

## 文件与修改入口

- `model/fog-gold-city.blend`：完整城市、材质、人物与机械模型。模型按街区、地标和活动主体命名。
- `model/urban-layout.json`：不规则街区、院落、道路和保护区坐标，单位米。
- `src/generate_layout.py`：街区、道路与地块生成；改变随机种子或道路控制点后重新生成布局。
- `src/build_world.py`：重建世界的入口；建筑样式在 `mountain_city.py`，不规则地块装配在 `organic_city.py`。
- `src/terrain.py`：道路、地基和居民共同使用的地形高度。
- `src/build_actors.py`：人物、船、马车、马匹及父子关系。
- `src/timeline.py`：90 秒摄影机轨迹及升桥、船、邮车的共享时间轴。
- `src/render_film.py`：逐帧动画、光照渲染和随关注点变化的深度／倾斜清晰带合成。
- `src/compose_score.py`：原创音乐与环境声源代码；`audio/` 保留音乐、音效、混音及音符／声音事件表。

动画由绝对时间计算，并非烘焙的物理模拟。直接打开 `.blend` 可以改模型；用 `打开动画工程.ps1` 启动可以拖动时间轴预览动作。每次重建会从源码覆盖 `model/fog-gold-city.blend`，手工修改请另存 `.blend` 并调整渲染入口。摄影机镜头不含文字或 UI。

## 运行

本工程使用 Blender 4.5.3、Python 3.12、NumPy、Pillow；布局生成另用随工程保留的 SciPy/Shapely；配乐另用 `vendor/` 的 tinysoundfont 与 `assets/GeneralUser-GS.sf2`。当前渲染设置使用 NVIDIA OptiX GPU。

在项目目录运行 `制作.ps1 -Mode layout` 生成地块，`-Mode build` 重建模型，`-Mode sample` 渲染 40–72 秒动作样段，`-Mode full` 渲染／续渲完整影片，`-Mode assemble` 重新封装已有完整帧。可通过 `BLENDER`、`FFMPEG`、`FFPROBE` 环境变量指定运行时。

渲染版本由 `FOG_VERSION` 指定，当前为 `organic-final-v2`。每个版本保存输入哈希；源码、模型或音轨变更后使用新版本名，避免把不同时期的帧混合。有效 PNG 会跳过，未完成帧先写入 `.partial.png`，完成后原子改名。正式输出为 `delivery/` 下的 MP4。

## 制作依据与素材

城市为原创生成几何，参考照片与油画没有作为画面贴图使用。布局吸收历史布拉格俯瞰中的曲折街巷、围合院落与不同尺度屋顶，以及爱丁堡山脊主街／分叉巷道的空间特点；这些后来拍摄的城市照片不代表未经变化的十八世纪。绘画参考为 Canaletto 的圣马可广场与 Hubert Robert 1773 年的门廊作品。具体文件和元数据在 `references/`。

音乐未沿用巴比伦短片。原创 D 大调三拍子乐段使用 GeneralUser GS 的弦乐、木管、羽管键琴与圆号采样；声音为代码合成。SoundFont 原许可在 `assets/LICENSE-GeneralUser.txt`，允许私人和商业音乐制作，原许可的样本来源说明一并保留。

## 验证边界

`qa/constraints.json` 记录道路／地标保护区、船与桥净空、停车距离等数值检查；并非全城所有动态网格的碰撞证明。最终编码、完整解码、画幅、时长与音轨检查记录随成片放在 `qa/organic-final-v2/`。

交付方式为 AI 审核一轮。审核覆盖以同目录实际审核记录为准。当前工具不能把声音提供给模型实际听辨，因此音乐听感和实际音画同步听审不能标为通过；音频解码与信号检查不替代听音。
