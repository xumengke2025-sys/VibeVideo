from pathlib import Path
import json
p=Path(__file__).parent
def edit(name,a,b):
 f=p/name;s=f.read_text(encoding='utf-8');assert a in s,(name,a);f.write_text(s.replace(a,b),encoding='utf-8')
edit('timeline.js','DUR=60','DUR=40')
edit('main.js',"import {drawBaby,drawCat} from './baby.js';","import {drawCat} from './baby.js';\nimport {drawBaby,loadHeads} from './baby-rig.js';\nimport {storyTime} from './pacing.js';\nawait loadHeads();")
edit('main.js','function scene(t,cam=camera(t)){','function scene(t,cam=camera(t),clock=t){')
edit('main.js','BOIL.step=Math.floor(t*12+1e-6)','BOIL.step=Math.floor(clock*12+1e-6)')
edit('main.js','drawBaby(BABY,b);','drawBaby(BABY,{...b,clock});')
edit('main.js','window.render=t=>{t=Math.max(0,Math.min(60,t));if(t<55)scene(t);','window.render=clock=>{const t=storyTime(clock);if(t<55)scene(t,camera(t),clock);')
edit('render.mjs',"'0:60'","'0:40'")
edit('render.mjs',"range[1]===60?'宝宝和太阳的晚安-v1.mp4'","range[1]===40?'宝宝和太阳的晚安-v2.mp4'")
edit('verify.py','晚安-v1.mp4','晚安-v2.mp4')
edit('verify.py',"'duration_60s':abs(float(meta['format']['duration'])-60)","'duration_40s':abs(float(meta['format']['duration'])-40)")
edit('verify.py',"'1440_video_frames':int(v.get('nb_frames',0))==1440","'960_video_frames':int(v.get('nb_frames',0))==960")
edit('verify.py','Basic engineering checks; representative stills and 16 samples from 17–24.5s viewed during production.','Basic engineering checks; representative v2 poses and continuous crawl/transition samples viewed during production.')
# Shared pacing anchors are parsed directly; no independent foley clock.
edit('score.py','SR=48000; DUR=60;','SR=48000; DUR=40;')
edit('score.py','audio=np.zeros((SR*DUR,2),np.float32)',"""audio=np.zeros((SR*DUR,2),np.float32)
pacing=json.loads((Path(__file__).parent/'pacing.js').read_text(encoding='utf-8').split('export const PACING=')[1].split(';')[0])
def present(t):
    return float(np.interp(t,[s for p,s in pacing],[p for p,s in pacing]))
def event(signal,t,gain=.1,pan=0):
    place(signal,present(t),gain,pan)""")
edit('score.py','beat=60/78','beat=60/106')
edit('score.py','np.arange(0,53,beat*2)','np.arange(0,33.5,beat*1.5)')
edit('score.py','quiet=.78 if t>40 else 1','quiet=.78 if t>25.7 else 1')
edit('score.py','place(bell(n,3),t,.045','place(bell(n,3),present(t),.045')
edit('score.py','place(noise(.22,18),t,.035)','event(noise(.22,18),t,.035)')
edit('score.py','for t in np.arange(a,b,.39):place(noise(.09,28),float(t),.025,pan=-.15)','for t in np.arange(present(a),present(b),.23):place(noise(.09,28),float(t),.023,pan=-.15)')
edit('score.py','place(noise(2.1,35),t,.056,pan=p)','event(noise(present(t+2.1)-present(t),35),t,.056,pan=p)')
edit('score.py','place(bell(n,2),t,.055,pan=.22)','event(bell(n,2),t,.055,pan=.22)')
edit('score.py','place(noise(.5,16),58','event(noise(.5,16),58')
edit('score.py','place(noise(.66,10),58.4','event(noise(.66,10),58.4')
edit('score.py','place(noise(.15,28),59.3','event(noise(.15,28),59.3')
edit('score.py','place(s,float(t),.0035','event(s,float(t),.0035')
edit('score.py','place(s,float(t+.18),.0035','event(s,float(t+.18),.0035')
edit('score.py','score.wav: 60 s','score.wav: 40 s')
edit('REVISION.md','1. 重新依据三张照片建立宝宝脸型：','1. 按用户最新要求用内置imagegen参照三张照片生成透明蜡笔头部，代码只控制锚点和轻微转动，保持：')
(p/'CHECKPOINT.md').write_text("""# 宝宝绘本 v2 checkpoint

delivery_mode: user_feedback

目标：按四项用户反馈修正相似度、四肢、持续张嘴和节奏；按最新要求以照片生成脸部素材。保留v1，零子代理。

已完成：内置imagegen生成闭嘴、眨眼与哈欠透明头部，保存在assets；固定骨长短肢身体、距离相位爬行和40秒共享时间映射已实现；尚未验证渲染。

下一步：角色姿态设定帧与连续爬行/坐爬样段；整片渲染；文件、解码、画幅、时长、音轨基本检查；展示用户反馈。

约束：1080×1920，24fps，无文字/旁白，家→院子→院外花园，日夜显星与回书页。相似度最终由用户判断。
""",encoding='utf-8')
print('v2 integrated')
