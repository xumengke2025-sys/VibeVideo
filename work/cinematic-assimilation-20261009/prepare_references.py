"""Localize code dependencies and fonts; no remote video assets are fetched."""
from pathlib import Path
import urllib.request, re, json, hashlib

BASE = Path('C:/CodexTemp/vibe-github-20261009')
OUT = Path(__file__).parent / 'reference-adapter'
OUT.mkdir(exist_ok=True)
sources = {
    'beach': BASE/'particle-beach/index.html',
    'reel': BASE/'opus-video-skills/skills/kinetic-reel/template/reel/index.html',
}
records=[]
for name, path in sources.items():
    html=path.read_text(encoding='utf-8')
    links=re.findall(r'<link[^>]+href="(https://fonts.googleapis.com/[^\"]+)"[^>]*>',html)
    csses=[]
    for url in links:
        req=urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0 Chrome/131.0.0.0'})
        css=urllib.request.urlopen(req,timeout=45).read().decode()
        for fonturl in set(re.findall(r'url\((https://[^)]+)\)',css)):
            key=hashlib.sha256(fonturl.encode()).hexdigest()[:20]+'.woff2'
            dst=OUT/key
            if not dst.exists(): dst.write_bytes(urllib.request.urlopen(fonturl,timeout=45).read())
            records.append({'type':'font','source':fonturl,'local':key,'sha256':hashlib.sha256(dst.read_bytes()).hexdigest()})
            css=css.replace(fonturl,'/adapter/'+key)
        csses.append(css)
    html=re.sub(r'<link[^>]+href="https://fonts.googleapis.com/[^\"]+"[^>]*>','',html)
    html=html.replace('</head>', '<style>'+ '\n'.join(csses)+'</style></head>')
    html=html.replace('https://cdn.jsdelivr.net/npm/three@0.169.0/','/three169/')
    (OUT/(name+'.html')).write_text(html,encoding='utf-8')
(OUT/'fonts-provenance.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'html':list(sources),'font_files':len(set(x['local'] for x in records))}))
