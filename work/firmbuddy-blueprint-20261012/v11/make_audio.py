from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name('make_opening_audio.py')),run_name='__main__')
