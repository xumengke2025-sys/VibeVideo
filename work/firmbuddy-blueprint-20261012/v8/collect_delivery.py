import hashlib,json,subprocess,sys,wave
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parent; B=R.parent; O=B/'out/final-v8-reduction'
sys.path.insert(0,str(B/'tools/python'))
import imageio_ffmpeg
FF=imageio_ffmpeg.get_ffmpeg_exe()
evidence=json.loads((O/'evidence.json').read_text(encoding='utf-8'))
probe=json.loads((O/'ffprobe.json').read_text(encoding='utf-8'))
timing=json.loads((R/'audio/timing.json').read_text(encoding='utf-8'))
v=next(s for s in probe['streams'] if s['codec_type']=='video')
a=next(s for s in probe['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1920,1080,'30/1',1560)
assert a['channels']==2 and abs(float(probe['format']['duration'])-52)<.1
assert timing['voiceover'] is False and timing['speech_assets_read']==0
old=(B/'v7/scene-body.js').read_text(encoding='utf-8')
new=(R/'scene-body.js').read_text(encoding='utf-8')
def camera_source(source):return source[source.index('const keys=['):source.index('function pathPoint(')]
def path_source(source):return source[source.index('const paths='):source.index('// Quintic Hermite')]
assert camera_source(old)==camera_source(new) and path_source(old)==path_source(new), 'Unexpected motion change'
assert (R/'audio/mix.wav').read_bytes()==(B/'v7/audio/mix.wav').read_bytes(), 'Unexpected music change'
assert '示例客户信息' in new and all(s not in new for s in ['扩产','资金安排','融资','示例客户\',222'])
times=[2.6,7.6,15.5,21.5,24.8,31.5,33.8,39.9,42.6,44.6,47.8,50.8]
P=O/'decoded-stills';P.mkdir(exist_ok=True)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',19)
canvas=Image.new('RGB',(1440,1200),'#111e2c');draw=ImageDraw.Draw(canvas)
for i,t in enumerate(times):
    dst=P/f'{t}.png'
    subprocess.run([FF,'-v','error','-y','-ss',str(t),'-i',str(O/'video.mp4'),'-frames:v','1',str(dst)],check=True,timeout=45)
    im=Image.open(dst).convert('RGB');im.thumbnail((480,270));x=(i%3)*480;y=(i//3)*300
    canvas.paste(im,(x,y));draw.text((x+10,y+274),f'{t:.2f}s',font=font,fill='white')
canvas.save(O/'decoded-overview.jpg',quality=94)
raw=subprocess.run([FF,'-v','error','-i',str(O/'video.mp4'),'-t','52','-f','f32le','-acodec','pcm_f32le','-ar','48000','-ac','2','-'],capture_output=True,check=True,timeout=60).stdout
decoded=np.frombuffer(raw,dtype='<f4').reshape(-1,2).mean(axis=1)
with wave.open(str(R/'audio/mix.wav'),'rb') as w:
    reference=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').reshape(-1,2).mean(axis=1)/32768
lags=[]
for at in [.2,12.1,31.2,37.9,47.5]:
    k=round(at*48000); width=round(.16*48000); expected=reference[k:k+width]
    offsets=list(range(-96,97)); similarities=[]
    for delta in offsets:
        measured=decoded[k+delta:k+delta+width]
        similarities.append(float(np.dot(expected,measured)/(np.linalg.norm(expected)*np.linalg.norm(measured)+1e-12)))
    best=int(np.argmax(similarities)); lag=offsets[best]
    assert abs(lag)<=48, f'Encoded audio shift {lag} samples'
    lags.append({'at':at,'lag_samples':lag,'lag_ms':lag/48,'correlation':similarities[best]})
layout=json.loads((B/'out/layout-v8.json').read_text(encoding='utf-8'))
stills=json.loads((B/'out/stills-v8-content/checks.json').read_text(encoding='utf-8'))
checks={'video_sha256':evidence['sha256'],'source_signature':evidence['signature'],'decoded':evidence['decoded'],'width':1920,'height':1080,'duration':52,'fps':30,'frames':1560,'audio_channels':2,'voiceover':False,'speech_assets_read':0,'narration_captions':False,'camera_and_paths_unchanged_from_v7':True,'music_binary_unchanged_from_v7':True,'client_label':'示例客户信息','business_example':'reduction-precontact','layout_samples':len(layout['samples']),'layout_issues':layout['issues'],'seeks':stills['seeks'],'action_events':len(timing['action_sync']),'max_event_error_ms':max(s['error_ms'] for s in timing['action_sync']),'aac_alignment':lags,'loudness':timing['loudness'],'audio_peak':timing['peak'],'decoded_audio_peak':float(np.max(np.abs(decoded))),'decoded_stills':times,'listening_verified':False,'independent_review':'No new review; historical ai_review_once budget already used','bytes':(O/'video.mp4').stat().st_size}
(O/'delivery-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(checks,ensure_ascii=False))
