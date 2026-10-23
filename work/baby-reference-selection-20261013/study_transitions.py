import io, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw

TASK = Path(__file__).resolve().parent
ROOT = TASK.parents[1]
FF = ROOT.parent / 'node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe'
SRC = ROOT / 'reference-sources/upstream-videos/lemo-opuscar/crayon-book.mp4'
windows = {
 'character-camera': [round(18.0+i*.5,3) for i in range(17)],
 'night-wash': [round(27.5+i*.5,3) for i in range(17)],
 'page-return': [44.5,45,45.5,45.8,45.9,46,46.1,46.25,46.5,46.9,47.25,47.5,47.6,47.8,48,48.2,48.4,48.6,48.8,49.2],
}
evidence=[]
for name, times in windows.items():
 sheet=Image.new('RGB',(1440,((len(times)+3)//4)*230),'#eee9df')
 dr=ImageDraw.Draw(sheet)
 for i,t in enumerate(times):
  data=subprocess.check_output([str(FF),'-v','error','-ss',str(t),'-i',str(SRC),'-frames:v','1','-vf','scale=360:-1','-f','image2pipe','-vcodec','png','-'],timeout=30)
  im=Image.open(io.BytesIO(data)).convert('RGB')
  x,y=(i%4)*360,(i//4)*230
  sheet.paste(im,(x,y+25));dr.text((x+7,y+6),f'{name} {t:.3f}s',fill='#222')
 sheet.save(TASK/f'{name}-sequence.jpg',quality=92)
 evidence.append({'window':name,'times':times,'decoded_width':360,'source':str(SRC),'method':'sampled sequence; no normal-speed playback or listening'})
 print(name,flush=True)
(TASK/'transition-evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf-8')
