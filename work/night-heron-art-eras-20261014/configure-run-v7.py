from pathlib import Path
root=Path(__file__).resolve().parent
p=root/'extract-run-v7.py';text=p.read_text('utf8').replace('run-v6','run-v7')
text=text.replace(" b=outbounds[0]\n",''' # Freeze the load-bearing lower body in every pose after rigid registration.
 # Head/neck drawings remain untouched; no mouth or bill deformation.
 b=outbounds[0]
 band={1:.80,2:.56,4:.73,8:.73,11:.73,12:.56,13:.73,14:.73}.get(n,.63)
 seam=round(b[1]+(350-b[1])*band)
 base=Image.open(target/frames[0]).convert('RGBA')
 for name in frames[1:]:
  pic=Image.open(target/name).convert('RGBA')
  # All pixels below this anatomical division are the exact same static drawing.
  pic.paste(base.crop((0,seam,384,384)),(0,seam));pic.save(target/name)
''')
text=text.replace("'method':'genuine redrawn poses; uniform scale and rigid foot/body registration; no facial deformation'","'staticLowerBodyFromY':seam,'method':'real head turn drawings; rigid foot registration; identical lower-body pixels; no facial deformation'")
p.write_text(text,encoding='utf8')
p=root/'render-run-v7.mjs';text=p.read_text('utf8').replace("...walk('assets/run-v7'),'audio/score-run-v4.wav'","...walk('assets/run-v6'),...walk('assets/run-v7'),'audio/score-run-v4.wav'")
# V7 dependencies are versioned and every asset is captured in the source signature.
p.write_text(text,encoding='utf8')
print('Configured extraction and source snapshots')
