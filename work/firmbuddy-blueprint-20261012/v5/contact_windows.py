import sys,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'tools/python'))
import imageio_ffmpeg
ff=imageio_ffmpeg.get_ffmpeg_exe()
folder=ROOT/'out'/sys.argv[1];mode=sys.argv[2] if len(sys.argv)>2 else 'preview'
use_frames=len(sys.argv)>3 and sys.argv[3]=='frames'
specs={'preview':[('overview',[i*2 for i in range(26)]),('gear',[10.5+i*.25 for i in range(17)]),('section',[20.5+i*.25 for i in range(16)]),('carriage',[30.2+i*.2 for i in range(13)])], 'sample':[('gear',[11+i*.25 for i in range(15)]),('section',[20.5+i*.25 for i in range(16)]),('citation',[25+i*.15 for i in range(12)])], 'final':[('delivery',[2.8,8.9,11.7,16.9,22.4,24.5,27.7,31.3,35.5,41.7,46.5,50.5]),('carriage',[30.2+i*.2 for i in range(13)]),('ending',[43.8+i*.4 for i in range(21)])]}
config=__import__('json').loads((folder/'config.json').read_text())
target=folder/'delivery-frames';target.mkdir(exist_ok=True);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17)
for name,times in specs[mode]:
    board=Image.new('RGB',(1600,245*((len(times)+3)//4)),'#0b1830');draw=ImageDraw.Draw(board)
    for i,t in enumerate(times):
        src=target/f'{t:.3f}.png'
        if use_frames:src=folder/'frames'/f'{round((t-config["start"])*config["fps"]):05}.jpg'
        else:subprocess.run([ff,'-v','error','-y','-ss',str(max(0,t-config['start'])),'-i',str(folder/'video.mp4'),'-frames:v','1',str(src)],check=True)
        im=Image.open(src);im.thumbnail((400,225));x=i%4*400;y=i//4*245;board.paste(im,(x,y+20));draw.text((x+8,y+1),f'{t:.2f}s / '+('rendered' if use_frames else 'decoded'),font=font,fill='#daeaf7')
    board.save(target/f'{name}.jpg',quality=94)
    print(str(target/f'{name}.jpg'))
