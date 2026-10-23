"""Alpine architecture assets, independent of the timeline and shared-world layout.

Usage inside Blender: import craft as C; C.palette(); import architecture_assets as A;
roots = A.build_variants(). All roots have local ground origin, entrance toward -Y.
Run this file directly to save an editable asset library and two portrait studies.
"""
import bpy, math, random, sys, os, json, time
from pathlib import Path
from mathutils import Vector, Matrix
from mathutils.noise import noise_vector
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'src'))
import craft as C
TAU=math.tau

def materials():
    global CU, EN, BLUE, SHOP, AMBER
    CU=C.material('ARCH | aged copper roof',(.10,.25,.22),.55,.68)
    EN=C.material('ARCH | ivory enamel clock',(.73,.69,.55),.32)
    BLUE=C.material('ARCH | blued steel hands',(.021,.034,.046),.30,.75)
    SHOP=C.material('ARCH | shop window interior',(.40,.25,.12),.76,emission=.12)
    AMBER=C.material('ARCH | amber glass jars',(.33,.12,.025),.24)

def finish(mesh,name,parent,bevel=.012):
    if mesh.v:return mesh.obj(name,parent,bevel)

def cuts_for(x0,x1,z,holes):
    cuts=[(x0,x1)]
    for x,zc,w,h in holes:
        if not zc-h/2 < z < zc+h/2:continue
        nc=[]
        for a,b in cuts:
            lo=x-w/2;hi=x+w/2
            if b<=lo or a>=hi:nc.append((a,b));continue
            if a<lo:nc.append((a,lo))
            if b>hi:nc.append((hi,b))
        cuts=nc
    return cuts

def facade(name,parent,w,y,z0,h,holes,kind='stone',seed=21):
    """Wall shell with actual apertures, not glass pasted onto a solid cuboid."""
    rng=random.Random(seed);m=C.Mesh();detail=C.Mesh()
    # Thin mortar/plaster strips exactly preserve the rectangular openings.
    step=.075 if kind=='stone' else .18
    for j in range(math.ceil(h/step)):
        z=z0+min(h,(j+.5)*step)
        for a,b in cuts_for(-w/2,w/2,z,holes):
            if b-a<.005:continue
            m.box(((a+b)/2,y+.065,z),(b-a,.18,step*.96),C.MO if kind=='stone' else C.WO,wood=kind!='stone',seed=seed+j)
    if kind=='stone':
        for j in range(math.ceil(h/.27)):
            z=z0+(j+.5)*.27;x=-w/2
            while x<w/2-.02:
                ww=min(rng.uniform(.38,.75),w/2-x);cx=x+ww/2
                if not any(abs(cx-ox)<ow/2+ww*.46 and abs(z-oz)<oh/2+.125 for ox,oz,ow,oh in holes):
                    detail.box((cx,y-.025+rng.uniform(-.018,.018),z),(ww-.026,.22,.25),C.ST,jitter=.012,seed=seed+j*100+int((x+w)*20))
                x+=ww
    else:
        for x in [-w/2+.08,w/2-.08]:detail.box((x,y-.045,z0+h/2),(.18,.22,h+.12),C.DK,wood=True)
        for z in [z0+.04,z0+h-.06]:detail.box((0,y-.06,z),(w+.13,.24,.15),C.DK,wood=True)
    finish(m,name+' | wall skin with openings',parent,.008)
    finish(detail,name+' | individually dressed stones' if kind=='stone' else name+' | structural timber',parent,.012)

def shell(name,parent,w,d,base,upper,front_holes,upper_holes,side=True,seed=51):
    fy=-d/2
    facade(name+' front masonry',parent,w,fy,0,base,front_holes,'stone',seed)
    if upper:facade(name+' front planking',parent,w,fy,base,upper,upper_holes,'wood',seed+1)
    m=C.Mesh();m.box((0,d/2-.08,base/2),(w,.22,base),C.ST)
    if upper:
        for i in range(math.ceil(upper/.18)):
            m.box((0,d/2,base+(i+.5)*.18),(w,.14,.169),C.WO,wood=True,seed=i+seed)
    # Interior volume is recessed farther than the glazing; the openings have depth.
    m.box((0,0,(base+upper)/2),(max(.2,w-.8),max(.2,d-.8),base+upper-.1),C.DK)
    finish(m,name+' rear and dark recessed interior',parent,.009)
    for sign in [-1,1]:
        wall=C.root(name+' side '+str(sign),(sign*w/2,0,0),parent);wall.rotation_euler.z=sign*math.pi/2
        xs=[-d*.22,d*.22] if d>4 else [0]
        ph=[(x,1.4,.75,1.1) for x in xs] if side else []
        uh=[(x,base+upper*.54,.83,1.23) for x in xs] if side and upper else []
        facade(name+' side masonry',wall,d,0,0,base,ph,'stone',seed+sign+6)
        if upper:facade(name+' side planks',wall,d,0,base,upper,uh,'wood',seed+sign+8)
        wm=C.Mesh()
        for x,z,ww,hh in ph+uh:C.window(wm,x,-.14,z,ww,hh,upper and z>base)
        finish(wm,name+' side recessed windows',wall,.008)
    return fy

def windows(parent,name,holes,y,shutters=True):
    m=C.Mesh()
    for x,z,w,h in holes:
        C.window(m,x,y-.14,z,w,h,shutters)
        C.drift(name+' | patch of sill snow',(x-w/2-.13,x+w/2+.13),(y-.48,y-.22),lambda a,b,z=z,h=h,x=x:z-h/2-.042+.035*math.cos((a-x)*3),parent,.12)
    finish(m,name+' | deep window joinery',parent,.008)

def door(parent,name,x,y,w=1.0,h=2.15):
    m=C.Mesh();m.box((x,y+.07,h/2),(w,.12,h),C.DK,wood=True)
    for i in range(7):m.box((x-w*.43+i*w*.143,y-.01,h*.47),(w*.134,.07,h*.93),C.WO,wood=True,seed=i+52)
    for sign in [-1,1]:m.box((x+sign*(w/2+.10),y-.03,h/2),(.16,.27,h+.15),C.ST)
    m.box((x,y-.04,h+.06),(w+.36,.29,.20),C.ST)
    for z in [.44,1.38]:m.box((x,y-.065,z),(w*.92,.04,.06),C.IR)
    m.torus((x+w*.31,y-.13,1.05),.055,.01,C.BR,Matrix.Rotation(math.pi/2,3,'X'),24)
    m.box((x,y-.27,.04),(w+.55,.7,.13),C.ST)
    finish(m,name+' | oak door and stone surround',parent,.01)

def gable_roof(parent,name,w,d,eave,rise,seed=21,over=.40,material=None,chimney=True):
    rng=random.Random(seed);wood=C.Mesh();roof=C.Mesh();ice=C.Mesh();half=w/2+over;end=d/2+.42
    slope=rise/(w/2);angle=math.atan(slope);ridge=eave+rise
    for y in [-d/2,d/2]:
        count=math.ceil(w/.20)
        for j in range(count):
            x=-w/2+(j+.5)*w/count;top=eave+rise*(1-abs(x)/(w/2))
            # A real loft aperture breaks the broad front gable and gives it scale.
            zlo=eave+.38;zhi=eave+1.47
            if rise>=1.8 and y<0 and abs(x)<.39 and top>zlo:
                wood.box((x,y,(eave+zlo)/2),(w/count-.011,.14,zlo-eave),C.WO,wood=True,seed=seed+j)
                if top>zhi:wood.box((x,y,(zhi+top)/2),(w/count-.011,.14,top-zhi),C.WO,wood=True,seed=seed+j)
            else:wood.box((x,y,(eave+top)/2),(w/count-.011,.14,top-eave),C.WO,wood=True,seed=seed+j)
        for s in [-1,1]:wood.beam((0,y-.06,ridge),(s*half,y-.06,ridge-half*slope),.16,.20,C.DK)
        if y>0:wood.box((0,y-.09,eave+rise*.42),(.15,.2,rise*.86),C.DK,wood=True)
    if rise>=1.8:C.window(wood,0,-d/2-.13,eave+.93,.77,1.08,False)
    nr=math.ceil(half/.28);nc=math.ceil(end*2/.31)
    for s in [-1,1]:
        for j in range(math.ceil(end*2/.8)+1):
            y=-end+j*.8;wood.beam((0,y,ridge-.11),(s*half,y,ridge-half*slope-.12),.12,.15,C.DK)
        for row in range(nr):
            x=s*(row+.5)*half/nr;z=ridge-abs(x)*slope
            for col in range(nc):
                y=-end+(col+.5+(row%2)*.5)*(end*2/nc)
                if y>end:continue
                roof.box((x,y,z),(.36,end*2/nc-.012,.04),C.SL if material is None else material,Matrix.Rotation(s*angle,3,'Y'),jitter=.005,seed=row*40+col)
        def height(x,y):
            edge=max(0,min(1,(half-abs(x))/.23,(end-abs(y))/.21));n=noise_vector(Vector((x*.8,y*.85,seed*.1))).x
            return ridge-abs(x)*slope+.08+edge*(.16+.09*n+.045*math.sin(y*2.1))
        C.drift(name+' | variable wind-set snow',(-half,0) if s<0 else (0,half),(-end,end),height,parent,.15)
        for j in range(9):
            y=rng.uniform(-end+.2,end-.2);z=ridge-half*slope+.07;length=rng.uniform(.06,.26)
            ice.rod((s*half,y,z),(s*half,y,z-length),rng.uniform(.013,.026),C.IC,10,.001)
    finish(wood,name+' | gables, bargeboards and rafters',parent,.009)
    finish(roof,name+' | overlapping slate',parent,.007);finish(ice,name+' | uneven icicles',parent,.004)
    if chimney:
        x=w*.24;y=d*.18;z=ridge-abs(x)*slope
        chimney_asset(parent,name,x,y,z,.58,.67,1.5)
    return ridge

def hipped_roof(parent,name,w,d,eave,rise,seed=34):
    """Low four-sided hipped roof, distinct from the taller front-gabled houses."""
    hw=w/2+.40;hd=d/2+.40;rh=w*.19;m=C.Mesh();rafters=C.Mesh()
    v=[(-hw,-hd,eave),(hw,-hd,eave),(hw,hd,eave),(-hw,hd,eave),(-rh,0,eave+rise),(rh,0,eave+rise)]
    m.add(v,[(0,1,5,4),(1,2,5),(2,3,4,5),(3,0,4)],C.SL)
    for a,b in [(0,4),(1,5),(2,5),(3,4),(4,5)]:rafters.beam(v[a],v[b],.13,.14,C.DK)
    for a,b in [(0,1),(1,2),(2,3),(3,0)]:rafters.beam(v[a],v[b],.16,.18,C.DK)
    def height(x,y):
        t=max(abs(y)/hd,max(0,(abs(x)-rh)/(hw-rh)))
        edge=max(0,min(1,(hw-abs(x))/.19,(hd-abs(y))/.19))
        return eave+rise*(1-t)+.07+edge*(.16+.055*noise_vector(Vector((x,y,seed))).x)
    C.drift(name+' | broad hipped snow cap',(-hw,hw),(-hd,hd),height,parent,.12)
    finish(m,name+' | four-sided slate roof',parent,.01);finish(rafters,name+' | hipped roof framing',parent,.009)
    chimney_asset(parent,name,-w*.27,d*.10,height(-w*.27,d*.10),.58,.66,1.1)

def chimney_asset(parent,name,x,y,z,w,d,h):
    m=C.Mesh();m.box((x,y,z+h*.40),(w,d,h),C.ST)
    for j in range(math.ceil(h/.25)):m.box((x,y,z-.10+j*.25),(w+.012,d+.012,.025),C.MO)
    m.box((x,y,z+h*.9),(w+.22,d+.22,.14),C.ST)
    m.box((x,y,z+h*.9+.09),(w*.68,d*.7,.04),C.IR)
    m.box((x,y,z+h*.9+.13),(w+.20,d+.20,.09),C.SN)
    finish(m,name+' | capped stone chimney',parent,.015)

def balcony(parent,name,x,y,z,w,depth=1.0):
    m=C.Mesh()
    for j in range(math.ceil(w/.22)):
        m.box((x-w/2+(j+.5)*.22,y-depth/2,z),(.211,depth,.11),C.WO,wood=True,seed=j+30)
    for xx in [x-w/2+.10,x,x+w/2-.10]:
        m.beam((xx,y+.06,z-.80),(xx,y-depth+.1,z-.02),.14,.14,C.DK)
        m.box((xx,y-depth+.05,z+.51),(.11,.11,1.06),C.DK,wood=True)
        m.ellipsoid((xx,y-depth+.05,z+1.07),(.075,.075,.045),C.WO,16,8)
    for j in range(math.ceil(w/.22)-1):
        xx=x-w/2+.22+j*.22
        # Shaped flat balusters, a strong Alpine silhouette in oblique shots.
        profile=[(-.06,0),(.06,0),(.06,.11),(.027,.20),(.05,.33),(.028,.46),(.061,.69),(-.061,.69),(-.028,.46),(-.05,.33),(-.027,.20),(-.06,.11)]
        v=[(xx+a,y-depth+b,z+.18+c) for b in [-.035,.035] for a,c in profile];n=len(profile)
        m.add(v,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],C.WO)
    for zz in [z+.14,z+.92]:m.box((x,y-depth,zz),(w+.10,.15,.11),C.DK,wood=True)
    for sx in [-1,1]:
        for zz in [z+.14,z+.92]:m.box((x+sx*w/2,y-depth/2,zz),(.12,depth,.10),C.DK,wood=True)
    finish(m,name+' | shaped balcony and corbels',parent,.008)

def hanging_sign(parent,name,x,y,z,body,icon=False):
    m=C.Mesh();m.box((x,y,z),(1.38,.13,.50),C.DK,wood=True)
    for xx in [x-.57,x+.57]:m.rod((xx,y,z+.24),(xx,y,z+.53),.014,C.IR,12)
    m.box((x,y+.16,z+.55),(1.72,.16,.10),C.DK,wood=True)
    finish(m,name+' | carved shop sign',parent,.008)
    C.lettering(body,(x,y-.075,z-.07),.17,C.BR,parent)

def build_inn():
    name='ARCH_INN';r=C.root(name);w=6.7;d=5.4;base=2.65;upper=2.7
    holes=[(-2.0,1.38,1.20,1.28),(0,1.08,1.1,2.16),(2.0,1.38,1.20,1.28)]
    uh=[(x,4.05,1.05,1.35) for x in [-2.15,0,2.15]]
    fy=shell(name,r,w,d,base,upper,holes,uh,True,67)
    windows(r,name,[q for q in holes if q[0]],fy,False);windows(r,name,uh,fy)
    door(r,name,0,fy-.11,1.05);balcony(r,name,0,fy-.05,2.96,6.3,1.1)
    gable_roof(r,name,w,d,5.36,2.58,71)
    # Offset low stone stable wing with its own long roof; no scaled chalet reuse.
    wing=C.root(name+' | stable wing',(4.1,.85,0),r)
    shell(name+' stable',wing,2.8,4.5,2.25,0,[(0,1.0,1.65,2.0)],[],False,127)
    door(wing,name+' stable',0,-2.36,1.65,1.99)
    gable_roof(wing,name+' stable',2.8,4.5,2.28,1.25,52,chimney=False)
    # Front covered porch over the doorway only, supported beside its passage.
    m=C.Mesh()
    for x in [-.92,.92]:
        m.box((x,fy-1.28,1.35),(.16,.16,2.70),C.DK,wood=True)
        m.beam((x,fy-1.28,2.18),(x*.48,fy-1.28,2.62),.10,.10,C.DK)
    finish(m,name+' | porch uprights',r,.01)
    hanging_sign(r,name,-2.1,fy-.28,2.48,'AUBERGE')
    C.lantern((.77,fy-.25,2.26),r)
    r['footprint_m']=[9.85,7.1];r['height_m']=8.4;r['entrance']='-Y'
    return r

def clock_face(parent,name,p,radius=.85,rotation=0):
    dial=C.root(name,p,parent);dial.rotation_euler.z=rotation;m=C.Mesh();rot=Matrix.Rotation(math.pi/2,3,'X')
    m.rod((0,.02,0),(0,-.055,0),radius,C.EN if hasattr(C,'EN') else EN,96)
    for rr,thick in [(radius+.06,.045),(radius-.06,.012)]:m.torus((0,-.08,0),rr,thick,C.BR,rot,96)
    for j in range(60):
        a=j*TAU/60;ri=radius*(.84 if j%5==0 else .90);ro=radius*.95
        m.beam((math.sin(a)*ri,-.092,math.cos(a)*ri),(math.sin(a)*ro,-.092,math.cos(a)*ro),.018 if j%5==0 else .008,.012,BLUE)
    finish(m,name+' | enamel dial and minute ring',dial,.004)
    numerals=['XII','I','II','III','IV','V','VI','VII','VIII','IX','X','XI']
    for j,s in enumerate(numerals):
        a=j*TAU/12;C.lettering(s,(math.sin(a)*radius*.69,-.105,math.cos(a)*radius*.69-radius*.065),radius*.15,BLUE,dial)
    for typ,length,width,angle in [('hour',radius*.43,.042,-2*math.pi/3),('minute',radius*.67,.028,0)]:
        hand=C.root(name+' | '+typ+' hand',(0,-.14,0),dial);hand.rotation_euler.y=angle;hm=C.Mesh()
        hm.beam((0,0,-length*.14),(0,0,length),width,.035,BLUE);hm.ellipsoid((0,0,length*.76),(width*.85,.019,width*1.7),BLUE)
        hm.obj(name+' | '+typ+' pointer',hand,.005)
    pin=C.Mesh();pin.rod((0,-.12,0),(0,-.19,0),radius*.06,C.BR,24);pin.obj(name+' | spindle',dial,.004)
    return dial

def build_workshop():
    name='ARCH_WORKSHOP';r=C.root(name);w=4.6;d=5.2;base=2.7;upper=2.65;fy=-d/2
    holes=[(-.9,1.42,2.0,1.55),(1.5,1.07,.9,2.14)];uh=[(-1.25,4.10,.9,1.40),(1.25,4.10,.9,1.40)]
    shell(name,r,w,d,base,upper,holes,uh,True,72)
    # Glazed bay projects from stone, with watches and clocks within the recess.
    bay=C.Mesh();bay.box((-.9,fy-.12,.62),(2.22,.57,.17),C.ST)
    bay.box((-.9,fy-.12,2.27),(2.23,.58,.13),C.DK,wood=True)
    bay.box((-.9,fy+.12,1.43),(1.97,.03,1.43),SHOP)
    for x in [-1.94,-.9,.14]:bay.box((x,fy-.34,1.43),(.065,.08,1.57),C.DK,wood=True)
    for z in [.69,1.38,2.19]:bay.box((-.9,fy-.34,z),(2.08,.09,.055),C.WO,wood=True)
    bay.box((-.9,fy-.08,1.36),(2.04,.50,.065),C.WO,wood=True)
    for j in range(3):
        x=-1.60+j*.69
        bay.box((x,fy-.01,.86),(.31,.23,.31),C.DK,wood=True)
        bay.box((x,fy-.01,1.47),(.32,.24,.11),C.DK,wood=True)
    finish(bay,name+' | projecting watch display bay',r,.008)
    for j in range(3):clock_face(r,name+' | display clock '+str(j),(-1.60+j*.69,fy-.16,1.10),.19)
    for j in range(2):clock_face(r,name+' | display pocket watch '+str(j),(-1.35+j*.9,fy-.12,1.80),.16)
    door(r,name,1.49,fy-.1,.86);windows(r,name,uh,fy,True)
    gable_roof(r,name,w,d,5.36,2.66,53)
    # Side stair up to the craftsman's loft, on building footprint, not carriage street.
    m=C.Mesh()
    for i in range(14):m.box((w/2+.49,1.8-i*.26,(i+1)*.195/2),(1.03,.30,(i+1)*.195),C.ST,jitter=.008,seed=i)
    for i in [0,5,10,13]:m.rod((w/2+1.0,1.8-i*.26,(i+1)*.195),(w/2+1.0,1.8-i*.26,(i+1)*.195+.86),.026,C.IR)
    m.rod((w/2+1.0,1.8,1.05),(w/2+1.0,1.8-13*.26,3.59),.025,C.IR)
    finish(m,name+' | external loft stair',r,.012)
    hanging_sign(r,name,-.90,fy-.28,2.56,'HORLOGER')
    C.lantern((2.02,fy-.20,2.25),r)
    r['footprint_m']=[5.9,6.1];r['height_m']=8.4;r['entrance']='-Y'
    return r

def build_grocer():
    name='ARCH_GROCER';r=C.root(name);w=5.7;d=4.7;base=2.48;upper=2.0;fy=-d/2
    holes=[(-1.55,1.3,1.6,1.40),(.65,1.02,.92,2.04),(2.03,1.3,.70,1.10)]
    uh=[(-1.75,3.46,.85,1.13),(.15,3.46,.85,1.13),(1.95,3.46,.70,1.13)]
    shell(name,r,w,d,base,upper,holes,uh,True,39)
    windows(r,name,[holes[0],holes[2]],fy,False);windows(r,name,uh,fy)
    door(r,name,.65,fy-.10,.88,2.04)
    hipped_roof(r,name,w,d,4.50,1.72,82)
    # Independent shop canopy: heavy timber rafters, restrained canvas strip.
    m=C.Mesh()
    for x in [-2.48,2.48]:
        m.box((x,fy-1.15,1.12),(.115,.115,2.24),C.DK,wood=True)
        m.beam((x,fy,2.45),(x,fy-1.20,2.21),.09,.10,C.DK)
    m.box((0,fy-1.19,2.21),(5.12,.14,.15),C.DK,wood=True)
    for j in range(17):
        x=-2.50+(j+.5)*5/17
        m.add([(x-.145,fy-.05,2.53),(x+.145,fy-.05,2.53),(x+.145,fy-1.25,2.25),(x-.145,fy-1.25,2.25)],[(0,1,2,3)],C.GR if j%2 else C.CL)
    # Low open produce crates, earthenware and firewood under the awning.
    for k,x in enumerate([-1.8,-.65,1.85]):
        y=fy-.60
        m.box((x,y,.20),(.85,.66,.10),C.DK,wood=True)
        for sy in [-1,1]:m.box((x,y+sy*.32,.34),(.88,.06,.27),C.WO,wood=True)
        for sx in [-1,1]:m.box((x+sx*.43,y,.34),(.06,.63,.27),C.WO,wood=True)
        for j in range(7):m.ellipsoid((x-.28+(j%3)*.27,y-.17+(j//3)*.16,.43),(.11,.09,.10),C.BD if k==0 else C.GR,16,8)
    finish(m,name+' | awning and market crates',r,.009)
    hanging_sign(r,name,0,fy-.22,2.72,'EPICERIE')
    r['footprint_m']=[6.5,6.2];r['height_m']=7.1;r['entrance']='-Y'
    return r

def build_cottage():
    name='ARCH_COTTAGE';r=C.root(name);w=4.25;d=4.6;fy=-d/2
    holes=[(-1.12,1.23,1.02,1.15),(1.12,1.01,.88,2.02)];uh=[(-1.12,3.40,.92,1.20),(1.12,3.4,.92,1.20)]
    shell(name,r,w,d,2.25,2.35,holes,uh,True,113)
    windows(r,name,[holes[0]],fy,True);windows(r,name,uh,fy,True);door(r,name,1.12,fy-.1,.86,2.02)
    balcony(r,name,-.70,fy-.04,2.48,2.63,.80)
    gable_roof(r,name,w,d,4.6,2.50,111)
    # Timber lean-to storage shed and sloping roof on the back/side.
    m=C.Mesh()
    for i in range(9):m.box((-2.68,.5,.12+i*.19),(1.1,3.2,.178),C.WO,wood=True,seed=i+21)
    for i in range(9):m.box((-2.68,-1.1,.12+i*.19),(1.1,.14,.178),C.WO,wood=True,seed=i+21)
    for i in range(7):m.rod((-3.25,-.89+i*.25,.16),(-2.2,-.89+i*.25,.16),.11,C.WO,12)
    finish(m,name+' | timber woodshed',r,.01)
    C.drift(name+' | shed snow',(-3.35,-2.0),(-1.25,2.25),lambda x,y:1.90+(x+3.35)*.45+.04*math.sin(y*2),r,.13)
    r['footprint_m']=[6.0,5.6];r['height_m']=7.7;r['entrance']='-Y'
    return r

def arch_window(parent,name,x,y,z,w,h):
    m=C.Mesh();rad=w/2;spring=z+h/2-rad
    # Front plane dark inset plus warm leaded panes, framed by voussoirs.
    m.box((x,y+.10,z-rad*.25),(w,.035,h-rad*.5),C.GL)
    for s in [-1,1]:m.box((x+s*(rad+.10),y,z-rad*.22),(.18,.23,h-rad*.44),C.ST)
    for j in range(13):
        a=math.pi*j/12
        cx=x+math.cos(a)*(rad+.10);cz=spring+math.sin(a)*(rad+.10)
        m.box((cx,y,cz),(.23,.25,.20),C.ST,Matrix.Rotation(-a,3,'Y'),jitter=.004,seed=j)
    m.box((x,y-.05,z-.05),(.035,.06,h-.05),C.IR)
    for zz in [z-h*.25,z,z+h*.25]:m.box((x,y-.05,zz),(w,.06,.027),C.IR)
    m.box((x,y-.04,z-h/2-.09),(w+.30,.40,.13),C.ST)
    finish(m,name+' | arched leaded light',parent,.008)

def build_chapel():
    name='ARCH_CHAPEL';r=C.root(name);w=4.9;d=8.4;eave=5.1;fy=-d/2
    facade(name+' entrance',r,w,fy,0,eave,[(0,1.32,1.55,2.64),(0,3.81,1.15,1.40)],'stone',87)
    m=C.Mesh();m.box((0,d/2-.06,2.55),(w,.28,5.1),C.ST);m.box((0,0,2.45),(w-.8,d-.8,4.8),C.DK)
    finish(m,name+' | nave interior and rear',r,.014)
    for s in [-1,1]:
        wall=C.root(name+' | aisle side '+str(s),(s*w/2,0,0),r);wall.rotation_euler.z=s*math.pi/2
        holes=[(x,2.85,1.05,2.30) for x in [-2.8,0,2.8]]
        facade(name+' long side',wall,d,0,0,eave,holes,'stone',98+s)
        for x,z,ww,hh in holes:arch_window(wall,name+' side window',x,-.13,z,ww,hh)
        butt=C.Mesh()
        for yy in [-4.05,-1.45,1.45,4.05]:
            butt.box((s*(w/2+.21),yy,1.8),(.44,.46,3.6),C.ST)
            butt.box((s*(w/2+.32),yy,.4),(.66,.68,.8),C.ST)
            butt.box((s*(w/2+.20),yy,3.68),(.49,.52,.16),C.SN)
        finish(butt,name+' | stone buttresses',r,.018)
    door(r,name,0,fy-.12,1.47,2.60);arch_window(r,name+' choir light',0,fy-.14,3.81,1.15,1.4)
    # The nave roof is longer and narrower than a dwelling, with a copper finial.
    gable_roof(r,name,w,d,eave,2.76,36,over=.28,chimney=False)
    m=C.Mesh();m.rod((0,fy-.1,7.86),(0,fy-.1,8.55),.032,C.BR)
    m.rod((-.20,fy-.1,8.33),(.20,fy-.1,8.33),.025,C.BR)
    for j in range(3):m.box((0,fy-.44-j*.33,.07-j*.04),(2.45+j*.22,.70,.15),C.ST)
    finish(m,name+' | cross and entrance steps',r,.01)
    r['footprint_m']=[6.0,9.7];r['height_m']=8.55;r['entrance']='-Y'
    return r

def lathe(mesh,profile,ma,n=64):
    v=[(rad*math.cos(i*TAU/n),rad*math.sin(i*TAU/n),z) for rad,z in profile for i in range(n)]
    mesh.add(v,[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(len(profile)-1) for i in range(n)],ma,smooth=True)

def build_tower():
    name='ARCH_TOWER';r=C.root(name);m=C.Mesh();stone=C.Mesh();trim=C.Mesh();w=3.8;fy=-w/2
    # Tall narrowing masonry shaft with hand-dressed quoins and deep lower openings.
    for face in range(4):
        fr=C.root(name+' | shaft face '+str(face),(0,0,0),r);fr.rotation_euler.z=face*math.pi/2
        holes=[(0,1.20,1.10,2.40)] if face==0 else [(0,3.60,.48,1.30)]
        facade(name+' lower shaft',fr,w,fy,0,7.5,holes,'stone',face+85)
        if face==0:door(fr,name,0,fy-.10,1.03,2.36)
        else:windows(fr,name,holes,fy,False)
        # Cream lime infill behind the clock keeps the dial clean at a distance.
        mm=C.Mesh();mm.box((0,fy+.04,9.67),(w,.22,4.35),C.PL)
        for x in [-1.79,1.79]:
            for j in range(15):mm.box((x,fy-.06,7.64+j*.28),(.25 if j%2 else .42,.27,.265),C.ST)
        mm.obj(name+' | upper lime and quoins',fr,.012)
        clock_face(fr,name+' | clock '+str(face),(0,fy-.17,10.45),1.18)
    m.box((0,0,6.5),(3.3,3.3,13.0),C.DK)
    # Dark core stops below the open belfry.
    m.v=[];m.f=[];m.mi=[];m.uv=[];m.sm=[]
    m.box((0,0,5.9),(3.31,3.31,11.8),C.DK)
    for z,ww,th in [(.20,4.12,.40),(7.45,4.02,.22),(11.86,4.24,.28),(12.14,4.05,.23),(14.95,4.25,.25)]:
        stone.box((0,0,z),(ww,ww,th),C.ST)
        if z>7:stone.box((0,0,z+th/2+.035),(ww+.05,ww+.05,.07),C.SN)
    for x in [-1.67,1.67]:
        for y in [-1.67,1.67]:
            stone.box((x,y,13.55),(.40,.40,2.7),C.ST)
            trim.box((x,y,12.40),(.53,.53,.18),C.ST)
            trim.box((x,y,14.77),(.53,.53,.22),C.ST)
    # Belfry oak crossbeam supports a bronze bell with a real hollow mouth.
    trim.box((0,0,14.55),(3.48,.34,.31),C.DK,wood=True)
    trim.rod((-.25,0,14.52),(.25,0,14.52),.095,C.IR,32)
    trim.box((-1.50,0,13.90),(.14,3.38,.17),C.DK,wood=True)
    for y in [-.22,.22]:
        trim.box((-1.50,y,13.90),(.22,.06,.24),C.IR)
        trim.rod((-1.50,y-.05,13.90),(-1.50,y+.05,13.90),.084,C.BR,24)
    bell=C.root(name+' | BELL',(0,0,13.12),r);bm=C.Mesh()
    profile=[(.08,1.32),(.19,1.25),(.25,1.03),(.29,.75),(.37,.44),(.52,.19),(.64,.08),(.67,0),(.57,-.015),(.53,.12),(.40,.32),(.28,.63),(.22,1.02),(.08,1.15)]
    lathe(bm,profile,C.BR,96)
    for rad,z in [(.635,.04),(.50,.22),(.26,.88)]:bm.torus((0,0,z),rad,.018,C.BR,n=64)
    bm.rod((0,0,.85),(0,0,-.08),.034,C.IR,16);bm.ellipsoid((0,0,-.03),(.09,.09,.11),C.BR,24,12)
    bm.obj(name+' | cast bell with lip and clapper',bell,.005)
    pivot=C.root(name+' | HAMMER_PIVOT',(-1.50,0,13.90),r);hm=C.Mesh()
    hm.rod((0,0,0),(.78,0,-.68),.041,C.IR,20);hm.ellipsoid((.78,0,-.68),(.115,.14,.11),C.BR,32,16)
    hm.rod((0,-.19,0),(0,.19,0),.075,C.BR,24);hm.obj(name+' | bell striking hammer',pivot,.006);pivot.rotation_euler.y=.32
    pivot['rest_y_rad']=.32;pivot['contact_y_rad']=0.0;pivot['contact_local_head']=[.78,0,-.68]
    # Architectural spire: square copper bell roof, then an eight-sided taper.
    roof=C.Mesh()
    verts=[(-2.35,-2.35,15.08),(2.35,-2.35,15.08),(2.35,2.35,15.08),(-2.35,2.35,15.08),(-1.10,-1.10,16.08),(1.10,-1.10,16.08),(1.10,1.10,16.08),(-1.10,1.10,16.08)]
    roof.add(verts,[(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],CU)
    # Copper ribs follow panel seams and carry restrained snow at the eaves.
    for j in range(4):roof.beam(verts[j],verts[j+4],.045,.045,C.BR)
    roof.box((0,0,16.13),(2.35,2.35,.15),CU)
    for j in range(8):
        a=j*TAU/8+math.pi/8;b=(j+1)*TAU/8+math.pi/8
        p1=(math.cos(a)*1.30,math.sin(a)*1.30,16.18);p2=(math.cos(b)*1.30,math.sin(b)*1.30,16.18)
        roof.add([p1,p2,(0,0,18.05)],[(0,1,2)],CU)
        roof.rod(p1,(0,0,18.05),.022,C.BR,10)
    roof.rod((0,0,18.02),(0,0,18.59),.028,C.BR);roof.ellipsoid((0,0,18.18),(.105,.105,.105),C.BR)
    roof.rod((-.31,0,18.48),(.34,0,18.48),.018,C.BR)
    roof.add([(.34,0,18.48),(.12,0,18.60),(.12,0,18.36)],[(0,1,2)],C.BR)
    # Snow is asymmetric and only settles on the shallow shoulders.
    for s in [-1,1]:
        C.drift(name+' | belfry snow shoulder',(-2.31,2.31),(s*2.18-.10,s*2.18+.10),lambda x,y:15.19+.055*math.sin(x*2),r,.15)
    # Brass bird outside the lower clock on a real bracket and axle housing.
    bird=C.root(name+' | BIRD_BODY',(0,fy-.43,8.69),r);body=C.Mesh()
    body.ellipsoid((0,0,.13),(.17,.27,.17),C.BR,32,16)
    body.ellipsoid((0,-.20,.28),(.115,.125,.12),C.BR,32,16)
    body.rod((0,-.29,.27),(0,-.46,.25),.06,C.BR,16,.001)
    for s in [-1,1]:body.ellipsoid((s*.092,-.261,.305),(.019,.019,.019),BLUE,12,8)
    for j in range(5):body.rod((0,.15,.12),((j-2)*.045,.52,.17),.028,C.BR,12,.008)
    body.rod((-.13,0,-.08),(.13,0,-.08),.027,C.IR,16)
    body.obj(name+' | engraved mechanical bird body',bird,.005)
    for s,label in [(-1,'L'),(1,'R')]:
        wr=C.root(name+' | BIRD_WING_'+label,(s*.14,.02,.17),bird);wm=C.Mesh()
        wm.rod((0,-.10,0),(0,.10,0),.037,C.BR,16)
        wm.add([(0,-.10,0),(s*.28,-.12,.025),(s*.66,.13,-.05),(s*.42,.28,-.08),(0,.15,0)],[(0,1,2,3,4)],C.BR)
        for j in range(7):
            xx=s*(.17+j*.073);wm.rod((xx,-.08+j*.026,.005),(xx+s*.07,.22+j*.012,-.065),.026,C.BR,12,.010)
        wm.obj(name+' | articulated feather plates '+label,wr,.005);wr.rotation_euler.y=s*1.05
        wr['closed_y_rad']=s*1.05;wr['open_y_rad']=0.0
    trim.box((0,fy-.28,8.44),(1.55,.67,.12),C.ST)
    for x in [-.55,.55]:trim.beam((x,fy-.02,8.02),(x,fy-.54,8.38),.09,.10,C.IR)
    trim.box((0,fy-.07,8.69),(.42,.18,.40),C.DK,wood=True)
    finish(m,name+' | recessed shaft core',r,.01);finish(stone,name+' | cornices and belfry piers',r,.018)
    finish(trim,name+' | bell support and bird bracket',r,.01);finish(roof,name+' | patinated copper spire',r,.006)
    r['footprint_m']=[4.7,4.7];r['height_m']=18.6;r['entrance']='-Y'
    r['animation_parts']=json.dumps({'hammer':pivot.name,'bell':bell.name,'bird':bird.name,'wing_left':name+' | BIRD_WING_L','wing_right':name+' | BIRD_WING_R','hammer_contact_y':0.,'hammer_rest_y':.32})
    return r

def build_variants():
    if not C.M:raise RuntimeError('Call craft.palette() before building architecture assets')
    materials()
    return {'inn':build_inn(),'workshop':build_workshop(),'grocer':build_grocer(),'cottage':build_cottage(),'chapel':build_chapel(),'tower':build_tower()}

def _studio():
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    C.palette();assets=build_variants()
    # Asset library uses distinct ground-root assemblies; staging can be reset to 0.
    for key,p in {'inn':(-5.6,4.9,0),'workshop':(3.4,6.6,0),'grocer':(-5.3,-3.8,0),'cottage':(4.1,-3.1,0),'chapel':(22,3.2,0),'tower':(27.2,6.8,0)}.items():assets[key].location=p
    ground=C.Mesh();ground.box((7,4,-.18),(100,100,.3),C.SN);ground.obj('ARCH_STUDIO | continuous snow ground',None,.05)
    paving=C.Mesh();rng=random.Random(198)
    for row in range(28):
        y=-7.5+row*.28
        for col in range(67):
            x=-12+col*.35+(row%2)*.17
            paving.box((x,y,.025),(.33,.263,.09),C.ST,jitter=.008,seed=row*100+col)
    paving.obj('ARCH_STUDIO | setts',None,.014)
    world=bpy.data.worlds.new('ARCH_STUDIO | winter sky');world.use_nodes=True
    world.node_tree.nodes['Background'].inputs[0].default_value=(.36,.48,.68,1);world.node_tree.nodes['Background'].inputs[1].default_value=.40;bpy.context.scene.world=world
    def light(name,typ,p,e,color,target,size=1):
        ld=bpy.data.lights.new(name,typ);ld.energy=e;ld.color=color
        if typ=='AREA':ld.shape='DISK';ld.size=size
        else:ld.angle=.12
        ob=bpy.data.objects.new(name,ld);bpy.context.collection.objects.link(ob);ob.location=p;ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler()
    light('ARCH_STUDIO | winter dawn','SUN',(-15,-15,25),2.5,(1,.78,.53),(0,0,0))
    light('ARCH_STUDIO | sky reflection','AREA',(7,-8,25),1600,(.62,.76,1),(7,0,0),24)
    sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.samples=int(os.environ.get('ARCH_SAMPLES','64'));sc.cycles.use_denoising=True;sc.cycles.adaptive_threshold=.025;sc.cycles.max_bounces=7
    prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='OPTIX';prefs.get_devices()
    for device in prefs.devices:device.use=device.type=='OPTIX'
    sc.cycles.device='GPU';sc.cycles.seed=162;sc.cycles.use_animated_seed=False
    sc.render.resolution_x=1080;sc.render.resolution_y=1920;sc.render.resolution_percentage=int(os.environ.get('ARCH_SCALE','100'))
    sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGB';sc.render.fps=24;sc.render.threads_mode='FIXED';sc.render.threads=3
    sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=.65
    cd=bpy.data.cameras.new('ARCH_STUDIO | portrait asset camera');cam=bpy.data.objects.new('ARCH_STUDIO | portrait asset camera',cd);bpy.context.collection.objects.link(cam);sc.camera=cam
    def shot(p,target,lens):
        cam.location=p;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cd.lens=lens;cd.dof.use_dof=True;cd.dof.focus_distance=(Vector(target)-cam.location).length;cd.dof.aperture_fstop=14
    folder=R/'render/architecture-assets';folder.mkdir(parents=True,exist_ok=True)
    shot((26,-47,36),(-.7,1.0,3.2),63)
    bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(R/'model/architecture-library.blend'))
    sc.render.filepath=str(folder/'commercial-quarter.png');bpy.ops.render.render(write_still=True)
    shot((48,-36,31),(24.3,4.1,8.1),65)
    sc.render.filepath=str(folder/'chapel-clocktower.png');bpy.ops.render.render(write_still=True)
    # Additional closer mechanical view so hinge and hammer geometry are reviewable.
    bpy.data.objects['ARCH_TOWER | BIRD_WING_L'].rotation_euler.y=0
    bpy.data.objects['ARCH_TOWER | BIRD_WING_R'].rotation_euler.y=0
    bpy.data.objects['ARCH_TOWER | HAMMER_PIVOT'].rotation_euler.y=0
    shot((34.4,-7.8,16.8),(27.2,6.7,11.3),75)
    sc.render.filepath=str(folder/'clock-mechanism-detail.png');bpy.ops.render.render(write_still=True)
    report={'assets':{k:{'root':v.name,'height_m':v.get('height_m'),'footprint_m':list(v.get('footprint_m'))} for k,v in assets.items()},'render_size':[sc.render.resolution_x*sc.render.resolution_percentage//100,sc.render.resolution_y*sc.render.resolution_percentage//100],'samples':sc.cycles.samples,'source':'src/architecture_assets.py','model':'model/architecture-library.blend','tower_parts':json.loads(assets['tower']['animation_parts'])}
    (folder/'asset-manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    print('ARCHITECTURE_ASSETS_READY',flush=True)

if __name__=='__main__':_studio()
