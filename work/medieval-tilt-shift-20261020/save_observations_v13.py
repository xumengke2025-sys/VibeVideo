from pathlib import Path
from datetime import datetime, timezone
import json
import subprocess
import sys

r=Path(__file__).resolve().parent
qa=r/'qa/v13'
e=json.loads((qa/'producer-evidence-v13.json').read_text(encoding='utf8'))
observations={
 'created_at':datetime.now(timezone.utc).isoformat(),
 'producer':'/root','independent_review':False,
 'video':e['video'],'video_sha256':e['video_sha256'],
 'method':'Actually viewed seven representative contact sheets, seven 24-frame consecutive contact sheets, and six original-resolution decoded images. No realtime playback or audio listening.',
 'actual_viewed_frames':[f['frame'] for f in e['frames']],
 'original_resolution_frames':[288,528,756,934,1176,1752],
 'actual_viewed_window_labels':[w['label'] for w in e['motion_windows']],
 'consecutive_ranges':[{k:w[k] for k in ['label','start_frame','end_frame','path','sha256']} for w in e['motion_windows']],
 'observations':[
  {'range':[12,35],'observation':'City rises into view above the sandy foreground. No strong colour flash is visible in this consecutive window. Later opening representatives show the connected avenue, canal, blue gate and temple; foreground and distance soften outside the focal band.'},
  {'range':[276,299],'original_frame':288,'observation':'Gift bearers with pale clothing, a priest, blue-clad guards and the king statue remain legible at the gate. The encounter uses restrained miniature gestures.'},
  {'range':[516,539],'original_frame':528,'observation':'Ten armed soldiers retain two parallel files with regular row spacing. Shields and spears remain attached in the inspected sequence; surrounding citizens are scattered around the formation. Small feet limit fine gait judgment on the reduced contact sheet; the formal-size source gait sample was separately checked during production.'},
  {'range':[732,755],'original_frame':756,'observation':'Four towmen are visible on each opposite bank. The west team stands on the stone quay and connects to the lower-left boat; the east team uses the paved strip beside planted beds and connects to the upper-right cargo boat. Both teams remain on shore in the inspected window. Coloured hulls, tied loads, canopy, sail and crew remain visible.'},
  {'range':[922,945],'original_frame':934,'observation':'Rerendered frame 934 matches surrounding garden views in colour and structure; no former isolated flash is visible in this inspected window. Terraces, stairs, palms and blue trim remain intact.'},
  {'range':[1103,1126],'original_frame':1176,'observation':'Two distinct large statues face the forecourt with pale-robed priests and offering vessels below. No strong colour flash is visible in this window.'},
  {'frames':[1284,1392,1492,1493,1560,1622],'observation':'Temple court and grain exchange contain visitors and retain blue architectural trim. Representative adjacent cut frames contain complete images.'},
  {'range':[1740,1763],'original_frame':1752,'observation':'The pullback retains a populated main avenue, cross streets and bridge decks through the focused middle distance. Far people become too small or blurred for individual-action assessment. Final frame 1823 is the intended ending black.'}
 ],
 'audio_perceived':False,'actual_listened_ranges_seconds':[],
 'limits':[
  'Producer visual checks cover only the stated representatives and consecutive windows; not all 1824 frames were visually reviewed.',
  'No new independent review; historical review does not certify this revised output.',
  'Actual audio listening unavailable. Audio decode and track specifications were checked, but subjective music synchronization was not verified.',
  'All encoded frames passed strong-green and isolated temporal-discontinuity detectors; subtle temporal shimmer is not ruled out.',
  'Stylized fantasy miniature interpretation of Babylon rather than an archaeological reconstruction.'
 ]
}
(qa/'producer-observations-v13.json').write_text(json.dumps(observations,ensure_ascii=False,indent=2),encoding='utf8')
subprocess.run([sys.executable,'-X','utf8',str(r/'record_delivery_v13.py')],check=True)
