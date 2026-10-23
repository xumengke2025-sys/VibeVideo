from pathlib import Path
import json,shutil,hashlib,wave,re
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;old=R.parent/'baby-agent-20261012';out=R/'out/final-v1';qa=R/'qa';qa.mkdir(exist_ok=True)
times=[.5,2.5,4.25,5.375,6.25,8.5,11.5,14,15.75,17.5,20.25,22.75,24.5,27,29.25]
sheet=Image.new('RGB',(5*216,3*408),'#302a25');d=ImageDraw.Draw(sheet)
for j,t in enumerate(times):
    im=Image.open(out/f'still-{t}.png').convert('RGB');im.thumbnail((216,384));x=j%5*216;y=j//5*408;sheet.paste(im,(x,y));d.text((x+5,y+387),str(t)+'s',fill='white')
sheet.save(qa/'representatives.jpg',quality=92)
windows=[]
for j,cut in enumerate([3.75,7.5,13.125,16.875,21.5625,26.25]):
    frames=list(range(round((cut-.36)*24),round((cut+.36)*24)+1));sheet=Image.new('RGB',(6*180,3*344),'#302a25');d=ImageDraw.Draw(sheet)
    for k,idx in enumerate(frames):
        im=Image.open(out/'frames'/f'{idx:05d}.jpg');im.thumbnail((180,320));x=k%6*180;y=k//6*344;sheet.paste(im,(x,y));d.text((x+4,y+322),f'{idx/24:.3f}s',fill='white')
    name=f'transition-{j+1}.jpg';sheet.save(qa/name,quality=94);windows.append({'cut':cut,'frames':frames,'contact':name})
(qa/'maker-inspection-index.json').write_text(json.dumps({'scope':'maker inspection; not new independent review','representative_times':times,'transition_windows':windows,'actual_viewed':False,'audio_heard':False},indent=2),encoding='utf-8')
# Rebuildable audio: generate original 60-second cue, then time stretch at unchanged pitch.
shutil.copy2(old/'events.json',R/'events-original.json')
a=(old/'make_audio.py').read_text(encoding='utf-8').replace("R/'events.json'","R/'events-original.json'").replace("out=R/'audio'","out=R/'audio-original'")
(R/'generate-original-audio.py').write_text(a,encoding='utf-8')
(R/'make_audio.py').write_text('''"""Rebuild the original cue and speed it up to 30 seconds without pitch shift."""
from pathlib import Path
import subprocess,sys,os,shutil
R=Path(__file__).resolve().parent
subprocess.run([sys.executable,str(R/'generate-original-audio.py')],check=True)
ff=os.environ.get('FFMPEG') or shutil.which('ffmpeg') or 'D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe'
(R/'audio').mkdir(exist_ok=True)
subprocess.run([ff,'-hide_banner','-loglevel','error','-y','-i',str(R/'audio-original/mix.wav'),'-af','atempo=2','-t','30','-c:a','pcm_s16le',str(R/'audio/mix.wav')],check=True)
''',encoding='utf-8')
with wave.open(str(R/'audio/mix.wav')) as w:
    dur=w.getnframes()/w.getframerate();sr=w.getframerate();a=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype('f4')/32768
(R/'audio/audio-info.json').write_text(json.dumps({'duration':dur,'sample_rate':sr,'source_bpm':128,'effective_bpm':256,'processing':'FFmpeg atempo=2; pitch preserved','external_samples':False,'voice':False,'intentional_silence':[15.7,16.4],'peak':float(np.max(np.abs(a))),'rms':float(np.sqrt(np.mean(a*a)))},indent=2),encoding='utf-8')
p=(R/'package-delivery.py').read_text(encoding='utf-8').replace("'make_audio.py',","'make_audio.py','generate-original-audio.py','events-original.json',").replace("else 'final-v1'","else 'final-v1'")
(R/'package-delivery.py').write_text(p,encoding='utf-8')
(R/'README.md').write_text('''# 宝宝无字书页冒险 · 30秒

1080×1920竖屏，24fps。画面没有文字、字母、数字、标题或印章。宝宝使用认可的五官素材，移动为爬行，四肢肤色#f8c28b。

## 运行与渲染

Node.js：`node server.mjs 8770`，打开 http://127.0.0.1:8770 。界面播放按钮和时间显示不进入视频画面。
`window.render(seconds)`为30秒可寻址入口，内部以2倍速映射原60秒动作。六处转场采用0.56秒斜向纸页擦拭，不交叉淡化人物。

`node render.mjs --mode=final --version=v2`生成MP4。renderer使用相邻sand-journey工程中的playwright-core、Chrome及Remotion附带FFmpeg；在其他机器可将import路径、Chrome路径和FFmpeg/ffprobe路径改为本机配置。源码变动后使用新版本号，避免复用旧帧。

音频已包含，可直接渲染。重建：Python安装NumPy后运行`python make_audio.py`；先以events-original.json生成原创60秒爵士与拟音，再通过FFmpeg atempo=2输出30秒，保持音高。FFmpeg可由环境变量FFMPEG指定。

## 来源与许可

参考lemomo-ai/lemo-opuscar固定commit e3cb16f63768c68693ff0e15171d6e755457cc32的spy-titles绘制入口、纸边/纸纹、纸偶节拍与摄影机制。许可证在assets/LICENSE-lemo.txt。不声称原片逐像素复现。无外部音乐、字体文件或地图。head-atlas.png为用户认可的形象素材。

## 检查范围

前60秒版本的一轮独立审核已完成预算，本次是用户具体反馈修改，不新增独立审核。30秒成片做画幅、时长、帧数、音轨和完整解码检查；制作查看代表帧与六处转场连续接触表。没有实际听音或正常速度观看的完整视听通过声明。
''',encoding='utf-8')
print('Contacts and source documentation ready')
