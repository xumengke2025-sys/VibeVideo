# 拿破仑 · 皮影名画

- objective: 制作1080×1920竖屏皮影片，以经典名画讲完1796—1804从将军到皇帝的阶段，结合真实Boids规则与连续转场，继承夜鹭制作流程。
- delivery_mode: user_feedback（用户2026-10-13选择①）；零子代理。
- completed: 四景源码、五张透明分件图集、64秒中文旁白/锣鼓/拟音音轨已完成；已读夜鹭v10、红隼Boids、上游皮影gl.js及STYLE。四幅历史原型来源保存在research/SOURCES.md。阿尔卑斯图集v2已将王室百合花改为几何金点。
- creative_direction: 《一顶皇冠之前》；旗帜→雅法拱廊→阿尔卑斯披风→加冕长袍，皮革碎片使用分离/对齐/聚合规则参与场景交接；人物保持刚性关节。
- output_plan: 64秒，1080×1920，24fps，中文旁白、事件日期/作品标注，戏曲锣鼓和原创环境拟音。
- verification: Boids重复模拟一致、关闭邻域规则轨迹改变、数值有限；160个ID，1/60秒模拟、12fps缓存/24fps插值。音轨48kHz双声道64秒、峰值0.442无削波。layout2/layout3静帧重复乱序取帧哈希一致，浏览器无错误；实际查看24、38、56、60.8秒，皇冠接触成立，袖口遮脸已修正。未声称完整参考回放或实际听音。
- next: 已完成四景人物及马的v2修复并交付，等待用户对新版具体反馈；delivery_mode沿用user_feedback，零子代理。
- final: film/out/final-v1/video.mp4；64.000秒，1080×1920，24fps，1536帧，H.264视频/AAC 48kHz双声道音频，84,102,059字节。完整解码通过，无浏览器异常；evidence.json/ffprobe.json已保存。SHA256: 1469f15bcdb651296dd3651d6c864fe62217ff82804bccea1880942b372678f3。源码签名与sample-transition2一致。README、提示词及历史/声音署名齐全。
- sample: sample-transition2已输出1080×1920/24fps/7秒/168帧，双声道音轨及完整解码通过。实际查看47—53.75秒每0.25秒画面序列，49.5—50秒幕片覆盖换景，随后加冕关系显露和举冠动作启动。翻山38秒静帧v3已查看，面部无遮挡。无完整听音或独立审片结论。
- unresolved: 本机中文语音采用Microsoft Huihui Desktop；Edge TTS 403已停止重试。当前无独立审核安排。
- motion_feedback: 已查看四组实际渲染帧序列并核算目标可达性；主要问题为分件结构/层级不完整、身体无重心动作、白马腾跃姿态整体滑行、手道具不可达（持剑超51px、加冕末段超38px）。诊断见film/out/motion-diagnosis/DIAGNOSIS.md。静帧接触判断不能视为全段动作接触验证。
- repair_v2: 新rig-v2.js接入。人物分件先source-over组装后一次透光合成，拆分手臂/大小腿，固定骨长，手和道具绑定可达端点，加入重心准备/动作/回收。冠袍使用原生袖子，骑手跟随马鞍；新增透明horse-rig-v2.png、站立到抬前蹄再落地的马骨架。v1源码/音轨/成片均保存。
- repair_visual: 已实际查看layout1的4、23、39、57秒，layout2的4、39秒及crown的60.8秒；修正袖口误裁碎片、骑马后腿出框及加冕袖子遮脸。还查看v2四组各8帧的动作序列：旗1—8秒；探病18/19/20/21/22/23/25/27秒；马35/36/37/38/40/43/45/46秒；冠51.5/53/54.5/56/57.5/59/60/61秒。证据film/out/motion-v2-verification/*.jpg。属于制作抽查，未声称全帧审美审核或完整听音。
- repair_constraints: verify-rig.mjs覆盖1536个输出时刻，最大骨长/目标/接触/脚底误差2.6e-13px，无不可达姿态。结果film/out/motion-v2-verification/constraints.json。layout2及crown静帧乱序重复取帧一致，无浏览器异常。
- final_v2: film/out/final-v2/video.mp4，64秒，1080×1920/24fps/1536帧，H.264/AAC，完整音视频解码通过，零浏览器异常。SHA256 2cece04d19295fba1a1249b05adaec0132179183d8bcead0b712111a77cba778；与10秒加冕样段签名相同14f248180497eed20f710fb697a0ee9211b39323b3af470c1546123d352511d7，详见evidence.json/ffprobe.json。渲染+编码+检查170.315秒。
