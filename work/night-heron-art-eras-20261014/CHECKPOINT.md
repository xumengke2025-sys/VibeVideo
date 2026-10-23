# 跨时代夜鹭 · 计划检查点

- objective: 研究花叔35种艺术风格代码重绘版，计划夜鹭在十几个艺术史时代偷吃对应场景动物的鱼。
- aspect_ratio: 9:16
- width: 1080
- height: 1920
- delivery_mode: ai_review_once（用户2026-10-14明确选择）
- proposed: 16时代，40秒，24fps；完整计划见 production-plan.json（v2）。
- completed: 已读核心引擎、35风格时间轴、长卷主体/相机骨架及代表材质代码；核对旧夜鹭v10记录、关节/鱼绑定实现。已查看35个参考抽帧和六帧转场取样。
- evidence: research/contact.jpg 与 research/coverage.json。仅抽帧观察；未实时播放、未听音、未重渲上游工程。
- concept_path: out/concept-v3/styleboard.jpg；已在对话展示黑绘陶与水墨竖屏设定帧，沿用用户连续执行授权。
- concept_feedback: pending
- protected: 旧夜鹭形象辨识特征；旧工程及历史版本不覆盖；用户指定竖屏及一轮AI审核。
- user_direction: 用户已授权执行；每个时代动作基本一致；从旁边动物脚边/地上偷走其捕获的鱼，无打架、抵抗或追逐。
- implementation: 已搭建共享夜鹭骨架、16场景、地面鱼/喙绑定/吞咽和可寻址时间轴；首批16竖屏设定帧已输出。
- verification: 绘制上下文已逐帧重置；concept-v3三处乱序像素比较一致、无运行错误。sample-v1实际6.75秒相邻三时代动作已输出并查看接触/抬头/吞咽连续阶段。film-v1已完成960帧、1080×1920、24fps、40秒、双声道AAC及全片解码检查。
- video_path: out/film-v1/video.mp4
- video_sha256: 13760b5140c1a120468152ff6fc13de085550695e1e787d83596918c55644e3b
- audio: 原创合成40秒双声道配乐已生成；峰值0.72，听音未完成，不能声明视听通过。
- unresolved: 正在从成片导出全部960帧作为唯一审片角色证据；一轮审核尚未完成。
- next: 唯一独立审片者先盲看理解，再对照brief；最多一次修复及必要复核，交付注明实际覆盖和工具限制。

## 当前交付 film-v2
- video_path: out/film-v2/video.mp4
- video_sha256: 8fcb06404f5d7c122822d65ff41e835675ac1ba4f4f87dd904f3d12fbf09eb6a
- production: 16时代、40秒、1080×1920、24fps、960帧、双声道AAC；完整解码和媒体约束通过。
- repair: 一轮中唯一一次修复已用，开场文字改为浅米白。
- review_status: incomplete；独立审片原版实际保存330帧，修正版由主制作角色局部查看0–71帧，非独立；完整听音及实时感知未完成。不得写全片通过。
- review_evidence: qa/film-v2/delivery-report.md 与 delivery-review.json；原审片进度快照保留。
- source: 当前src及out/film-v2/source快照；旧视频与概念保留。
- next: 展示当前版本，由用户观看反馈；不自动开启第二轮审核或创意重构。晚到审核报告保留真实覆盖。

## 2026-10-15 用户反馈驱动重做
- authorization: 用户要求生图精修夜鹭及动物、改善生硬转场、基于参考源码还原背景、仅显示时代标签，时代和生物符合历史；连续执行授权沿用。
- protected: 16时代、9:16 / 1080×1920、40秒 / 24fps；共享伸颈取鱼—抬头吞咽—归位，无对抗。旧版全部保留。
- route: 内置imagegen生成可动画角色素材；实际移植上游材质/背景代码并作竖屏重排；先展示效果图与相邻时代样段再展开。
- review_budget: 既有一轮记录保留，不新建第二个审片者、不重置全片审核预算；新增版本需如实记录实际查看范围。
- status: 已重读当前实现；发现背景为另写近似图形，转场仅3帧横向揭示，文字层含多余说明，均列入替换范围。
- next: 生成角色资产；核对16时代/地点/动物台账，移植真实源码背景材质。

## 2026-10-15 rebuild-v3 制作检查点
- aspect_ratio: 9:16
- width: 1080
- height: 1920
- delivery_mode: ai_review_once（沿用，既有审核预算不重置）
- user_latest: 16时代全部分别生图，夜鹭、其他动物和鱼都使用对应时代画风，不遗漏时代，不以单套图片换滤镜替代。
- assets: assets/rebuild-v3/era-01.png 至 era-16.png 全部已生成并保存；每组5拆件；prompts.json 保存完整提示词；atlas-manifest.json 保存透明轮廓测量。
- source: vendor/huashu/ 已移植16个场景及6个依赖库，MIT许可与逐文件来源/改编哈希见 provenance.json。rebuild-v3.html 为独立新版入口，旧版不覆盖。
- history: research/history-v3.md 保存16时代、地点、生物、事实来源及证据强度。
- concept_path: out/rebuild-concept-v2/styleboard.jpg（已实际查看全部16格）；改进接头后的概念图正在输出 rebuild-concept-v3。
- sample: out/rebuild-sample-v1/video.mp4，6.75秒、1080×1920、162帧、双声道、全解码通过；主制作实际查看每3帧联系表54格及原尺寸起始帧，非独立审核、未听音。
- findings: 源码材质已跑通；半秒材质叠化保留共享动作；样段发现静止颈部偏长、接口切面外露，已缩颈并增加透明端部混合，待复看。
- next: 检查新版接头与相邻转场；输出40秒全片，执行媒体检查并保存当前新版的实际查看范围。不得把旧版审核结论当新版通过。

## 当前交付 film-v3（2026-10-15）
- user_latest: 颈部允许多关节，须体现伸缩，初始缩颈；被偷动物也有反应，所有时代反应基本相同。
- completed: 16/16时代分别生图，全部含夜鹭身体、头、颈、鱼与其他动物；完整提示词保存在assets/rebuild-v3/prompts.json。实际移植16场景原生背景与材质；只有时代年份；半秒叠化。
- rig: 肩根、两处颈控制关节、头部连接；初始缩颈，低头取鱼伸展，抬头吞咽后收回。各动物在相同相位轻微后仰抬头，再俯身看鱼原位置；无争抢、追逐或对抗。
- crop_repair: 古希腊鹈鹕长喙跨素材列，已扩大裁切保留完整喙。
- concept_path: out/rebuild-concept-final/styleboard.jpg（实际查看全部16格）
- video_path: out/film-v3/video.mp4
- video_sha256: da9e5bc9e9a6a46966bcd87f947bd1e78a63c61515369e51f06ec25c76cf8b5b
- verification: 1080×1920、24fps、960帧、40.000秒、双声道AAC；完整解码通过；运行错误0；素材16/16齐全；三处乱序寻址像素一致。
- actual_view: 主制作查看最终联系表80帧（每12帧，0–948）、最终384/396/414帧大图；另查看修改前相邻样段的4帧大图。非独立抽查，未逐帧看完960帧，未实时完整播放或听音。
- limitations: 颈部铺展纹理有轻微拼接感；动物反应是共享身体倾斜和伸缩，未制作眨眼；叠化时短暂重影。完整听音和独立视听审核未完成，旧结论不覆盖本版。
- evidence: qa/film-v3/production-check.md，out/film-v3/evidence.json，out/film-v3/source-manifest.json；56个源码/素材文件已快照。
- source_entry: rebuild-v3.html / src/film-v3.js；production-plan.json与README已同步；旧计划另存production-plan-v2-historical.json，所有历史版本保留。
- next: 展示当前可播放版本及16画风总览，依据用户具体反馈继续；不自动再开全面审核。

## 当前工作 run-v4 重设计（2026-10-15，取代下一步方向，不覆盖旧片）
- objective_current: 同一夜鹭持续向右跑，16时代越跑越快，每场经过一个动物，偷走其脚边鱼并仰头吞下；物种/体型合理，全要素同画风。
- aspect_ratio: 9:16
- width: 1080
- height: 1920
- delivery_mode: ai_review_once（沿用既有预算，已用，不新增审片角色）
- user_latest: 每阶段动物类型/大小合理；“叼了鱼也得仰头吃掉，不然不是完整动作”。
- design: REDESIGN-RUN-V4.md 与 production-plan-run-v4.json；计划31秒、24fps、744帧，16场共702帧；开头24帧、结尾18帧。每场54帧逐步降至36帧，1.5秒下限保障完整动作。
- action: 缩颈跑→伸颈叼鱼→边跑边仰头→鱼头先进入口腔、尾部最后消失→闭喙吞咽→收颈继续跑。下一场不携鱼。鱼在地面/喙/口腔/已吞下的状态不可重复或凭空跳变。
- owner_reaction: 鱼离地后轻抬/转头，再低头看空处；同相位同反应语义，按物种关节适配；无攻击、追逐、争抢。
- fauna: 9种动物分布16场；06/10苍鹭、07普通翠鸟、15白头海雕、16普通鸬鹚，其他沿用。鸟长与站高、兽类头体长与尾长严格分开，model*仅为美术代表目标；熊不缩小、翠鸟不放大。鱼4–12厘米。
- sources: research/history-run-v4.md 与 source-transfer-run-v4.md；实际再读洞穴/黑绘/水墨代码，并读particle-beach的pelicans跟拍镜头214–239行。新跑动摄影尚未实现，源码阅读不等于已验证。
- concepts: concepts/run-v4/01-cave-bear.png、03-black-figure-pelican.png、09-ink-cormorant.png、09-ink-swallow.png；均内置imagegen生成/编辑，已实际查看，复制进工程。原图941×1672，近似9:16；正式片仍按1080×1920。prompt记录/原文边界见prompts.json，尺寸与SHA256见manifest.json。
- concept_feedback: 用户已明确补充仰头吞咽，已落实第四张关键姿态与每场事件表。其他静帧未单独确认，连续执行授权沿用，不额外逐图询问。
- verified_current: 16镜连续时间覆盖、702+24+18=744、所有镜头grab<headUp<swallowStart<fishGone<neckTucked<safeCutStart<镜头结束，四张文件存在/可读。制作实际查看四张生成图；不属于独立动态/听音审核。
- not_done: 新版奔跑样段/全片/其余13时代新版奔跑资产均未生成。旧v3静站素材不能自动算新版完成；不能把概念图横移当连续跑。
- protected: 旧film-v3、production-plan.json、全部历史素材不覆盖；仅时代年份、无对抗、同动作和同反应。
- next: 正式品质制作熊→猫、鹈鹕→水獭的连续跑/接触/仰头吞咽/收颈和转场样段；水墨核对仰头。样段验证后扩展16场，再做媒体检查；不新开全面审核。

## 2026-10-15 用户补充：不同美术风格切换合理
- user_latest: 整体要注意不同美术艺术风格切换的合理性。
- completed_design: 新增transitions-run-v4.json，逐一记录15个相邻切口的轮廓锚点与媒介变化，并同步REDESIGN-RUN-V4.md及production-plan-run-v4.json。
- constraints: 年代递进不等于跨地域艺术线性进化；各场全元素同媒介，保留自身色盘/空间规则；夜鹭体型、跑向、绝对步态、岸线承担连续性；不在接触或仰头吞鱼时切，吞完收颈后借前景遮挡匹配切。旧动物离开、新动物进入，不变形为彼此。
- verification: 目前仅完善设计，15切口未渲染/观看动态；下一步仍为正式品质连续动作和相邻切换样段。

## 2026-10-15 动画专用生图关键姿势纳入计划
- user_latest: 用户担心跑动不和谐，要求考虑增加自己绘制/生成的图片，并询问是否加入计划。
- completed_plan: REDESIGN-RUN-V4.md新增“动画专用生图关键姿势”，production-plan-run-v4.json新增animationImageContract；制作顺序已同步。
- requirements: 左右完整跑步周期的蹬地/腾空/落脚/承重姿态；缩颈/伸颈叼鱼/叼起/仰头吞咽/闭喙收颈姿态；生图身份和体型锁定、同风格、分层；共享骨架连续变形和落脚世界接触，避免滑步/跳帧/颈接头。先共享动作验证，再16时代分别重绘。
- next_current: 先制作水墨完整“奔跑→偷鱼→仰头吞下→收颈继续跑”样段，再验证熊→猫、鹈鹕→水獭的尺度及转场，最后扩展16时代。
- status: 要求已写入文件；动画姿势资产和新版样段尚未完成。既有四张概念图不能作为动态完成证明。


## run-v4 执行：水墨动画图集与独立入口
- 已生成 assets/run-v4/era-09-atlas.png，内置生图，4×4透明图集，八跑步/四取食/两鸬鹚反应/鱼/芦苇。原图1254×1254；实际查看透明图及宣纸合成，边缘正常。
- 新入口 run-v4.html、src/run-v4.js 使用生成姿势、头颈网格变形、连续主体/相机世界路径；正在输出水墨动作样段。
- 尚未确认：网格中间态、落脚、鱼口接触及完整动态。其余15组新版动画资产待生成。
- next: 查看实际水墨样段，修复已发现动作问题，再扩展困难转场和全片。

## 用户指出样例大小/位置错误（当前优先修复）
- 根因已定位：渲染入口 query 拼接用了第二个问号，水墨测试开关失效；水墨鸬鹚素材套用了史前熊参数。已修复 query。
- 已按 model* 米制高度统一换算像素，不再用按物种硬编码像素表。鸬鹚/夜鹭恢复约1.8倍站高关系；已恢复鸬鹚被截头顶。
- 已调整主体屏幕位置、鱼/原持有动物的世界位置与反应时机；仍在验证源姿势裁切、地面接触和中间形变，不称样段完成。
- 临时样段 out/ink-run-sample-01 至 -04 保留作错误证据，不能作为最终样段或全片交付。

## 当前可查看：run-v4 水墨体型/站位修正版
- video_current_sample: out/ink-run-layout-fix/video.mp4（仅水墨1.792秒样段，非整片）
- completed: 修复水墨开关/熊参数误用；恢复鸬鹚头顶；统一米制高度投影，目标鸬鹚/夜鹭约1.8；主体整体上移160px；鱼/动物世界位置重排；去除两姿势透明双影；伸颈源图头/喙裁切修复。
- mechanical: 1080×1920 / 24fps / 43帧 / stereo AAC / full decode / browser errors 0；source快照保存在输出目录。
- actual_view: 主制作已看43帧动作区联系表及最终16/29帧完整画幅；非独立，无完整实时播放/听音声明。
- limitations: 落脚尚非世界锁定，动物两姿势反应待补中间态；旧测试配乐未改事件同步。详见qa/run-v4-layout-fix.md。
- pending_original_goal: 其余15时代新版动画资产、熊猫/鹈鹕水獭转场、31秒744帧整片均未完成，旧审核预算不重置。当前缺资产回退只供开发，不得直接全片渲染交付。
- next_current: 根据本次大小和站位反馈继续完善共享跑步/反应，再扩展困难场景和16时代，保持用户既有执行授权，不重复启动询问。

## 整片继续执行
- 已补齐史前岩画动画图集 assets/run-v4/era-01-atlas.png；内置生图并实际查看，待提取对齐。
- 其余14套提示词已写入assets/run-v4/prompts-all.json；当前继续逐套生成，不使用水墨回退交付。

- 16/16新版动画图集已全部生成并保存（era-01..16-atlas.png）；主制作实际查看各图。后续提取跨格轮廓、对齐动作；尚未渲染整片。

## run-v4 全片已完成，交付前接缝修正
- 当前目标：完成31秒 / 744帧 / 1080×1920 / 24fps / 16时代整片交付；沿用连续执行授权与既有审核预算。
- 已完成：16套分别生图、256格提取；连续跑动、伸颈取鱼、仰头吞咽与收颈；物种米制尺度、共同轻微低头反应、15处前景遮挡匹配切；源码材质户外背景及三层视差；原创31秒配乐和316个声音事件。
- 初版整片：out/film-run-v4/video.mp4，744帧、双声道AAC、全片解码通过、browser errors 0。
- 实际查看：16套图集；80个动作节点帧、75个切口帧、16场最终画风总览、完整画幅184/550及开头/结尾和入场边缘。属于主制作观察，非新独立审核；未完整实时播放/听音。
- 修正：远山循环多边形收口伸至画布底，去除地平线以下接缝；最终输出out/film-run-v4-final。
- 下一步：完成最终导出和改动附近查看，保存源码/哈希/交付说明，展示成片。

## run-v4 最终交付
- video_path: out/film-run-v4-final/video.mp4
- video_sha256: 99d89e1662a802cc11a7e349e2d602a9831a5ad34438c6460ff7c15749ebae55
- format: 31秒 / 1080×1920 / 24fps / 744帧 / 双声道AAC；全片解码通过；browser errors 0。
- final_view: 已查看最终改动/相邻及结尾12帧联系表、最终734整幅；接缝已修复。主制作查看，非新独立审核；完整听音未完成，足部接触仍为近似。
- source_snapshot: out/film-run-v4-final/source 与 source-manifest.json，绑定本视频哈希。
- delivery: DELIVERY-RUN-V4.md；实际观察证据qa/run-v4-final/production-check.md。
- status: 完整制作与工程交付已完成，展示成片后由用户反馈；不新开全面审核或自动创意重做。

## run-v5 用户反馈继续制作
- 用户要求：动作更顺畅；被偷动物惊愕、滑稽；生成符合时代及美术媒介的完整背景。
- 方案：16张独立生图背景；连续时间驱动跑步/伸颈，48fps输出；统一愣住—探头找鱼—惊讶抬头的弹性反应，无打架或追逐。
- 保留：run-v4-final及源码快照；16场/31秒/1080×1920/无额外文字/既有审核预算不重开。
- 当前：背景提示词已保存assets/run-v5/background-prompts.json；开始生成与动作改造，待困难样段再展开整片。

## run-v5 背景统一性反馈
- 用户指出首批背景过细，担心与角色/切换前景违和；当前不能确认通过，首批细节背景列作试稿，不直接整片采用。
- 调整：以实际夜鹭/芦苇PNG作为生图风格参照，先重做埃及与古希腊相邻两场，降低背景细节/对比、统一色盘/轮廓；前景树干按各场媒介重新处理，不再全片同一棕色。
- 下一步：两场真实合成样段同时核对角色、背景、遮挡、动作反应；验证后再扩展。
## run-v5 合成样段制作观察
- 已实际查看埃及→希腊4.25秒/204帧样段的22帧联系表及完整画幅。简化背景比细节试稿更接近动物；已修正树干在满屏覆盖时切换到下一时代材质。
- 样段发现喙/颈双轮廓，已取消姿势叠化，改为同一生成角色上身的连续关节蒙皮；头部保持刚性转动，避免喙被压短。查看4.0/4.6秒整幅验证，继续核对口部/鱼接触。
- 背景：12张过细试稿存入assets/run-v5/rejected-detail；匹配版埃及/希腊已采用，1/4/5/6/7/8/9/10已生成保存，11-14生成中。提示词assets/run-v5/background-prompts-matched.json。
- 仍需：剩余背景、全16场真实合成、48fps最终导出和工程检查。非新独立审核，不扩充已用审核预算。

## run-v5 最终交付（取代上文未完成状态）
- objective: 完成用户要求的顺畅动作、惊愕喜剧反应及背景/动物/遮挡前景风格统一。
- aspect_ratio: 9:16；width: 1080；height: 1920；delivery_mode: ai_review_once（原一轮预算不重开）。
- completed: 16/16匹配背景已保存；连续关节腿/上身蒙皮、统一失鱼反应、各时代遮挡材质均完成。油画树干最终改为棕褐与笔触。
- video_path: out/film-run-v5-matched-final/video.mp4
- video_sha256: 1d8be086889f2aa9050cd531221807111ce96611045a62175c7a6851c4b466f8
- verification: 31秒 / 1080×1920 / 48fps / 1488帧 / stereo AAC，全片解码通过，浏览器错误0；350文件源码快照签名核对通过。
- actual_view: 最终MP4解码的16场总览及18个局部动作/转场/结尾帧已实际查看；非独立；详见qa/film-run-v5-matched-final/production-check.md。
- source_snapshot: out/film-run-v5-matched-final/source/；source-manifest.json绑定最终视频哈希；旧版本保留。
- unresolved: 未完成最终全片连续观看及完整听音，不声称完整视听通过；生成图层仍可能有局部笔触差异。
- delivery: DELIVERY-RUN-V5.md；out/film-run-v5-matched-final/styleboard.jpg。
- next: 展示本版成片和实际合成总览，由用户反馈；不自动开启新审核或进一步创意重做。计划中的早期assetStatus保留历史，状态以本节及交付记录为准。

## run-v6 用户反馈继续制作
- 用户要求：所有失鱼动物嘴部扭曲需修复，16场动物动作/神态全部重绘；年代文字放大。
- cause: run-v5 ownerImage统一控制点网格变形作用于口鼻/喙，造成解剖扭曲。
- route: 每个时代独立生成九格真实姿势图，嘴/喙保持正常解剖，以眼神/耳朵/自然颈部动作表达惊愕；取消失鱼动物的网格变形。共16套，与现有素材匹配媒介；年代从40px增大至60px并检查完整显示。
- preserve: run-v5-matched-final、背景、夜鹭及动作顺序；31秒/1080×1920/48fps；不重开已有一轮审核。
- progress: v6入口/源码/渲染器与16套提示词已准备；1–12时代九格动作图已生成保存。已实际查看1–11的99张姿势，取消动物面部网格，改为真实绘制姿势直接切换；整体等比缩放/刚性脚底对齐，不叠化。13–16生成中。
- pilot: out/run-v6-reaction-pilot-02/video.mp4；埃及→希腊4.25秒/1080×1920/48fps/204帧解码通过。实际查看10个反应节点与完整猫场画幅；嘴/喙正常，60px年代字完整。qa/run-v6-reaction-pilot-02/reaction-check-1.jpg。
- extraction: 连通轮廓提取替代严格切格，清除串格杂点、完整保留嘴/喙/尾；assets/run-v6/manifest.json记录注册参数。
- assets_complete: 16套九格生图已保存并提取144张姿势，主制作已实际查看全部姿势联系表。prompts/provenance/manifest见assets/run-v6；嘴/喙没有使用网格或叠化。
- composite_check: 16场实际1080×1920合成图已查看，随机寻址3点一致、浏览器错误0；年代60px实测宽420–600px，预留924px。进一步提高洞穴/哥特/后印象/像素等场景文字对比。
- rendering: out/film-run-v6-redrawn-final；31秒/1488帧/48fps正式导出中，尚未交付。
- next: 最终MP4解码后提取16场反应节点，查看实际嘴/喙与姿势接触，保存哈希、源码和交付说明；不增加独立审核轮次。

## run-v6 最终交付
- completed: 16场失鱼动物动作/表情全部重绘，9张/场共144张；删除失鱼动物面部网格，使用等比/刚性注册的真实姿势序列。年代40px→60px并调整对比；旧版本保留。
- aspect_ratio: 9:16；width: 1080；height: 1920；delivery_mode: ai_review_once（既有预算保留，不重开）。
- video_path: out/film-run-v6-redrawn-final/video.mp4
- video_sha256: 23dd981e06cac41ac190d9b0cabc19277c4a86b5eb598fdfa038c79041082958
- verification: 31秒/48fps/1488帧/stereo AAC，全片音视频解码通过，browser errors 0；518文件源码快照签名核对通过。
- actual_view: 全部144张姿势；样段10帧；最终MP4的16场总览、80个反应节点、18个局部/转场/结尾帧及1344完整画幅已查看。所查看节点未再见原面部拉伸扭曲。
- evidence: qa/film-run-v6-redrawn-final/production-check.md、reaction-extraction.json、extraction-index.json。
- source_snapshot: out/film-run-v6-redrawn-final/source/；source-manifest.json绑定最终视频哈希。
- limitation: 主制作观察，非独立审核；未完整连续观看最终全片/完整听音；部分低头动作被前方夜鹭短暂遮挡；不声称完整视听通过。
- delivery: DELIVERY-RUN-V6.md，最终成片及实际反应对照可展示。
- next: 由用户观看本版反馈；不自动开启新审核或创意重做。

## run-v7 用户反馈继续制作（2026-10-15）
- objective: 动物相对岸边静止，失鱼后惊讶，头与目光跟踪夜鹭由左向右跑过。
- aspect_ratio: 9:16；width: 1080；height: 1920；delivery_mode: ai_review_once（既有预算已用，不新增审片者）。
- cause: v6动物按世界相机每秒约600–850px横移，背景却仅按镜头进度缓移约50px/秒；两者摄影位移不一致，造成沿岸滑动。九姿势也均朝左，缺少追踪朝向。
- implementation_plan: 背景岸线和固定动物共用同一摄影位移；16时代分别生成身体固定的头眼左→正面→右转动姿势，按夜鹭相对位置驱动。旧v6与历史版本保留。
- next: 生成真实转头姿势，困难样段验证岸边固定与头眼跟随，再导出31秒48fps整片。

## run-v7 生成与困难样段完成
- assets: 16/16独立转头图集已生成，共144姿势；内置imagegen，全部复制到assets/run-v7；完整提示词和来源见prompts.json与provenance.json。
- implementation: 近岸与动物共用摄影位移，远景保留缓移；脚底刚性注册，承重部位锁定；动物按夜鹭当前头部位置选择惊讶、左/正面/右转头姿势，嘴喙不网格变形。
- pilot: out/run-v7-tracking-pilot-02/video.mp4，4.25秒/204帧/1080×1920/48fps/双声道，全片解码通过；已查看12节点联系表。此为全景同步摄影的早期样段；其后近岸/远景分层，实际查看1.95/4.7/6.8秒三幅最终尺寸设定帧。
- mechanical: 首次16场按48fps采样，世界锚点/岸边相对位置波动小于1e-9像素；实际岸边纹理跟踪差异0–2.12/255，主要来自亚像素重采样。最终代码正在复验。
- rendering: out/film-run-v7-bank-tracking-final 正式整片导出中，尚未完成交付。
- next: 全解码、最终MP4逐场反应抽帧、源码快照/哈希及交付记录；不重开独立审核。

## run-v7 最终交付（2026-10-15）
- completed: 动物与近岸共用摄影位移，脚底/承重部分固定；16时代分别绘制惊讶及头眼左→正面→右追视，共144姿势。追视以实测眼部位置为起点跟随夜鹭头部，已校正转头时机。
- aspect_ratio: 9:16；width: 1080；height: 1920；delivery_mode: ai_review_once（既有预算已用，不新增角色或审核轮次）。
- video_path: out/film-run-v7-bank-tracking-final-02/video.mp4
- video_sha256: f1949be95da37ce3b076610a806e1fa30e7de9e43c65928c0a6728cfd17af417
- verification: 31秒/48fps/1488帧/双声道AAC，全片音视频解码通过，浏览器错误0，684文件源码快照签名与成片哈希已绑定。16场1404时刻的岸边/世界锚点波动小于1e-9像素，三处乱序寻址一致。
- actual_view: 主制作实际查看最终MP4的80个反应节点、16场完整画幅取样、18个局部/转场/结尾帧；此前查看144姿势、12帧困难样段与代表性大图。非独立审核，未完整连续观看及听音。
- limitation: 小动物反应有时被前景夜鹭短暂遮挡；不声明全片独立视听通过。
- evidence: qa/film-run-v7-bank-tracking-final-02/production-check.md、kinematics-binding.json；qa/run-v7-kinematics/verification.json；out/film-run-v7-bank-tracking-final-02/evidence.json与source-manifest.json。
- delivery: DELIVERY-RUN-V7.md；最终采用-02，旧v6及v7中间版保留。
- next: 展示本版，依据用户观看后的具体反馈继续，不自动重开创意返工或全面审核。

## run-v8 用户反馈继续制作（2026-10-16）
- objective: 取消追随夜鹭/回头，失鱼后低头看原来鱼所在的空地，停住并惊讶。
- aspect_ratio: 9:16；width: 1080；height: 1920；delivery_mode: ai_review_once（原预算已用，不新增审片）。
- protected: 近岸与动物固定关系、16时代、31秒、1080×1920、48fps、夜鹭动作/原配乐、历史版本。
- implementation: 新建v8入口/源码/计划；复用v6各时代低头生图姿势，移除追踪夜鹭头部和左右转头驱动；只用0/1/3/4姿势，最后停在向下看空地。
- next: 刚性脚底注册后检查困难场景，输出整片并作机械/解码及实际画面抽查；不新开全面审核。
- pilot_complete: out/run-v8-ground-pilot/video.mp4，4.25秒/204帧/1080×1920/48fps/双声道，完整解码通过；主制作实际查看11帧接触表，熊与猫低头看空地且不回头。系统Chrome启动退出，使用本机已有headless-shell成功完成。
- assets_complete: 已看16时代全套素材联系表；仅使用0/1/3/4四姿势，按0.065/0.16/0.30秒进入惊讶/低头/看地面停住。无新生图。
- next: 正式全片渲染与相对岸边/目标空地约束检查。

- mechanical_complete: 16时代共354时刻已检查；全部只用0/1/3/4，失鱼0.30秒后保持低头、始终朝原方向；空地目标的世界位置固定；岸边相对波动小于1e-9像素，3处乱序寻址一致，无运行错误。qa/run-v8-kinematics/summary.json。
- rendering: 正式1488帧已绘制，编码/全解码检查中。

## run-v8 最终交付（2026-10-16）
- completed: 去除跟随夜鹭与回头，鱼离地后惊讶→低头→看空地停住；16时代统一，仅使用0/1/3/4姿势。动物与近岸固定关系保留，未新增生图。
- aspect_ratio: 9:16；width: 1080；height: 1920；delivery_mode: ai_review_once（既有预算已用，不新增独立审核）。
- video_path: out/film-run-v8-empty-ground-final/video.mp4
- video_sha256: e04f58fdef126cf9f173a68f3c86e672e3da02feaefec58e308b555291e9deec
- verification: 31秒/48fps/1488帧/双声道AAC，全片音视频解码通过，浏览器错误0；832文件快照签名核对通过。16场354时刻行为/岸边/固定空地目标检查通过，三处乱序寻址一致。
- actual_view: 最终MP4的80反应节点、16场完整画幅取样、18个局部/转场/结尾帧；全部素材联系表及11帧困难样段。主制作抽查，非独立审核，未完整连续播放/完整听音。
- limitation: 前景夜鹭短暂遮挡部分小动物反应；不声明全片独立视听通过。
- evidence: qa/film-run-v8-empty-ground-final/production-check.md与production-check.json；qa/run-v8-kinematics/；最终输出evidence.json和source-manifest.json。
- delivery: DELIVERY-RUN-V8.md；旧v7及全部历史版本保留。
- next: 展示新版，由用户观看后反馈；不自动新开全面审核或创意返工。

## 2026-10-16 run-v9 动物去重制作
- objective_current: 替换7场重复动物，实现16场16种；保留岸边静止、失鱼后惊讶并低头看空地，无回头。
- aspect_ratio: 9:16
- width: 1080
- height: 1920
- delivery_mode: ai_review_once（既有预算已用，不新增角色）
- replacement_plan: 08琵鹭、09小白鹭、10凤头鸊鷉、11赤狐、12欧洲獾、14白鹳、16日本貉。
- completed: 核对原16场仅9物种；查阅地域/食性资料；历史v8保留。
- next: 分别生图、脚底注册、合入v9、正式渲染及媒体/物种唯一性检查。

- v9 assets_ready: 7份独立透明四姿势图集/28张新绘制；9套v8素材保留。prompts/provenance/manifest在assets/run-v9。已逐套查看原图、注册姿势联系表和16场布局。
- v9 layout: 体型按米投影；凤头鸊鷉低伏；貉无环短尾；图集裁格边缘碎片已按连通组件清除。
- v9 initial_kinematics: 16场岸边相对位置误差小于2e-12，低头保持/左朝向/乱序寻址通过；素材清理后再做最终状态检查。
- next: 检查替换场景反应及转场样段，然后正式31秒渲染。

- sample_video: out/sample-run-v9-species/video.mp4；6.5秒/312帧/1080×1920/48fps/双声道AAC，完整解码通过。主制作实际查看39个有序动作区抽帧（15.125–21.458秒）及7场35个反应节点，非独立审核，未完整实时播放/听音。
- next: 正式输出out/film-run-v9-unique-animals-final/video.mp4，渲染后冻结源码签名/打包并核对最终帧。

## 当前交付 run-v9（2026-10-16）
- objective_complete: 16场被抢动物16种，无重复；替换7份独立图集，另外9场保留。
- video_path: out/film-run-v9-unique-animals-final/video.mp4
- video_sha256: e9ae381507354ec76f072ff20137d1043d7c3e159a7c6c13913ef6a70e241491
- format: 31秒 / 1080×1920 / 48fps / 1488帧 / 双声道AAC；全片解码通过；浏览器错误0。
- reaction: 脚底/身体相对近岸固定，失鱼后惊讶→低头看原鱼位置→保持低头；无转头追视。
- verification: 354时刻机械检查、16物种唯一性、静态脚底像素、3处乱序seek通过；955份源码及素材快照与哈希对应。
- actual_view: 主制作查看最终16场总览、80个反应节点、18处局部/转场/结尾；另看18源帧新场景联系表及6.5秒样段39个有序抽帧。非独立审核，未完整连续播放/听音。
- delivery: DELIVERY-RUN-V9.md；qa/film-run-v9-unique-animals-final/production-check.md。
- tooling: 后置抽帧使用check-reactions-run-v9-resting.py以支持低伏高度，源码快照不改。
- next: 展示当前可播放版，依据用户反馈继续；不自动重开独立审核或其他项目。

## run-v10 音乐、文字和嚣张步态（2026-10-16）
- objective: 用户要求音乐优化并踩点、时代年份文字清楚、夜鹭尤其腿部动作夸张嚣张。
- aspect_ratio: 9:16；width: 1080；height: 1920；delivery_mode: ai_review_once（原预算已用，不新增角色）。
- protected: 16时代16种动物；岸边相对静止；失鱼后惊讶→低头看空地，无追视/回头；历史v9保留。
- implementation: 独立run-v10入口/源码/计划；400单位绝对距离步态与音乐共享时钟；高抬脚、前踢落地、身体得意摆动；叼鱼窗口稳定。70px嵌入粗体与顶部渐隐暗底。原创低音/木琴/短铜管/轻鼓编曲，抓鱼/仰头/吞咽/时代切换共用事件时刻。
- completed: 源码语法检查通过；31秒原创WAV已生成，107个落脚事件，峰值0.87、RMS0.137，未实际听音；关键姿态渲染中。
- next: 看实际腿部剪影及文字，样段→全片；机械同步和媒体检查，记录实际观看/听音范围。
- sample_complete: out/sample-run-v10-swagger/video.mp4，4.5秒/216帧/1080×1920/48fps/双声道，全解码通过。主制作实际查看12张源姿态关键帧及编码后48个有序动作抽帧（1.125–5.531秒）；高抬腿、前踢、叼鱼/吞咽、相邻转场已抽查。未连续实时播放/听音。
- mechanical: 16场354时刻、16物种唯一、固定岸边/看空地、3处乱序seek通过；107次落脚相位误差<3e-14，承重脚世界漂移<4e-12像素，最高抬脚114.75px，全部腿长可达；16场音乐故事事件时差0。
- rendering: out/film-run-v10-swagger-beats-final 正式1488帧导出中，源码冻结。
- next: 完成编码/解码，快照哈希绑定，查看最终文字/步态/转场与结尾，交付可播放MP4。


## 当前交付 run-v10（2026-10-16）
- completed: 原创音乐重新编排，脚步及16场叼鱼/仰头/吞咽/时代切换按共享时钟踩点；时代年份70px嵌入粗体、暖白字和渐隐暗底；夜鹭高抬腿约115px、前踢大步、加粗腿趾与得意身体摆动。16种动物及原地惊讶/看空地反应保留。
- aspect_ratio: 9:16；width: 1080；height: 1920；delivery_mode: ai_review_once（原预算已用，不新增角色）。
- video_path: out/film-run-v10-swagger-beats-final/video.mp4
- video_sha256: 11f71ee40cdb85a2b728ae93690f0b9c3da0dd1644b947ae9099d748b24fca47
- verification: 31秒/48fps/1488帧/双声道AAC，全片解码，浏览器错误0；963文件快照签名通过。354时刻行为与岸边检查、16物种唯一、三处乱序seek通过；107落脚音同步、腿长可达、无AAC满量程削波。
- actual_view: 主制作看12源关键姿态、样段48有序抽帧、最终16场全幅总览及18局部/转场/结尾帧。非独立审核，未完整连续播放/实际听音。
- delivery: DELIVERY-RUN-V10.md；qa/film-run-v10-swagger-beats-final/production-check.json；历史v9保留。
- next: 展示当前可播放版本，由用户播放后反馈音乐和动作；不自动重开审核或其他项目。

## run-v11 步频与腿部再强化（2026-10-16）
- objective: 用户要求步伐更快、腿形更明显、动作更夸张嚣张。
- aspect_ratio: 9:16；width: 1080；height: 1920；delivery_mode: ai_review_once（原预算已用，不新增角色）。
- protected: 年代文字、16种动物、岸边固定/低头看空地、抢鱼吞咽事件，历史v10保留。
- implementation: 独立v11，步态周期400→280世界单位，步频约+43%；正常奔跑抬高身体露腿，折腿上抬约133px、前踢更远；腿改为粗细变化的实体段、清楚踝关节、张开脚趾和深色轮廓；摆身更强。取鱼/吞咽时收住摆身，脚步音乐重算为152落脚事件。
- verification: 全部正常/收身幅度的腿长可达，落脚相位误差<3e-14、承重脚世界漂移<2e-12px，16场故事音效时刻不变。未实际听音。
- next: 检查正式样段与快速腿部轮廓，然后完整渲染和媒体检查。
- sample_complete: out/sample-run-v11-fast-strut-02/video.mp4，4.5秒/216帧/1080×1920/48fps/双声道，全解码通过；主制作实际查看48个有序编码后抽帧（1.125–5.531秒），快速前踢/折腿与邻接抢鱼、吞咽、换时代窗口。更清楚的实体腿段与大前踢可见；未连续实时播放或听音。
- mechanical_complete: 16场354时刻反应与岸边固定、16物种唯一、3处乱序寻址通过。正常→取鱼收身的5种身体幅度均检查腿长可达；152落脚音共享时钟，16场动作声音时差0。
- rendering: out/film-run-v11-fast-strut-final正式整片导出中；源码冻结。
- next: 完成最终媒体检查/源码快照，抽查成片后交付。
- local_fix: 首个整片最终抽帧发现一处收腿时踝部从背部上方穿出；旧输出保留但不交付。已将高抬脚轨迹向前收回，使踝部始终低于髋部，五档身体幅度/完整周期数值检查最小低于髋部34.13px。
- fixed_sample: out/sample-run-v11-fast-strut-03/video.mp4，全解码通过；主制作实际查看新版48有序动作抽帧，背部穿出已消除，快步/前踢/抬身保留。
- final_render: out/film-run-v11-fast-strut-final-02，正式重新导出；仅本次轨迹局部修正，无新角色或全面审核。


## 当前交付 run-v11（2026-10-16）
- completed: 步频较v10提高约43%，平跑抬高身体32–58px露腿，最高抬脚约133px、前踢更远、身体摆动更强。腿改为粗细变化的实体轮廓、自然踝部、鳞纹及张开脚趾，152落脚声音与音乐重新踩点。16种动物、清楚年代文字、岸边固定/失鱼看空地保留。
- aspect_ratio: 9:16；width: 1080；height: 1920；delivery_mode: ai_review_once（原预算已用，不新增角色）。
- video_path: out/film-run-v11-fast-strut-final-02/video.mp4
- video_sha256: ffe246e11ce95d929b8a52d9be6b4cf81df15b0d4cde8de7d9394b048c81941f
- verification: 31秒/48fps/1488帧/双声道AAC，全片解码，浏览器错误0；966文件快照签名通过。354时刻行为与岸边检查、16物种唯一、三处乱序seek通过；152落脚音同步、正常/收身幅度腿长可达，无AAC满量程削波。
- actual_view: 主制作查看样段48有序抽帧、最终16场全幅总览及18局部/转场/结尾帧。非独立审核，未完整连续播放/实际听音。
- delivery: DELIVERY-RUN-V11.md；qa/film-run-v11-fast-strut-final-02/production-check.json；历史v10保留。
- next: 展示本次可播放成片，按用户反馈继续，不自动重开审核或其他项目。


## run-v12 夜鹭形体修正（2026-10-16）
- objective: 纠正过长腿部；恢复紧凑夜鹭比例，16画风红眼睛和两根白色枕羽。
- aspect_ratio: 9:16；width: 1080；height: 1920；delivery_mode: ai_review_once（原预算已用，不新增角色）。
- completed: 查看16套源素材与头部对照；v12独立入口/源码已建立。腿段总长由260px缩至173px，取消32–58px抬身，抬脚约54px；快速时钟保留。眼位置按各画风单独注册，饰羽刚性跟随头部。
- protected: 历史版本、16种动物/低头看空地、清晰文字、原踩点音乐。
- next: 检查关键姿态和短样段，确认比例/头部细节后输出整片。

- sample_complete: out/sample-run-v12-natural-heron/video.mp4，4.5秒/216帧/1080×1920/48fps/双声道，全解码通过；主制作实际查看48张有序抽帧和16画风关键帧，短腿/红眼/双白枕羽在低头与仰头时保持。未完整连续播放/实际听音。
- mechanical: 354时刻岸边固定/低头看空地，16物种唯一，3处乱序seek通过；152落脚音共享时钟，腿长全周期可达，抬脚53.55px，踝部始终低于髋部至少11.37px。
- next: 正式整片渲染，冻结源码，媒体解码/打包/最终抽帧。


## 当前交付 run-v12（2026-10-16）
- completed: 夜鹭腿段由260px缩到173px，取消持续上抬身体，抬脚约54px；保留快步节奏。16画风逐套眼位置注册，红色虹膜/黑瞳、两根白色枕羽随头运动。
- aspect_ratio: 9:16；width: 1080；height: 1920；delivery_mode: ai_review_once（既有预算已用，不新增角色）。
- video_path: out/film-run-v12-natural-heron-final/video.mp4
- video_sha256: 364a92c3146a40ab1789ababa2a41f0dcd3770f8a5f2056507fa591289fe5a51
- verification: 31秒/1080×1920/48fps/1488帧/双声道AAC，全片解码通过；浏览器错误0；970份文件快照签名通过。354时刻动物岸边固定/看空地、16物种唯一、三处乱序seek通过；152落脚音同步，全部腿长可达。
- actual_view: 主制作查看16套源图/头部、16画风新版关键帧、样段48有序抽帧，以及最终16场布局/18处局部转场结尾；非独立审核，未完整连续播放/实际听音。
- protected: 文字、16时代16种动物、低头看空地、原音乐；历史v11及更早版本保留。
- delivery: DELIVERY-RUN-V12.md；qa/film-run-v12-natural-heron-final/production-check.json。
- next: 展示新版，按用户反馈继续；不自动增加审核或恢复其他项目。
