"""Review actual consecutive rendered frames, separate from media validation."""
from pathlib import Path
from PIL import Image,ImageDraw
import json
R=Path(__file__).parent;O=R/'out/review';O.mkdir(exist_ok=True)
F=R/'out/final-render/frames'
windows=[('opening',0,7),('crossing',7,16),('march',16,25),('sea-battle',25,36),('scholar',36,46),('departure',46,54),('ending',54,60)]
for name,start,end in windows:
 # 24 chronological frames per sheet: visible intermediate states.
 indices=[round((start+(end-start)*i/24)*24) for i in range(24)]
 sheet=Image.new('RGB',(6*180,4*346),'#d6d4ca');d=ImageDraw.Draw(sheet)
 for j,f in enumerate(indices):
  image=Image.open(F/f'{f:05}.jpg').resize((180,320))
  x=(j%6)*180;y=(j//6)*346;sheet.paste(image,(x,y));d.text((x+5,y+323),f'{f/24:.3f}s',fill='#222')
 sheet.save(O/f'{name}.jpg',quality=94)
for cut in [7,16,25,36,46,54]:
 indices=list(range(round((cut-.25)*24),round((cut+1.9)*24)+1,2))
 sheet=Image.new('RGB',(7*154,4*296),'#d6d4ca');d=ImageDraw.Draw(sheet)
 for j,f in enumerate(indices):
  image=Image.open(F/f'{f:05}.jpg').resize((154,274));x=(j%7)*154;y=(j//7)*296;sheet.paste(image,(x,y));d.text((x+4,y+276),f'{f/24:.3f}s',fill='#222')
 sheet.save(O/f'cut-{cut}.jpg',quality=94)
(O/'sampling.json').write_text(json.dumps({'shot_windows':windows,'frames_per_shot':24,'transition_every_frames':2,'fps':24,'frame_source':'final-render/frames','method':'chronological frame sheets; not real-time playback'},indent=2))
print('7 action sheets + 6 dense transition sheets written')
