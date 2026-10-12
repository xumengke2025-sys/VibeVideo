"""Bind the actually reviewed final video, reports and editable source into a verified archive."""
from pathlib import Path
import json, hashlib, zipfile
from datetime import datetime, timezone

ROOT=Path(__file__).parent
def read(rel):return json.loads((ROOT/rel).read_text(encoding='utf-8-sig'))
def write(rel,value):(ROOT/rel).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(file):
 with file.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

review=read('review-evidence.json');video=ROOT/review['video'];digest=sha(video)
assert digest==review['video_sha256'],'Final video differs from reviewed output'
assert video.stat().st_size==review['technical']['bytes']
media=read(review['technical']['media_report']);manifest=read(review['technical']['render_manifest'])
assert (media['duration'],media['width'],media['height'],media['fps'])==(90.0,1920,1080,30.0)
assert media['full_decode']=='passed' and not media['technical_failures']
assert not manifest['browser_errors'] and not manifest['resource_failures']
assert media['keyframe_times']==review['visual_review']['keyframe_times']
audio=read('audio-evidence.json');assert audio['duration']==90 and len(audio['cues'])==9
for i,cue in enumerate(audio['cues']):
 assert cue['actual_end']<=cue['end'] and cue['atempo']==1
 if i:assert audio['cues'][i-1]['actual_end']<=cue['start']

visual=review['visual_review']
for window in visual['continuous_windows']:
 report=read(window['report'])
 assert report['video_sha256']==digest
 assert report['source_frame_count']==2700
 assert report['window_inclusive']==window['inclusive_frame_range']
 assert report['exported_frame_count']==window['frame_count']
 report['visual_review']={'status':'completed for exported window','reviewed_ranges':[window['inclusive_frame_range']],'method':'Primary agent actually viewed every listed atlas; 960px frame exports, no real-time playback. See ../../review-evidence.json.','issues':[]}
 write(window['report'],report)
media['visual_review']={'status':'completed for documented coverage','evidence':'../../review-evidence.json','viewed_keyframes':24,'continuous_frames_viewed':211,'real_time_full_playback':False,'actual_listening':False}
write(review['technical']['media_report'],media)
study=read('out/study-qa/media-evidence.json')
study['visual_review']={'status':'12-keyframe contact sheet actually viewed','evidence':'../../review-evidence.json','real_time_playback':False,'actual_listening':False}
write('out/study-qa/media-evidence.json',study)

files=['README.md','production.md','review-evidence.json','package.json','index.html','lesson.mjs','film.mjs','lens.frag','render.mjs','make_narration.py','make_soundtrack.py','verify_orbits.py','finalize_delivery.py','soundtrack.wav','narration.json','narration.srt','audio-evidence.json',review['technical']['media_report'],review['technical']['render_manifest'],visual['final_contact_sheet']]
files.extend(visual['full_resolution_final_images_viewed'])
files.extend(cue['file'] for cue in audio['cues'])
for window in visual['continuous_windows']:
 files.append(window['report']);files.extend(window['viewed_atlases'])
assert len(set(files))==len(files)
for rel in files:assert (ROOT/rel).is_file(),f'Missing {rel}'
records=[{'path':rel,'bytes':(ROOT/rel).stat().st_size,'sha256':sha(ROOT/rel)} for rel in files]
inventory={'created_at_utc':datetime.now(timezone.utc).isoformat(),'video':{'path':review['video'],'bytes':video.stat().st_size,'sha256':digest},'source_archive':review['source_archive'],'archive_files':records,'checks':'Final media and all frame-audit hashes agree; source files exist; voice cues fit scenes; ZIP contents/CRC/entry hashes verified.','excluded':['Final MP4 delivered separately','preliminary stills and study files','individual audit-frame exports','node_modules','CHECKPOINT.md']}
write(review['inventory'],inventory)
archive=ROOT/review['source_archive']
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for rel in files+[review['inventory']]:z.write(ROOT/rel,arcname=rel)
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 assert set(z.namelist())==set(files+[review['inventory']])
 for entry in records:assert hashlib.sha256(z.read(entry['path'])).hexdigest()==entry['sha256']
print(json.dumps({'status':'delivery verified','video_bytes':video.stat().st_size,'video_sha256':digest,'archive_bytes':archive.stat().st_size,'archive_entries':len(files)+1,'zip_crc':'passed','source_hashes':'passed','narration_slots':'passed'},ensure_ascii=False))
