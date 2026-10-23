import json,hashlib,subprocess,zipfile
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parent;B=R.parent;O=B/'out/final-v6-delivery'
FF=B.parent.parent/'node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe'
times=[2.6,7.6,15.5,21.5,24.8,31.5,33.8,39.9,42.6,44.6,47.8,50.8]
P=O/'decoded-stills';P.mkdir(exist_ok=True)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',19)
canvas=Image.new('RGB',(1440,1200),'#111e2c');draw=ImageDraw.Draw(canvas)
for i,t in enumerate(times):
    dst=P/f'{t}.png'
    subprocess.run([str(FF),'-v','error','-y','-ss',str(t),'-i',str(O/'video.mp4'),'-frames:v','1',str(dst)],check=True,timeout=45)
    im=Image.open(dst).convert('RGB');im.thumbnail((480,270));x=(i%3)*480;y=(i//3)*300;canvas.paste(im,(x,y));draw.text((x+10,y+274),f'{t:.2f}s',font=font,fill='white')
canvas.save(O/'decoded-overview.jpg',quality=94)
probe=json.loads((O/'ffprobe.json').read_text(encoding='utf-8'))
evidence=json.loads((O/'evidence.json').read_text(encoding='utf-8'))
layout=json.loads((B/'out/layout-v6.json').read_text(encoding='utf-8'))
stills=json.loads((B/'out/stills-v6-release/checks.json').read_text(encoding='utf-8'))
motion=json.loads((B/'out/motion-v6.json').read_text(encoding='utf-8'))
timing=json.loads((R/'audio/timing.json').read_text(encoding='utf-8'))
checks={'video_sha256':evidence['sha256'],'decoded':evidence['decoded'],'video_stream':{k:probe['streams'][0].get(k) for k in ['width','height','r_frame_rate','nb_frames','codec_name']},'audio_stream_present':any(x['codec_type']=='audio' for x in probe['streams']),'duration':probe['format']['duration'],'source_signature':evidence['signature'],'layout_samples':len(layout['samples']),'layout_issues':layout['issues'],'deterministic_seeks':stills['seeks'],'camera_numerical_continuity':motion['pass'],'voice_max_speed':max(x['speed'] for x in timing['entries']),'max_audio_peak':timing['peak'],'listening_verified':False,'independent_review':'No new review; inherited ai_review_once budget already used','decoded_stills':times,'bytes':(O/'video.mp4').stat().st_size}
(O/'delivery-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(checks,ensure_ascii=False))
