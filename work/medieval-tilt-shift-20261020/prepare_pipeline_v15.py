"""Version the tested bounded pipeline without altering historical production."""
from pathlib import Path
import json
P=Path(__file__).resolve().parent
s=(P/'render_pipeline_v14.py').read_text(encoding='utf8').replace('v14','v15').replace('V14','V15').replace('1824','2160').replace('1823','2159').replace('1786','2122').replace("'duration':76","'duration':90")
s=s.replace("SAMPLE=sorted(set([48,288,528,934,1115,1752]+list(range(720,792))+list(range(1320,1494))))", "SAMPLE=sorted(set([48,192,324,359,360,456,552,599,600,744,864,1055,1056,1212,1319,1320,1535,1536,1775,1776,1872,1943,1944,2064,2159]+list(range(1560,1680))+list(range(948,984))))")
s=s.replace("files=['model/babylon-city-v15.blend','render_city_v15.py','v15_motion.py','traffic-v15.npz','v15-timeline.json','audio/final-mix-v15.wav']", "files=['model/babylon-city-v15-detail.blend','render_city_v15.py','v15_motion.py','v15_route.py','v14_motion.py','traffic-v14.npz','v14-timeline.json','audio/final-mix-v15.wav']")
s=s.replace("cuts=[round(s[0]*24) for s in json.loads((ROOT/'v15-timeline.json').read_text(encoding='utf8'))['shots'][1:]]", "cuts=[round(t*24) for t in [8,15,19,25,31,44,55,64,74,81]]")
(P/'render_pipeline_v15.py').write_text(s,encoding='utf8')
s=(P/'assemble_city_v14.py').read_text(encoding='utf8').replace('v14','v15').replace('1824','2160').replace("'-t','76'","'-t','90'").replace("report['duration']-76","report['duration']-90").replace('暮河城-巴比伦巨城-Dream-of-Babylon-v15','风衣骑手-巴比伦巨城-Dream-of-Babylon-v15')
(P/'assemble_city_v15.py').write_text(s,encoding='utf8')
timeline={'duration':90,'fps':24,'width':1080,'height':1920,'aspect_ratio':'9:16','subject_id':'persistent trenchcoat cyclist','facial_detail':'none, explicit user request','shots':[{'range':[a,b],'reads':reads,'camera':'v15_motion.camera(t)','route':'v15_route.state(t)'} for a,b,reads in [(0,8,'rider silhouette; city emerges from horizon'),(8,15,'recognise trenchcoat and bicycle; greet Egyptian delegation'),(15,19,'front view after gate passage'),(19,25,'market bell; pedestrians make room'),(25,31,'connected right turn toward canal'),(31,44,'wave to boat crew; duck beneath awning'),(44,55,'inhabited north street; festival ribbon'),(55,64,'slow at temple approach'),(64,74,'foot down; tip hat; ritual finishes'),(74,81,'push off; return to avenue'),(81,90,'rider continues; metropolis unfolds')]],'music_source_excerpt':[29.5,119.5],'actual_listening':False}
(P/'v15-timeline.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2),encoding='utf8')
print('V15_PIPELINE_READY')
