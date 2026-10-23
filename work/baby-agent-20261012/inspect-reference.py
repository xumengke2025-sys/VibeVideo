import subprocess,json,hashlib
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
root=Path(__file__).resolve().parent
out=root/'qa'/'reference-video';out.mkdir(parents=True,exist_ok=True)
video=Path('D:/腾讯电脑管家文件搬家/xwechat_files/wxid_6965669652111_a61a/msg/video/2026-10/85e0acac266f6a6bbbb61320c106161a.mp4')
ff='D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe'
times=[i*.5 for i in range(35)]
for i,t in enumerate(times):
    subprocess.run([ff,'-hide_banner','-loglevel','error','-y','-ss',str(t),'-i',str(video),'-frames:v','1',str(out/f'frame-{i:03d}.png')],check=True,timeout=30)
for p in range(2):
    sheet=Image.new('RGB',(1200,1712),'#eee8d8');d=ImageDraw.Draw(sheet)
    for k,i in enumerate(range(p*20,min((p+1)*20,len(times)))):
        im=Image.open(out/f'frame-{i:03d}.png').convert('RGB');im.thumbnail((240,400))
        x=(k%5)*240;y=(k//5)*428
        sheet.paste(im,(x,y+24));d.text((x+8,y+5),f'{times[i]:.1f}s',fill='black')
    sheet.save(out/f'contact-{p+1}.jpg',quality=92)
(out/'index.json').write_text(json.dumps({'source':str(video),'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'duration':17.517233,'sample_times':times,'method':'0.5 second sequential visual sampling; not all-frame or audio review'},ensure_ascii=False,indent=2),encoding='utf8')
print(str(out))
