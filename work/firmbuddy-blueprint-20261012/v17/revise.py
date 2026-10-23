from pathlib import Path
R=Path(__file__).resolve().parent
s=(R/'scene-body.js').read_text(encoding='utf-8')
a=s.index('function experts()');b=s.index('function cabinet(',a)
s=s[:a]+(R/'hall.js').read_text(encoding='utf-8')+'\n'+s[b:]
s=s.replace("visibility*=ease(p(openingClock(filmTime),10.7,11));","visibility*=filmTime>=38?1:0;")
(R/'scene-body.js').write_text(s,encoding='utf-8')
s=(R/'story.js').read_text(encoding='utf-8')
s=s.replace('function originalTime(t){return linearClock(t,storyClock);}', 'function originalTime(t){return linearClock(t-20,storyClock);}')
s=s.replace('function storyCamera(t){return t>=60&&t<=76?sampleKeys(t,detourKeys):cameraAt(originalTime(t));}', '''const openingKeys=[[0,1050,1105,.94,-.006],[7.4,1050,1105,.96,0],[9.2,1050,1105,.96,0],[16.4,1050,1105,.95,0],[18.4,1050,1070,.95,0],[27.4,1050,1070,.95,0],[32,1050,1070,.95,0],[35.2,1050,1070,.95,0],[38,1050,1070,.95,0]];
function storyCamera(t){if(t<=38)return sampleKeys(t,openingKeys);const old=t-20;return old>=60&&old<=76?sampleKeys(old,detourKeys):cameraAt(originalTime(t));}''')
s=s.replace('p(filmTime,a,b)','p(filmTime-20,a,b)').replace('const t=filmTime;','const t=filmTime-20;').replace('p(filmTime,31.7,32.5)','p(filmTime-20,31.7,32.5)')
s=s.replace('if(filmTime>=60&&filmTime<=64)','if(filmTime>=80&&filmTime<=84)').replace('p(filmTime,60,64)','p(filmTime-20,60,64)')
s=s.replace('if(filmTime>=72.8&&filmTime<=76)','if(filmTime>=92.8&&filmTime<=96)').replace('p(filmTime,72.8,76)','p(filmTime-20,72.8,76)')
s=s.replace('if(filmTime<100)','if(filmTime<120)').replace('p(filmTime,100,100.8)','p(filmTime-20,100,100.8)').replace("'#dcc28b'","'#d7e8f3'")
s=s.replace('Math.min(104,t)','Math.min(124,t)')
a=s.index(' const openingTime=openingClock(filmTime);');b=s.index(' compose(inkC',a)
s=s[:a]+''' chassis();
 inkLayer(ease(p(filmTime,35.2,37.2)),()=>intro());
 signals();experts();knowledge();visit();follow();industry();
 opening();businessNarrative(filmTime);caseTag();ending();
'''+s[b:]
s=s.replace('duration:104','duration:124').replace('base>=104','base>=124').replace('Math.min(104,base','Math.min(124,base').replace('t>=104','t>=124').replace(' / 104',' / 124')
s=s.replace('...storyClock.map(k=>[k[0]]),...detourKeys','...openingKeys,...storyClock.map(k=>[k[0]+20]),...detourKeys.map(k=>[k[0]+20,...k.slice(1)])')
(R/'story.js').write_text(s,encoding='utf-8')
s=(R/'setup.py').read_text(encoding='utf-8').replace("'intro.js'","'opening.js'")
(R/'setup.py').write_text(s,encoding='utf-8')
# Keep only the active opening source; original intro is preserved in v16.
(R/'intro.js').unlink()
s=(R/'helpers.js').read_text(encoding='utf-8')
s=s.replace('const corners=[[x+dx,y-size*.95],[x+dx+width,y-size*.95],[x+dx+width,y+size*.22],[x+dx,y+size*.22]].map(([a,b])=>S(ox+a,oy+b));','const rot=o.rot||0;const corners=[[dx,-size*.95],[dx+width,-size*.95],[dx+width,size*.22],[dx,size*.22]].map(([a,b])=>S(ox+x+a*Math.cos(rot)-b*Math.sin(rot),oy+y+a*Math.sin(rot)+b*Math.cos(rot)));')
(R/'helpers.js').write_text(s,encoding='utf-8')
print('V17 world opening and seated expert hall assembled')
