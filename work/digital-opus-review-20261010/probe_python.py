import importlib.util, importlib.metadata, importlib, json, sys, os
from pathlib import Path

names = {'numpy':'numpy','Pillow':'PIL','torch':'torch','torchaudio':'torchaudio','demucs':'demucs','librosa':'librosa','scipy':'scipy','soundfile':'soundfile','numba':'numba','faster-whisper':'faster_whisper','pypinyin':'pypinyin','matplotlib':'matplotlib','pedalboard':'pedalboard','mido':'mido','fonttools':'fontTools','dashscope':'dashscope','requests':'requests','edge-tts':'edge_tts','yt-dlp':'yt_dlp'}
packages={}
for dist, module in names.items():
    try:
        spec=importlib.util.find_spec(module)
        version=importlib.metadata.version(dist) if spec else None
        packages[dist]={'present':bool(spec),'version':version}
    except Exception as e:
        packages[dist]={'error':type(e).__name__}
smoke={}
for module in ('numpy','PIL'):
    try:
        if module=='numpy':
            import numpy as np
            smoke[module]=int(np.arange(3).sum())==3
        else:
            from PIL import Image
            smoke[module]=Image.new('RGB',(2,2)).size==(2,2)
    except Exception as e:
        smoke[module]=type(e).__name__
opus=Path(os.environ.get('OPUS_HOME',Path.home()/'opus-video'))
out={'executable':sys.executable,'python':sys.version.split()[0],'packages':packages,'smoke':smoke,'opus_home':str(opus),'opus_home_exists':opus.exists(),'optional_api_env_present':{key:bool(os.environ.get(key)) for key in ['OPENAI_API_KEY','OPUS_IMAGE_KEY_FILE','DASHSCOPE_API_KEY']}}
if '--imports' in sys.argv:
    out['import_checks']={}
    for module in ('torch','scipy','soundfile','numba'):
        try:
            obj=importlib.import_module(module)
            out['import_checks'][module]={'ok':True,'version':obj.__version__}
        except Exception as e:
            out['import_checks'][module]={'ok':False,'error':str(e)[:700]}
dest=Path(__file__).parent/('python-app.json' if '.cache' in sys.executable else 'python-system.json')
dest.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False))
