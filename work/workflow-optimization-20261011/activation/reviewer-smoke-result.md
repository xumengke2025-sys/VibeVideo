# 审片角色真实派工测试

派工：collaboration.spawn_agent；独立上下文；model=gpt-6-astra，reasoning_effort=medium。角色契约来自项目.codex/agents/video-reviewer.toml；不是客户端按自定义名称选择的测试。未观察/听取真实影片。

输入：15秒有声片只给5张关键帧和ASR，没有实际听音工具，希望一次审核交付。

返回：incomplete。全部视觉、实时及听音覆盖为空；音频感知unavailable；ASR和关键帧不能证明完整视听通过。要求媒体身份、全帧分页和实际音轨感知；完成可做的检查后诚实展示当前版，工具限制不靠盲目返工解决，两轮上限不重置。没有虚构缺陷时间码或模型运行元数据。
