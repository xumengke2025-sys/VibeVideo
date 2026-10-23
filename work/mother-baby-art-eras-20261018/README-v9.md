# 圆毯上的时光 · v9

40秒，1080×1920竖屏，24fps，20个时代按历史顺序排列，有意无声。
宝宝全程手膝爬行绕圆形地毯，妈妈弯腰小步跟随。最后宝宝减速，轻轻栽到软毯上睡着，妈妈停下俯身。

## 运行

Windows 安装 Node.js 后，在源码目录运行：

```powershell
npm install
npm run preview
npm run check
npm run render
```

预览打开控制台打印的本地地址；点击画面播放/暂停。正式渲染输出 `out/mother-baby-20-eras-portrait-v9-40s.mp4`。
`npm run sample` 输出前6秒。可用环境变量 START_SECONDS 和 FRAMES 指定样段起点和帧数。
画面为可寻址Canvas：`renderAt(seconds)`；无墙上时钟驱动的输出动画。

## 修改

- `film/chase-scenes-v9.js` / `timeline-v9.json`：20时代的顺序、颜色、时间、素材路径。
- `film/chase-v9.js`：地毯、路线、手膝支撑、步态、身体与头部朝向、趴下和睡着。
- `film/environment-v9.js`：场景局部植物、帘布、水波、云运动，沿用旧版已生成环境。
- `assets/characters-v9/heads-0.png` 至 `heads-3.png`：内置imagegen生成的20组时代人物头部原图。
- `head-turns.png`、`sleep-head.png`：正背面过渡与睡着表情。
- 同目录 `prompt-*.txt` 保存实际生图提示词。此版采用生成头像与代码绘制的连贯二维身体，未声称整个人物由生成视频驱动。

## 检查范围

`qa/v9/`记录机械检查、实际查看的连续帧和最终MP4工程结果。历史AI审核一轮已用完，本次是用户反馈后的制作修改，未追加独立审片；不宣称正常速度全片审美验收通过。
本版全身构图不使用旧人物裁切素材，不使用桌子/常驻花/咖啡杯或奶瓶。此前蹲姿和迈步概念图已弃用。
原照片不包含在分发包中。参考来源与原许可见 THIRD_PARTY_NOTICES.md / REFERENCE-LICENSE.txt。
