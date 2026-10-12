# 有限上下文独立审核

先读技能 independent-av-review.md、review-performance.md。继承用户当前模型。首次先看指定batch图片并保存实际理解/困惑，再打开packet的brief_after_blind做符合性核对。材料已在本地，不等待制作方第二次交接。

每个batch最多加载它的分页图和必要原尺寸细节；只读其他batch的简短已确认发现和待审范围。累计图片较多时保存当前报告并用新上下文续接剩余batch，不能把首次盲看重置。边界图用于连续性；只把实际可辨认且已观察的帧登记为已审。

只在本目录reports/写check_av_review兼容JSON；附batch_id、reviewer身份、当前视频哈希、观察方式/具体发现及证据文件哈希。未听音保持pending。机器合并不授予pass。修复轮数取packet，不因换上下文/审片者重置。
