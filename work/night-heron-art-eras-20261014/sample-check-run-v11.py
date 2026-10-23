from pathlib import Path
import json,subprocess
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parent
out=root/'out/sample-run-v11-fast-strut-03';qa=root/'qa/sample-run-v11-fast-strut-03';qa.mkdir(exist_ok=True)
ff='D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe'
board=Image.new('RGB',(1440,1440),'#22282b');d=ImageDraw.Draw(board)
for k in range(48):
 t=k*4.5/48;dst=qa/f'frame-{k:02}.jpg'
 subprocess.run([ff,'-v','error','-y','-ss',str(t),'-i',str(out/'video.mp4'),'-frames:v','1',str(dst)],check=True,capture_output=True)
 im=Image.open(dst).crop((140,810,920,1470)).resize((240,203));x=k%6*240;y=k//6*180
 # Slightly crop the ground below the feet; preserve the full head-up window.
 board.paste(im.resize((212,156)),(x+14,y));d.text((x+16,y+160),f'{t+1.125:.3f}s',fill='white')
board.save(qa/'sequence-48.jpg')
json.dump({'video':str(out/'video.mp4'),'startGlobalSeconds':1.125,'duration':4.5,'samples':48,'status':'extracted; actual viewing recorded separately'},open(qa/'index.json','w'),indent=2)
print(qa/'sequence-48.jpg')
