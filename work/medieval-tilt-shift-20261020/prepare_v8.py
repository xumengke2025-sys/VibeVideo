from pathlib import Path
import json,shutil
ROOT=Path(__file__).resolve().parent
hist=ROOT/'history/v7';hist.mkdir(parents=True,exist_ok=True)
for name in ['CHECKPOINT.json','plan.json','视频制作计划.md']:
    if not (hist/name).exists():shutil.copy2(ROOT/name,hist/name)
music=json.loads((ROOT/'audio/music-structure-v8.json').read_text(encoding='utf8'))
shots=[
 [0,8,[-48,-153,6],[-60,-89,104],[15,72,8],[14,61,9],45,48],
 [8,16,[-25,-42,40],[-18,-14,38],[-4,5,3.6],[0,27,3],50,50],
 [16,26.6,[23,9,41],[22,36,42],[0,29,1],[0,56,1],52,52],
 [26.6,36,[6,38,47],[12,63,49],[33,63,0],[34,85,1],52,52],
 [36,44.4,[-8,21,78],[-9,53,70],[-48,69,9],[-49,84,12],47,47],
 [44.4,51,[22,33,76],[20,45,80],[60,65,18],[66,82,20],50,50],
 [51,56,[-76,-113,153],[-128,-171,227],[8,89,6],[8,120,6],43,43]
]
names=['地平线显城','蓝釉祭仪大道与国王雕像','繁华市集与驮畜队','运河商船与装卸码头','王宫和台地花园','神明雕像与蓝釉神庙','巨城全景']
events=[{'id':f'v8-shot-{i}','start':s[0],'end':s[1],'name':names[i],'camera':s[2:],
         'music_source_time':music['excerpt_start']+s[0]} for i,s in enumerate(shots)]
plan=json.loads((ROOT/'plan.json').read_text(encoding='utf8'))
plan['v8_revision']={'music_master':music,'events':events,'tilt_shift':{'focus_band_half_height':.075,'blur_max_pixels':38,'world_motion':'8 Hz discrete updates, crowd about 4x prior speed, camera continuous','haze_start_metres':400},'historical_scope':'巴比伦风格幻想城邦；台地花园与王神雕像为解释性重构','sources':['https://www.metmuseum.org/essays/babylon','https://www.britishmuseum.org/blog/paradise-earth-gardens-ashurbanipal']}
(ROOT/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf8')
(ROOT/'v8-timeline.json').write_text(json.dumps({'music':music,'shots':shots,'events':events},ensure_ascii=False,indent=2),encoding='utf8')
cp=json.loads((ROOT/'CHECKPOINT.json').read_text(encoding='utf8'))
cp.update(version='v8',status='user_revision_model_building',next_action='真实模型效果图→强移轴与节奏关键样段→完整渲染；沿用同一交付模式，不重开审片轮次')
cp['feedback'].extend(['音乐强段开场并同步运镜','增建巴比伦奇观、蓝釉街区、王神雕像','增加居民、牲畜、商船表现繁荣','移轴感不明显：强化高位俯拍、窄清晰带与独立延时活动'])
cp['v8_music']=music;cp['v8_visual_validation']='pending actual render'
cp['verification']['independent_review']='旧v7审片已结束，0–1019帧连续缩图，结论incomplete；不适用于v8。'
cp['unresolved']=['v8新增模型、运镜和景深尚待实际渲染验证','音乐已分析能量与起音，但未实际听音']
(ROOT/'CHECKPOINT.json').write_text(json.dumps(cp,ensure_ascii=False,indent=2),encoding='utf8')
with (ROOT/'视频制作计划.md').open('a',encoding='utf8') as f:
    f.write('\n\n## v8 用户反馈改造（2026-10-20）\n\n沿用1080×1920、56秒。音乐主时钟采用原曲29.5–85.5秒候选片段；能量与起音分析不等于实际听音。真实模型增加王宫、独立台地花园、蓝釉祭仪长墙、王神雕像、居民及驮畜商队与商船。保留大道、运河和桥头连续性。建筑与雕像为巴比伦启发的幻想重构，不声称考古精确还原。\n\n移轴：中近景高位斜俯拍，清晰带半宽由17%缩至7.5%，前后景渐变虚化上限38px，降低远景雾，居民与牲畜采用8Hz延时更新，相机逐帧平滑。主体保持清晰，避免通过全画面模糊伪造微缩。\n\n'+ '\n'.join(f'- {s[0]}–{s[1]}秒：{names[i]}' for i,s in enumerate(shots))+'\n\n先渲染同一模型的整体效果图、街市与雕像细节；再做市集→运河切换与音乐同步样段。现有v7保留，审核记录不继承至v8。\n')

# Preserve v7 renderer; inherit its proven memory settings and replace only V8 art/time.
src=(ROOT/'render_city.py').read_text(encoding='utf8')
src=src.replace('babylon-city-v6.blend','babylon-city-v8.blend').replace('babylon-film-v6.blend','babylon-film-v8.blend')
src=src.replace("cam.data.clip_end=2000","cam.data.clip_end=5000")
src=src.replace('mist_settings.start=130','mist_settings.start=400').replace('mist_settings.depth=1200','mist_settings.depth=2200')
src=src.replace('np.abs(v-.49)-.17)/.5','np.abs(v-.49)-.075)/.23')
src=src.replace("physical.outputs[0],.58","physical.outputs[0],.30").replace("bn.outputs[0],.42","bn.outputs[0],.70")
src=src.replace('blur.z_scale=22;blur.blur_max=22','blur.z_scale=38;blur.blur_max=38')
begin=src.index('shots=[');end=src.index('actors=[',begin)
src=src[:begin]+"shots=json.loads((ROOT/'v8-timeline.json').read_text(encoding='utf8'))['shots']\n"+src[end:]
src=src.replace("noise.noise_dimensions='4D'","""noise.noise_dimensions='4D'
v8crowd=[bpy.data.objects[n] for n in json.loads(scene['v8_crowd'])]
v8animals=[bpy.data.objects[n] for n in json.loads(scene['v8_animals'])]
v8boats=[bpy.data.objects[n] for n in json.loads(scene['v8_boats'])]
""")
src=src.replace('),5);a,b', '),len(shots)-1);a,b')
src=src.replace('(4 if si==5 else b-a)','(b-a)')
src=src.replace('blur.z_scale=22*smooth(t/6);blur.blur_max=22','blur.z_scale=38*smooth(t/3);blur.blur_max=38')
src=src.replace('wt=math.floor(t*10)/10','wt=math.floor(t*8)/8')
src=src.replace("noise.inputs['W'].default_value=t*.055","""# Deterministic lane motion; no wrapping or teleportation in the shot window.
 for ob in v8crowd:
  base=Vector(ob['base']);speed=ob['speed']
  if base.x>40:base.x=21.1
  # New pedestrian paths occupy open main avenue and unobstructed quay sections.
  dy=math.sin(wt*.14+ob['phase'])*speed*10 if ob['span'] else 0
  if ob['span']==78 and base.y+dy<8:dy=16-2*base.y-dy
  ob.location=base+Vector((0,dy,.025*math.sin(wt*9+ob['phase'])))
 for ob in v8animals:
  ob.location=Vector(ob['base'])+Vector((0,math.sin(wt*.027)*ob['speed']*8,.018*math.sin(wt*8+ob['phase'])))
 for ob in v8boats:
  ob.location=Vector(ob['base'])+Vector((0,math.sin(wt*.04)*ob['speed']*12,.018*math.sin(t*1.3+ob['phase'])))
 noise.inputs['W'].default_value=t*.09""")
src=src.replace('smooth(t/.65)','smooth(t/.18)')
src=src.replace("if mode=='proof':frames=[24,96,192,480,624,720,960,1248]","if mode=='proof':frames=[168,288,504,744,960,1152,1296]\nelif mode=='stills':frames=[int(x) for x in args[1:]]")
src=src.replace("elif mode=='range':", "elif mode=='sample':frames=list(range(576,720))\nelif mode=='range':")
src=src.replace("folder=OUT/('proof-v6'", "folder=OUT/('sample-v8' if mode=='sample' else 'proof-v8' if mode=='stills' else 'proof-v8'")
src=src.replace('benchmark-v6','benchmark-v8').replace('eevee-test-v6','eevee-test-v8').replace('preview-v6','preview-v8').replace('frames-v6','frames-v8')
src=src.replace("scene.render.image_settings.file_format='PNG'","if mode=='stills':scene.cycles.samples=32\nscene.render.image_settings.file_format='PNG'")
compile(src,'render_city_v8.py','exec')
(ROOT/'render_city_v8.py').write_text(src,encoding='utf8')
print('V8 timeline, checkpoint and renderer ready')
