from pathlib import Path
from datetime import datetime
import json,sys
ROOT=Path(__file__).resolve().parent
p=ROOT/'CHECKPOINT.json';d=json.loads(p.read_text(encoding='utf8'))
d['status']=sys.argv[1] if len(sys.argv)>1 else 'v8_continuous_sample_rendering'
d['updated_at']=datetime.now().isoformat(timespec='seconds')
d['v8_visual_validation']={'actual_viewed':['7s overall city from earlier v8','12s royal forecourt after occlusion fix','21s market','31s canal','40s garden after supported stairs','48s divine forecourt','54s giant city'],'current_proofs':'render/proof-v8-final/','pending':'3-second moving sample; closed crown and diagonal divine focus are subsequent source refinements, not yet viewed'}
d['v8_runtime_note']='非分块 + GPU OpenImageDenoise + GPU合成已成功；修正真实RenderSettings持久缓存。CUDA六关键帧通过；正在检验OptiX连续72帧。此前分块EXR读回/OptiX降噪内存错误已改路，保留失败日志。'
d['v8_model_fixes']=['国王移到门前空地，保留通行空间','花园采用实体支撑折返楼梯与平台连接','王冠封顶','神像镜头改为前庭，斜清晰带穿过两尊神像','人畜按8Hz更新、2.4倍活动时间；相机逐帧平滑']
d['unresolved']=['连续样段与全片v8尚未交付','能量/起音分析不等于实际听音，当前无音频感知工具']
d['next_action']='完成市集→运河3秒连续样段与关键图，冻结源码后渲染全部1344帧、合成Dream Of Babylon并做工程检查。'
d['review_budget']['note']='沿用唯一既有审片角色；v7结论不覆盖v8，不重置审核预算。实际音频感知不可用，不能声称听音通过。'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
print(d['status'])
