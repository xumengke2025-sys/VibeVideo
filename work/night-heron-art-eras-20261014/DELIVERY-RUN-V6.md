# 夜鹭跨时代狂奔 · run-v6

最终视频：`out/film-run-v6-redrawn-final/video.mp4`。

- 31秒；9:16，1080×1920；48fps，1488帧；双声道AAC。
- SHA256：`23dd981e06cac41ac190d9b0cabc19277c4a86b5eb598fdfa038c79041082958`。
- 16场成片总览：`out/film-run-v6-redrawn-final/styleboard.jpg`。
- 实际动物反应近景：`qa/film-run-v6-redrawn-final/reaction-check-1.jpg` 至 `reaction-check-4.jpg`。
- 源码与素材快照：`out/film-run-v6-redrawn-final/source/`，518文件；同目录 `source-manifest.json` 含逐文件哈希，已核对渲染源码签名。

## 修改内容

16场失鱼动物全部重绘，每场9张，合计144张真实姿势。平静、察觉、后缩、低头寻找、疑惑抬头、惊愕停顿采用共同的动作顺序，按物种保持自然解剖。删除原有失鱼动物的控制点网格变形；新素材仅等比缩放和刚性脚底/躯干对齐，直接播放绘制姿势，不对嘴、口鼻或喙进行拉伸，也不叠化两张头部。鸟喙保持闭合与正常形状，表情通过眼神和头颈动作表达。

年代文字由40px增加至60px（50%），调整各场文字明暗及细轮廓，提高在背景上的可读性；实测标签宽420–600px，预留924px。保留16时代、原有背景、夜鹭跑动/完整吞鱼、前景遮挡与历史版本。

生成使用内置imagegen，参考各时代既有动物图，保持对应色盘、轮廓与颜料媒介。最终素材已保存到项目：`assets/run-v6/owner-01-sheet.png` 至 `owner-16-sheet.png`，拆分姿势为 `assets/run-v6/era-XX/pose-0.png` 至 `pose-8.png`。完整提示词、来源路径及提取参数见同目录 `prompts.json`、`provenance.json`、`manifest.json`。

## 实际检查

主制作实际查看全部144张重绘姿势联系表；先完成埃及→希腊4.25秒正式画幅样段，查看10个反应节点和完整画幅，再扩展全片。

最终MP4的16场总览、80个反应节点、18个动作/转场/结尾局部帧已实际查看，并打开第1344帧完整画幅核对。所查看节点未再发现原先网格拉伸造成的嘴/喙扭曲。部分低头阶段会短暂被前方跑过的夜鹭身体遮挡；九姿势属于逐帧绘制动画，未宣称连续形变或物理模拟。

最终媒体参数、全片音视频解码、浏览器错误检查通过。实际观察范围及限制见 `qa/film-run-v6-redrawn-final/production-check.md`。这是主制作观察，非新独立审核；已有一轮审核预算不重置，未完成最终全片连续观看和完整听音，不能标为完整视听验收通过。

## 重建

```text
node render-run-v6.mjs --mode=video --version=run-v6-rebuild --width=1080
```

入口 `run-v6.html`；主实现 `src/run-v6.js`；动物姿势播放 `src/run-v6-owners.js`。渲染器使用本机Chrome、Playwright及FFmpeg路径，迁移机器需调整相应路径。素材已包含，重建不需再次生图。`extract-run-v6.py` 用于连通轮廓提取、等比缩放和刚性注册；`check-reactions-run-v6.py` 用于成片反应证据提取。
