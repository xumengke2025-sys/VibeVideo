# 宝宝蜡笔绘本动画 · CHECKPOINT

- objective: 以用户选定① Lemo《The Moon Can't Sleep》原片和源码为主参考，设计宝宝从家经院子到院外花园、看日落与夜色、回到绘本书页的动画。当前完成无字视觉故事和连续镜头设计。
- delivery_mode: user_feedback。2026-10-13用户明确授权制定计划后执行，先生成视频再由用户审核；不再询问。
- format: 1080×1920，9:16；约60秒设计提案。
- latest_constraints: 无文字、无字幕、无旁白，纯画面推动；深入参考源码，重点转场顺畅。家门和院门不同，花园在院外。
- skill: D:/Codex/skills/vibe-video/SKILL.md；已读 reference-study、director-design、art-direction、production-quality、motion-craft、subject-cinematography、code-cinema。用户已指定故事，不重新列三种候选。
- completed: 5部候选原片各12张分布抽帧已看，用户选①蜡笔绘本；其余不继续。来源证据在 evidence.json。
- completed: 已查看宝宝三张、院子/花园两张照片；提炼五官比例及场景特征。院门连接位置属动画设计，未声称实际复原。
- completed: 深入阅读 core/lib.js、film.js、chars.js、rig.js、crayon.js、gl.js、world.js、main.js、end.js 的摄影、动作、多视角、笔压材质、夜色与纸页接管实现。固定commit e3cb16f63768c68693ff0e15171d6e755457cc32。
- completed: study_transitions.py 已成功完成；三个取样序列接触表实际查看：18–26s（17样本）、27.5–35.5s（17样本）、44.5–49.2s（20样本）。生成命令进程87461已结束，退出码0；不需继续轮询。
- evidence: character-camera-sequence.jpg、night-wash-sequence.jpg、page-return-sequence.jpg、transition-evidence.json；取样宽360，非全帧/正常速度播放，未听音。
- deliverables: production-brief.md 已重写为完全无字视觉版；source-study.md 记录源码链、观察范围、转场迁移及无字删除清单。
- design: 光斑→家门→橘猫回应/回头→院门→院外石板→摸花→光引导抬眼→日落→三道蓝色水彩刷痕显白蜡星→月牙/灯→哈欠→同画回右页→无字翻页。主要在同一世界内连续摄影，非逐场换背景。
- production: 独立工程 ../baby-crayon-garden-20261013/ 已完成代表帧、跨门关键样段及完整60秒成片；跨门裁切、日落遮挡和月牙轮廓已局部修正。
- verification: 完整成片文件/画幅/帧率/时长/音轨/完整解码全部通过；报告 ../baby-crayon-garden-20261013/out/verification.json。制作代表帧与17–24.5秒16个连续取样已查看。上游未重渲、未完整播放/听音；本片未独立审片或完整听音，不声称完整视听审核通过。
- deliverable: ../../动画成品/宝宝和太阳的晚安-蜡笔绘本-v1.mp4；sha256 494b989a4c50dc9157bfd0a3b7d68fa0b9539b912beb5785b3c83338656e30c1。
- next: 按 user_feedback 直接展示第一版，待用户反馈；零子代理，不改变模型，不恢复其他宝宝项目。
