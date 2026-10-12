import json, pathlib,hashlib
R=pathlib.Path(__file__).parent
shots=[
 ('wing',0,7,'蓝色的悬念', [.6,3,6.6],'精细蝶翼上的短标题入退，近景小幅推进','近法线宏观近景，小裁切'),
 ('scales',7,14,'鳞片→细脊',[7.2,10.7,13.7],'鳞片建立，中心脊线定位，继续放大','俯视概念图，不转向背面'),
 ('ridges',14,22,'层间结构显露',[14.2,18,21.5],'同向脊线，镜头降低看见层间空隙','真实三维高机位降到侧视，末尾落定'),
 ('two-paths',22,32,'不同反射路程',[22.8,25.5,30],'24.4上层接触，25.5下层接触，两路出射','固定侧视剖面，由光移动'),
 ('phase',32,41,'相位叠加的结果',[32.7,35,39.5],'两路波峰合拍变强，另一波长示意错位减弱','局部波形定机；按解释需要横向分开'),
 ('field',41,47,'从局部回收许多脊线',[41.2,43.5,45.4],'多个脊线逐次反射蓝色信号，拉远看系统','低近景升高拉开，保留中心结构'),
 ('answer',47,52,'兑现开场',[47.2,49,51.5],'回到同一蝶翼，结论与科学限定落定','宏观近景停止追镜，留余音')]
p={'duration':52,'fps':30,'shots':[],'connections':[]}
for ident,a,b,intent,ts,action,camera in shots:
    d={'id':ident,'start':a,'end':b,'intent':intent,'states':dict(zip(['establish','action','result'],ts)),'action':action,'camera':camera}
    if ident=='two-paths':d['risks']=[[24.2,24.7],[25.3,25.8],[28.3,29.3]]
    if ident=='phase':d['risks']=[[34.1,34.6],[36.7,38.6]]
    if ident=='ridges':d['risks']=[[16.8,18.4]]
    p['shots'].append(d)
for t,kind,anchor in [(7,'magnification cut','蓝色纹理和翅面→鳞片尺度'),(14,'direction match cut','脊线从左下到右上；同一青蓝材质'),(22,'section cut','相同层架，但明确改成可读剖面'),(32,'semantic cut','两路反射→两条波形，蓝/青颜色身份'),(41,'result-to-system cut','蓝色叠加结果→许多细脊反射场'),(47,'return cut','同一片蓝色，完成尺度回收')]:
    p['connections'].append({'time':t,'kind':kind,'anchor':anchor,'window':[t-.2,t+.4]})
(R/'shot-plan.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8')
ledger={'generated_by':'built-in image_gen.imagegen','assets':[],'science_sources':['https://www.nhm.ac.uk/discover/spotlight-blue-morpho.html'],'rights':'Generated concepts used for this original film; no third-party reference imagery/music appears in film. Three.js MIT runtime. System font rasterization. Original synthetic audio.'}
for f,purpose in [('wing-concept.png','Opening and return; crop push, no fake 3D rotation'),('scales-concept.png','Scale hierarchy and directional match to 3D')]:
    im=R/'assets'/f;ledger['assets'].append({'file':'assets/'+f,'sha256':hashlib.sha256(im.read_bytes()).hexdigest(),'truth':'AI concept, not SEM or real observation','lighting':'cool grazing upper left','perspective':'near normal, diagonal ridges','permitted_motion':'crop translation/modest zoom only','purpose':purpose})
(R/'asset-ledger.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2),encoding='utf-8')
print('Plan and asset ledger saved')
