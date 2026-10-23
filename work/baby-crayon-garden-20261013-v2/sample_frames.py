from PIL import Image,ImageDraw
from pathlib import Path
import subprocess,json
p=Path(__file__).parent
ff='D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe'
frames=p/'out/sample-frames';frames.mkdir(exist_ok=True)
times=[i*5/20 for i in range(20)]
sheet=Image.new('RGB',(300*5,550*4),'#fff');g=ImageDraw.Draw(sheet)
for i,t in enumerate(times):
 f=frames/f'{i:02d}.png'
 subprocess.run([ff,'-y','-v','error','-ss',str(t),'-i',str(p/'out/crawl-transition-v2.mp4'),'-frames:v','1','-s','270x480',str(f)],check=True,capture_output=True,timeout=30)
 sheet.paste(Image.open(f),((i%5)*300,(i//5)*550))
 g.text(((i%5)*300,(i//5)*550+485),f'{t+2:.2f}s',fill='black')
sheet.save(p/'out/crawl-contact-v2.jpg')
print('20 consecutive-time samples extracted')
