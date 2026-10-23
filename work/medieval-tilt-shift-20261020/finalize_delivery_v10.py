"""Bind completed v10 output, producer observations, and honest delivery limits."""
from datetime import datetime
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent

def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf8'))

def write(path, value):
    (ROOT / path).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf8')

engineering = read('delivery/engineering-check-v10.json')
frozen = read('render/frozen-v10-manifest.json')
evidence = read('qa/v10/producer-evidence-v10.json')
observations = read('qa/v10/producer-observations-v10.json')
style = read('qa/v10/style-source-check-v10.json')
video = Path(engineering['video'])
assert hashlib.sha256(video.read_bytes()).hexdigest() == engineering['sha256']
assert evidence['video_sha256'] == observations['video_sha256'] == engineering['sha256']
assert observations['actual_viewed_encoded_frames']
assert all(frame in observations['actual_viewed_encoded_frames'] for frame in [168, 288, 504, 744, 852, 960, 1152, 1296])
for key, path in [('model_sha256', 'model/babylon-city-v10.blend'),
                  ('renderer_sha256', 'render_city_v10.py'),
                  ('timeline_sha256', 'v8-timeline.json'),
                  ('mix_sha256', 'audio/final-mix-v8.wav')]:
    assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == frozen[key], path
assert engineering['decode_exit'] == 0 and not engineering['decode_errors']
assert (engineering['width'], engineering['height'], engineering['frames']) == (1080, 1920, 1344)

now = datetime.now().isoformat(timespec='seconds')
evidence['actual_viewed_frames'] = observations['actual_viewed_encoded_frames']
evidence['actual_view_method'] = observations['method']
write('qa/v10/producer-evidence-v10.json', evidence)
status = {
    'version': 'v10', 'video': str(video), 'sha256': engineering['sha256'],
    'engineering': 'passed', 'source_freeze_verified': True,
    'specification': {'width': 1080, 'height': 1920, 'duration': 56, 'fps': 24,
                      'decoded_frames': 1344, 'audio': '48kHz stereo'},
    'producer_observations': 'qa/v10/producer-observations-v10.json',
    'review': 'incomplete', 'new_independent_review_round': False,
    'review_budget': {'used': 1, 'maximum': 1, 'reviewer': '/root/babylon_av_review'},
    'historical_review_reference': 'qa/v9/av-review.json (v9 hash; not a v10 pass)',
    'actual_audio_listening': 'unavailable',
    'limits': ['v10 only has producer inspection of the stated representative encoded frames.',
               'Full independent visual coverage and actual listening were not completed.',
               'Babylon-inspired fantasy reconstruction; not an archaeological reconstruction.'],
    'updated_at': now,
}
write('delivery/delivery-status-v10.json', status)
style.update(video_sha256=engineering['sha256'], current_status='completed_with_stated_artistic_boundaries',
             encoded_observation_record='qa/v10/producer-observations-v10.json',
             observed_encoded_frames=observations['actual_viewed_encoded_frames'],
             encoded_observations=observations['observations'],
             result='整体风貌采用新巴比伦与古代近东视觉语汇；代表编码画面可辨识移轴微缩景深。幻想布局、花园、雕像和船型的边界保留，不称考古复原。',
             completion_gate='完整编码、1344帧解码、冻结哈希与所列代表编码画面已核对；未宣称独立全片视听审核通过。')
write('qa/v10/style-source-check-v10.json', style)

(ROOT / 'delivery/交付说明-v10.md').write_text('''# 暮河城 · 巴比伦巨城 v10

完整影片：暮河城-巴比伦巨城-Dream-of-Babylon-v10.mp4。竖屏1080×1920，56秒，24fps。

保留地平线显城、蓝釉大道与国王雕像、市集人畜、运河商船、台地花园、神像前庭和巨城全景。摄影沿用高位斜俯、窄清晰带与真实深度混合散焦；人物和牲畜按8Hz更新、2.4倍活动时间，相机逐帧平滑。开场先完成城市显露，再逐渐增强散焦。

v10将第四艘船的七根坐板重新归入动画船体层级，避免船已移动而坐板留在河中。桥头引坡、砖墩木梁桥、既有街道布局、城市规模、蓝釉和土金材质均保留。建筑、人物和雕像为巴比伦启发的幻想重构，不声称精确复原某一历史城市或神像。

音乐采用用户提供的《Dream Of Babylon》29.5–85.5秒连续节选，0.15秒渐入、最后3秒渐出，配低音量环境声。摄影按音乐能量与起音候选安排；没有实际听音，不能将候选强段和节奏对齐写成听感验收。

工程检查通过：1344帧与完整音轨解码无错误，画幅、时长、帧率和48kHz双声道符合计划；冻结模型、摄影、时间表及混音哈希一致。制作角色实际查看的编码画面和具体观察见qa/v10/producer-observations-v10.json。

已沿用本片唯一审片角色完成此前的一轮局部审核及修复，预算为1/1。v9报告不自动覆盖v10；本版是制作角色验证，不是新增独立审核。全片独立画面覆盖和实际听音未完成，因此不标注完整视听审核通过。

可编辑工程与复现入口见工程入口-v10.md；旧版模型、源码、成片及审核记录均保留。
''', encoding='utf8')

(ROOT / 'delivery/工程入口-v10.md').write_text('''# v10 可编辑工程与复现入口

项目根目录：D:/ai项目/ai动画/VibeVideo项目/work/medieval-tilt-shift-20261020

- 城市模型：model/babylon-city-v10.blend
- 摄影及后期：render_city_v10.py
- 摄影时间表：v8-timeline.json（v10继续使用）
- 模型修改：model/fix_boat_parenting_v10.py（输入为v9模型）
- 完整渲染：start_full_v10.py → render_pipeline_v10.py
- 编码与全片解码：assemble_city_v10.py
- 音乐混音：audio/final-mix-v8.wav；制作脚本mix_music_v8.py
- 来源与迁移范围：source-adoption.json
- 冻结哈希：render/frozen-v10-manifest.json
- 工程检查：delivery/engineering-check-v10.json
- 制作观察：qa/v10/producer-observations-v10.json

本机Blender：D:/ai项目/ai动画/VibeVideo项目/tools/blender-portable/blender-4.5.3-windows-x64/blender.exe。
正式配置：Cycles OptiX、24采样、GPU降噪和合成，1080×1920、24fps。32帧一批，PNG原子写入，可断点续渲。修改模型或摄影后应使用新的输出目录和冻结记录，不将不同源码的PNG混入当前序列。

参考Lemo《Toy Town Rush Hour》的深度+清晰带散焦、绝对时间摄影和独立量化活动机制；当前影片采用Blender原创城市模型与Defocus后期，并非原WebGL着色器的逐项复制。原来源和许可保留在source-adoption.json所列位置。
''', encoding='utf8')

cp = read('CHECKPOINT.json')
cp.update(version='v10', status='v10_delivery_ready_review_incomplete', updated_at=now,
          final_candidate=str(video), final_candidate_sha256=engineering['sha256'],
          next_action='展示完整v10影片与简明审核范围，后续按用户反馈修改。')
cp['verification'].update(
    render='v10全部1344帧，1080×1920、24fps、56秒，完整音视频解码无错误；冻结源码哈希一致。',
    assets='model/babylon-city-v10.blend：沿用巨城、蓝釉建筑、街道、人畜、雕像、砖墩木梁桥与货驳；第四艘船坐板已归属动画船体。',
    independent_review='既有一轮预算1/1已用；v10仅制作角色代表帧检查。v9局部报告不作为v10通过结论。全片独立画面覆盖及实际听音未完成。',
    review_evidence_consistency='v9报告为历史归档；v10制作检查绑定当前视频哈希，见qa/v10/producer-evidence-v10.json。',
    producer_evidence='qa/v10/producer-evidence-v10.json 与 producer-observations-v10.json，绑定当前成片哈希。')
cp['unresolved'] = status['limits']
cp['delivery_note'] = '完整v10可播放，工程检查通过；制作角色实际查看记录见qa/v10。全片独立视听审核未完成，实际听音不可用。'
cp['v10_producer_verification'] = observations
cp['v10_style_check'] = 'qa/v10/style-source-check-v10.json'
cp['v10_resume'].update(active_pipeline_pid=None, launcher_pid=None,
                       progress_at_check='1344 of 1344 frames; encoded and decoded',
                       next_action='Completed; show current film and await user feedback.')
done = 'v10当前编码输出已完成制作角色代表画面核对、冻结源码核对与交付记录；没有新增独立审核轮次。'
if done not in cp['completed']:
    cp['completed'].append(done)
write('CHECKPOINT.json', cp)

plan = read('plan.json')
plan.update(version='v10', status='complete_video_review_incomplete',
            assets_status='model/babylon-city-v10.blend；第四艘船坐板归属修复，既有摄影、美术、音频保留。')
plan['quality_contract']['status'] = 'full_render_decoded_source_freeze_verified_review_incomplete'
plan['evidence'].update(validation_scope='完整v10输出并全片解码通过；代表编码画面由制作角色实际查看，非新增独立审片。',
                        engineering_report='delivery/engineering-check-v10.json',
                        frame_audit='qa/v10/producer-evidence-v10.json', heard_audio=False)
plan['v10_revision'] = {'model': 'model/babylon-city-v10.blend',
                        'renderer': 'render_city_v10.py',
                        'authoritative_timeline': 'v8-timeline.json',
                        'frozen_manifest': 'render/frozen-v10-manifest.json',
                        'encoded_video': str(video),
                        'review': 'Producer inspection only; existing independent round exhausted.'}
write('plan.json', plan)
adopt = read('source-adoption.json')
adopt['adoption']['current_blender'] = 'render_city_v10.py沿用v8摄影、真实深度+窄清晰带Defocus与8Hz独立活动；模型采用v10坐板归属修复。'
adopt['verification']['v10'] = '1344帧正式Cycles渲染、56秒音画编码、完整解码及冻结源码核对完成。制作角色实际查看范围见qa/v10；全片独立视听审核未完成。'
write('source-adoption.json', adopt)
pipeline = read('render/pipeline-status-v10.json')
assert pipeline['completed_frames'] == 1344
pipeline.update(stage='delivery_ready_with_review_limits', process_id=None)
write('render/pipeline-status-v10.json', pipeline)
md = ROOT / '视频制作计划.md'
text = md.read_text(encoding='utf8')
text = text.replace('（移轴城市版 v9）', '（移轴城市版 v10）', 1)
lines = text.splitlines()
if len(lines) > 2 and lines[2].startswith('当前交付为v9：'):
    lines[2] = '当前交付为v10：沿用v8七段摄影和v9桥船修复，并完成第四艘船坐板归属修正。1080×1920、56秒、24fps；原曲29.5–85.5秒节选；模型为 `model/babylon-city-v10.blend`，摄影入口为 `render_city_v10.py`。下文早期方案保留为制作历史。完整音画已输出；本版制作核对见 `qa/v10/`，此前独立局部审核见 `qa/v9/`，均不能视为本版全片独立视听通过。'
    text = '\n'.join(lines) + '\n'
section = '''\n\n## v10 续接完成\n\nv10将第四艘船的七根坐板归入动画船体，修复河中孤立木条。模型为model/babylon-city-v10.blend，摄影为render_city_v10.py；v8摄影时间表、配乐、移轴与城市布局保留。完整1344帧已正式渲染并编码为56秒影片，全片解码与冻结哈希核对通过。制作角色实际查看范围见qa/v10/producer-observations-v10.json；本片一轮独立审核预算已用，v9报告不自动覆盖v10，全片独立视听审核及实际听音未完成。\n'''
if '## v10 续接完成' not in text:
    text += section
md.write_text(text, encoding='utf8')
print(json.dumps({'delivered': str(video), 'sha256': engineering['sha256'],
                  'engineering': 'passed', 'review': 'incomplete'}, ensure_ascii=False))
