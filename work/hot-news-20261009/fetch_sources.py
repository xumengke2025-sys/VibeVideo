import urllib.request,json,re,html,hashlib
from pathlib import Path
root=Path(__file__).parent
(root/'sources').mkdir(parents=True,exist_ok=True)
(root/'assets').mkdir(exist_ok=True)
urls={'nobel':'https://www.nobelprize.org/prizes/physics/2026/press-release/','icecube-news':'https://icecube.wisc.edu/news/awards/2026/10/francis-halzen-icecube-principal-investigator-wins-2026-physics-nobel-prize/','press-guide':'https://icecube.wisc.edu/press-guide/','gallery':'https://icecube.wisc.edu/gallery/landscapes-and-skyscapes/'}
sources=[]
for key,url in urls.items():
    cached=root/'sources'/f'{key}.html'
    content=cached.read_bytes() if cached.exists() else urllib.request.urlopen(url,timeout=30).read()
    (root/'sources'/f'{key}.html').write_bytes(content)
    text=re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>',' ',content.decode())
    text=html.unescape(re.sub('<[^>]+>',' ',text))
    (root/'sources'/f'{key}.txt').write_text(re.sub(r'\s+',' ',text),encoding='utf-8')
    sources.append({'url':url,'local':f'sources/{key}.html','sha256':hashlib.sha256(content).hexdigest(),'retrieved_date':'2026-10-09'})
photo='https://res.cloudinary.com/icecube/images/q_auto/v1602553497/gal_Landscapes_IMG_6308-712448984_2093800b7/gal_Landscapes_IMG_6308-712448984_2093800b7.jpg?_i=AA'
cached=root/'assets/antarctica.jpg'
data=cached.read_bytes() if cached.exists() else urllib.request.urlopen(photo,timeout=30).read();cached.write_bytes(data)
sources.append({'url':photo,'source_page':urls['gallery'],'local':'assets/antarctica.jpg','credit':'Keith Vanderlinde, NSF','title':'Swirling aurora with ICL on horizon','kind':'historical real photograph, not 2026 award footage','reuse_basis':'IceCube gallery permits educational/informational/noncommercial use with caption credit; press-guide snapshot retained.','sha256':hashlib.sha256(data).hexdigest(),'derivative':'portrait editorial crop, original preserved'})
(root/'sources/manifest.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'sources':len(sources),'photo_bytes':len(data)}))
