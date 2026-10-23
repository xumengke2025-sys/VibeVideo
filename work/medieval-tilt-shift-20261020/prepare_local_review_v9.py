"""Targeted evidence for the same reviewer's one-repair recheck; no full re-review."""
from pathlib import Path
import subprocess,json,hashlib,sys
ROOT=Path(__file__).resolve().parent
FF=Path('D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe')
AUDIT=Path('D:/Codex/skills/vibe-video/scripts/frame_audit.py')
report=json.loads((ROOT/'delivery/engineering-check-v9.json').read_text(encoding='utf8'))
video=Path(report['video']);assert hashlib.sha256(video.read_bytes()).hexdigest()==report['sha256']
windows=[('opening-bridge-gate',144,203),('market-canal-cut',624,659),('cargo-barges',728,775),('canal-garden-cut',840,875),('city-ending-cut',1216,1247)]
index={'video':str(video),'video_sha256':report['sha256'],'mode':'necessary_local_recheck_after_one_repair','windows':[],'review_budget':{'repair_rounds_used':1,'max_repair_rounds':1},'actual_audio_perception':'unavailable','original_v8_coverage':'0–149 only, not automatically mapped to v9','visual_production_checks':['formal-size proof 168 and 744 actually viewed by maker'],'changes':['24 pier/timber bridges with continuous ramps','4 legacy sailboats converted to loaded unrigged barges'],'preserved':['camera and timeline','8Hz activity','38px tilt/depth compositor','original v8 mix']}
for name,a,b in windows:
    out=ROOT/'qa/v9'/name
    if not (out/'frame-audit.json').exists():
        subprocess.run([sys.executable,str(AUDIT),str(video),'--out',str(out),'--start-frame',str(a),'--end-frame',str(b),'--width','1080','--cuts','192,384,639,864,1066,1224','--ffmpeg',str(FF),'--ffprobe',str(FF.with_name('ffprobe.exe'))],check=True)
    index['windows'].append({'name':name,'range':[a,b],'report':str(out/'frame-audit.json'),'atlas_paths':[str(out/p) for p in json.loads((out/'frame-audit.json').read_text(encoding='utf8'))['atlases']]})
adts=[]
for version in ['v8','v9']:
    path=ROOT/'delivery'/('暮河城-巴比伦巨城-Dream-of-Babylon-'+version+'.mp4')
    output=ROOT/'qa/v9'/('encoded-music-'+version+'.aac')
    subprocess.run([str(FF),'-y','-v','error','-i',str(path),'-map','0:a:0','-c:a','copy','-f','adts',str(output)],check=True)
    adts.append(hashlib.sha256(output.read_bytes()).hexdigest())
index['encoded_audio_equivalence']={'v8_aac_sha256':adts[0],'v9_aac_sha256':adts[1],'identical':adts[0]==adts[1],'meaning':'same encoded audio, not evidence of actual listening'}
(ROOT/'qa/v9/recheck-index.json').write_text(json.dumps(index,ensure_ascii=False,indent=2),encoding='utf8')
print('V9_LOCAL_RECHECK_EVIDENCE_READY',sum(b-a+1 for _,a,b in windows),'frames',flush=True)
