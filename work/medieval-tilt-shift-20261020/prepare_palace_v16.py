from pathlib import Path
import json,datetime
P=Path(__file__).resolve().parent
s=(P/'render_city_v15.py').read_text(encoding='utf8')
s=s.replace("import v15_motion\n","import v15_motion\nimport v16_camera\n")
s=s.replace('babylon-city-v15-detail.blend','babylon-city-v16-palace.blend')
s=s.replace("pose=v15_motion.camera(t)","pose=v16_camera.camera(t)")
s=s.replace("if mode=='character':blur_strength.outputs[0].default_value=.12","if mode=='character':blur_strength.outputs[0].default_value=.12\n if pose['shot']==9:\n  band_center.outputs[0].default_value=.51;band_half.outputs[0].default_value=.16;band_tilt.outputs[0].default_value=-.11\n  focus.outputs[0].default_value=1/(Vector((61,1,10))-cam.location).length")
s=s.replace('qa/v15/','qa/v16/').replace("'-v15'","'-v16'")
for name in ['sample','proof','benchmark','eevee-test','preview','frames']:s=s.replace(name+'-v15',name+'-v16')
s=s.replace("model/babylon-film-v15.blend","model/babylon-film-v16.blend")
(P/'render_city_v16.py').write_text(s,encoding='utf8')
s=(P/'render_pipeline_v15.py').read_text(encoding='utf8')
s=s.replace('v15','v16').replace("'v16_motion.py','v16_route.py'","'v15_motion.py','v15_route.py','v16_camera.py','qa/v15/camera-height-corrections.json'")
s=s.replace('model/babylon-city-v16-detail.blend','model/babylon-city-v16-palace.blend').replace('audio/final-mix-v16.wav','audio/final-mix-v15.wav')
s=s.replace('[8,15,19,25,31,44,55,64,74,81]','[8,19,25,31,44,55,64,74,81]')
(P/'render_pipeline_v16.py').write_text(s,encoding='utf8')
s=(P/'assemble_city_v15.py').read_text(encoding='utf8').replace('v15','v16').replace('audio/final-mix-v16.wav','audio/final-mix-v15.wav').replace('风衣骑手-巴比伦巨城','风衣骑手-临河宫殿-巴比伦巨城')
(P/'assemble_city_v16.py').write_text(s,encoding='utf8')
cp={'objective':'Complete 90-second featureless cyclist Babylon film with a detailed river palace inspired by user image.','status':'palace_model_build_and_proof','aspect_ratio':'9:16','width':1080,'height':1920,'fps':24,'duration':90,'frame_count':2160,'delivery_mode':'ai_review_once','review_budget':'Existing independent review round exhausted; producer verification only, actual listening unavailable.','reference_image':'C:/Users/67236/AppData/Local/Temp/codex-clipboard-5e8df68e-c771-4cb6-b181-4ab736ff4c46.jpg','protected':['v15 frozen inputs and 107 existing frames','featureless rider geometry and continuous world route','blue glaze and city population','two-bank towpaths and bridges','user Dream of Babylon music'],'completed':['Read project and current v15 checkpoint','Verified no active Blender or Babylon pipeline process','Inspected reference image and east-bank site; selected southern riverfront before temple and south of bridge','Authored original layered palace builder and versioned v16 renderer; no mixed-world frame reuse'],'unresolved':['Palace proof composition and site checks','All-frame render, encode and decode','Actual listening unavailable'],'next_action':'Build palace; view actual final-size proof frames and establish six-second river palace view; then freeze and render v16.','updated_at':datetime.datetime.now().astimezone().isoformat()}
(P/'CHECKPOINT-v16.json').write_text(json.dumps(cp,ensure_ascii=False,indent=2),encoding='utf8')
old=json.loads((P/'CHECKPOINT-v15.json').read_text(encoding='utf8'));old.update(status='superseded_by_palace_v16',next_action='Preserve frozen inputs and old frames; continue CHECKPOINT-v16.json.',updated_at=cp['updated_at'])
(P/'CHECKPOINT-v15.json').write_text(json.dumps(old,ensure_ascii=False,indent=2),encoding='utf8')
print('V16_RENDER_FILES_PREPARED')
