"""Rebuild the edited scene; never overwrite business or music data."""
from pathlib import Path
R=Path(__file__).resolve().parent
film=(R/'film.js').read_text(encoding='utf-8')
helpers=film[:film.index('// V6 original world geometry.')]
(R/'film.js').write_text(helpers+(R/'scene-body.js').read_text(encoding='utf-8'),encoding='utf-8')
print('V10 scene rebuilt; timeline and instrumental music preserved.')
