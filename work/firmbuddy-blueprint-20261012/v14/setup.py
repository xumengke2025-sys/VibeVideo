"""Rebuild the edited scene; never overwrite business or music data."""
from pathlib import Path
R=Path(__file__).resolve().parent
film=(R/'film.js').read_text(encoding='utf-8')
helpers=film[:film.index('// Screen-space drafting table')]
(R/'film.js').write_text(helpers+(R/'intro.js').read_text(encoding='utf-8')+'\n'+(R/'scene-body.js').read_text(encoding='utf-8')+'\n'+(R/'journey.js').read_text(encoding='utf-8'),encoding='utf-8')
print('V14 rebuilt: 90-second business burden journey')
