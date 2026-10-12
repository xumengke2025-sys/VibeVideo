# 方法论吸收 checkpoint
目标：广泛覆盖513条资料，提炼导演/摄影/美术/动作方法与代码实现关系；本轮不制作样片。
已完成：513条索引去重为459段公开文本；420段短文本全文、39段长文本机制摘录已阅读。保留两套已有完整绘制运行部分及其回放证据，新增mg-styles-15、papermotion、water-opus、three-avbd四套MIT文本源码包，共418文件约4.94MB；六包共457个上游文件，保留固定commit、原样源码、LICENSE和逐文件SHA256。原帖到源码的已核查关联为beach/water/rigid三条；补充工程不冒充图库同作。
成果：vibe-video 0.7.0已接入references/opus-methodology.md、opus-methods.json的26张人工方法卡、opus-source-index.json的513条逐条阅读/来源索引，以及scripts/opus_methodology.py中文检索、方法卡、源码路径/行号、来源追溯与校验命令。已修正opus-gallery.md混合来源说明和code-cinema.md两套回放/四套只读范围。
验证：verify_methodology.py完成14次CLI验证，检查中文需求、未知query空结果、纯代码筛选、混合来源trace、无效ID错误、六套本地绝对路径、文件行号和文档相对链接。validate检查457个源码SHA256、manifest commit/仓库、26卡引用、513条覆盖/prompt哈希/原文候选及证据边界，零错误。skill-creator quick_validate.py返回Skill is valid。证据在retrieval-verification.json、verification-summary.json；本轮没有渲染新样片。
状态：上一阶段v0.7.0完成；本次扩充与质量分层已完成，更新为v0.8.0。未来用户具体制作时按需求读取源码副本、补齐必要素材/依赖、迁移实时模拟时间轴，再用实际输出对标；本轮不自动扩大为样片制作或逐部复现。
验证边界：未逐部观看513原片；新找到工程尚未运行；长文本仅摘录阅读不能称全文吸收；提示词要求不能当成已实现效果。
约束：原作代码来源未知不得标为已证实；重制标签只作线索；本项目9:16竖屏1080×1920，保留历史横版。

2026-10-09新增：固定版本归档songbie（8文件）、lemo-opuscar选定4风格/共享代码（147）、i-like-ur-look-lyric-video（72）、clearwater（4），共231文件。原样复制并比对下载SHA256；现10包688上游文件、35方法卡。源码位置D:/Codex/skills/vibe-video/assets/code-studies。归档脚本extend_recent_sources.py可重复核对，不执行上游源码。
新增方法：共享乐谱/角色接棒、单状态表演变化、追逐静音接触、工程图零件身份、世界锚点标注、干湿水墨、阅读约束摄影、曲面纸页交接、折射网格焦散。每卡有实现文件/行号、导演目的、失败条件和审片窗；新卡不虚构图库同作关联。
质量分层：beach/reel只验证过代表帧与连续窗，其他新增影片未运行/审片。water/rigid/clearwater标为组件；paper为引擎及影片且不是统一Opus归属，lyric编码模型未知。recent-film-selection.md列提交日期和用途；opus_methodology.py返回用途/质量/日期，--film-only排除仅组件支撑的方法，但不认证剩余影片优质。
日期/来源：六包提交日期经GitHub commit API核查并保存pinned-commit-dates.json，新包元数据保留仓库创建与固定commit时间。未核实热潮起点与各片首发日期，不声称全部热潮后首发。采用路径的Canvas/Three/WebGL绘制证据及静态端点搜索边界见visual-path-evidence.json。
最新验证：verify_methodology.py通过23次CLI检索/错误/过滤/路径测试；validate检查688文件哈希、35卡锚点、513条索引来源及文档链接，零错误。skill-creator quick_validate返回Skill is valid。最新结果已覆盖retrieval-verification.json及verification-summary.json；没有新增样片。
未完成/后续：新增影片尚无实际动态审片；mg远程成片页CUA超时，没有新增观看证据，不重复同样调用。songbie钢琴样本、lyric版权歌曲/时间数据、lemo多种素材依赖未完整归档；Clearwater涟漪需寻址改写。用户给具体需求时选择并实际观看对应作品/窗口再迁移和比对，不以源码阅读代替质量判断。
