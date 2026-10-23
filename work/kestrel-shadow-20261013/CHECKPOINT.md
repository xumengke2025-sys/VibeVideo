# 红隼与珠颈斑鸠 · 检查点

- objective: 按皮影参考源码及夜鹭制作流程，制作红隼捕猎珠颈斑鸠群的可播放视频，结合真实Boids邻域算法。
- delivery_mode: user_feedback（2026-10-13用户选择①）。默认零子代理。
- output: 1080×1920，24fps，约30秒；无解释字幕、无旁白，动作与戏曲锣鼓事件同步。
- completed: 已研究夜鹭v10及上游皮影源码；生成红隼、斑鸠和景片透明素材；完成关节装配、连续相机、14只Boids、721帧运动缓存和30秒音轨；6秒正式品质追击样段已导出。
- creative_direction: 红隼尝试捕猎，群体分裂、绕树、重聚，追击未成功。保留同一鸟群ID和连续世界，不重置镜头位置。
- sources: 本地lemo-opuscar皮影54.4秒影片；夜鹭v10为流程参考；Reynolds Boids原作者资料。
- verification: simulation-checks.json确认固定模拟、乱序缓存及捕食者扰动有效；修复Chrome加速2D栅格差异后，stills-seekdiag3/checks.json中4个乱序重复时刻像素哈希相同；样段解码通过。已查看代表帧和追击接触表，未全片连续审阅或实际听音。
- current: 正式v1成片完成，输出film/out/final-v1/video.mp4，SHA256为2274167e2d8b651eb460c43c3f1e454c07dba36fee4abfde58437291e1178ad0。
- final_verification: H.264，1080×1920，9:16，24fps，720帧；视频和AAC立体声音轨均30秒，音频48kHz；完整画面/音频解码通过，浏览器错误为空，文件72504293字节。证据见film/out/final-v1/evidence.json与ffprobe.json。
- unresolved: 无工程阻塞；此版本由用户反馈修改，未进行独立视听审核或完整听音。
- next: 直接展示成片与README，等待用户针对画面、节奏和声音的反馈。
