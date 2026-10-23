from pathlib import Path
R=Path(__file__).resolve().parent
(R/'film.js').write_text('\n'.join((R/f).read_text(encoding='utf-8') for f in ['helpers.js','geometry.js','mechanisms.js','conductor.js']),encoding='utf-8')
print('Built V19 / 120s / 1920x1080')
