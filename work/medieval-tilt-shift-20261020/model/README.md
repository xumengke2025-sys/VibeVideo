# 巴比伦城门与街区：模型质量样板

当前交付对应 `babylon-city-v8.blend`，已完成56秒、1344帧影片渲染。摄影入口为 `../render_city_v8.py`，现行说明见 `../delivery/工程入口-v8.md`。下文保留早期模型制作记录，不作为当前版本状态。

用户已取消龙。此工程只制作建筑、街道、水面与少量尺度参照。

`build_city.py` 为独立原创 Blender 建模脚本，生成真实三维砖、拱门、浮雕、建筑、陶器、布棚与棕榈。使用 Cycles，模型验证视角关闭景深。概念图仅作为方向参考，没有投影进模型或放在背景冒充几何。

第一版已生成 `babylon-gate-street-v1.blend`，以及 `out/gate-street-v1.png`、`out/glaze-detail-v1.png`、`out/street-reverse-v1.png`。制作检查发现釉面偏哑、浮雕圆钝、城市背景不足；此版保留为历史样板，脚本保存在 `build_city_v1.py`。

当前 `build_city.py` 输出目标为 `babylon-city-v2.blend`：重做浅浮雕及釉面，扩展连通街区、神庙、运河、两座桥与船只。对应四个无景深验证视角为 `out/city-overview-v2.png`、`out/gate-street-v2.png`、`out/glaze-detail-v2.png`、`out/canal-temple-v2.png`。文件是否已实际完成以当前 CHECKPOINT 和渲染日志为准。

模型样板属于制作检查，尚不是影片，也不占用用户选择的一轮最终AI审片。连续运镜、移轴后期、活动细节和正式配乐仍需后续制作。

当前可编辑版本为 `babylon-city-v3.blend`。运行 `polish_city.py` 从 v2 生成 v3：用院落模块替换远景方块，增加街区朝向与高度变化、前景街区、棕榈叶片及柏树针叶，并调整侧光。三个实际输出为 `out/city-overview-v3.png`、`out/gate-street-v3.png`、`out/canal-temple-v3.png`，均为 1080×1920、Cycles、关闭景深的模型验证图。

三张 v3 图均已由制作角色查看。当前模型仍有建筑重复、空街、神庙露台和立面细节不足、地平线生硬的问题，城门阴影也偏暗。没有达到已认可概念图的自然丰富度，不能称为完美模型或最终摄影质感。先完善这些可见问题，再验证真实遮挡的地平线显城和斜俯移轴连续样段。

参考代码机制：Lemo《Toy Town Rush Hour》的真实深度移轴后期、连续相机与独立背景时间轴。Blender模型本身未复制其城市几何。旧预演中实际采用的 `post.js` 及MIT许可保存在 `../film/`；不能把参考机制研究说成新模型已接入影片。
