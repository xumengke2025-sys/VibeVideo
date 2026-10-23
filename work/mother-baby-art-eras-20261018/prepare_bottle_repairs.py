from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parent/'assets/bottle-v3'
for i in [7,8,9,14]:
 start=i//5*5;row=i%5;im=Image.open(R/f'batch-{start:02d}.png').convert('RGBA');w,h=im.size
 out=Image.new('RGBA',(1000,620))
 for col in range(4):
  cel=im.crop((round(col*w/4),round(row*h/5),round((col+1)*w/4),round((row+1)*h/5))).resize((500,310),Image.Resampling.LANCZOS)
  out.alpha_composite(cel,((col%2)*500,(col//2)*310))
 out.save(R/f'repair-ref-{i:02d}.png')
print('Prepared four individual 2x2 repair atlases')
