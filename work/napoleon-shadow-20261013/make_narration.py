import asyncio,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).parent
sys.path.insert(0,str(ROOT/'vendor-python'))
import edge_tts
FP='D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffprobe.exe'
CUES=[
 {'id':'arcole','start':1.2,'end':12.7,'text':'一七九六年，年轻的波拿巴在意大利成名。格罗把他画成举旗的英雄，传奇由此开场。'},
 {'id':'jaffa','start':16.1,'end':27.8,'text':'三年后，东方远征遭遇瘟疫与挫折。雅法这幅画，却把他塑造成敢于靠近病人的领袖。'},
 {'id':'brumaire','start':28.4,'end':34.6,'text':'回到法国，他发动雾月政变，成为第一执政。'},
 {'id':'alps','start':35.1,'end':46.8,'text':'一八〇〇年，他翻越阿尔卑斯，再入意大利。现实中骑的是骡，大卫却让他驾驭昂首的白马。'},
 {'id':'coronation','start':51.1,'end':62.7,'text':'一八〇四年，他成为皇帝，并为约瑟芬加冕。从军旗到皇冠，八年之间，名画也塑造了他的帝国传奇。'}]
async def main():
 out=ROOT/'film/narration';out.mkdir(exist_ok=True)
 for i,c in enumerate(CUES):
  f=out/f'{i:02d}.mp3'
  if not f.exists():
   for attempt in range(3):
    try:
     await edge_tts.Communicate(c['text'],'zh-CN-YunxiNeural',rate='+8%').save(str(f));break
    except Exception as e:
     print('retry',i,attempt,type(e).__name__,flush=True)
     if attempt==2:raise
  c['duration']=float(subprocess.check_output([FP,'-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(f)]))
  c['file']=f'narration/{i:02d}.mp3';c['voice']='zh-CN-YunxiNeural';c['synthetic']=True
  print(c['id'],c['duration'],'window',c['end']-c['start'],flush=True)
 (ROOT/'film/narration.json').write_text(json.dumps(CUES,ensure_ascii=False,indent=2),encoding='utf-8')
asyncio.run(main())
