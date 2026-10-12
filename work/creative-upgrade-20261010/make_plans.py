import json
from pathlib import Path
base=Path('work/creative-upgrade-20261010')
def shot(id,a,b,intent,action,camera,states,risks=[]):return dict(id=id,start=a,end=b,intent=intent,action=action,camera=camera,states=dict(zip(['establish','action','result'],states)),risks=risks)
flight={'duration':8,'fps':24,'width':1080,'height':1920,'type':'3D','events':[{'id':'request','at':2.4,'duration':.7,'trigger':'drone stopped before closed gate','receiver':'gate','result':'signal acknowledged'},{'id':'gate-open','at':3.05,'duration':1.1,'trigger':'request','receiver':'two door panels','result':'safe gap'}],
'shots':[
shot('approach',0,2.4,'前方闭门使主体改变速度','伴随接近并减速','偏后方伴随，闭门在前', [.1,1.2,2.25],[[1.85,2.35]]),
shot('negotiate',2.4,4.4,'请求导致门响应','等待、扫描、门退让','同一伴随位置稳定读相互作用',[2.45,3.3,4.3],[[2.4,4.3]]),
shot('cross',4.4,6.5,'主体穿过自己改变的环境','加速穿越并轻微侧倾','伴随通过门，前景视差证明穿越',[4.45,5.15,6.35],[[4.5,5.7]]),
shot('consequence',6.5,8,'行动留下开放通道','上升回看','升高揭示门与出口关系',[6.55,7.2,7.85],[[7.3,7.95]])],
'connections':[dict(time=t,kind='continuous',anchor='drone / gate',window=[t-.1,t+.1]) for t in [2.4,4.4,6.5]]}
(base/'flight/plan.json').write_text(json.dumps(flight,ensure_ascii=False,indent=2),encoding='utf-8')
valve=json.loads((base/'valve/clips/one-way-portrait.json').read_text(encoding='utf-8'))
ev=[('phenomenon-open',.15,.4),('phenomenon-close',1.15,.4),('section',2.5,1.3),('near',3.8,1.2),('open',5,1.7),('close',8.7,1.4),('reverse',11,.5),('far',12.2,1.8),('settle',12.4,1.6)]
valve['events']=[dict(id=id,at=a,duration=d,anchor='valve-disc' if id in ['open','close','reverse'] else 'valve-body',action=id,result='shared pressure/section/camera state') for id,a,d in ev]
valve['captions']=[dict(start=a,end=b,text=text) for a,b,text in [(0,2.5,'正向通过，反向停住'),(2.5,5,'答案藏在接触处'),(5,8.7,'压差推开，弹簧压缩'),(8.7,11,'卸载后，弹簧复位'),(11,12.5,'逆压更紧'),(12.5,15,'一开一闭，单向通行')]]
valve['shots']=[
shot('phenomenon',0,2.5,'先有现象和问题','正向/逆向符号对照','完整同一器件',[.1,.8,2.3],[[1.4,2.3]]),
shot('discover',2.5,5,'从外观揭示同一接触','下移剖切再靠近','保留中心线与器件身份',[2.6,3.3,4.8],[[3.4,4.95]]),
shot('force',5,10.5,'开度与弹簧压缩由载荷控制','正向力增加、开通、卸载回座','近景读行程，接触处停机',[5.1,6.4,10.3],[[5.4,6.8],[9.1,10.4]]),
shot('blocked',10.5,15,'逆压止于闭合接触后收束','逆向箭头停在阀瓣下，回收总览','停机观察接触，再拉回',[10.6,11.8,14.7],[[10.6,11.8],[12.2,14]])]
valve['connections']=[dict(time=t,kind='continuous',anchor='valve-disc / centreline',window=[t-.1,t+.1]) for t in [2.5,5,10.5]]
valve['silences']=[]
valve['facts']['claim']='正向压差克服预载后开启，位移由刚度/行程限制；卸载弹簧复位，逆压加强关闭。准静态示意，不是动态力学或流体仿真。'
(base/'valve/clips/one-way-portrait.json').write_text(json.dumps(valve,ensure_ascii=False,indent=2),encoding='utf-8')
print('Event-aligned plans generated')
