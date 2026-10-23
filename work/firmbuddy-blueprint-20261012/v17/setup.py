from pathlib import Path
R=Path(__file__).resolve().parent
s=(R/'scene-body.js').read_text(encoding='utf-8')
a=s.index('// Reference translation:');b=s.index('function cabinet(',a)
(R/'scene-body.js').write_text(s[:a]+(R/'hall.js').read_text(encoding='utf-8')+'\n'+s[b:],encoding='utf-8')
(R/'film.js').write_text('\n'.join((R/f).read_text(encoding='utf-8') for f in ['helpers.js','opening.js','scene-body.js','story.js']),encoding='utf-8')
print('Rebuilt V17: 124 seconds, one case, original blueprint apparatus.')
