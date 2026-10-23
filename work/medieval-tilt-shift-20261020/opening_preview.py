from pathlib import Path
from PIL import Image,ImageDraw
import subprocess,json
root=Path(__file__).resolve().parent;frames=root/'render/frames-v6';out=root/'render/opening-check-v6';out.mkdir(exist_ok=True)
times=[0,12,24,36,48,60,72,84,96,108,120,132,144,156,168,180]
sheet=Image.new('RGB',(4*270,4*504),'#eee8dc');d=ImageDraw.Draw(sheet)
for i,f in enumerate(times):
    im=Image.open(frames/f'{f:05d}.png').convert('RGB').resize((270,480))
    x=(i%4)*270;y=(i//4)*504;sheet.paste(im,(x,y));d.text((x+7,y+483),f'{f/24:.1f}s / frame {f}',fill='#222222')
sheet.save(out/'opening-sequence.jpg',quality=92)
if all((frames/f'{i:05d}.png').exists() for i in range(192)):
    ff=Path('D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe')
    subprocess.run([str(ff),'-y','-hide_banner','-loglevel','warning','-framerate','24','-i',str(frames/'%05d.png'),'-i',str(root/'audio/final-mix.wav'),'-t','8','-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-threads:v','1','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out/'opening-8s.mp4')],check=True)
print(str(out))
