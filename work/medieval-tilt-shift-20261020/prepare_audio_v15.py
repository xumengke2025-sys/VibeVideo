from pathlib import Path
P=Path(__file__).resolve().parent
s=(P/'mix_music_v14.py').read_text(encoding='utf8').replace('v14','v15').replace('V14','V15').replace('DURATION=76','DURATION=90').replace("'-t','76'","'-t','90'")
s=s.replace("(76,0)","(90,0)").replace("(73,.0005)","(87,.0005)")
s=s.replace("(25.8,.0002),(28,.0045),(34.5,.0045),(37.5,.0002)","(30,.0002),(32,.0045),(42,.0045),(45,.0002)")
s=s.replace('at=16.45','at=19.45').replace('at<26.7','at<30.7')
s=s.replace('[(28.7,.70),(30.1,.24),(32.4,.65),(34.8,.35)]','[(32.7,.70),(35.1,.24),(38.4,.65),(42.1,.35)]')
s=s.replace("put(61.2,contact", "put(61.2*90/76,contact")
extra='''
# Quiet speed-shaped tyre and cloth layers, plus two restrained brass bell cues.
import v15_route as route
keyt=np.arange(0,DURATION+1/24,1/24);speeds=np.array([route.state(float(x))['speed'] for x in keyt]);velocity=np.interp(t,keyt,speeds)
rolling=noise(N,350,2200)*np.minimum(1,velocity/4)*.0013
env[:,0]+=rolling;env[:,1]+=np.roll(rolling,203)*.88
for at in [12.65,24.1,35.2]:
 tt=np.arange(round(.8*SR))/SR
 bell=(np.sin(math.tau*1470*tt)*np.exp(-tt*5)+.45*np.sin(math.tau*2967*tt)*np.exp(-tt*9)+.2*np.sin(math.tau*4123*tt)*np.exp(-tt*13))*(1-np.exp(-tt*3500))
 put(at,bell,.0038,.48,'bicycle brass bell')
tt=np.arange(round(.45*SR))/SR
put(65.4,noise(len(tt),700,3200)*np.sin(math.pi*tt/.45)**2,.0017,.5,'gentle bicycle braking')
'''
s=s.replace('fade=np.sin',extra+'\nfade=np.sin')
s=s.replace("[('opening',0,8),('gate',8,16),('market',16,27),('canal',27,36.5),('garden',36.5,44.5),('statue',44.5,53.5),('ritual',53.5,62.2),('return',62.2,67.6),('panorama',67.6,76)]","[('opening',0,8),('gate',8,19),('market',19,31),('canal',31,44),('garden',44,55),('temple approach',55,64),('ritual',64,74),('return',74,81),('panorama',81,90)]")
s=s.replace("'duration':76","'duration':90").replace('[29.5,105.5]','[29.5,119.5]').replace('[73,76]','[87,90]')
s=s.replace('quiet stone footfalls and altar contact','quiet stone footfalls, rolling tyres, brass bicycle bell, gentle braking and altar contact')
(P/'mix_music_v15.py').write_text(s,encoding='utf8');print('V15_AUDIO_SCRIPT_READY')
