"""Original Chinese script, public synthetic voice; no cloned human voice."""
import asyncio, json
from pathlib import Path
import edge_tts

ROOT=Path(__file__).parent
CUES=[
 (0.6,12,'先看一张二维图。没有明显引力影响时，光沿直线传播。沿光到达眼睛时的方向反向延长，就能找到光源。'),
 (12.5,25,'加入一个有质量的天体，光路会偏折。其他条件相同，掠过天体越近，偏折通常越明显。这里的公式描述弱场近似。'),
 (25.5,40,'现在跟着这束光。它从真实光源出发，弯向观察者。但眼睛只知道它最后从哪个方向到达。把这个方向反向延长，就得到偏移后的视位置。'),
 (40.5,54,'如果光源不只是一个点呢？把它铺成一片，每一点都产生自己的像。这些像连续排开，就形成明亮的弧线。这是一个简化的透镜模型。'),
 (54.3,62,'再把二维图解放回三维。围绕黑洞发光的，是周围热气体形成的吸积盘。'),
 (62.3,72,'取背面的一束光。虽然光源在黑洞身后，弯曲的光路仍能让它抵达我们。'),
 (72.3,80,'于是，盘背面的光，看起来出现在黑洞上方。亮弧是光源的像，不是另一层盘。'),
 (80.2,86,'换个观察角度，同一个盘的表观形状也会改变。'),
 (86.1,90,'引力改变光路，也改变我们看见的宇宙。')
]

async def main():
 out=ROOT/'narration';out.mkdir(exist_ok=True)
 records=[]
 for i,(start,end,text) in enumerate(CUES):
  target=out/f'{i:02d}.mp3'
  if not target.exists() or target.stat().st_size<1000:
   for attempt in range(2):
    try:
     await asyncio.wait_for(edge_tts.Communicate(text,'zh-CN-YunxiNeural',rate='+15%' if i<8 else '+25%').save(str(target)),timeout=45)
     break
    except Exception:
     if attempt:raise
  records.append({'start':start,'end':end,'text':text,'file':f'narration/{i:02d}.mp3','voice':'zh-CN-YunxiNeural','synthetic':True})
  print(f'VOICE {i+1}/{len(CUES)} {target.stat().st_size} bytes',flush=True)
 (ROOT/'narration.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')

if __name__=='__main__':asyncio.run(main())
