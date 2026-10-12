import hashlib, json, re
from pathlib import Path

SKILL = Path('D:/Codex/skills/vibe-video')
ROOT = Path(__file__).parent
gallery = json.loads((SKILL/'assets/opus-gallery.json').read_text(encoding='utf-8'))
sources = {}

def source(id, repo, commit, local, relation, runtime, scope):
    sources[id] = dict(id=id, repository='https://github.com/'+repo if repo else None,
                       commit=commit, local_root=local, relation=relation, runtime=runtime, scope=scope)

source('beach','ishuagrawal/particle-beach','92db82255b962acf2930f19bf6e5e7790174a790','assets/code-studies/particle-beach',
       'gallery_original_link','representative_frames_and_continuous_window',
       '完整绘制运行源码已保存；回放有少量重复像素差和局部近黑帧，不作为全片质量保证。')
source('reel','tuzhechen2005/opus-video-skills','59744a69c7b916cfbe4c4ec84006b0c2f5e2fde1','assets/code-studies/work-reel-26',
       'supplementary_film','representative_frames_and_continuous_window',
       'work-reel-26完整绘制运行部分；补充作品，不是图库513原作的同一工程。')
source('mg','Vincentwei1021/mg-styles-15','49052d80bfaf9fa8412cc9710530e5e95a3b8d8c','assets/code-studies/mg-styles-15',
       'supplementary_films','source_read_only',
       '保存15种风格工程的文本源码；本轮精读形变/液体/手绘/像素/等距采样的选定实现。媒体、字体及部分素材不在包中，没有逐片回放。')
source('paper','francozanardi/papermotion','aafddbe2dbc2b594bcd57c19c4a5a75c5c271be8','assets/code-studies/papermotion',
       'supplementary_engine_and_films','source_read_only',
       '纸片引擎与影片文本源码；light由作者标为GPT 6 Astra，其他示例模型归属各异，不统一标为Opus。Stage仅递增帧。')
source('water','AiondaDotCom/ai-sim-benchmark','680f87e6d54984199525dd12005bd95711bb47bb','assets/code-studies/water-opus',
       'gallery_source_link','source_read_only',
       '只采用claude-code-opus-5-5分支。源码证明网格浅水与着色；原帖与具体录屏像素一致性未验证，实时循环会丢积压步。')
source('rigid','sbobyn/three-avbd','9b9c27b6b65a1212896e4d90e7e3d154c06e428a','assets/code-studies/three-avbd',
       'gallery_source_link','source_read_only',
       'WebGPU刚体/关节/GPU绘制代码；basic随机数与Clock不是可乱序电影时间轴。没有运行或确认发布录屏与此commit一致。')
source('glass','Faraz-Portfolio/demo-2025-raymarched-liquid-glass','a1a3b134ef82e7ace42273b40d8c20616aefe4b0',None,
       'supplementary_implementation','source_read_only',
       '未找到明确LICENSE，不在本地skill分发原代码；只研究公共SDF与光线步进原理。')
source('codex-tools',None,None,'assets','independent_implementation','tested_in_previous_study',
       '原创解析弹簧/对数缩放/点插值工具；8秒连续UI测试通过。不是任意字形和所有原作效果都已实现。')

cards=[]
def card(id,title,terms,purpose,relation,decisions,implementation,failure,review,refs=(),cases=()):
    refs=[(a,'skills/kinetic-reel/examples/work-reel-26/'+b if a=='reel' else b,c) for a,b,c in refs]
    cards.append(dict(id=id,title=title,terms=terms.split('|'),purpose=purpose,relation=relation,
                      decisions=decisions,implementation=implementation,failure=failure,review=review,
                      source_refs=[dict(source=a,path=b,line=c) for a,b,c in refs],gallery_slugs=list(cases),
                      status='code_observed_with_adaptation' if refs else 'design_inference_from_public_brief',
                      status_note='源码观察与迁移设计分开；成片质量仍需按当前任务验证。' if refs else '公开需求或独立设计，不证明原作已经按此实现，也未在本机验证。'))

card('ui-identity','单对象贯穿多种UI','界面|UI|按钮|滑杆|开关|连续变形|容器|交互',
     '观众跟住一个对象，在变化中读懂不同功能。','几何身份持续；容器、内容和光标有独立状态。',
     '拖拽时值由指针直接控制，松手后从实际速度接续。先退旧内容再入新内容，关键结果给阅读时间。',
     '使用闭式弹簧或预定事件；宽高、边缘、圆角分别求值。不是两组件叠化。',
     '轮廓断裂、文字双影、指针先走对象后到；所有边缘同速会失去材料感。',
     '检查同一ID、拖拽接触、内容最拥挤的中间态、落定和末帧到首帧。',
     [('codex-tools','continuity.mjs',1)],['twoclipping-402193'])
card('outline-morph','轮廓、孔洞与附属笔画分别形变','形变|morph|轮廓|图标|字形|logo',
     '让转变保留身份，同时有可辨认的中间形。','主体轮廓、孔洞、笔画和阴影分别配对。',
     '先选择需要保留的负形；拓扑相差大时通过共同圆形中间态。辅笔画错峰收拢，避免主体糊成一团。',
     '弧长重采样→统一绕向→循环位移最小距离配点→分阶段插值；孔洞缩到质心再长出。',
     '点数一致仍可能自交；孔洞突然闪灭，笔画与主体挤压。',
     '逐看25/50/75%轮廓、凹陷和孔洞；以主对象身份连续和中间态干净为标准。',
     [('mg','demos/08-morph/index.html',60),('mg','demos/08-morph/index.html',344)])
card('portal-scale','从选中局部进入下一层世界','门户|无限缩放|进入|尺度|微观|宏观|穿越|zoom',
     '把进入空间变成揭示内容的叙事动作。','入口里提前存在下一世界；跨越时保留焦点、裁切和方向。',
     '先让观众识别入口，再加速进入；对数缩放决定各段时长。需要真实绕行时用几何或多视图。',
     '冻结帧/渲染纹理+矩形遮罩可实现局部穿入；分层2.5D或真正相机提供视差。',
     '四角露出旧世界、入口内部跳图、只放大单图却声称空间穿行。',
     '核对入前/覆盖画幅/出后三态和边角；对比实际视差，不只看中心。',
     [('reel','reel.js',1045)],['acoramaa-053577','irinatoxi-962937'])
card('select-transition','选择动作成为镜头连接','选择|转场|图表|信号|进入|局部|transition',
     '下一个镜头是当前选择的含义，降低理解成本。','旧镜选框的坐标变成新镜入口。',
     '目标在选择前可读；旧镜冻结只发生于必要窗口，新镜内容同时开始自己的动作。',
     '末帧纹理→选中区域矩阵变换→clip揭示新场景；明确这是遮罩交接。',
     '中心漂移、先换背景后选中、进入后只有另一张标题卡。',
     '检查选中目标、速度接续、交接像素和新镜首个有意义动作。',
     [('reel','reel.js',1045)],['daniel-haida-636937','howdevelop-733090'])
card('type-window','文字作为运动材质窗口','文字|排版|字体|字形|遮罩|typography',
     '文字既承载内容，也参与场景结构。','运动材质经过字形mask，信息轮廓保持稳定。',
     '只强调与主题有关的字；材质在字内动作，正文保持清晰。字体尺寸依实际手机阅读判断。',
     '字体加载后生成mask；世界材质和清晰文字分层，避免后处理糊掉正文。',
     '材质漂亮但词读不清；RGB分离常驻，中文缺字或字距失衡。',
     '手机尺寸读字、字内运动相位、边缘抗锯齿和字体ready。',
     [('reel','reel.js',1)],['howdevelop-733090'])
card('type-architecture','文字搭建场景并兑现句意','文字|建筑|语义|诗歌|句子|结构|typography',
     '词义与物体功能相互解释。','前一句建立支撑、地面或开口，后一句真正使用它。',
     '先写空间因果，再排文字；最终立在前文构成的地面，比不断换字更有回收感。',
     '可用字形轮廓/SVG/三维文本加状态图；角色、碰撞和支撑是待题材设计。',
     '仅把名词摆成图形，最后落定与此前无关；文字成为看不清的装饰。',
     '对照每句意义、支撑关系、最终空间结果；不能由提示词推定成片成功。',cases=['gdgtify-929495'])
card('semantic-finale','同一材料在结尾变为标志','logo|品牌|结尾|回收|组装|语义|标志',
     '结尾兑现整片的形式想法。','开场材料、负形或运动锚点成为最终符号。',
     '先读懂符号，再安排残余动作落定；避免最后凭空放logo。不要改变真实标志的比例。',
     '给形状配对并分离底色交接；源码的heart→圆→字母可作为结构参考。',
     '终点图形与之前无关，轮廓已落定但粒子仍乱飞，品牌字不可读。',
     '遮住最终字标时，仍能辨认前文与它的关系；实际片尾检查比例和停留。',
     [('mg','demos/08-morph/index.html',273)],['leowenai-125931','mounnna-497266','zeezomb-726206'])
card('data-state','让数值、图形和标签共享状态','数据|图表|累计|流程|科普|配方|仪表|数值|token',
     '过程可见，观众能追溯结果从何而来。','数量、容积、颜色、速度和标签来自同一数据状态。',
     '先建立单位与空状态；用主变量驱动变化。需要教学压缩时声明示意，不装成测量。',
     '独立模拟/事件数据→渲染几何/颜色→投影标签；water的depth和velocity驱动网格与shader是实际例子。',
     '计数与液位不同步、单位漂移、只动箭头却无结果状态。',
     '复核起点、累计预算、关键事件和终值，区分真实计算与视觉映射。',
     [('water','runs/claude-code-opus-5-5/src/render/waterMesh.ts',165)],['ror-fly-880547','astrothewizard-618782','parkerrex-701462'])
card('mechanical-section','先建立器件，再剖开关键接触','机械|剖面|止回阀|弹簧|阀门|爆炸图|拆解|流体|装配',
     '解释看不见的接触、密封和受力关系。','整机、剖面和零件保留同一坐标系、装配轴和身份。',
     '关键接触处停机；先切外壳再解释动作。爆炸距离服务装配关系，不能让零件任意飞散。',
     '由实际尺寸/结构建立几何；剖切面封口、零件轴向轨迹、受力阈值和标注共享状态。此卡是迁移设计，未确认图库原作源码。',
     '假内部、铰链错轴、弹簧穿壳、受力未变阀芯先开；照片mask不可当真实剖面。',
     '核对关闭→压力增长→阀芯离座→回座接触；9:16构图要完整呈现流向与接触点。',cases=['op7418-814408'])
card('world-light','共享世界光照塑造层次','光照|照明|逆光|日落|材质|层次|曝光|lighting',
     '让同一世界的时间、气氛与主体关系可信。','天空、实体、点云、雾和曝光共享光照状态。',
     '亮暗关系先服务主体轮廓，细节只在有效处增加；变化要进入场景而非顶层滤镜。',
     '世界uniforms、太阳方向、雾和镜头曝光共同编排；材质颜色在线性空间处理。',
     '玻璃/金属发白，暗景点云仍自发光，背景与阴影方向矛盾。',
     '对比主光、轮廓、接触和暗部；保留原作局部近黑的已知限制。',
     [('beach','js/trailer-shots.js',241)])
card('telephoto','远机位与窄视角压缩空间','长焦|压缩|摄影|镜头|太阳|轮廓|焦段|远景',
     '让背景与主体形成强图形关系。','机位距离改变透视，FOV控制取景。',
     '先决定主体占比，再配距离和FOV；横移保留轮廓，不把缩FOV当成透视压缩。',
     '摄影机position/lookAt/FOV分轨，测试背景相对主体的尺寸。',
     '主体变大但背景比例不变；取景过窄导致主体瞬间裁出。',
     '匹配景别比较近/远机位的空间关系；在竖屏重新构图。',
     [('beach','js/trailer-shots.js',49)])
card('low-travel','低位穿行，用遮挡证明纵深','低机位|穿行|运镜|视差|前景|纵深|摄影',
     '让观众进入场景并感受规模。','前中后景有不同速度与真实遮挡。',
     '前景只暂时遮住锚点，随后重现；轨迹围绕发现安排，不均匀绕原点。',
     '真实空间相机+世界遮挡；2.5D分层需要补被遮区域。',
     '穿模、锚点长期被挡、前景像贴纸与相机一起移动。',
     '检查最近遮挡、重新出现和最窄通道；原路横屏不能直接裁成竖屏。',
     [('beach','js/trailer-shots.js',75)])
card('reveal-path','位置与目标双轨迹揭示主体','揭示|升高|发现|运镜|相机|摄影|轨迹',
     '用机位变化带来新理解。','相机位置和看向目标分别变化，始终保留视觉锚点。',
     '先局部障碍，再升高见全貌；结果出现后减速或停留。目标偏移用来转移注意。',
     '独立centripetal样条；必要时按弧长采样，外层ease另管速度。',
     '轨迹流畅但主体一直不在画面；目标移动导致角速度骤变。',
     '检查屏幕占比、锚点轨迹、实体碰撞和落定，不只检查路径曲线。',
     [('beach','js/trailer-shots.js',133)])
card('hold-cause','在因果点保持相机稳定','因果|接触|动作|静止|特写|阀门|科普|碰撞',
     '观众能分清原因、变化与结果。','主体动，相机保持可读；主动作完毕再转移注意。',
     '接触/开合/选择处留时间；选择跟随目标而非同时绕转。按动作密度确定时长。',
     '相机近固定或lookAt轻跟随；把接触事件登记在动作表。',
     '机构和相机同时高速动，关键接触总发生在转场里。',
     '静音看一次能否指出原因；查看接触前、中、后三态。',
     [('beach','js/trailer-shots.js',162)])
card('point-volume','点云有实体深度与遮挡','点云|粒子|粒子世界|体积|遮挡|particle',
     '点的风格保留空间结构。','可见点与不可见实体共同维护深度。',
     '近景粒径、远景衰减和剪影一起设计；遮挡体不抢视觉，但决定谁在前。',
     '共享uniforms、深度写入occluder、透明排序和尺度衰减。',
     '穿墙、远场噪点、粒子像屏幕平面；透明全关depthWrite又没有遮挡。',
     '对照实体轮廓、逆光、重叠和相机穿行窗口。',
     [('beach','js/core.js',1)])
card('point-correspondence','点身份持续，形态才能接续','点云|点对应|粒子|形态|morph|投影|标注',
     '从抽象点场变为有意义的形状。','A/B点集共用ID；标注来自最终世界位置。',
     '先确定关键轮廓和配对，再加wobble；不同阶段密度变化不能随机换点。',
     '固定种子A/B数组、逐点插值，shader偏移后投影或保持CPU/GPU一致。',
     '点云中途炸散，标注贴着原始坐标而主体已经偏移。',
     '检查点ID、半程轮廓、终点和标注位置。',
     [('reel','reel.js',122)])
card('procedural-surface','场的结构形成材质与地形','着色器|shader|噪声|地形|表面|程序化|材质',
     '结构、材料和运动拥有共同的视觉逻辑。','多尺度噪声与domain warp驱动真实表面或粒子高度。',
     '噪声频率对应主形/细节，远场减少密度；matcap与真实环境反射区分。',
     'fbm/domain-warp、顶点位移、matcap和背壳轮廓；先定大形，再看材质。',
     '满屏同强度细节、地形尖刺、运动材质不贴对象。',
     '大形轮廓、局部法线、深度密度和时间闪烁。',
     [('reel','reel.js',40)])
card('glass-sdf','玻璃轮廓、折射和内容分层','玻璃|折射|SDF|光学|透明|液态玻璃|glass',
     '背景弯曲能被读出，文字仍清晰。','距离场决定轮廓/法线，背景采样决定折射效果。',
     '先选有结构的背景；把清晰内容与玻璃处理分离。必要时真实几何厚度/出口求交。',
     'SDF融合、法线梯度、Fresnel及屏幕采样；本地sdf-glass-lab只是一界面近似。',
     '背景本来平坦无法读出折射、玻璃发白、内容被滤糊。',
     '对比有/无玻璃背景位移；分别声明有无出口、多次反射和焦散。',
     [('glass','src/Raymarching/RayMarchingMaterial.tsx',1)])
card('liquid-union','液体用连续场融合并继承颜色','液体|流体|融合|胶状|goo|metaball|SDF',
     '分离、连接和落定看起来属于同一种材料。','椭圆、线段、字形成为同一距离场的成员。',
     '融合颈、主轮廓和内部颜色分别控制；先确定接触面与软光箱，再加入高光。',
     '稳定log-sum-exp smooth union，同时混合梯度/色参数；slot椭圆向字形SDF过渡。不是Navier–Stokes流体。',
     '融合范围突然跳，颜色归属错乱，高光条纹把内部误画成波浪。',
     '看分离颈、合并时梯度、字形边缘和接触面；特效焦散需独立说明近似。',
     [('mg','demos/07-liquid/js/shaders.js',95)])
card('hand-ink','手绘感来自笔压与稳定线条变化','手绘|绘画|水彩|线条|笔触|boil|纸张',
     '保留手作感，同时让主动作清晰。','几何稳定，笔宽、阴影侧与绘画时刻有受控变化。',
     '绘画与相机可以不同帧率；按元素ID固定随机流。特写时补偿笔宽和扰动幅度。',
     '弧长重采样、世界空间噪声扰动、切线法向生成可变宽轮廓；起止笔收细。',
     '全画面每帧重抖，粗细与放大比例失控，笔触成为白板式机械揭示。',
     '同元素重复时刻、静止区域、特写线宽和主动作连续窗。',
     [('mg','demos/05-cel-boil/js/engine.js',152)])
card('pixel-palette','像素风用语义色板表达时间','像素|pixel|色板|复古|整数缩放|日夜',
     '让有限像素和色数承担光照与剧情。','环境槽位→阶段LUT→主色板；角色色与环境色分别管理。',
     '逻辑画布先成立，输出整数放大；色板变化落在事件点而不是全屏白闪。',
     'indexed buffer、最近色映射、dither、局部colour cycling；保持统一逻辑像素。',
     '近景像素大小变化不一致，连续抗锯齿破坏像素边，角色也跟背景洗色。',
     '逻辑分辨率、轮廓、阶段LUT与关键物品发光。',
     [('mg','demos/20-pixel/film.js',16)],['zacxbt-944604'])
card('paper-acting','角色意图驱动骨骼与跟随动作','角色|表演|纸片|剪纸|行走|风筝|头发|动画',
     '角色的行动有动机，身体有重量与余动。','意图→步态/骨骼→头发围巾/手持物→相机。',
     '先写角色想做什么；注视、伸手、停步、情绪形成表演。镜头预留行进方向空间。',
     '骨骼层级、gait、弹簧链、地面/风共享world；相机跟随角色与手持物的加权中心。',
     '手持物脱手、脚滑、头发与风无关、嘴部抖动冒充口型同步。',
     '脚接地、持物接触、转身轮廓、身体余动与视线；Stage仅顺序运行，要另做seek重播。',
     [('paper','examples/kite/main.ts',91),('paper','examples/cast/Child.ts',54)])
card('event-story','接触事件同时推进剧情与声音','事件|接触|碰撞|因果|声音|叙事|音画同步',
     '观众相信变化是行动造成的。','距离/接触阈值触发beat，触发时刻也写入sound log。',
     '接近→观察→接触→反应→展开→落定；先近景读接触，揭示时再拉远。',
     '有限状态机enter/during/next/after；模拟时间映射到视频时间后合成声音。',
     '音效按预定秒数响而接触晚到；等待条件永远不满足；慢动作后音画不同步。',
     '对照beat历史、接触gap、声音cue与镜头切换；听音仍需实际播放。',
     [('paper','examples/light/main.ts',25),('paper','src/direction/Beats.ts',78)],['kamstudiolabs-440893','acoramaa-248467'])
card('water-cause','地形、水量和材质形成因果','水流|雨水|湖泊|浅水|流体|地形|瀑布|水深',
     '看到水为什么沿坡走、在何处蓄积。','terrain+depth形成水面高度；通量更新水深，velocity影响外观。',
     '来源、积累与出口都可追溯；教学阀内流动不能直接套高度场。',
     '四邻虚拟管通量→出流限幅→入出预算→深度/速度mesh属性；浅水颜色/Fresnel/泡沫为视觉近似。',
     '负水深、质量不守恒、墙边漏水、把shader波纹当完整流体；时间循环丢步。',
     '预算和边界、干湿过渡、速度/泡沫对应；离线导出要固定模拟步并保存状态。',
     [('water','runs/claude-code-opus-5-5/src/sim/water.ts',159),('water','runs/claude-code-opus-5-5/src/render/waterMesh.ts',165)],['stephanferraro-224281'])
card('rigid-contact','受力、关节与断裂提供动作因果','物理|刚体|关节|碰撞|断裂|弹簧|机构|积木',
     '大数量对象运动有接触、重量和后果。','world保存模拟状态；mesh从GPU状态绘制，断裂事件改变外观。',
     '选择真正影响故事的受力事件；接触影/AO与实体一致，大数量并不替代构图。',
     'WebGPU solver、BodyMesh、joint anchors与breakForce；需要可寻址导出则固定种子并缓存/重播模拟。',
     '锚点偏移、爆炸式散射、碰撞先于视觉接触、实时Math.random无法复现。',
     '接触前后、固定端、断裂阈值与状态/mesh一致；这些示例本轮未运行。',
     [('rigid','examples/basic.ts',29)],['nybobs-680050'])
card('sample-quality','采样服务轮廓、阴影与高速动作','抗锯齿|采样|阴影|闪烁|运动模糊|渲染|质感',
     '精细轮廓与光照在运动中仍然干净。','每次子采样都重新求几何时间、相机和灯光。',
     '先修几何和曝光再提高样本；硬切不能跨窗混合，静止文字可独立保持锐度。',
     'Halton视口jitter、面积光抖动、normal/depth AO与浮点累积→tone mapping→sRGB。',
     '叠旧帧鬼影、软化正文、切点重影，30fps复制成60fps。',
     '细线连续窗、接触阴影、高光稳定性与硬切；性能与画质按实际输出评估。',
     [('mg','demos/03-isometric/js/render.js',151)])

def dump(path,data):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

dump(SKILL/'references/opus-methods.json',{'schema_version':1,'checked':'2026-10-09',
     'reading_scope':{'catalogue_rows':513,'unique_prompts':459,'short_prompts_read_in_full':420,'long_prompts_read_as_excerpts':39,'all_original_videos_watched':False},
     'sources':sources,'cards':cards})

# Candidate screening is deliberately kept apart from human-authored cards and code evidence.
rules={
 'ui-identity':r'\b(button|slider|toggle|UI|interface|drag)\b',
 'outline-morph':r'\b(morph|morphing)\b',
 'portal-scale':r'infinite zoom|portal|nested world|atomic scale|zoom.*(?:CPU|atom)',
 'type-window':r'kinetic typography|text mask|glyph|typograph',
 'data-state':r'token.bucket|recipe|random walk|measurements|chart|graph',
 'mechanical-section':r'cutaway|cross.section|hinge|bevel|exploded',
 'world-light':r'lighting|sunlight|sunset|ambient occlusion|Fresnel',
 'point-volume':r'particle|point.cloud',
 'procedural-surface':r'shader|procedural|terrain|domain.warp',
 'glass-sdf':r'glass|refraction|refract|\bSDF\b',
 'liquid-union':r'liquid|metaball|gooey|fluid',
 'hand-ink':r'watercolou?r|hand.drawn|brush|line boil',
 'pixel-palette':r'pixel.art|pixelated|sprite|palette',
 'paper-acting':r'paper.cut|origami|character animation|skeleton',
 'event-story':r'collision|bounc|beat.sync|audio.react|music.*sync',
 'water-cause':r'waterfall|rainwater|hydrolog|shallow.water',
 'rigid-contact':r'rigid.body|physics|joint|break.force',
 'sample-quality':r'motion.blur|supersampl|anti.alias|sub.frame',
}
manual_visual={
 'koldo2k-778767':('generated_video_required_in_prompt','Kling 2.5 animation'),
 'anabology-491441':('generated_video_required_in_prompt','Seedance'),
 'anjmaxx-459455':('generated_video_required_in_prompt','Seedance'),
 'jesscaroline7-955094':('generated_video_required_in_prompt','Higgsfield'),
 'tardigrade111-160686':('generated_video_required_in_prompt','Runway / Veo'),
 'mattworkman-309357':('generated_video_required_in_prompt','Seedance'),
 'paranoidamerica-686717':('generated_image_required_in_prompt','SDXL'),
 'ayumi-t820-871023':('generated_image_required_in_prompt','Midjourney'),
 'iamtanzil-675031':('video_asset_origin_unknown','background MP4'),
 'iamtanzil-120030':('photographic_composite','two-photo radial mask; not proof of internal 3D'),
}
direct={'ishuagra02-678129':'beach','stephanferraro-224281':'water','nybobs-680050':'rigid'}
hashgroups={}
for x in gallery['entries']:
    h=hashlib.sha256(x['prompt'].encode('utf-8')).hexdigest()
    hashgroups.setdefault(h,[]).append(x['slug'])
rows=[]
for x in gallery['entries']:
    p=x['prompt'];h=hashlib.sha256(p.encode('utf-8')).hexdigest()
    matches=[]
    for id,pattern in rules.items():
        match=re.search(pattern,p,re.I)
        if match:
            matches.append({'card':id,'text':p[max(0,match.start()-35):match.end()+55], 'basis':'automatic_text_candidate_only'})
    flag,reason=manual_visual.get(x['slug'],('unknown','no original pixel provenance established'))
    src=direct.get(x['slug'])
    rows.append({'slug':x['slug'],'prompt_sha256':h,'same_text_slugs':hashgroups[h],
        'text_reading':'full_available_text' if len(p)<=1000 else 'mechanism_excerpt_only',
        'prompt_partial':x['prompt_partial'],'candidate_cards':matches,
        'manual_cards':[c['id'] for c in cards if x['slug'] in c['gallery_slugs']],
        'original_visual_provenance':flag,'provenance_reason':reason,
        'source_id':src,'source_relation':sources[src]['relation'] if src else 'unresolved',
        'code_source_evidence':sources[src]['runtime'] if src else 'no_inspected_renderer_tied_to_this_row',
        'source_discovery_urls':re.findall(r'https?://github\.com/[^\s<>]+',p),
        'pixel_match_verified':False,
        'tech_tags_used_for_original_provenance':False})
dump(SKILL/'references/opus-source-index.json',{'schema_version':1,'catalogue_commit':gallery['provenance']['commit'],
     'checked':'2026-10-09','scope':'Reading coverage and source trace, not 513 watched films or verified techniques',
     'entries':rows})
dump(ROOT/'research-summary.json',{'cards':len(cards),'source_entries':len(sources),'indexed_rows':len(rows),
     'source_link_rows':len(direct),'manual_mixed_or_unknown_assets':len(manual_visual),
     'retrieved_sources': ['Vincentwei1021/mg-styles-15','francozanardi/papermotion','sbobyn/three-avbd','AiondaDotCom/ai-sim-benchmark'],
     'search_boundary':'twoclipping repo-name search returned none; in:readme gave catalogues/toolkits, not verified exact source. ror_fly/gdgtify searches did not identify a confirmed original renderer.',
     'rejected_as_core_methods':{'motionloom-studio':'inspected demo/math; supplementary toolkit. Generic title+wipe demo does not establish original UI/portal implementations.',
       'opus-video-recipes':'inspected kinetic example and README; useful export recipe, mostly title beats, not core cinematic mechanism.',
       'JohnHeibel/PDoomVideo':'direct author source lead for doubleunplussed; no declared licence, not copied to skill or falsely folded into earlier MIT mexicat version.'}})
print('cards',len(cards),'indexed',len(rows),'sources',len(sources))
