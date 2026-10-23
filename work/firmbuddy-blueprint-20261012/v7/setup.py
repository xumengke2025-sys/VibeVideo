"""Rebuild the music-only revision without changing historical editions."""
import json
from pathlib import Path

R = Path(__file__).resolve().parent
scene = (R/'scene-body.js').read_text(encoding='utf-8')
first = scene.index('// Music-only edition:') if '// Music-only edition:' in scene else scene.index('function caption()')
last = scene.index('window.renderAt=', first)
scene = scene[:first] + '// Music-only edition: business labels remain in world space.\nfunction caption(){}\n' + scene[last:]
(R/'scene-body.js').write_text(scene, encoding='utf-8')
film = (R/'film.js').read_text(encoding='utf-8')
helpers = film[:film.index('// V6 original world geometry.')]
(R/'film.js').write_text(helpers+scene, encoding='utf-8')
p = R/'render.mjs'
p.write_text(p.read_text(encoding='utf-8').replace("version||'v6'", "version||'v7-music'").replace('/v6/index.html', '/v7/index.html'), encoding='utf-8')
plan = json.loads((R/'plan.json').read_text(encoding='utf-8'))
plan['revision'] = 'V7 music-only'
for shot in plan['shots']:
    shot['voiceover'] = ''
plan['soundtrack'] = {
    'master_clock': 'visual action events; musical phrases fit their anchor times',
    'voiceover': False, 'narration_captions': False, 'sample_rate': 48000,
    'style': 'Original instrumental electronic groove, warm analog bass, precision percussion, D minor harmony',
    'phrases': [
        {'start':1.2, 'end':12.1, 'beats':28, 'name':'input to experts'},
        {'start':12.1, 'end':21.4, 'beats':24, 'name':'expert relay to evidence'},
        {'start':21.4, 'end':31.2, 'beats':24, 'name':'evidence to question'},
        {'start':31.2, 'end':37.9, 'beats':16, 'name':'outputs to confirmation'},
        {'start':37.9, 'end':47.5, 'beats':24, 'name':'feedback to whole machine'},
        {'start':47.5, 'end':50.4, 'beats':8, 'name':'brand resolution'},
    ],
    'events': [
        {'id':'entry-one','at':.2,'action':'商机入口描绘','sound':'tick'},
        {'id':'entry-two','at':.36,'action':'疑问入口描绘','sound':'tick'},
        {'id':'entry-three','at':.52,'action':'拜访入口描绘','sound':'tick'},
        {'id':'paper-enter','at':1.2,'action':'载纸进入','sound':'downbeat'},
        {'id':'scan','at':5.1,'action':'筛选扫描启动','sound':'accent'},
        {'id':'expert-one','at':12.1,'action':'专家一亮起','sound':'relay','note':74},
        {'id':'expert-two','at':12.5,'action':'专家二亮起','sound':'relay','note':77},
        {'id':'expert-three','at':12.9,'action':'专家三亮起','sound':'relay','note':81},
        {'id':'opinion-one','at':14,'action':'意见一汇入','sound':'relay','note':69},
        {'id':'opinion-two','at':14.4,'action':'意见二汇入','sound':'relay','note':72},
        {'id':'opinion-three','at':14.8,'action':'意见三汇入','sound':'relay','note':77},
        {'id':'archive-travel','at':16.3,'action':'沿支路进入知识库','sound':'travel'},
        {'id':'evidence-extract','at':21.4,'action':'资料抽页','sound':'downbeat'},
        {'id':'gap-reveal','at':22.5,'action':'资金安排未提供','sound':'tick'},
        {'id':'evidence-result','at':23.4,'action':'核实结论出现','sound':'accent'},
        {'id':'output-travel','at':25.8,'action':'缺项送向成果台','sound':'travel'},
        {'id':'slider-travel','at':29.4,'action':'缺项滑块移动','sound':'travel'},
        {'id':'slider-lock','at':31.2,'action':'滑块落定成为具体问题','sound':'drop'},
        {'id':'output-one','at':32.8,'action':'成果口一出现','sound':'relay','note':74},
        {'id':'output-two','at':33,'action':'成果口二出现','sound':'relay','note':77},
        {'id':'output-three','at':33.2,'action':'成果口三出现','sound':'relay','note':81},
        {'id':'confirm-lock','at':37.9,'action':'用户确认锁扣闭合','sound':'drop'},
        {'id':'task-create','at':38.3,'action':'跟进任务出现','sound':'tick'},
        {'id':'feedback-travel','at':40.3,'action':'记录沿反馈轨道返回','sound':'travel'},
        {'id':'machine-reveal','at':44,'action':'全景关系标注','sound':'accent'},
        {'id':'brand-complete','at':46.8,'action':'品牌标题栏完成','sound':'accent'},
        {'id':'pullback-complete','at':47.5,'action':'整机拉远完成','sound':'drop'},
        {'id':'ending-hold','at':50.4,'action':'稳定结尾','sound':'resolve'},
    ],
    'breaks': [[30.99,31.2],[37.67,37.9],[47.27,47.5]],
    'density': [
        {'start':0,'end':1.2,'gain':.2,'name':'mechanical count-in'},
        {'start':1.2,'end':12.1,'gain':.82,'name':'forward groove'},
        {'start':12.1,'end':16.3,'gain':.52,'name':'expert relay foreground'},
        {'start':16.3,'end':21.4,'gain':.95,'name':'camera travel build'},
        {'start':21.4,'end':25.8,'gain':.48,'name':'evidence reading space'},
        {'start':25.8,'end':31.2,'gain':1,'name':'output build'},
        {'start':31.2,'end':35,'gain':.74,'name':'outputs'},
        {'start':35,'end':37.9,'gain':1,'name':'confirmation build'},
        {'start':37.9,'end':44,'gain':.84,'name':'feedback groove'},
        {'start':44,'end':47.5,'gain':1,'name':'whole-machine lift'},
        {'start':47.5,'end':50.4,'gain':.78,'name':'brand cadence'},
        {'start':50.4,'end':52,'gain':.18,'name':'final decay'},
    ]
}
(R/'plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding='utf-8')
print('V7: voiceover and narration captions removed; action-anchored score timeline prepared.')
