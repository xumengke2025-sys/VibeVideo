from pathlib import Path
R=Path(__file__).resolve().parent
(R/'film.js').write_text('\n'.join((R/f).read_text(encoding='utf-8') for f in ['helpers.js','intro.js','scene-body.js','story.js']),encoding='utf-8')
print('Rebuilt V16: 104 seconds, one case, original blueprint apparatus.')
