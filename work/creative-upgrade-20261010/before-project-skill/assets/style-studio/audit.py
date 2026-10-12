"""Create review images from actual rendered frames; does not assign a verdict.
Pillow required. Review coverage and findings must be filled after observation.
"""
import argparse,json,math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

def sheet(items,out,cols=4,width=420):
    thumbh=round(width*720/1280);h=thumbh+30
    im=Image.new('RGB',(width*cols,h*math.ceil(len(items)/cols)),(24,28,33));draw=ImageDraw.Draw(im)
    for i,(file,label) in enumerate(items):
        tile=Image.open(file).convert('RGB');tile.thumbnail((width,thumbh));x=i%cols*width;y=i//cols*h
        im.paste(tile,(x,y));draw.text((x+7,y+thumbh+6),label,fill=(235,235,235))
    im.save(out,quality=93)

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--clip',required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    root=Path(__file__).parent;p=json.loads((root/'clips'/f'{a.clip}.json').read_text(encoding='utf-8'));frames=a.out/'frames';qa=a.out/'review';qa.mkdir(exist_ok=True)
    def at(t):return frames/f'{min(round(t*p["fps"]),round(p["duration"]*p["fps"])-1):05}.jpg'
    samples=[(at(t),f'{s["id"]}/{state}  t={t:.2f}') for s in p['shots'] for state,t in s['states'].items()]
    sheet(samples,qa/'overview.jpg')
    sequence=[]
    for e in p['events']:
        times=[];t=max(0,e['at']-.2);end=min(p['duration']-1/p['fps'],e['at']+e['duration']+.2)
        while t<=end+1e-8:times.append(round(t,5));t+=.2
        sequence.extend((at(t),f'{e["id"]} t={t:.2f}') for t in times)
    for i in range(0,len(sequence),12):sheet(sequence[i:i+12],qa/f'actions-{i//12:02}.jpg',cols=4)
    (qa/'schedule.json').write_text(json.dumps({'clip':a.clip,'overview_frames':len(samples),'action_frames':len(sequence),'action_step':.2,'observed':False,'scope':'Selected source frames at 0.2s intervals, not real-time playback or every decoded frame.'},indent=2),encoding='utf-8')
    print(json.dumps({'clip':a.clip,'overview':len(samples),'action_samples':len(sequence),'sheets':math.ceil(len(sequence)/12),'out':str(qa)}))
if __name__=='__main__':main()
