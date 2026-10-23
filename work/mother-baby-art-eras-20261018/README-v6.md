# 宝宝与妈妈 · 35时代二维卡通 v6

正式输出：`out/mother-baby-35-eras-portrait-v6.mp4`。9:16，1080×1920，24fps，175秒，4200帧；沿用有意无声方案。

每个时代5秒，宝宝完整抱瓶喝奶、妈妈完整举杯喝一口，然后放稳再转场。前后时代共享相机与环境时钟。主体、服饰、道具和环境的绘画媒介同步改变。

## 本次修复

- 固定两段手臂长度，缩短旧臂长并注册到躯干肩点；可达腕点与道具握点一致，避免靠缩放前臂补差。
- 避开手腕经过肩点引起的肘部翻转；手臂独立转动，人物躯干不做网格拉扯。
- 每场完成动作后再进入24帧环境过渡，人物6帧短叠化；仍可能出现几帧衣饰重影，非拓扑连续变形。
- 保留前景枝叶摆动、飘叶、咖啡蒸汽、环境视差和连续相机。
- 合成时按来源矩形排除桌子旁的椅子碎条和蓝色时代人物下缘误裁头部。源图只读。

## Windows运行

需要Node.js。`npm install`后：

```text
npm run sample
npm run render
npm run check
```

默认入口`film/index-v6.html`，主实现`film/rig-v6.js`，离线渲染`render-v6.mjs`。`renderAt(t)`可按绝对秒数寻址；点击网页中的画布可播放内部预览，正式交付仍是MP4。

素材：`assets/rig-v4/00–34`内的分层人物/手臂/杯瓶/桌子/前景与`assets/generated-v2/layers/*/background.jpg`。生成图不代表动作已验证，实际动画由上述合成与关节代码渲染。

## 验证及限制

4200帧关节几何检查记录于`out/fixed-bone-check-v6.json`。实际整片解码及哈希见`qa/v6/full/engineering-check.json`，修改处连续帧与关键帧索引见`qa/v6/final/evidence.json`。这些工程检查不等于审美验收。

沿用原唯一审片者做必要局部复核。旧v5覆盖不继承为v6通过；最终覆盖与限制见`qa/v6/production-notes.md`及同一审片者记录。没有音轨，无需声称完成了听音审核。

参考来源、固定版本与采用边界见`research/REFERENCE-TRANSFER.md`；转场研究见`research/transition-study-v5.md`和`research/transition-and-rig-v6.md`。运行素材包不包含用户原照片、node_modules或历史成片。
