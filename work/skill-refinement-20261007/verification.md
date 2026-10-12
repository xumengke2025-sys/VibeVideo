# vibe-video 0.2 制作与验证记录

完成检查：2026-10-08（Asia/Shanghai）。旧榫卯任务保持停止，原工程保留。本次「看见不可见」为独立流程样片。

## 流程改进

技能将精细主体和完整构图放在主体代码之前：先完成代表帧和完整短动作，再扩展整片；真实素材、生图和代码按场景层共同工作。增加美术决策、素材清单、逐帧浏览与具体缺陷记录。旧几何范例仅作为时间轴工程参考。

实际安装目录 `C:\Users\67236\.codex\skills` 是指向 `D:\Codex\skills` 的 Windows junction，两条路径访问的是同一套技能文件，因此修改自动生效，无需复制覆盖。

## 研究依据

- [iArt javascript-animation-skills 0.4.1](https://github.com/iart-ai/javascript-animation-skills/commit/f7d0882a313249cbd43f0e4e9e209b1622870253)：提交时间 2026-09-30 19:40 +08:00。研究确定性时序、布局检查以及取消固定音乐/镜头数量限制的改动。
- [huashu-art-motion](https://github.com/alchaincyf/huashu-art-motion)：方法文档标记 10-04/05；已读本地提交 `26dba25b2b495c2138848c29a2c90df356a20325` 为 10-06 16:32 +08:00。吸收一帧先行、按层选工具及连续审片；未挪用受独立许可约束的角色素材。
- [iArt Motion Graphics](https://www.iart.ai/blog/claude-motion-graphics) 与 [Launch Videos](https://www.iart.ai/blog/opus-5-5-product-launch-videos)：页面明确更新 10-03，首次发布日期未核实。

参考记录在技能 `references/sources.md`；本地研究快照为 `research-javascript-animation.md` 与 `research-iart-commits.json`。没有进行同题、同素材、同预算的 Claude/GPT 对比。

## 成片与素材

入口：[index.jsx](index.jsx)；主场景：[OpticalStudy.jsx](OpticalStudy.jsx)；渲染：[render.mjs](render.mjs)。完整意图见 [production-brief.md](production-brief.md)，来源见 [asset-manifest.json](asset-manifest.json)，生图提示词见 [image-prompt.txt](image-prompt.txt)。

成片：[optical-study.mp4](out/optical-study.mp4)，10 秒、1920×1080、30fps、H.264。

NASA 真实星云图与 AI 生成金属概念装置分开标记。影像裁切层从已发布 RGB 图生成，仅说明归位与赋色过程，不声称重建了各滤镜原始数据。

成片 SHA256：`86b233c585646f21813e15c29e0ae16ebe0ec73e5b85ef3a2366a03c9191d984`。

## 已完成检查

| 检查 | 结果与范围 |
|---|---|
| 媒体技术 | 全片完整解码通过；时长、尺寸、帧率符合 brief；1 条非静音音轨；峰值 −16.96 dBFS、RMS −27.23 dBFS；无技术失败 |
| 全帧缩略检查 | 最终成片 0–299 帧全部导出，10 页 atlas 全部实际查看；两处预定硬切与末尾落定的低变化候选均有解释 |
| 最终高清检查 | 1920×1080 查看帧 90、144、180、195、225、299；检查金属细节、alpha 边缘、文字可读性、剪口主体、分层归位及最终赋色 |
| 浏览器功能 | 实际验证下一帧 0→1、滑块到 299、左键 299→298，图像/时间/帧号对应；无空载图 |
| 非零窗口提帧 | 在此前一版媒体上测试 85–95 的 11 帧，全部与完整提取的对应 JPG 字节一致；检验的是脚本窗口方法 |
| 技能与脚本 | 实际安装路径的 quick_validate 返回 Skill is valid；全部 Python 脚本语法、frame_audit CLI、技能及本记录的本地 Markdown 链接检查通过；报告 JSON 可解析、最终视频哈希一致；不把工程检查当成审美通过 |

技术证据：[media-evidence.json](out/media-qa-final/media-evidence.json)。全帧证据：[frame-audit.json](out/frame-audit-final/frame-audit.json)。逐帧查看：[review.html](out/frame-audit-final/review.html)。最终高清图在 `out/media-qa-final/`；旧 `out/frame-*.png` 属于前版，不用于最终检查。

## 实际修复

1. SVG 路径长度猜测导致光线不到目标，改用 `pathLength={1}` 和归一化进度。
2. 基础灰度擦除改为错位影像层依次归位，再揭示彩色，形成可见主动作。
3. 连续审帧发现帧 90 硬切后主体从零透明度开始，改为首帧直接建立主体；帧 180 同样检查了建立状态。
4. 提帧工具改为实际时间戳寻址，适应没有 select 过滤器的精简 FFmpeg；修复窗口提取与 HTML 替换问题。

上述画面改动后重新渲染整片，并重新生成最终哈希对应的证据。

## 本次结论与限制

这次验证证明混合素材、精细位图主体、代码动画和全帧检查工具已在本机跑通。所查高清帧未见关键文字遮挡、主体丢失或明显白边；连续缩略帧中未发现额外空画面。它不证明所有题材已达到专业栏目水准，也不保证与网上 Claude 样片等同。

没有完成实时全片播放或听音；音轨是原创合成测试声音，无旁白，不作专业配乐验收。生成仪器只作概念示意；未验证真实三维转身、机械接触、原始多波段数据重建或长片叙事。后续新作品应继续逐项验证这些能力。
