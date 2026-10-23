"""Rebuild the original cue and speed it up to 30 seconds without pitch shift."""
from pathlib import Path
import subprocess,sys,os,shutil
R=Path(__file__).resolve().parent
subprocess.run([sys.executable,str(R/'generate-original-audio.py')],check=True)
ff=os.environ.get('FFMPEG') or shutil.which('ffmpeg') or 'D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe'
(R/'audio').mkdir(exist_ok=True)
subprocess.run([ff,'-hide_banner','-loglevel','error','-y','-i',str(R/'audio-original/mix.wav'),'-af','atempo=2','-t','30','-c:a','pcm_s16le',str(R/'audio/mix.wav')],check=True)
