"""Prepare a resumable full render/encode route, preserving previous versions."""
from pathlib import Path
ROOT=Path(__file__).resolve().parent
s=(ROOT/'assemble_city.py').read_text(encoding='utf8')
s=s.replace('frames-v6','frames-v8').replace('1080x1920-v6.mp4','Dream-of-Babylon-v8.mp4').replace("audio/final-mix.wav","audio/final-mix-v8.wav").replace("'engineering-check.json'","'engineering-check-v8.json'").replace("'ffprobe.json'","'ffprobe-v8.json'")
(ROOT/'assemble_city_v8.py').write_text(s,encoding='utf8')
s=(ROOT/'render_pipeline.py').read_text(encoding='utf8')
s=s.replace('frames-v6','frames-v8').replace('batch-logs-v6','batch-logs-v8').replace('babylon-city-v6.blend','babylon-city-v8.blend')
s=s.replace("'render_city.py'","'render_city_v8.py'").replace("'assemble_city.py'","'assemble_city_v8.py'").replace("'pipeline-status.json'","'pipeline-status-v8.json'")
(ROOT/'render_pipeline_v8.py').write_text(s,encoding='utf8')
print('V8 full-render and encode commands prepared; not launched')
