"""Editable architectural assemblies for the replacement Alpine world.

All coordinates are metres. Meshes contain proper depth and bevels; surface
maps are CC0 Poly Haven scans, not a substitute for modeled construction.
"""
import bpy, math, random
from pathlib import Path
from mathutils import Vector, Matrix
from mathutils.noise import noise_vector
R=Path(__file__).resolve().parents[1]
TAU=math.tau
M=[]

def material(name, color, rough=.65, metal=0, emission=0, texture=None, tint=None):
    m=bpy.data.materials.new(name); m.use_nodes=True; m.diffuse_color=(*color,1)
    n=m.node_tree.nodes; l=m.node_tree.links; p=n.get('Principled BSDF')
    p.inputs['Base Color'].default_value=(*color,1); p.inputs['Roughness'].default_value=rough
    p.inputs['Metallic'].default_value=metal
    if emission:
        p.inputs['Emission Color'].default_value=(*color,1);p.inputs['Emission Strength'].default_value=emission
    if texture:
        folder=R/'assets/pbr'/texture
        for suffix,socket in [('diff','Base Color'),('rough','Roughness'),('nor_gl','Normal')]:
            candidates=list(folder.glob('*_'+suffix+'_2k.*'))
            if not candidates: continue
            t=n.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(candidates[0]),check_existing=True)
            if suffix!='diff':t.image.colorspace_settings.name='Non-Color'
            if suffix=='nor_gl':
                normal=n.new('ShaderNodeNormalMap');normal.inputs['Strength'].default_value=.5
                l.new(t.outputs['Color'],normal.inputs['Color']);l.new(normal.outputs[0],p.inputs['Normal'])
            elif suffix=='diff' and tint:
                mx=n.new('ShaderNodeMixRGB');mx.blend_type='MULTIPLY';mx.inputs[0].default_value=.72
                mx.inputs[2].default_value=(*tint,1);l.new(t.outputs[0],mx.inputs[1]);l.new(mx.outputs[0],p.inputs[socket])
            else:l.new(t.outputs[0],p.inputs[socket])
    else:
        tc=n.new('ShaderNodeTexCoord');noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=23
        noise.inputs['Detail'].default_value=3; l.new(tc.outputs['Object'],noise.inputs['Vector'])
        bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.12;bump.inputs['Distance'].default_value=.012
        l.new(noise.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs[0],p.inputs['Normal'])
    M.append(m);return len(M)-1

def palette():
    global SN, WO, DK, ST, SQ, MO, SL, BR, IR, GL, RD, GR, PL, IC, BD, BL, SK, CL, LE
    SN=material('Fresh settled snow',(.83,.88,.94),.79)
    p=M[SN].node_tree.nodes.get('Principled BSDF');p.inputs['Subsurface Weight'].default_value=.06
    WO=material('Larch | photographed grain',(.34,.16,.07),texture='weathered_brown_planks',tint=(1.35,.88,.58))
    DK=material('Old structural oak',(.12,.055,.027),texture='weathered_brown_planks',tint=(.43,.30,.22))
    ST=material('Hand dressed mountain stone',(.38,.40,.42),texture='old_stone_wall',tint=(.8,.86,.92))
    SQ=material('Dressed limestone blocks',(.31,.32,.30),.89)
    MO=material('Recessed lime mortar',(.24,.25,.25),.95)
    SL=material('Blue grey split slate',(.105,.15,.18),.76)
    BR=material('Old brass | satin patina',(.48,.29,.095),.34,.76)
    IR=material('Forged iron',(.045,.052,.056),.42,.7)
    GL=material('Warm interior behind glass',(.95,.54,.20),.45,emission=.7)
    RD=material('Oxblood cargo lacquer',(.22,.027,.034),texture='weathered_brown_planks',tint=(.85,.12,.16))
    GR=material('Oxidized green shutters',(.05,.16,.12),texture='weathered_brown_planks',tint=(.2,.61,.43))
    PL=material('Lime plaster',(.62,.59,.49),texture='plastered_stone_wall',tint=(1,.92,.78))
    IC=material('Transparent icicle',(.7,.82,.9),.16)
    M[IC].node_tree.nodes.get('Principled BSDF').inputs['Transmission Weight'].default_value=.8
    BD=material('Bread crust',(.49,.22,.057),.9)
    BL=material('Indigo wool',(.065,.10,.15),.95)
    SK=material('Painted warm skin',(.46,.25,.15),.83)
    CL=material('Undyed linen',(.64,.61,.51),.97)
    LE=material('Oiled leather',(.07,.036,.019),.59)

class Mesh:
    def __init__(self):self.v=[];self.f=[];self.mi=[];self.uv=[];self.sm=[]
    def add(self,v,f,ma,uv=None,smooth=False):
        k=len(self.v);self.v.extend(tuple(p) for p in v)
        for j,face in enumerate(f):
            self.f.append(tuple(k+i for i in face));self.mi.append(ma);self.sm.append(smooth)
            if uv:self.uv.append(uv[j])
            else:
                a,b,c=[Vector(v[i]) for i in face[:3]];normal=(b-a).cross(c-a)
                ax=max(range(3),key=lambda i:abs(normal[i]));ij=[(1,2),(0,2),(0,1)][ax]
                self.uv.append([(v[i][ij[0]]/2,v[i][ij[1]]/2) for i in face])
    def box(self,p,s,ma,rot=None,wood=False,jitter=0,seed=1):
        v=[];rand=random.Random(seed);rot=rot or Matrix.Identity(3)
        for i,j,k in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]:
            local=Vector((i*s[0]/2,j*s[1]/2,k*s[2]/2))
            if jitter: local+=Vector(tuple(rand.uniform(-jitter,jitter) for _ in range(3)))
            v.append(Vector(p)+rot@local)
        faces=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
        uv=None
        if wood:
            # Use a narrow strip from one photographed board. Grain follows
            # the longest dimension rather than an arbitrary world axis.
            long=max(range(3),key=lambda i:s[i]);rand=random.Random(seed);u=rand.random();v0=(rand.randrange(10)+.12)/10
            uv=[]
            for face in faces:
                local=[rot.inverted()@(v[idx]-Vector(p)) for idx in face]
                normal=(local[1]-local[0]).cross(local[2]-local[0]);normalaxis=max(range(3),key=lambda i:abs(normal[i]))
                axes=[i for i in range(3) if i!=normalaxis];along=max(axes,key=lambda i:s[i]);across=next(i for i in axes if i!=along)
                co=[]
                for q in local:co.append((u+q[along]/3,v0+(q[across]/max(s[across],.01))*.06))
                uv.append(co)
        self.add(v,faces,ma,uv)
    def beam(self,a,b,width,depth,ma):
        a=Vector(a);b=Vector(b);rot=(b-a).to_track_quat('Z','Y').to_matrix()
        self.box((a+b)/2,(width,depth,(b-a).length),ma,rot,True)
    def rod(self,a,b,r,ma,n=16,r2=None):
        a=Vector(a);b=Vector(b);rot=(b-a).to_track_quat('Z','Y').to_matrix();v=[]
        for center,rad in [(a,r),(b,r if r2 is None else r2)]:
            v.extend(center+rot@Vector((rad*math.cos(i*TAU/n),rad*math.sin(i*TAU/n),0)) for i in range(n))
        self.add(v,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],ma,smooth=True)
    def ellipsoid(self,p,s,ma,n=24,rings=12):
        v=[(p[0]+s[0]*math.sin(j*math.pi/rings)*math.cos(i*TAU/n),p[1]+s[1]*math.sin(j*math.pi/rings)*math.sin(i*TAU/n),p[2]+s[2]*math.cos(j*math.pi/rings)) for j in range(rings+1) for i in range(n)]
        self.add(v,[(j*n+i,(j+1)*n+i,(j+1)*n+(i+1)%n,j*n+(i+1)%n) for j in range(rings) for i in range(n)],ma,smooth=True)
    def torus(self,p,major,minor,ma,rot=None,n=64):
        rot=rot or Matrix.Identity(3);v=[]
        for i in range(n):
            a=i*TAU/n
            for j in range(10):
                b=j*TAU/10;v.append(Vector(p)+rot@Vector(((major+minor*math.cos(b))*math.cos(a),(major+minor*math.cos(b))*math.sin(a),minor*math.sin(b))))
        self.add(v,[(i*10+j,i*10+(j+1)%10,((i+1)%n)*10+(j+1)%10,((i+1)%n)*10+j) for i in range(n) for j in range(10)],ma,smooth=True)
    def obj(self,name,parent=None,bevel=.012):
        me=bpy.data.meshes.new(name);me.from_pydata(self.v,[],self.f);me.update()
        for m in M:me.materials.append(m)
        uv=me.uv_layers.new(name='Surface scale')
        for poly,ma,tex,sm in zip(me.polygons,self.mi,self.uv,self.sm):
            poly.material_index=ma;poly.use_smooth=sm
            for li,co in zip(poly.loop_indices,tex):uv.data[li].uv=co
        o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.parent=parent
        if bevel:
            b=o.modifiers.new('Worn edge radius','BEVEL');b.width=bevel;b.segments=3
            b=o.modifiers.new('Weighted corner normals','WEIGHTED_NORMAL');b.keep_sharp=True;b.weight=30
        return o

def root(name,p=(0,0,0),parent=None):
    o=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(o);o.location=p;o.parent=parent;return o

def curve(name,pts,r,ma,parent=None):
    cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=16;cu.bevel_depth=r;cu.bevel_resolution=3
    spl=cu.splines.new('POLY');spl.points.add(len(pts)-1)
    for q,p in zip(spl.points,pts):q.co=(*p,1)
    ob=bpy.data.objects.new(name,cu);bpy.context.collection.objects.link(ob);cu.materials.append(M[ma]);ob.parent=parent;return ob

def lettering(body,p,size,ma,parent=None):
    cu=bpy.data.curves.new('Carved lettering','FONT');cu.body=body;cu.align_x='CENTER';cu.size=size;cu.extrude=.0025
    font=Path('C:/Windows/Fonts/georgia.ttf')
    if font.exists():cu.font=bpy.data.fonts.load(str(font),check_existing=True)
    ob=bpy.data.objects.new(body,cu);bpy.context.collection.objects.link(ob);cu.materials.append(M[ma]);ob.location=p;ob.rotation_euler=(math.pi/2,0,0);ob.parent=parent;return ob

def drift(name,xrange,yrange,height,parent=None,step=.15):
    nx=max(3,round((xrange[1]-xrange[0])/step));ny=max(3,round((yrange[1]-yrange[0])/step));v=[]
    for j in range(ny+1):
        y=yrange[0]+(yrange[1]-yrange[0])*j/ny
        for i in range(nx+1):
            x=xrange[0]+(xrange[1]-xrange[0])*i/nx;v.append((x,y,height(x,y)))
    m=Mesh();m.add(v,[(j*(nx+1)+i,j*(nx+1)+i+1,(j+1)*(nx+1)+i+1,(j+1)*(nx+1)+i) for j in range(ny) for i in range(nx)],SN,smooth=True)
    o=m.obj(name,parent,0);sol=o.modifiers.new('Snow thickness','SOLIDIFY');sol.thickness=.09
    sub=o.modifiers.new('Soft settled edge','SUBSURF');sub.levels=1;sub.render_levels=1;return o

def window(m,cx,y,z,w,h,shutters=True):
    # Individual panes sit 14 cm behind the carved outer frame.
    m.box((cx,y+.16,z),(w-.10,.028,h-.1),GL)
    for sx in [-1,1]:
        m.box((cx+sx*w/2,y,z),(.10,.22,h+.2),DK,wood=True,seed=int(cx*90)%97)
        m.box((cx+sx*(w/2+.07),y+.03,z),(.035,.19,h+.3),WO,wood=True)
    for zz in [z-h/2,z+h/2]:m.box((cx,y,zz),(w+.16,.22,.1),DK,wood=True)
    m.box((cx,y-.025,z),(.045,.1,h),WO,wood=True)
    for zz in [z-h*.17,z+h*.17]:m.box((cx,y-.025,zz),(w,.09,.037),WO,wood=True)
    m.box((cx,y-.12,z-h/2-.11),(w+.33,.47,.10),ST)
    if shutters:
        for sign in [-1,1]:
            sx=cx+sign*(w*.75+.14)
            m.box((sx,y+.045,z),(w*.43,.075,h+.03),GR,wood=True,seed=int(abs(sx)*20))
            for j in range(8):m.box((sx,y-.012,z-h*.44+j*h*.125),(w*.40,.037,.035),DK,wood=True)
            for zz in [z-h*.32,z+h*.32]:
                m.box((sx,y-.055,zz),(w*.45,.024,.045),IR)
                m.rod((sx-sign*w*.18,y-.045,zz-.07),(sx-sign*w*.18,y-.045,zz+.07),.016,IR,8)

def chalet(name,p=(0,0,0),seed=71,variant='bakery'):
    r=root(name,p);rng=random.Random(seed);w=7;d=5.9;front=-d/2;back=d/2;eave=5.85;rise=2.7
    m=Mesh();wood=Mesh();snow=Mesh();stone=Mesh()
    # Interior volume kept away from the window openings.
    m.box((0,.12,1.3),(6.5,5.3,2.6),MO)
    openings=[(-2.15,1.35,1.45,1.35),(0,1.12,1.08,2.24),(2.15,1.35,1.45,1.35)]
    for row in range(52):
        z=.025+row*.05;cuts=[(-3.5,3.5)]
        for ox,oz,ow,oh in openings:
            if abs(z-oz)>oh/2:continue
            updated=[]
            for a,b in cuts:
                if b<ox-ow/2 or a>ox+ow/2:updated.append((a,b));continue
                if a<ox-ow/2:updated.append((a,ox-ow/2))
                if b>ox+ow/2:updated.append((ox+ow/2,b))
            cuts=updated
        for a,b in cuts:m.box(((a+b)/2,front+.05,z),(b-a,.12,.052),MO)
    # Opaque interior is set back; glass masks the visible cavity.
    for row in range(9):
        z=.16+row*.285;x=-3.5
        while x<3.48:
            sw=min(rng.uniform(.38,.8),3.5-x);cx=x+sw/2
            if not any(abs(cx-ox)<ow/2+sw*.45 and abs(z-oz)<oh/2+.10 for ox,oz,ow,oh in openings):
                stone.box((cx,front+.02+rng.uniform(-.025,.025),z),(sw-.026,.24,.265),SQ,jitter=.018,seed=row*41+int(x*20))
            x+=sw
    for side in [-1,1]:
        # Side walls use 2 m real-scale masonry texture plus dressed quoins.
        m.box((side*3.42,0,1.3),(.3,d,2.6),ST)
        for row in range(9):
            for yy in [front+.1,back-.1]:stone.box((side*3.43,yy,.145+row*.285),(.45,.44,.27),ST,jitter=.017,seed=row+int(yy*7))
    for ox,oz,ow,oh in openings:
        if ox:
            window(wood,ox,front-.15,oz,ow,oh,False)
            for sx in [-1,1]:stone.box((ox+sx*(ow/2+.15),front-.05,oz),(.22,.28,oh+.3),ST)
            stone.box((ox,front-.06,oz+oh/2+.16),(ow+.52,.3,.25),ST)
            # Bread shelving visible in the warm bay.
            for zz in [oz-.3,oz+.18]:
                wood.box((ox,front+.09,zz),(ow-.12,.35,.045),WO,wood=True)
                for q in range(4):
                    wood.ellipsoid((ox-.45+q*.30,front+.05,zz+.09),(.12,.09,.065),BD,16,8)
        else:
            for sx in [-1,1]:stone.box((sx*.64,front-.12,1.12),(.21,.31,2.24),SQ)
            stone.box((0,front-.12,2.35),(1.53,.32,.23),SQ)
            wood.box((0,front-.08,1.08),(1.02,.12,2.15),DK,wood=True)
            for j in range(6):wood.box((-.425+j*.17,front-.16,.88),(.157,.06,1.69),WO,wood=True,seed=j+88)
            window(wood,0,front-.21,1.79,.66,.54,False)
            for zz in [.45,1.25]:wood.box((0,front-.20,zz),(.92,.035,.055),IR)
            wood.torus((.34,front-.24,1.0),.065,.011,BR,Matrix.Rotation(math.pi/2,3,'X'),24)
            for j in range(3):stone.box((0,front-.26-j*.25,.09-j*.055),(1.52,.60,.16),ST,jitter=.014,seed=j)
    # Upper floor is formed from real planks and beams, leaving front apertures.
    for side in [-1,1]:
        for row in range(18):
            z=2.7+row*.177
            cuts=[(-d/2,-2.13),(-.97,.97),(2.13,d/2)] if 3.58<z<5.04 else [(-d/2,d/2)]
            for a,b in cuts:wood.box((side*3.45,(a+b)/2,z),(.14,b-a,.167),WO,wood=True,seed=seed+row)
        sw=Mesh()
        for x in [-1.55,1.55]:window(sw,x,-.06,4.32,1.07,1.38,True)
        sr=root(name+' | side windows',(side*3.45,0,0),r);sr.rotation_euler.z=side*math.pi/2
        sw.obj('Recessed side windows',sr,.009)
    for y in [front,back]:
        for row in range(18):
            z=2.7+row*.177;x=-3.5
            cuts=[(-3.5,-2.73),(-1.57,-.58),(.58,1.57),(2.73,3.5)] if y==front and 3.58<z<5.04 else [(-3.5,3.5)]
            for a,b in cuts:wood.box(((a+b)/2,y,z),(b-a,.115,.167),WO,wood=True,seed=seed+row)
        # Front and rear gables are closed with vertical boards of varying heights.
        for j in range(31):
            x=-3.4+j*.227;top=eave+rise*(1-abs(x)/3.5)
            if top>eave:wood.box((x,y,(top+eave)/2),(.215,.13,top-eave),WO,wood=True,seed=j+seed)
    for xx in [-3.45,3.45]:
        for yy in [front-.045,back+.045]:wood.box((xx,yy,4.2),(.23,.25,3.4),DK,wood=True,seed=12)
    for z in [2.64,3.10,5.56,5.87]:wood.box((0,front-.095,z),(7.16,.24,.17),DK,wood=True,seed=int(z*100))
    for x in [-2.15,0,2.15]:window(wood,x,front-.13,4.32,1.07,1.38,True)
    window(wood,0,front-.14,6.60,.83,1.05,False)
    for y in [front-.14,back+.14]:
        for side in [-1,1]:wood.beam((0,y,8.6),(side*3.88,y,5.63),.18,.22,DK)
        wood.box((0,y,7.10),(.17,.2,2.65),DK,wood=True)
    # Long balcony with individually shaped cutout balusters and curved brackets.
    for j in range(24):wood.box((-3.24+j*.282,front-.60,3.10),(.266,1.2,.105),WO,wood=True,seed=j+1)
    for x in [-3.20,-1.6,0,1.6,3.2]:
        wood.beam((x,front+.04,2.3),(x,front-1.13,3.05),.16,.16,DK)
        wood.box((x,front-1.13,3.65),(.12,.12,1.15),DK,wood=True)
        wood.ellipsoid((x,front-1.13,4.26),(.09,.09,.055),WO)
    for j in range(27):
        x=-3.04+j*.234
        profile=[(-.073,0),(.073,0),(.073,.12),(.034,.22),(.058,.34),(.035,.47),(.073,.66),(-.073,.66),(-.035,.47),(-.058,.34),(-.034,.22),(-.073,.12)]
        v=[(x+xx,front-1.13+yy,3.33+zz) for yy in [-.035,.035] for xx,zz in profile];n=len(profile)
        wood.add(v,[tuple(range(n-1,-1,-1)),tuple(range(n,n*2))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],WO)
    for z in [3.27,4.07]:wood.box((0,front-1.13,z),(6.7,.16,.11),DK,wood=True)
    # Main roof structure, visible rafters and staggered overlapping slate.
    roof=Mesh();angle=math.atan2(rise,3.5);half=3.98;ridge=eave+rise
    for sign in [-1,1]:
        for yy in [-3.35,-2.55,-1.6,-.7,.2,1.1,2,2.9,3.45]:
            wood.beam((0,yy,ridge-.12),(sign*half,yy,ridge-half*math.tan(angle)-.13),.13,.17,DK)
        for row in range(16):
            u=(row+.5)/16;xx=sign*half*u;zz=ridge-half*u*math.tan(angle)
            for col in range(24):
                yy=-3.65+(col+.5+(row%2)*.5)*.30
                if yy>3.63:continue
                roof.box((xx,yy,zz),(.36,.292,.046),SL,Matrix.Rotation(sign*angle,3,'Y'),jitter=.008,seed=row*30+col)
        def roofheight(x,y):
            u=abs(x)/half;edge=min(1,(half-abs(x))/.23,(3.70-abs(y))/.25);edge=max(0,edge)
            n=noise_vector(Vector((x*1.1,y*.9,seed*.1))).x
            return ridge-abs(x)*math.tan(angle)+.07+edge*(.17+.085*n+.045*math.sin(y*2)+.03*math.sin(x*3.1+y*2.4))
        drift(name+' | wind-set roof snow',(-half,0) if sign<0 else (0,half),(-3.69,3.69),roofheight,r,.12)
        # Uneven few icicles, with no regular teeth pattern.
        for k in range(17):
            yy=rng.uniform(-3.4,3.4);zz=ridge-half*math.tan(angle)+.08;length=rng.uniform(.09,.39)
            snow.rod((sign*half,yy,zz),(sign*half,yy,zz-length),rng.uniform(.015,.031),IC,10,.0015)
    # Broad stone chimney with cap, soot-lined opening, brick courses.
    cx=1.75;cy=1.0;cz=ridge-abs(cx)*math.tan(angle)
    stone.box((cx,cy,cz+.65),(.67,.79,1.9),ST)
    for k in range(6):stone.box((cx,cy,cz+.03+k*.28),(.69,.81,.025),MO)
    stone.box((cx,cy,cz+1.64),(.91,1.04,.16),ST)
    stone.box((cx,cy,cz+1.73),(.53,.62,.05),IR)
    snow.box((cx,cy,cz+1.77),(.91,1.04,.1),SN)
    if variant=='bakery':
        dm=root(name+' | side dormer',(2.32,-.85,6.68),r);dm.rotation_euler.z=math.pi/2
        dmesh=Mesh();dmesh.box((0,.15,.32),(1.5,1.5,.63),DK,wood=True)
        dmesh.box((0,-.68,.52),(1.44,.08,.92),WO,wood=True)
        window(dmesh,0,-.78,.56,.77,.78,False)
        dmesh.add([(-.8,-.8,1.02),(.8,-.8,1.02),(0,-.8,1.58),(-.8,.9,1.02),(.8,.9,1.02),(0,.9,1.58)],[(0,1,2),(3,5,4),(0,2,5,3),(2,1,4,5)],WO)
        dmesh.obj('Dormer cheeks and front',dm,.01)
        for sign in [-1,1]:
            drift('Dormer settled cap',(-.9,0) if sign<0 else (0,.9),(-.94,1.0),lambda x,y:1.70-abs(x)*.7+.025*math.sin(y*4),dm,.10)
    # Carved lintel, restrained sign, bread peel and firewood.
    wood.box((0,front-.22,2.58),(3.8,.18,.43),DK,wood=True)
    lettering('LE PREMIER PAIN',(0,front-.32,2.48),.23,BR,r)
    lettering('•  1 7 6 8  •',(0,front-.25,5.61),.15,BR,r)
    for row in range(4):
        for col in range(7-row//2):
            xx=-3.05+col*.17;zz=.12+row*.16
            wood.rod((xx,front-.13,zz),(xx,front-.62,zz),.083,WO,12)
    stone.obj(name+' | irregular masonry',r,.018);m.obj(name+' | plaster and recessed interior',r,.018)
    wood.obj(name+' | joinery and carved balcony',r,.009);roof.obj(name+' | lapped slate tiles',r,.008);snow.obj(name+' | ice and small deposits',r,.008)
    for x in [-2.15,0,2.15]:
        drift(name+' | sill snow '+str(x),(x-.72,x+.72),(front-.42,front-.12),lambda a,b:3.55+.045*math.cos((a-x)*2),r,.12)
    return r

def lantern(p,parent=None):
    x,y,z=p;m=Mesh();m.box((x,y,z),(.15,.15,.25),GL)
    for sx in [-1,1]:
        for sy in [-1,1]:m.beam((x+sx*.10,y+sy*.10,z-.18),(x+sx*.08,y+sy*.08,z+.17),.018,.018,IR)
    m.box((x,y,z-.18),(.24,.24,.04),IR)
    m.add([(x-.15,y-.15,z+.18),(x+.15,y-.15,z+.18),(x+.15,y+.15,z+.18),(x-.15,y+.15,z+.18),(x,y,z+.31)],[(0,1,4),(1,2,4),(2,3,4),(3,0,4)],IR)
    m.torus((x,y,z+.36),.04,.009,IR,Matrix.Rotation(math.pi/2,3,'X'),20)
    m.obj('Hand forged lantern',parent,.006)
    ld=bpy.data.lights.new('Lantern glow','POINT');ld.energy=9;ld.color=(1,.50,.20);ld.shadow_soft_size=.12
    ob=bpy.data.objects.new('Lantern glow',ld);bpy.context.collection.objects.link(ob);ob.location=p;ob.parent=parent

def station(name,p=(0,0,0)):
    r=root(name,p);m=Mesh();s=Mesh()
    # Stone sill / independent planks with joints; a clear loading side.
    m.box((0,0,.14),(3.8,3.6,.28),ST)
    for j in range(21):m.box((0,-1.67+j*.167,.34),(3.65,.157,.12),WO,wood=True,seed=j+3)
    for x in [-1.4,1.4]:
        m.box((x,0,1.83),(.20,.25,2.93),DK,wood=True)
        m.box((x,0,.54),(.26,.31,.31),IR)
        for yy in [-.13,.13]:
            for zz in [.48,.64,2.60,2.78]:m.rod((x,yy,zz),(x,yy*1.12,zz),.033,BR,12)
        m.beam((x,0,2.40),(x*.57,0,3.10),.13,.13,DK)
    m.box((0,0,3.11),(3.27,.30,.25),DK,wood=True)
    # Decorative curved iron cheeks hold actual wheel axle.
    for x in [-.21,.21]:
        m.box((x,0,3.25),(.085,.44,.40),IR)
        m.rod((x-.08,0,3.45),(x+.08,0,3.45),.09,BR,24)
    m.rod((-.43,0,3.45),(.43,0,3.45),.065,IR,24)
    wheel=root('Station traction wheel',(0,0,3.45),r);wh=Mesh();rot=Matrix.Rotation(math.pi/2,3,'Y')
    for x in [-.085,.085]:wh.torus((x,0,0),.58,.031,BR,rot)
    wh.torus((0,0,0),.565,.043,IR,rot)
    for j in range(8):
        a=j*TAU/8;wh.beam((0,.12*math.cos(a),.12*math.sin(a)),(0,.54*math.cos(a),.54*math.sin(a)),.045,.045,BR)
    wh.rod((-.15,0,0),(.15,0,0),.125,BR,32);wh.obj('Grooved brass sheave and spokes',wheel,.007)
    # Manual winch, toothed ratchet, brake and loading clamp.
    m.rod((-1.55,.0,1.15),(-.97,0,1.15),.12,BR,32)
    for xx in [-1.52,-1.03]:m.torus((xx,0,1.15),.25,.025,IR,rot,40)
    m.rod((-1.59,0,1.15),(-1.59,-.24,.89),.026,BR);m.rod((-1.59,-.24,.89),(-1.77,-.24,.89),.035,DK)
    m.box((0,-.26,.52),(1.5,.12,.16),IR)
    for x in [-.70,.70]:m.box((x,-.18,.66),(.08,.3,.18),BR)
    m.obj('Loading pier | joints, windlass and brake',r,.012)
    # Cargo box is an independent articulated assembly, with visible metal corners.
    basket=root('Cargo basket assembly',(0,0,.66),r);b=Mesh()
    for z in [.08,.24,.40,.56]:
        for sign in [-1,1]:
            b.box((0,sign*.43,z),(1.28,.06,.145),RD,wood=True,seed=int(z*100))
            b.box((sign*.64,0,z),(.06,.84,.145),RD,wood=True,seed=int(z*50))
    b.box((0,0,0),(1.32,.91,.10),DK,wood=True)
    for sx in [-1,1]:
        for sy in [-1,1]:
            b.box((sx*.64,sy*.43,.32),(.085,.085,.69),IR)
            for zz in [.08,.30,.53]:b.ellipsoid((sx*.66,sy*.465,zz),(.02,.012,.02),BR,12,6)
    for sx in [-1,1]:
        b.beam((sx*.65,0,.38),(sx*.43,0,1.43),.044,.055,IR)
        b.beam((sx*.43,0,1.43),(0,0,1.82),.044,.055,IR)
    b.rod((0,0,1.82),(0,0,2.42),.037,IR)
    b.torus((0,0,2.40),.067,.018,BR,rot,24)
    b.obj('Riveted burgundy larch cargo basket',basket,.008)
    lid=root('Hinged basket lid',(0,.43,.65),basket);lm=Mesh()
    for j in range(7):lm.box((-.56+j*.187,-.43,.015),(.177,.90,.055),RD,wood=True,seed=j+15)
    for xx in [-.43,.43]:lm.box((xx,-.43,.05),(.06,.93,.035),IR)
    lm.box((0,-.91,.02),(.18,.04,.10),BR);lm.obj('Lid with two strap hinges',lid,.007)
    lantern((1.37,-.2,2.35),r)
    return r
