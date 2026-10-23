from pathlib import Path
import hashlib,json,re,zipfile,shutil
R=Path(__file__).resolve().parent
readme='''# 宝宝与妈妈 · 20时代亲子互动 v19

40秒、竖屏9:16、1080×1920、24fps、二维卡通，有意无声。沿用已生成的20时代完整双人动作，婴儿与妈妈面对面近距离互动，保留窗外鸟蝶、云、太阳与夜景星点；室内家具与窗框固定。

Windows运行：`npm install`，`npm run preview`，打开 http://127.0.0.1:8768/film/index-v19.html 。点击画面播放/暂停。`npm run render` 导出四段并拼接40秒MP4。`npm run check` 检查图集边界与乱序/重载像素一致性；`npm run check:transitions` 检查19个转场端点像素及乱序寻址。

Node.js和Chromium为运行依赖。首次渲染可由Remotion准备浏览器；也可设置环境变量 `CHROME_EXECUTABLE` 为已有Chromium绝对路径。源码包不含node_modules、浏览器、用户原始家庭照片或视频。中文使用Microsoft YaHei，换机器需要可用中文字体。

本版改动：

- 在已有妈妈坐姿基线上，单独测量婴儿头部外轮廓，排除头发内部透明细缝、衣领与道具干扰；按统一参考尺度校准婴儿整体。
- 连续采样场保护妈妈面部并衔接双人接触区，保留原有姿态动作。19处连接的首尾复用相邻场景同一变换，避免时代切换重新变大变小。
- 黑底与白底分别补帧，再重建RGBA透明通道，保留手臂间的封闭透明空隙与白色服装。
- 每场完整原生姿态通过RIFE v4.6离线补为48幅烘焙动作，再按40秒共享时间线取样。模型不参与播放器；快速遮挡及服饰媒介转换处仍可能有局部软边或形变。
- 19处时代交接各增加完整双人连接姿态，末姿态是下一动作的起点，取消每场前后冻结。普通连接17幅、结尾放稳杯瓶连接25幅，均包含在40秒内。
- 结尾先降低杯子和奶瓶，放稳、松手后再碰掌；杯瓶保留在座位旁。结尾8幅完整碰掌姿态重新生成，动作不归零。
- 19次时代切换按媒介使用丝带、纸扇、马赛克、颜料和像素遮罩；遮罩只交接背景，完整人物在其后仅绘制一次，人物动作不会被背景擦断。
- 保留v15窗外逐格轻动画，无室内网格形变。

编辑入口：`film/sequences-v19.js`（时间轴与合成）、`film/transitions-v16.js`（背景转场）、`film/environment-stopmotion-v15.js`（外景）、`assets/motion-v19/manifest.json`（已烘焙动作位置）。`film/chase-scenes-v9.js`为历史文件名，当前采用坐姿版本。`render-v19.mjs`与`render-batched-v19.mjs`负责编码。

可选重建动作：安装 `requirements-build-v19.txt`；用 `fetch_rife_v16.py`准备`.tools/rife/runtime`，运行 `python build_continuity_v18.py --scenes 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19 --bridges 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19`，再运行 `python build_infant_v19.py` 生成本版烘焙动作。需兼容Vulkan的GPU；`RIFE_GPU`可指定设备，本机使用1号NVIDIA GPU。`build_motion_v16.py`为复用的注册工具。日常预览和导出不需要模型。生图已通过内置image_gen完成并随包保存，提示词见`assets/bridges-v17/prompt-*.txt`；拒用的多手草图不打包、不运行。

验证与观看范围见`qa/v19/production-review.json`和`qa/v19/final/engineering-check.json`。历史AI一轮审核预算已用完，此次为用户反馈后的定向制作检查，没有新一轮独立审核。抽帧和端点像素相等不代表解剖或正常速度全片审美通过。历史成片未改写。头部外轮廓测量是校准参考，不能等同于解剖精确度；原有跨画风补间仍可能有局部软边。
'''
(R/'README.md').write_text(readme,encoding='utf8')
(R/'README-v19.md').write_text(readme,encoding='utf8')
(R/'requirements-build-v19.txt').write_text('numpy\nPillow\nopencv-python\n',encoding='utf8')
brief=json.loads((R/'brief.json').read_text(encoding='utf8'))
brief.update(version=19,title='宝宝与妈妈 · 20时代连续亲子互动',entry='film/index-v19.html',plan='PLAN-v17-continuity.md',source='out/mother-baby-v19-source-and-assets.zip',video='out/mother-baby-20-eras-portrait-v19-40s.mp4',concept_approval='沿用已认可二维人物与构图；用户要求每个动作承接上一个动作，直接制作',production_route='Independent infant exterior-skull size registration with protected adult face and shared-contact mapping; dual-matte RGBA and exact actor endpoint continuity')
(R/'brief.json').write_text(json.dumps(brief,ensure_ascii=False,indent=2),encoding='utf8')
p=json.loads((R/'package.json').read_text(encoding='utf8'));p['version']='19.0.0'
p['scripts']={'render':'node render-batched-v19.mjs','stills':'node render-v19.mjs stills','sample':'node render-v19.mjs sample','check':'node render-v19.mjs check','check:transitions':'node render-v19.mjs transitioncheck','preview':'node preview-v19.mjs'}
(R/'package.json').write_text(json.dumps(p,indent=2),encoding='utf8')
names=['README.md','README-v19.md','CHECKPOINT.md','brief.json','package.json','PLAN-v17-continuity.md','THIRD_PARTY_NOTICES.md','REFERENCE-LICENSE.txt','requirements-build-v19.txt','render-v19.mjs','render-batched-v19.mjs','preview-v19.mjs','finalize_v19.py','inspect_transitions_v19.py','inspect_bridges_v19.py','package_source_v19.py','build_motion_v16.py','build_continuity_v18.py','build_continuity_v17.py','build_infant_v19.py','measure_infant_v19.py','inspect_infant_v19.py','inspect_encoded_infant_v19.py','fetch_rife_v16.py','film/index-v19.html','film/sequences-v19.js','film/chase-scenes-v9.js','film/environment-stopmotion-v15.js','film/transitions-v16.js','film/eras.js','qa/v15/mechanical-check.json']
files={R/n for n in names}
files.add(R/'check_assets_v19.py')
files.add(R/'clean_matte_v17.py')
files.add(R/'verify_source_runtime_v19.py')
scenes=json.loads((R/'film/chase-scenes-v9.js').read_text(encoding='utf8').split('=',1)[1].strip().rstrip(';'))
runtime={(R/'film'/s['background']).resolve() for s in scenes}
motion=json.loads((R/'assets/motion-v19/manifest.json').read_text())
runtime.update(R/'assets/motion-v19'/s['file'] for s in motion['scenes']+motion['bridges'])
runtime.update({R/'assets/motion-v19/manifest.json',R/'assets/environment-v15/animals-atlas.png'})
files.update(runtime)
for pattern in ['assets/sequences-v13/*','assets/environment-v15/*','assets/bridges-v17/batch-*.png','assets/bridges-v17/modern-action.png','assets/bridges-v17/prop-recovery-v3.png','assets/bridges-v17/prompt-*.txt','qa/v19/*.json','qa/v19/infant-overview-*.jpg','qa/v19/*-comparison.jpg','qa/v19/continuous-*.jpg','qa/v19/alpha-before-after.jpg','qa/v19/bridge-overview-*.jpg','qa/v19/final/*.json','qa/v19/final/*.txt','qa/v19/final/*.png','qa/v19/transitions/cut-*.jpg','qa/v19/transitions/all-actors-midpoint.jpg','qa/v19/transitions/capture.json']:
    files.update(f for f in R.glob(pattern) if f.is_file())
files={p for p in files if p.name!='infant-before-samples.json'}
assert all(p.is_file() for p in files)
manifest={'version':19,'video_included':False,'photos_included':False,'runtime_assets':len(runtime),'sha256':{p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}}
dest=R/'out/mother-baby-v19-source-and-assets.zip'
with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=2) as z:
    for p in sorted(files):z.write(p,p.relative_to(R))
    z.writestr('SOURCE-PACKAGE.json',json.dumps(manifest,indent=2))
with zipfile.ZipFile(dest) as z:
    assert z.testzip() is None
    for n,h in manifest['sha256'].items():assert hashlib.sha256(z.read(n)).hexdigest()==h,n
    for script in re.findall(r'<script src="([^"]+)"',(R/'film/index-v19.html').read_text(encoding='utf8')):assert 'film/'+script in z.namelist(),script
    target=R/'out/source-runtime-v19';target.mkdir(exist_ok=True);z.extractall(target)
result={'archive':str(dest),'files':len(files),'runtime_assets':len(runtime),'zip_integrity':True,'all_hashes_match':True,'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'extracted_to':str(target)}
(R/'out/source-package-v19-check.json').write_text(json.dumps(result,indent=2),encoding='utf8')
print(json.dumps(result))
