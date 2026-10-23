from pathlib import Path
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parent
out=root/'out/sample-v1'
board=Image.new('RGB',(1800,810),'#262b2d')
for era in range(3):
 for j,u in enumerate([.15,.4,.48,.64,.72,.84]):
  n=round((era*2.25+u*2.25)*24)
  im=Image.open(out/'frames'/f'{n:05}.jpg').crop((85,810,1045,1530)).resize((300,225))
  board.paste(im,(j*300,era*270))
  ImageDraw.Draw(board).text((j*300+8,era*270+232),f'era {era+2} / u {u} / F{n}',fill='white')
board.save(out/'action-board.jpg',quality=94)
