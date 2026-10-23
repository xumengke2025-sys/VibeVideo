from pathlib import Path
import json,datetime
root=Path(__file__).resolve().parent
p=root/'CHECKPOINT.json';c=json.loads(p.read_text(encoding='utf8'))
c['version']='v6'
c['status']='full_resolution_tiled_render_in_progress'
c['updated_at']=datetime.datetime.now().isoformat(timespec='seconds')
c['objective']='完成优雅、精细的近东巴比伦巨型城市移轴短片；街道连贯、城区延伸到地平线，无龙；1080×1920、56秒、一次AI审核。'
c['verification']['render']='v5巨城8张设定帧已经输出；本次实际查看4秒、26秒、52秒。v6补接西岸横街；OptiX 256px分块连续4帧成功，正在以32帧进程输出1344帧。完整成片未完成。'
c['verification']['assets']='model/babylon-city-v6.blend 保留v5的10972座远景院落、原有精细核心区；横街从x=12延伸到x=23西岸桥头。结构见model/out/street-connections-v6.json；新版最终画面待检查。'
c['verification']['audio']='原创56秒配乐和环境音已生成，48kHz立体声；已有测量约-15.91 LUFS、-1.83 dBTP。实际听音未完成，当前工具无音频感知通道。'
c['completed'] += [x for x in ['定位原失败为GPU/shared host memory分配失败；没有终止无关进程或降低正式画幅','CUDA/CPU合成成功但较慢；OptiX 256px分块+GPU降噪/合成连续4帧通过，约8–10秒/帧','v6补齐远景西岸横街至桥头，保留v5模型及旧输出','采用独立frames-v6目录、原子PNG写入、32帧进程、断点续渲，避免不同降噪器样片混入成片'] if x not in c['completed']]
c['unresolved']=['完整1344帧尚在渲染，完成后需合成、完整解码与画幅/音轨检查','待检查新版开场连续状态、街道连接及镜头切换','建筑仍有程序化重复，人物为简化微缩模型；不声称写实实拍或完美','一次独立审核尚未开始；实际听音工具受限，不能宣称完整视听通过']
c['next_action']='监控render/pipeline-status.json和batch-logs-v6，检查首段连续输出；候选片完成后一个独立审片角色实际审画面，按报告最多修复一次再交付；如听音不可感知，明确未完成。'
c['render_session_id']=82597
c['review_budget']={'reviewer_started':False,'repair_rounds_used':0,'max_repair_rounds':1}
p.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(c['status'])
