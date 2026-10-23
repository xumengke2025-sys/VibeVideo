# 十八世纪阿尔卑斯建筑资产

本组为《雪山钟城：第一篮面包》的制作资产，不是独立审片结论。复用已认可烘焙坊的 `craft.py` 材质和建造尺度，模型原创建造，纹理沿用工程内已有 CC0 PBR 材料。

## 调用

```python
import craft as C
C.palette()
import architecture_assets as A
assets = A.build_variants()
assets['inn'].location = (x, y, z)
assets['inn'].rotation_euler.z = angle
```

`build_variants()` 返回 `inn/workshop/grocer/cottage/chapel/tower` 对应的 Blender 根 Empty。入口不清空场景，不改变相机、灯光或时间轴。各资产源坐标为米，Z 向上，正门朝局部 -Y，根位于地面。所有几何、灯具和字牌均在对应根的后代中，可整组布置。不要分别移动子网格。

`architecture-library.blend` 是带摄影棚布局的可编辑资产库，包含六个根及地面/灯光/相机。整合影片建议调用源函数；从 `.blend` 追加时只取对应根及其后代，忽略 `ARCH_STUDIO` 对象。图像贴图已打包。

| 返回键 | 根名 | 主体尺度与差异 |
|---|---|---|
| inn | ARCH_INN | 主楼6.7×5.4m，檐高5.36m；长木廊、门前廊柱、侧面独立低马厩；总占地约9.85×7.1m |
| workshop | ARCH_WORKSHOP | 主楼4.6×5.2m，檐高5.36m；外凸钟表展示窗、陈列小钟、侧面阁楼台阶 |
| grocer | ARCH_GROCER | 主楼5.7×4.7m，檐高4.5m；四坡屋顶、布篷及低货箱 |
| cottage | ARCH_COTTAGE | 主楼4.25×4.6m，檐高4.6m；局部小阳台、单坡柴棚 |
| chapel | ARCH_CHAPEL | 窄长石砌4.9×8.4m，高约8.55m；扶壁、拱窗、尖屋顶与十字架 |
| tower | ARCH_TOWER | 石砌主体3.8×3.8m，屋檐最大4.7m见方，高18.6m；四面珐琅钟、开放钟架、铜绿尖顶 |

所有建筑都有实际壁厚/窗口空洞、分离窗框与玻璃、独立木板、屋面/积雪结构。雪面在屋脊、屋檐和风向处有厚薄变化。旅馆/工坊/小住宅保持山地家庭相似性，但尺寸、结构、功能和附属构筑各异；杂货铺使用四坡屋顶。

## 钟楼动画接口

`assets['tower']['animation_parts']` 为 JSON 字符串，包含下列名字：

- `hammer`: `ARCH_TOWER | HAMMER_PIVOT`
- `bell`: `ARCH_TOWER | BELL`
- `bird`: `ARCH_TOWER | BIRD_BODY`
- `wing_left`: `ARCH_TOWER | BIRD_WING_L`
- `wing_right`: `ARCH_TOWER | BIRD_WING_R`
- `hammer_contact_y`: `0.0`
- `hammer_rest_y`: `0.32`

钟锤绕局部 Y 枢轴转动。枢轴在钟楼局部 `(-1.50, 0, 13.90)`，锤头局部 `(0.78, 0, -0.68)`；`rotation_euler.y=0` 时锤头与钟口外缘轻微接触，`0.32` 为离开状态。有可见横梁、铁轴承板与黄铜轴套，杆和锤头同属于枢轴。钟体起点局部 `(0, 0, 13.12)`，是空心旋转体，含独立几何钟舌。

鸟身在钟楼局部 `(0, -2.33, 8.69)`，左右翼有实物铰轴。左翼 `rotation_euler.y=-1.05`、右翼 `+1.05` 为收拢；两翼均为 `0` 时展开。各翼根也有 `closed_y_rad` 与 `open_y_rad` 属性。鸟与钟锤均未写关键帧，供影片按绝对时间驱动。钟面初始化为08:00，时针/分针分别有命名根，见 `ARCH_TOWER | clock 0 | hour hand` 等。

## 实际渲染与检查

- `render/architecture-assets/commercial-quarter.png`
- `render/architecture-assets/chapel-clocktower.png`
- `render/architecture-assets/clock-mechanism-detail.png`
- `render/architecture-assets/asset-manifest.json`

第三张机构近景使用鸟翼展开、钟锤接触的检查姿态；资产库保存的是收翼/离开姿态。两者不应混淆成动画已验收。

首轮内部540×960检查已实际观看，修复了钟锤缺可见支承的问题，新增不同四坡屋顶和阁楼窗洞后输出1080×1920。此处只检模型与接触姿态，尚未验证整片运动、声音或与其他资产的避碰。最终影片中的山地基础、道路连接及遮挡仍由共享场景整合检查。

已知限制：此为历史风格原创设计而非文物级复原；窗口采用实体发光玻璃背板，不含完整室内房间；教堂拱窗背板由矩形开口与石券遮蔽构成，室外目标机位成立；模型库未包含钟楼内部全套走时轮系，已有可动画敲钟及鸟翼装置。
