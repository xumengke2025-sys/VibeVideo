import json,hashlib,shutil,subprocess,sys
from pathlib import Path
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parent
version=sys.argv[1];out=root/'out'/version;qa=root/'qa'/version;qa.mkdir(exist_ok=True)
cfg=json.loads((out/'config.json').read_text('utf8'));ev=json.loads((out/'evidence.json').read_text('utf8'));plan=json.loads((root/'production-plan-run-v7.json').read_text('utf8'))
h=hashlib.sha256()
for f in sorted(cfg['sourceFiles']):h.update(f.encode());h.update((root/f).read_bytes())
assert h.hexdigest()==cfg['signature'],'Source differs from render'
manifest=[]
for f in cfg['sourceFiles']:
 src=root/f;dst=out/'source'/f;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst);manifest.append({'file':f,'sha256':hashlib.sha256(src.read_bytes()).hexdigest()})
(out/'source-manifest.json').write_text(json.dumps({'video_sha256':ev['sha256'],'signature':cfg['signature'],'files':manifest},indent=2),encoding='utf8')
ff=Path('D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe')
frames=[]
def extract(f,dst):
 subprocess.run([str(ff),'-v','error','-y','-ss',str(f/48),'-i',str(out/'video.mp4'),'-frames:v','1',str(dst)],check=True,capture_output=True)
for i,s in enumerate(plan['timeline']['shots']):
 f=(s['startFrame']+s['events']['grab']-1)*2;dst=qa/f'era-{i+1:02}.png';extract(f,dst);frames.append({'era':i+1,'frame':f,'file':str(dst)})
board=Image.new('RGB',(1200,2232),'#242a2c');d=ImageDraw.Draw(board)
for k,f in enumerate(frames):
 x=12+(k%4)*298;y=12+(k//4)*555;board.paste(Image.open(f['file']).resize((282,501)),(x,y));d.text((x+4,y+510),f'{k+1:02}',fill='white')
board.save(out/'styleboard.jpg')
ids=[674,688,702,728,730,732,1238,1258,1268,1280,1302,1304,1306,1308,1344,1356,1468,1484]
board=Image.new('RGB',(1296,1455),'#242a2c');d=ImageDraw.Draw(board)
for k,f in enumerate(ids):
 dst=qa/f'frame-{f:05}.jpg';extract(f,dst);x=(k%6)*216;y=(k//6)*485;board.paste(Image.open(dst).resize((216,384)),(x,y));d.text((x+4,y+390),f'{f} / {f/48:.3f}s',fill='white')
board.save(qa/'final-local-recheck.jpg')
(qa/'extraction-index.json').write_text(json.dumps({'video_sha256':ev['sha256'],'eraFrames':frames,'localFrames':ids,'viewingStatus':'extracted; actual viewing must be logged separately'},indent=2),encoding='utf8')
print(json.dumps({'version':version,'sha256':ev['sha256'],'sourceFiles':len(manifest),'sourceSignatureVerified':True,'decoded':ev['decoded'],'browserErrors':ev['errors']}))

