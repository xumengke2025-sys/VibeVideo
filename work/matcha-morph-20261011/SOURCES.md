# 制作依据与素材许可

核对日期：2026-10-11。以下为制作路线的简化示意，不是工厂设备复原。

## 工艺资料

- 日本农林水产省《Uji Tea》：https://www.maff.go.jp/e/policies/market/dento_syoku/menu/uzi_tea.html 。覆下栽培、蒸青、不揉捻干燥制碾茶。用于11–15秒字幕与不揉捻动作。
- 丸久小山园《Growing and Processing of Matcha》：https://www.marukyu-koyamaen.co.jp/english/about-tea/know-matcha.html 。介绍遮阴、采摘、蒸青、干燥及后续精制、去梗叶脉、拼配、石磨。用于整片顺序；本片省略储藏、复干和拼配，不声称囊括每条生产线的全部工序。
- 伊藤园《Green Tea vs. Matcha》：https://www.itoen-global.com/enjoymore_tea/curiosity/green-tea-vs-matcha-what-is-the-difference.html 。茶粉入水并用茶筅击拂的饮用方式。

精度修订：将“蒸青，让氧化停下来”改为“蒸青，抑制酶促氧化”，避免暗示停止所有氧化反应。字幕用语变化不改变镜头。

## 视觉来源

- 参考影片：本项目 `reference-sources/upstream-videos/mg-styles-15/08-morph.mp4`，10秒，作者发布版本。
- 方法参考：https://github.com/Vincentwei1021/mg-styles-15 ，固定commit `49052d80bfaf9fa8412cc9710530e5e95a3b8d8c`。读取08-morph的SVG等距采样、分层轮廓及过渡方法；本片形状、绘制实现、配色、时序与声音为新建。未复制作者图案、字形、音轨或视频画面。
- `assets/storyboard-reference.png`：本对话由内置imagegen生成的六格提案，仅用于美术参考，不裁成视频卡片。
- `assets/paper-generated.png`：本轮内置imagegen生成的细纸纹，提示词见 `assets/paper-prompt.txt`。实际由Canvas作为背景/局部材质采样；没有图生视频调用。
- `assets/msyh-local.ttc`：本机Windows微软雅黑，仅用于本机渲染。源工程转交其他机器时应使用有相应许可的本地字体替换，不将此字体作为可自由分发素材。

## 声音

5秒小样使用新合成的蒸汽、热风、干叶摩擦以及96BPM原创和弦/旋律片段。用户认可小样后，35秒整片已扩展原创配乐，加入遮阴布、采叶、精制、磨石、注水、击拂与尾奏事件；声音源码为audio-full.py，事件及数值记录见technical/audio-full-evidence.json。无第三方录音、无旁白，不将音频数值检查视为实际听音。

## 工艺表现边界

蒸汽转气流属于视觉连接；茶叶不是蒸汽，磨盘不是茶粉。大型叶片、水分点、托盘和气流均为放大示意。干燥叶片自然展开而非揉成针形；石磨为选用路线，不定义所有抹茶只能石磨。茶粉入水按分散处理，不宣称全部溶解。
