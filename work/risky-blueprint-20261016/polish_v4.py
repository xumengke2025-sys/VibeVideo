from pathlib import Path
r=Path(__file__).resolve().parent
p=r/'v4/scene-body.js';s=p.read_text(encoding='utf-8')
s=s.replace('[30,5940,1000,.73],[32,5940,900,.8],[34,5940,970,.78],[36,5950,1250,.73]', '[30,5940,1120,.70],[32,5940,1180,.70],[34,5940,1230,.72],[36,5950,1270,.73]')
s=s.replace('if(T<39)goldLine','if(T<30)goldLine')
s=s.replace('z*550','z*260')
s=s.replace("if(T>=30&&T<34){const z=", "if(T>=30&&T<34){const previousVisibility=visibility;visibility*=ease(p(T,30,30.4))*(1-ease(p(T,33.4,34)));const z=")
s=s.replace('detail(-75,-270+z*260,150,3);}', 'detail(-75,-270+z*260,150,3);visibility=previousVisibility;}')
s=s.replace('mix(340,163,close)','mix(340,169,close)')
s=s.replace("TX('快照 S-001',0,-405,29,1,{align:'center',v:.6});", "TX('快照 S-001',0,-405,29,1,{align:'center',v:.6});panel(-165,-275,490,100,1,.45,12);L([[-236,-175],[-165,-175],[-165,-225]],1,2,.5);")
s=s.replace('y=mix(2780,2875,h)','y=mix(2800,2875,h)')
p.write_text(s,encoding='utf-8')
print('Polished knowledge framing, physical hypothesis sockets, exact clamp contact')
