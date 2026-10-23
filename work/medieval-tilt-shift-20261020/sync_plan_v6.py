from pathlib import Path
import json,shutil
root=Path(__file__).resolve().parent
history=root/'history/v5-before-continuity';history.mkdir(parents=True,exist_ok=True)
for name in ['plan.json','source-adoption.json','视频制作计划.md']:
    if not (history/name).exists():shutil.copy2(root/name,history/name)
p=root/'plan.json';j=json.loads(p.read_text(encoding='utf8'))
j['version']='v6';j['status']='full_resolution_tiled_render_in_progress'
j['user_requirements']+=['街道连贯','宏伟、一望无际的巨型巴比伦城市']
j['audio']['motif']='四音城市动机：地平线显城时建立，市集段减配器，神庙与全城段扩展声部，52秒后收束。'
j['audio']['source_status']='原创56秒配乐及环境声已生成；GeneralUser GS音源及授权已保留；实际听音未完成。'
j['assets_status']='可编辑Blender模型model/babylon-city-v6.blend；精细核心区、一万余座远景院落、连续中轴大道与运河、横街补接西岸桥头。'
j['world']['extent_m']=[-650,650,-29,1800]
j['world']['street_continuity_evidence']='model/out/street-connections-v6.json'
j['clock_design']['world']='floor(t*10)/10的绝对时间量化；船只与行人10Hz步进，相机24fps连续。水面变化保持连续。'
j['clock_design']['speed_curve']=[{'start':0,'end':56,'from':1,'to':1}]
j['quality_contract']['status']='model_and_static_proofs_rendered_continuous_candidate_pending'
j['quality_contract']['focus_depth']='Blender Z pass为相机到表面的距离，焦点使用相机到目标的距离；与屏幕清晰带幅值混合。不同于原Three参考的view-space z。'
j['quality_contract']['final_sampling']='Cycles OptiX 24 samples、adaptive threshold .065、GPU降噪；1080×1920原生输出、256px内部块；Blender Defocus合成。未使用原参考128次WebGL gather或2倍宽高超采样。'
j['pilot']['status']='v5_static_proofs_complete_v6_continuous_rendering'
j['evidence'].update(runtime_rendered=True,viewed_frames=True,heard_audio=False,validation_scope='模型及v5设定帧已看；v6输出中，不等同全片或听感通过。')
p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
p=root/'source-adoption.json';j=json.loads(p.read_text(encoding='utf8'))
j['adoption']['current_blender']='render_city.py：原片的深度与屏幕清晰带、机位与目标分轨、运动与摄影分离机制；Blender Z pass距离焦深+Defocus实现，未直接运行WebGL gather。'
j['verification']['current_model']='v6 Blender模型及最终1080×1920连续渲染中；旧Three预演不作为交付。'
p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
p=root/'视频制作计划.md';s=p.read_text(encoding='utf8').replace('巨城版 v5','巨城版 v6').replace('当前模型为 model/babylon-city-v5.blend','当前模型为 model/babylon-city-v6.blend').replace('finish_city.py → expand_metropolis.py','finish_city.py → expand_metropolis.py → connect_streets.py')
s+='\n## 连续渲染恢复（v6）\n\n保留v5模型和试帧；v6补齐横街到西岸桥头的11米铺装缺口。正式画幅、几何细节和原配乐保持。故障日志确认GPU/shared host memory不足；256px内部块、场景缓存与32帧进程已通过短段恢复测试。frames-v6与旧试验降噪输出分目录，采用原子PNG写入和断点续渲。全片待输出，不能把渲染进度当成审片通过。\n'
p.write_text(s,encoding='utf8')
print('plan and provenance synchronized to v6')
