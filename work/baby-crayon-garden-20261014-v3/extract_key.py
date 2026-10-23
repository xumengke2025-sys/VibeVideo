from pathlib import Path
import subprocess,json
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parent
ff='D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe'
out=root/'out/key-frames';out.mkdir(exist_ok=True)
for i in range(16):
    p=out/f'{i:02}.png'
    subprocess.run([ff,'-y','-hide_banner','-loglevel','error','-ss',str(i*.5),'-i',str(root/'out/跨院门关键样段.mp4'),'-frames:v','1','-s','270x480',str(p)],check=True,timeout=30)
sheet=Image.new('RGB',(1080,2040),'white');d=ImageDraw.Draw(sheet)
for i in range(16):
    sheet.paste(Image.open(out/f'{i:02}.png'),(i%4*270,i//4*510))
    d.text((i%4*270+8,i//4*510+484),f'{17+i*.5:.1f}s',fill='black')
sheet.save(root/'out/key-sequence-contact.jpg')
print('Extracted 16 samples, 17.0–24.5s; extraction is not a full playback audit.')
