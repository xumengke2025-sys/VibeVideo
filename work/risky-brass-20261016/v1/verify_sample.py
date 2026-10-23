from pathlib import Path
import hashlib
import json
import subprocess
from PIL import Image, ImageDraw

ROOT = Path(__file__).parent
BIN = Path('D:/ai项目/ai动画/VibeVideo项目/node_modules/@remotion/compositor-win32-x64-msvc')
VIDEO = ROOT/'risky-explainer-sample.mp4'
QA = ROOT/'qa'/'delivered-sample'
QA.mkdir(parents=True,exist_ok=True)
def run(args):
    result = subprocess.run(args,capture_output=True,text=True,encoding='utf-8',errors='replace')
    if result.returncode:
        raise RuntimeError(result.stderr[-4000:])
    return result
meta = json.loads(run([str(BIN/'ffprobe.exe'),'-v','error','-show_format','-show_streams','-of','json',str(VIDEO)]).stdout)
decoded = run([str(BIN/'ffmpeg.exe'),'-v','error','-i',str(VIDEO),'-c:v','rawvideo','-c:a','pcm_s16le','-f','null','-'])
assert not decoded.stderr.strip(), decoded.stderr
video = next(s for s in meta['streams'] if s['codec_type']=='video')
audio = next(s for s in meta['streams'] if s['codec_type']=='audio')
assert (video['width'],video['height'],video['r_frame_rate'],int(video['nb_frames'])) == (1920,1080,'30/1',720)
assert abs(float(meta['format']['duration'])-24)<.05
assert audio['channels']==2
for t in [3.7,5.5,8.8,12,16.9,20.8,23]:
    run([str(BIN/'ffmpeg.exe'),'-v','error','-y','-ss',str(t),'-i',str(VIDEO),'-frames:v','1',str(QA/f'frame-{t}.png')])
files=[]
for i in range(18):
    path = QA/f'path-{i+1:02d}.png'
    run([str(BIN/'ffmpeg.exe'),'-v','error','-y','-ss',str(14+i/6),'-i',str(VIDEO),'-frames:v','1',str(path)])
    files.append(path)
sheet=Image.new('RGB',(1920,6*390),(30,34,32))
draw=ImageDraw.Draw(sheet)
for i,path in enumerate(files):
    img=Image.open(path).convert('RGB').resize((640,360),Image.Resampling.LANCZOS)
    x,y=(i%3)*640,(i//3)*390
    sheet.paste(img,(x,y))
    draw.text((x+10,y+363),f'{14+i/6:.3f} s',fill='white')
sheet.save(QA/'path-continuity.jpg',quality=95)
record={'file':str(VIDEO),'sha256':hashlib.sha256(VIDEO.read_bytes()).hexdigest(),
        'full_decode':'passed','duration':meta['format']['duration'],
        'width':video['width'],'height':video['height'],'fps':video['r_frame_rate'],
        'frames':video['nb_frames'],'audio':{'codec':audio['codec_name'],'channels':audio['channels']},
        'audio_listened':False,'independent_review':'not_requested_for_internal_sample',
        'representative_frame_times':[3.7,5.5,8.8,12,16.9,20.8,23],
        'path_sequence':'14.000-16.833 s at 6 fps; must be viewed, export alone is not review'}
(QA/'verification.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(record,ensure_ascii=False))
