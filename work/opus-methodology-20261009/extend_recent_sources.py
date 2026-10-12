"""Install pinned text archives; retain source bytes and evidence boundaries. Never execute upstream."""
import hashlib
import json
import shutil
from pathlib import Path

SKILL = Path('D:/Codex/skills/vibe-video')
TEMP = Path('C:/CodexTemp/vibe-more-sources-20261009')
OUT = Path(__file__).resolve().parent
LIB = SKILL / 'references/opus-methods.json'
lib = json.loads(LIB.read_text(encoding='utf-8'))

def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

dates = {
    'beach': '2026-09-24T00:22:09Z', 'reel': '2026-09-27T01:17:14Z',
    'mg': '2026-10-05T11:23:16Z', 'paper': '2026-09-26T07:17:57Z',
    'water': '2026-09-24T07:04:05Z', 'rigid': '2026-10-06T18:28:01Z',
}
save(OUT / 'pinned-commit-dates.json', {'checked': '2026-10-09', 'source': 'GitHub commits API: commit.committer.date', 'dates': dates, 'not_film_release_dates': True})
for sid, date in dates.items():
    s = lib['sources'][sid]
    s['commit_date'] = date
    s['reference_role'] = 'component' if sid in ('water','rigid') else 'film_engine' if sid == 'paper' else 'film'
    s['quality_evidence'] = 'representative_frames_and_windows_only' if sid in ('beach','reel') else 'source_inspected_video_unreviewed'
    manifest_path = SKILL / s['local_root'] / 'SOURCE.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    manifest.update({k: s[k] for k in ('commit_date','reference_role','quality_evidence')})
    if sid == 'mg':
        s['license_note'] = '代码MIT；字体和glyphs等衍生轮廓保留OFL等原许可，见上游README及assets/fonts/README.md。不能把全包统一视为MIT。'
        manifest['license'] = s['license_note']
    save(manifest_path, manifest)
lib['sources']['glass'].update(reference_role='component', quality_evidence='remote_source_only_no_local_archive')
lib['sources']['codex-tools'].update(reference_role='independent_tool', quality_evidence='mechanism_test_only_not_film_benchmark')

configs = [
    ('songbie', 'songbie', 'film', 'supplementary_opus_film',
     'Node Canvas解析三维坐标投影、逐帧图像与FFmpeg输出；不是三维物理解算器。',
     '保存8个文本文件；旋律/绘制源码已读，未观看或运行成片；Logic Pro钢琴样本、歌曲音轨与成片不在包中。',
     '作者README声明Claude Opus 5.5制作代码；所读视觉路径为Canvas，不调用生成视频服务。',
     '代码MIT；钢琴样本不随包，曲谱旋律公共领域的说明来自作者。',
     ['README.md:1-63','score.js:1-96','render.js:1-74,147-206,278-323,592-657,934-1011']),
    ('lemo', 'lemo-opuscar', 'film', 'supplementary_opus_films_selected_styles',
     'Canvas/解析投影/自定义着色器，采用art-deco、blueprint、ink-wash、hologram-hud及core文本。',
     '作者称43种风格；只归档4种选定风格及共享代码共147文件，未逐风格运行/审片。字体、音频、图片、模型与依赖不完整。',
     '作者README声明Opus 5.5代码影片；已读选定绘制路径。43种风格及98长片没有全面审查。',
     '根LICENSE为MIT，第三方字体/音乐/声音/样本等独立许可；GitHub API的NOASSERTION不代表没有LICENSE。',
     ['LICENSE:1-26','styles/art-deco/demo/engine/cam.js:1-28','styles/art-deco/demo/timeline.js:1-55','styles/art-deco/demo/film.js:1-70','styles/blueprint/demo/machine.js:1-135','styles/blueprint/demo/film.js:1-234','styles/ink-wash/demo/ink.js:1-165','styles/ink-wash/demo/story.js:1-32','styles/hologram-hud/demo/engine/holo.js:1-115,195-259','styles/hologram-hud/demo/film.js:1-259']),
    ('lyric', 'i-like-ur-look-lyric-video', 'film', 'recent_code_film_candidate',
     'TypeScript/Three.js、Canvas页面纹理、曲面纸页与自定义景深；继承mexicat/pdoom-video引擎。',
     '保存72个选定文本文件；歌曲、歌词/节拍数据、字体和依赖未随包。README成片链接coming soon；未运行或审片。',
     'README声明逐帧代码绘制；未独立确认作者采用的编码模型，不能统一归因Opus。音频分析模型不是视觉生成。',
     '代码MIT，保留app/LICENSE的引擎来源署名；版权歌曲不随库。',
     ['README.md:1-70','app/LICENSE:1-24','app/src/engine/curl.ts:1-57','app/src/engine/page.ts:1-115','app/src/engine/scene.ts:1-83','app/src/scenes/magazine/focus.ts:1-107','app/src/scenes/magazine/view.ts:1-30','app/src/scenes/magazine/handheld.ts:1-32','app/src/scenes/magazine/schedule.ts:1-105']),
    ('clearwater', 'clearwater', 'component', 'contemporary_optics_reference_not_original_proven',
     'WebGL2 FFT水面、折射网格焦散、Fresnel/吸收、实时互动涟漪。',
     '保存4文件；光学/循环关键源码已读，未运行。不是完整导演影片；没有核实对应图库原帖或编码模型。固定t不会重建涟漪历史。',
     '视觉核心为WebGL2着色器；不把代码路径推导为Opus作者归属。',
     'MIT，原LICENSE及程序化鹅卵石生成脚本保留。',
     ['README.md:1-52','index.html:1-45,49-100,277-321,490-529,865-919']),
]

installed = []
for sid, folder, role, relation, engine, scope, attribution, license_note, inspected in configs:
    meta = json.loads((TEMP / folder / 'TEXT_SOURCE.json').read_text(encoding='utf-8'))
    source_dir = TEMP / folder / 'source'
    dest = SKILL / 'assets/code-studies' / folder
    dest.mkdir(parents=True, exist_ok=True)
    rows = []
    for item in meta['retrieval']:
        path = Path(item['path'])
        rel = path.relative_to(source_dir)
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        assert digest == item['sha256'], path
        target = dest / rel
        if target.exists():
            assert target.read_bytes() == data, ('refuse overwrite', target)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
        rows.append({'source_path': rel.as_posix(), 'local_path': rel.as_posix(), 'sha256': digest, 'bytes': len(data)})
    repository = 'https://github.com/' + meta['repository']
    manifest = dict(repository=repository, commit=meta['commit'], commit_date=meta['commit_date'],
                    repository_created=meta['created'], checked='2026-10-09', license=license_note,
                    reference_role=role, quality_evidence='source_inspected_video_unreviewed', scope=scope,
                    inspected=inspected, excluded=['unselected source paths, external assets, audio, video, installed dependencies; not a complete offline build'],
                    runtime_verification='not run; no video reviewed', files=rows)
    if sid == 'clearwater':
        manifest['excluded'] = ['展示媒体与未采用文档；HTML内嵌程序化纹理保持原样；重生成纹理的Python依赖未安装']
    save(dest / 'SOURCE.json', manifest)
    lib['sources'][sid] = dict(id=sid, repository=repository, commit=meta['commit'], local_root='assets/code-studies/' + folder,
                              relation=relation, runtime='source_read_only', scope=scope, engine=engine,
                              commit_date=meta['commit_date'], repository_created=meta['created'], reference_role=role,
                              quality_evidence='source_inspected_video_unreviewed', model_attribution=attribution,
                              license_note=license_note, inspected=inspected)
    installed.append({'id': sid, 'files': len(rows), 'bytes': sum(r['bytes'] for r in rows)})

new_cards = []
def card(id, title, terms, purpose, relation, decisions, implementation, failure, review, refs):
    new_cards.append(dict(id=id, title=title, terms=terms.split('|'), purpose=purpose, relation=relation,
                          decisions=decisions, implementation=implementation, failure=failure, review=review,
                          source_refs=[dict(source=s, path=p, line=n) for s,p,n in refs], gallery_slugs=[],
                          status='code_observed_with_adaptation', status_note='选定源码已读；作者成片未在本轮审看，不认证原片质量或本机可运行性。'))

card('performance-handoff','用同一乐谱完成角色表演接棒','弹琴|钢琴|表演|接棒|乐谱|音乐|角色|雪人',
     '让角色关系在同一个动作中发生变化，观众从接棒理解情绪。','音符who、时间和键位同时决定声音、琴键与手部；雪人→猫→雪花延续同一旋律。',
     '先建立谁在弹，再用迟疑、停手和视线表达交接；音乐减速留给结尾，不让手在发声后才碰琴键。',
     'score按小节构造notes；keyDepth与handAt从同一notes求值，和弦取手部中心位置，抬手高度随键距变化。',
     '独立手部和音轨会错接触；取和弦平均只适合风格化手势，不能冒充准确指法。音色样本不公开。',
     '看接棒前、接触、停手、猫迟疑和雪花落键；逐项听看，不用时间列表代替听音。',
     [('songbie','score.js',40),('songbie','render.js',284),('songbie','render.js',300)])
card('emotion-shared-state','一个变化状态同时改变身体与表演','情绪|融化|坍缩|角色|蜡笔|表演|形态',
     '让情绪由形体、视线和动作共同表达。','melt进度连接头/身体缩小、摆动减弱、手臂落平与湿润质感。',
     '保留角色辨认特征；变化先缓后重，关键视线有时段，不把所有部位均匀缩放。',
     'snowState从时间取m和视线pulse；snowGeom分别计算半径/中心，arm在最终坍缩窗把肩点接向键盘。',
     '只整体缩放会像离镜而非融化；转向/接触没有对应空间坐标会失去关系。此法是艺术映射，不是热力学模拟。',
     '检查身体与手的接触、角色辨认、湿高光及最终坍缩窗；不要从变量名推断观感达标。',
     [('songbie','render.js',295),('songbie','render.js',595),('songbie','render.js',616)])
card('chase-silence-catch','追逐加速之后用静音突出接触','追逐|静音|接住|节奏|悬念|art deco|叙事',
     '通过节奏变化让关键接触成为观众期待的兑现。','同一信件贯穿街道、楼梯和屋顶；共享事件规定投掷、接住与钟声。',
     '加速只发生于追逐段；时钟截断音乐，投掷留静音，接住触发首钟声，拉远揭示新的场景关系。',
     'timeline导出STAIR_BEATS/T/SEC；film按事件引用shot模块，门/拱成为场内转场载体。',
     '全片恒快或每拍都切会消耗高潮；抄秒数却没有共同对象，静音只会像音轨丢失。',
     '连续看加速→断音→放手→下落→接住；核对声音与接触，再核对拉远发现。',
     [('lemo','styles/art-deco/demo/timeline.js',6),('lemo','styles/art-deco/demo/film.js',16)])
card('blueprint-part-states','零件身份贯穿绘制、爆炸与剖切','蓝图|工程图|爆炸图|零件|机械|图纸|剖切',
     '把机械拆解变成连续发现，而不是不相关视图切换。','零件ID共享爆炸偏移、齿轮相位、剖面与标注。',
     '先建立完整轮廓；按装配关系错峰分离；回装后再运转，剖切窗口服务关键传动。',
     'EXP/EXSEQ定义零件方向和先后；gearAngles按齿数比/中心方向求相位；film共用E/gear/section，活尺寸从零件坐标求值。',
     '此接云机是虚构2.5D图纸；不能套作真实阀门内部或精确力学。齿比准确也不代表齿形/接触已验证。',
     '逐看完整→最拥挤爆炸中间态→剖切→回装；核对零件号、传动方向和标注锚点。',
     [('lemo','styles/blueprint/demo/machine.js',15),('lemo','styles/blueprint/demo/film.js',149),('lemo','styles/blueprint/demo/film.js',214)])
card('world-anchor-callout','相机、零件和产品标注共享世界锚点','全息|HUD|标注|产品|扫描|参数卡|锚点|甩镜',
     '观众在镜头移动和部件拆开时仍能追踪说明对应的对象。','模型顶点与anchor经过同一零件变换/投影，屏幕卡片由该锚点牵引。',
     '先锁定部件再滚出数字；读过的信息收进侧栏；甩镜前给目标提示，运动模糊限制在快速窗口。',
     'holo.draw返回bbox/anchor；film从info.anchor取引线起点，使用共享callBeats组织爆炸、锁定、标签；快速窗5子帧累积。',
     '仅叠固定屏幕线会离开部件；Canvas近似投影/辉光不等于体积全息。竖屏需重排侧栏，不能只裁横版。',
     '检查爆炸中间态引线、遮挡、甩镜落定与手机阅读；单位/参数需要用户事实依据。',
     [('lemo','styles/hologram-hud/demo/engine/holo.js',206),('lemo','styles/hologram-hud/demo/film.js',112),('lemo','styles/hologram-hud/demo/film.js',194)])
card('ink-material-layers','笔压、墨量和干湿分层形成水墨','水墨|飞白|笔触|书写|毛笔|美术|干湿',
     '让水墨风格来自材料行为，并用书写次序引导注意。','中心路径、压力轮廓、笔毫与墨量共享一笔身份，wet/dry层保留不同合成。',
     '浓淡与枯润服务主体层级；固定种子让纹理沿笔身稳定；按弧长安排书写，笔压变化不等于统一线宽。',
     'Catmull-Rom加密后弧长重采样；mk构造压力/法线/笔毫；draw在墨量阈值处断墨，drawSeq按笔长分配时间。',
     '每帧随机会闪烁；干湿一起模糊会丢飞白；调用层需稳定seed及boil，层合成尚未全面精读/运行。',
     '放大观察笔端、交叉、干边和湿墨；连续看书写方向与纹理稳定性。',
     [('lemo','styles/ink-wash/demo/ink.js',8),('lemo','styles/ink-wash/demo/ink.js',62),('lemo','styles/ink-wash/demo/ink.js',128)])
card('reading-constrained-lens','阅读区域约束景深与手持摄影','歌词|杂志|阅读|景深|摄影|手持|排版|焦点',
     '在纸张摄影质感中保持信息清晰。','页面焦点与相机目标共享距离，确定性微摆在镜头混合/节拍之后叠加。',
     '正文处于清晰阈值，翻起纸页和背景才模糊；近景限制微摆增长，歌词段减弱节拍运动。',
     'focusDistance/coc从镜头姿态和深度求散焦圆；shader在SHARP下直通；handheld用时间噪声并限制近景振幅；bookView组合各层姿态。',
     '全屏景深会糊字；作者测试/注释不是本机测试结果。深度边缘有gather限制，单采样输出可能露边。',
     '实际手机尺寸逐行读字；看翻页前景边缘、景深交接和镜头微摆，不照抄1080横版阈值到竖屏。',
     [('lyric','app/src/scenes/magazine/focus.ts',27),('lyric','app/src/scenes/magazine/handheld.ts',20),('lyric','app/src/scenes/magazine/view.ts',20)])
card('curved-page-handoff','曲面纸页与相机错时落定','翻页|纸页|杂志|曲面|纸张|连续交接|转场',
     '让版式切换发生在同一个可触摸对象上。','旧页正面/新页背面/下层页面有明确身份；相机过渡稍晚于纸页落地。',
     '自由边落后书脊，页角先后不同；纸页落地带弱回弹，相机略拉开后接到下一版式。',
     'curlPoint与顶点shader共享圆弧参数；shader用sinc避免小曲率数值相消；visibleFaces决定前后页，TURN_S与CAM_BLEND_S分离。',
     '页正反面错配、落地近零曲率破裂、页堆穿插；本卡不覆盖尚未精读的撕页/折页全路径。',
     '检查起翻、中间遮挡、最后5%曲率、落地回弹和镜头停稳；连续输出才证明纸页可靠。',
     [('lyric','app/src/engine/curl.ts',22),('lyric','app/src/engine/page.ts',55),('lyric','app/src/scenes/magazine/schedule.ts',57),('lyric','app/src/scenes/magazine/view.ts',12)])
card('refracted-caustic-grid','折射网格面积生成水底焦散','焦散|折射|水底|水面|光学|Fresnel|浅水',
     '让水底亮纹随表面法线与深度变化，形成有根据的光学层次。','FFT高度/斜率供折射落点，落点映射面积决定光集中；水深供透射吸收。',
     '水底大色块和接触先建立，焦散再成为动态细节；侧视增强反射，深水增加颜色吸收。',
     '折射太阳方向到固定深度平面，光栅化落点网格，以vSrc屏幕导数面积估计集中度；主shader加高度近似及涟漪曲率。',
     '这是浅水/固定平面等近似，不能当阀内流场或完整路径追踪；t参数固定FFT而涟漪按调用累积，不支持未经改写的任意seek。',
     '对比波峰/波谷亮纹与侧视反射；离线迁移需固定步长重播涟漪并测乱序，不把实时demo当完整影片。',
     [('clearwater','index.html',297),('clearwater','index.html',508),('clearwater','index.html',871)])

ids = {c['id'] for c in new_cards}
lib['cards'] = [c for c in lib['cards'] if c['id'] not in ids] + new_cards
lib['quality_scope'] = {
    'recent_commit_is_not_release_or_quality_proof': True,
    'opus_wave_start_date_verified': False,
    'new_films_watched_or_run': False,
    'all_local_sources_quality_certified': False,
    'roles': {'film': '影片工程；是否优质看quality_evidence', 'film_engine': '引擎及叙事影片；不是自动标杆', 'component': '材料/模拟机制，不能顶替影片标杆', 'independent_tool': '本地工具，不能证明原作质量'},
    'selection_rule': '优先近期实际作品工程、明确绘制路径、可追溯成片与源码；源码/日期不替代动态审片，旧基础demo不进入影片标杆名单。'
}
save(LIB, lib)
save(OUT / 'recent-source-installation.json', {'archives': installed, 'files': sum(x['files'] for x in installed), 'new_cards': list(ids), 'runtime_verified': False})
print(json.dumps({'installed': installed, 'cards': len(lib['cards']), 'new_files': sum(x['files'] for x in installed)}, ensure_ascii=False))
