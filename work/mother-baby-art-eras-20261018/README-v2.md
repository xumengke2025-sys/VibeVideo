# 妈妈与宝宝 · 35种时代画风

正式制作路线：生成式二维卡通素材 + 可编辑的确定性动画合成。竖屏1080×1920，24fps，41.25秒，35种画风；沿用参考片的无声形式。

妈妈重复端咖啡杯喝一口，宝宝按最新要求双手抱起奶瓶喝奶。人物占小比例，环境占主要篇幅。两人共用全局3.2秒动作循环，时代切换不重置相位。

## 编辑入口

- `film/index-v2.html`：成片预览入口，点击画面播放/暂停。用HTTP静态服务打开；控制台调用 `renderAt(seconds)` 可精确寻址。
- `film/film-v2.js`：生成cel的网格配准、动作时序、画面位置、字幕和时代擦拭；不包含程序化替代人形。
- `film/eras.js`：35个时代的名称、年份、顺序、配色和切换时间。
- `film/generated-manifest.js`：全部背景和角色动作层的路径。
- `assets/generated-v2/layers/`：每时代1张背景、4张妈妈动作图、4张宝宝动作图。
- `assets/generated-v2/*-v3-pack.png`及`34-modern-pack.png`：内置image_gen生成的原始素材包。
- `assets/generated-v2/*-prompt.txt`、`*-generation.json`：实际提示词、输入与输出路径、哈希。
- `normalize_generated.py`：按实际分栏位置提取图层，清理alpha杂点；修改原素材后运行此脚本更新图层和manifest。
- `assets/bottle-v3/`：宝宝奶瓶动作的生成原图、逐时代提取素材、定向修正、提示词和来源。`extract_bottle_assets.py`先提取奶瓶素材，随后`normalize_generated.py`以它覆盖历史捡星星姿态。

## 渲染

本机已安装 Node.js 24.15.0、Remotion renderer 4.0.506。源码包的package.json记录所需依赖；不包含node_modules。

```powershell
python extract_bottle_assets.py
python normalize_generated.py
node render-v2.mjs sample
node render-v2.mjs stills
node render-v2.mjs check
node render-v2.mjs full
python prepare_evidence_v2.py
python package_source_v2.py
```

`sample`输出现代/古埃及6.4秒动作样段；`stills`输出35个时代的实际代表帧；`full`导出MP4。渲染器通过仅监听127.0.0.1的临时静态服务加载本地素材，结束时关闭服务。

素材重裁切及审片证据脚本使用Python、Pillow与NumPy。`prepare_evidence_v2.py`中的FFmpeg路径按本机安装位置设置，换机器时可修改为对应路径。最终源码包含全部生成素材与动作层，直接编辑及重渲染不需要重新生图或API密钥。

## 验证与边界

`out/generated-mechanical-check-v2.json`检查990帧的素材覆盖、动作节点边界、全局相位及乱序/重新载入的像素确定性。节点只是生成图的近似配准点，不能用来证明像素中的手指抓握或杯口接嘴绝对准确；这些关系以实际画面审核为准。

`qa/v2/engineering-check.json`记录最终成片哈希、完整解码、尺寸、帧率、时长及无音轨。独立审核的实际覆盖、缺陷和工具限制保存在同目录；证据提取不等于看过，v1的旧审核不继承为v2通过。

历史纯路径版本保留在原工作目录的`film/index.html`、`film/film.js`及`render.mjs`，对应v1成片；本源码包只包含当前生图路线，请从本README及`film/index-v2.html`开始。

参考研究及MIT许可见`research/REFERENCE-TRANSFER.md`、`THIRD_PARTY_NOTICES.md`、`REFERENCE-LICENSE.txt`。参考发布片与所读源码版本不同，本片不宣称逐像素复刻。
