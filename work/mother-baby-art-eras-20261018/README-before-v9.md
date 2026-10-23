# 宝宝与妈妈 · 35时代独立动作（v8）

交付：40秒，1080×1920，24fps，35种二维画风，有意无声。

每个时代独立完成一个呼应场景的小动作。服饰、绘画风格、道具随时代改变；保留小人物、大环境、妈妈右侧和宝宝左下方的构图。咖啡和奶瓶只出现在各自场景，不重复循环饮用。

## 运行（Windows / Node.js 18+）

```powershell
npm install
npm run preview
npm run render
npm run check
```

预览打开 http://127.0.0.1:8768/film/index-v8.html ，点击画面播放/暂停。渲染输出 out/mother-baby-35-eras-portrait-v8-40s.mp4。首次使用 Remotion 可能需要下载浏览器。

## 修改

- `film/actions-v8.js`：35个动作、时间和关节目标。每场独立，不跨时代继承动作。
- `film/interaction-v8.js`：生图道具、接触关系、场景反馈、环境局部运动。
- `film/rig-v8.js`：角色分层、固定骨长、摄影机、转场及合成。
- `build_v8.py`：从保留的v7骨架重建v8；修改骨架时同步修改此生成器，避免重新生成覆盖。
- `assets/interaction-v8`：20个透明生图道具、母图、原始提示词和切分记录。
- `PLAN-v8-independent-scenes.md` / `timeline-v8.json`：逐场动作表。

源素材中的人脸是二维绘制，不贴照片。部分旧角色发顶平截仍可见；人物切换采用约3帧短叠化，可能出现短暂双轮廓。环境有局部枝叶、窗帘、水面和云运动，仍属于二维分层动画。

## 检查范围

全960帧骨长、可达性、握杯及喝奶接嘴约束检查；乱序与重载像素检查；成片完整解码、尺寸、时长和无音轨检查。

制作方实际查看35个场景中间姿态，以及30–32秒、36–37秒、38–40秒样段的连续角色裁切帧。其余成片抽查时间码见qa/v8/production-review.json。未完成正常速度全片感知检查，不声明完整独立审核通过；沿用原一轮审核预算，不新增审片轮次。

历史v7和原始输入保留在原项目中。素材授权与参考来源见THIRD_PARTY_NOTICES.md、REFERENCE-LICENSE.txt及research/。
