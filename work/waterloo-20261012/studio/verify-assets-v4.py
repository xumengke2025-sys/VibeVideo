from pathlib import Path
from PIL import Image
import hashlib,json
ROOT=Path(__file__).resolve().parent
originals={'master':'exec-6e558a1e-09b3-4ab9-963d-1249c4c83e0e.png','hero':'exec-e3aa42bd-6df0-4821-8e6b-70de664a9fdf.png','backdrop':'exec-6951b621-e8c2-47fa-9b6f-55628444c6dc.png','artillery':'exec-df6efc61-ae97-4e7a-827e-7babf06bbdb7.png','horse':'exec-14c05af1-ad99-44ef-b415-7f6a1ea58a9f.png'}
notes={'master':'统一纸雕灯箱风格设定母图；渲染使用其分层编辑图','hero':'整幅同源透明近层，手/旗杆/鹰固定；左下纸岩坡遮挡','backdrop':'无旗手同源军阵；不宣称历史地形复原','horse':'一个完整骑手与马；整体短程平移，不逐腿奔跑','artillery':'完整炮组；动态闪光与烟由时间轴绘制'}
items=[]
for name,source in originals.items():
 p=ROOT/'assets-v4'/f'{name}.png';im=Image.open(p)
 a=im.getchannel('A') if im.mode=='RGBA' else None
 bbox=a.point(lambda x:255 if x>16 else 0).getbbox() if a else (0,0,*im.size)
 items.append({'id':name,'path':str(p),'source':str(Path('C:/Users/67236/.codex/generated_images/01a12fda-7b5e-7ff3-913c-c8f79fb2ccc7')/source),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'size':im.size,'mode':im.mode,'alpha_range':a.getextrema() if a else None,'alpha_visible_bbox':bbox,'canvas_crop':'none','anchor':{'hero':[.29,.82],'horse':[.50,.96],'artillery':[.53,.96]}.get(name,[.5,.5]),'notes':notes[name]})
(ROOT/'asset-manifest-v4.json').write_text(json.dumps({'tool':'built-in image_gen','assets':items,'prompts':'assets-v4/prompts.json; original horse/artillery prompt export pending running generation cell72'},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps([{'id':x['id'],'size':x['size'],'alpha':x['alpha_range'],'bbox':x['alpha_visible_bbox']} for x in items]))
