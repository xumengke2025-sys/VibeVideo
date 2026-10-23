from pathlib import Path
import urllib.request, json, hashlib
root=Path(__file__).resolve().parent/'studio/audio-assets'
sources={
 'GeneralUser-GS.sf2':'https://raw.githubusercontent.com/mrbumpy409/GeneralUser-GS/main/GeneralUser-GS.sf2',
 'LICENSE-GeneralUser.txt':'https://raw.githubusercontent.com/mrbumpy409/GeneralUser-GS/main/documentation/LICENSE.txt'}
entries=[]
for name,url in sources.items():
 p=root/name
 if not p.exists():
  with urllib.request.urlopen(url,timeout=60) as r,p.open('wb') as w:
   while chunk:=r.read(1024*1024):w.write(chunk)
 entries.append({'file':name,'url':url,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 print(name,p.stat().st_size,flush=True)
(root/'sources.json').write_text(json.dumps(entries,indent=2))
