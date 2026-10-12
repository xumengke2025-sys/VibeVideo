import hashlib
import json
from pathlib import Path
from PIL import Image
root=Path(__file__).parent
assets=[
    {'id':'carina','local_path':'public/carina-nasa.png','kind':'real_observation',
     'source_page':'https://science.nasa.gov/asset/webb/cosmic-cliffs-in-the-carina-nebula-nircam-image/',
     'download_url':'https://assets.science.nasa.gov/dynamicimage/assets/science/missions/webb/science/2022/07/STScI-01GA6KKWG229B16K4Q38CH3BXS.png?fit=clip&w=3840',
     'creator_credit':'NASA, ESA, CSA, STScI','reuse_basis':'Educational/informational use under the NASA media guidelines; source credit preserved; no NASA endorsement asserted.',
     'reuse_reference':'https://www.nasa.gov/nasa-brand-center/images-and-media/',
     'source_release_date':'2022-07-12','retrieved_at':'2026-10-07 Asia/Shanghai',
     'derivatives':[{'type':'editorial_cover_crop','display_size':[1920,1080],'max_scale':1.24},
                    {'type':'six_vertical_editorial_slices','width_per_slice':320,'coordinate_space':[1920,1080],
                     'gray_source':'desaturation of published RGB image, not original filter observations',
                     'purpose':'illustrate alignment and color assignment only'}],
     'used_in':[[0,89],[90,179],[180,299]]},
    {'id':'optical-concept','local_path':'public/optical-mirror-concept.png','kind':'generated_concept',
     'creator_credit':'Built-in imagegen in Codex','source_page':None,
     'original_tool_output':'C:/Users/67236/.codex/generated_images/01a1166c-4f61-7bb3-9832-6d6668874450/exec-f4bc5563-7351-41d0-8589-252a88934411.png',
     'prompt_file':'image-prompt.txt','reuse_basis':'User-authorized generation for this test project',
     'generated_at':'2026-10-07 Asia/Shanghai',
     'derivatives':[{'type':'frame-driven editorial placement','display_width':1500,'max_scale':1.035,
                     'preserve_alpha':True,'notes':'Intentional right-edge crop; two-dimensional motion, not a 3D reconstruction'}],
     'used_in':[[90,179]],'accuracy':'Conceptual instrument, not accurate named-spacecraft geometry'},
    {'id':'sound','local_path':'public/study-sound.wav','kind':'original_code',
     'creator_credit':'Original synthesis in make_sound.py','reuse_basis':'Created for this test',
     'used_in':[[0,299]],'notes':'Test sound design, not commissioned music or narration'},
]
for asset in assets:
    path=root/asset['local_path']
    digest=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):
            digest.update(block)
    asset['sha256']=digest.hexdigest()
    asset['bytes']=path.stat().st_size
    if path.suffix=='.png':
        with Image.open(path) as image:
            asset['dimensions']=list(image.size)
            asset['mode']=image.mode
            if image.mode=='RGBA':
                asset['alpha_extrema']=list(image.getchannel('A').getextrema())
                asset['visible_bbox']=list(image.getchannel('A').getbbox())
(root/'asset-manifest.json').write_text(json.dumps(assets,ensure_ascii=False,indent=2),encoding='utf-8')
print('Recorded',len(assets),'assets with SHA256')
