"""Hand-built, articulated cable freight equipment. Metres, Z up.
Station origin is on its raised masonry landing; local -Y is the loading face.
"""
import bpy, math
from mathutils import Vector, Matrix
import craft as C

# +Y of the mechanism follows the shared upper-to-lower cable azimuth.  The
# loading galleries deliberately keep world axes so existing crate paths work.
_SPAN=Vector((14.6,-18.0,0))
CABLE_DIRECTION=_SPAN.normalized()
CABLE_HEADING=math.atan2(-CABLE_DIRECTION.x,CABLE_DIRECTION.y)
CABLE_SIDE=Vector((math.cos(CABLE_HEADING),math.sin(CABLE_HEADING),0))
HAUL_OFFSET=.55
SHEAVE_RADIUS=.58
CARRIER_CONTACT_Z=2.42

def station(name,position,heading=CABLE_HEADING,slope=0,departure_sign=None):
    r=C.root(name,position);m=C.Mesh()
    m.box((.65,0,.13),(6.0,4.4,.26),C.ST)
    for j in range(27):m.box((.65,-2.1+j*.16,.34),(5.9,.151,.12),C.WO,wood=True,seed=j+31)
    # The straight bearing cable has a saddle and anchor.  A separate haul
    # rope turns round the large sheave; the carrier can never hit that wheel.
    sign=(1 if 'Hill' in name else -1) if departure_sign is None else departure_sign
    mech=C.root(name+' cable-aligned mechanism',(0,0,0),r)
    mech.rotation_euler.z=heading
    m.obj(name+' | raised loading gallery',r,.011);m=C.Mesh()
    rim=SHEAVE_RADIUS;normal=Vector((0,-slope,1)).normalized()
    center=Vector((HAUL_OFFSET,0,3.62))+rim*normal
    # Mortise portal, braced posts, axle through two bronze bearing blocks.
    for x in [-1.3,1.3]:
        m.box((x,.32,2.54),(.19,.24,4.28),C.DK,wood=True)
        m.box((x,.32,.58),(.27,.32,.34),C.IR)
        m.beam((x,.32,3.86),(x*.50,.32,4.57),.13,.14,C.DK)
        for z in [.48,.68,3.87,4.12]:m.rod((x,.15,z),(x,.49,z),.031,C.BR,12)
    m.box((0,.32,4.60),(3.1,.30,.25),C.DK,wood=True)
    for dx in [-.18,.18]:
        x=center.x+dx
        m.box((x,center.y,4.42),(.09,.20,.38),C.IR)
        m.rod((x-.045,center.y,center.z),(x+.045,center.y,center.z),.105,C.BR,24)
    m.rod((center.x-.31,center.y,center.z),(center.x+.31,center.y,center.z),.052,C.IR,24)
    m.obj(name+' | mortise frame and bearing cheeks',mech,.011)
    wheel=C.root(name+' sheave',center,mech);wh=C.Mesh();rot=Matrix.Rotation(math.pi/2,3,'Y')
    for x in [-.07,.07]:wh.torus((x,0,0),.58,.032,C.BR,rot,48)
    wh.torus((0,0,0),.57,.033,C.IR,rot,48)
    for j in range(8):
        a=j*math.tau/8;wh.beam((0,.10*math.cos(a),.10*math.sin(a)),(0,.55*math.cos(a),.55*math.sin(a)),.042,.044,C.BR)
    wh.rod((-.14,0,0),(.14,0,0),.10,C.BR,24);wh.obj(name+' | brass grooved wheel',wheel,.006)
    # A small capstan, crank, pawl and timber bearing cheeks visibly carry
    # the input shaft.  Belt and pulleys occupy the same YZ plane.
    drive=C.Mesh();shaft_x=1.02;cy=-sign*.90;cz=1.18
    for x in [.76,1.27]:
        drive.box((x,cy,.80),(.12,.35,.90),C.DK,wood=True)
        drive.rod((x-.07,cy,cz),(x+.07,cy,cz),.10,C.BR,20)
    drive.rod((.64,cy,cz),(1.42,cy,cz),.052,C.IR,24)
    drive.torus((shaft_x,cy,cz),.23,.038,C.DK,rot,36)
    drive.rod((1.40,cy,cz),(1.40,cy-.24,cz-.17),.028,C.BR,16)
    drive.rod((1.40,cy-.24,cz-.17),(1.60,cy-.24,cz-.17),.035,C.DK,16)
    for j in range(14):
        a=j*math.tau/14
        drive.box((1.30,cy+.17*math.cos(a),cz+.17*math.sin(a)),(.04,.05,.05),C.BR,Matrix.Rotation(a,3,'X'))
    drive.beam((1.31,cy-.26,cz+.10),(1.31,cy-.13,cz+.12),.033,.045,C.IR)
    drive.torus((shaft_x,center.y,center.z),.18,.021,C.BR,rot,36)
    drive.obj(name+' | supported hand windlass and ratchet',mech,.006)
    # Common external tangents to the two auxiliary pulleys.
    dy=center.y-cy;dz=center.z-cz;L=math.hypot(dy,dz)
    ey,ez=dy/L,dz/L;delta=(.23-.18)/L;h=math.sqrt(1-delta*delta)
    belt=[]
    for sense in [-1,1]:
        ny,nz=delta*ey+sense*h*(-ez),delta*ez+sense*h*ey
        belt.extend([(shaft_x,cy+.23*ny,cz+.23*nz),(shaft_x,center.y+.18*ny,center.z+.18*nz)])
    C.curve(name+' | windlass belt ascending',belt[:2],.017,C.LE,mech)
    C.curve(name+' | windlass belt descending',belt[2:],.017,C.LE,mech)
    # Rope follows the wheel groove with an exact tangent at (haul_offset,0,3.62).
    a0=math.atan2(-1,slope)
    wrap=[center+Vector((0,rim*math.cos(a0-sign*j*math.pi/48),rim*math.sin(a0-sign*j*math.pi/48))) for j in range(49)]
    C.curve(name+' | haul rope around grooved sheave',wrap,.010,C.IR,mech)
    # No transverse beam crosses the hanger corridor below the cable.
    anchor=C.Mesh();ay=-sign*.91;az=3.62+slope*ay
    anchor.box((0,ay,az+.10),(.15,.23,.18),C.IR)
    anchor.beam((0,ay,az+.19),(0,ay,4.48),.10,.10,C.DK)
    anchor.rod((-.10,ay,az),(.10,ay,az),.045,C.BR,16)
    anchor.obj(name+' | fixed bearing rope anchor',mech,.006)
    C.curve(name+' | bearing rope to anchor',[(0,0,3.62),(0,ay,az)],.016,C.IR,mech)
    r['cable_heading']=heading;r['cable_slope']=slope
    r['bearing_contact']=[0,0,3.62];r['haul_offset']=HAUL_OFFSET
    for sign in [-1,1]:
        jaw=C.root(name+' clamp '+str(sign),(sign*.85,-.10,1.20),r);q=C.Mesh()
        q.box((0,0,0),(.09,.38,.30),C.BR);q.rod((sign*.02,0,-.08),(sign*.25,0,-.08),.035,C.IR,12);q.obj('Sliding dock clamp',jaw,.009)
    # The transfer table shares the platform; its top is at z 1.35.
    table=C.Mesh()
    for j in range(11):table.box((1.70-.70+j*.14,-.12,1.31),(.132,.96,.08),C.WO,wood=True,seed=j+4)
    for x in [1.12,2.28]:
        for y in [-.47,.22]:table.box((x,y,.85),(.08,.08,.90),C.DK,wood=True)
        table.beam((x,-.47,.57),(x,.22,1.20),.05,.055,C.DK)
    table.obj(name+' | bread receiving trestle',r,.008)
    # A fixed low footboard raises the porter above the basket's front edge.
    # Feet remain on this physical surface throughout lifting and set-down.
    step=C.Mesh()
    for j in range(15):step.box((-.65+(j+.5)*.20,-.69,.605),(.192,1.02,.09),C.WO,wood=True,seed=80+j)
    for x in [-.53,.80,2.23]:step.box((x,-.69,.50),(.11,.90,.20),C.DK,wood=True)
    step.box((.85,-1.32,.465),(3.0,.24,.13),C.WO,wood=True)
    step.obj(name+' | porter work footboard',r,.009)
    # Guard rail leaves the front approach and the cable corridor open.
    rail=C.Mesh()
    for x in [-2.20,3.50]:
        for y in ([-1.60,0,1.75] if x<0 else [-.35,1.75]):rail.box((x,y,.99),(.09,.09,1.18),C.DK,wood=True)
        rail.box((x,.08 if x<0 else .70,1.56),(.10,3.70 if x<0 else 2.10,.095),C.WO,wood=True)
    rail.obj(name+' | gallery balustrade',r,.008)
    C.lantern((1.3,-.05,2.7),r)
    return r

def basket():
    r=C.root('Bread cable basket');m=C.Mesh()
    m.box((0,0,0),(1.32,.91,.10),C.DK,wood=True)
    for z in [.09,.25,.41,.57]:
        for sign in [-1,1]:
            if sign>0:m.box((0,sign*.43,z),(1.28,.06,.147),C.RD,wood=True,seed=int(z*100))
            m.box((sign*.64,0,z),(.06,.84,.147),C.RD,wood=True)
    for sx in [-1,1]:
        for sy in [-1,1]:
            m.box((sx*.64,sy*.43,.32),(.075,.075,.69),C.IR)
            for z in [.08,.31,.56]:m.ellipsoid((sx*.663,sy*.465,z),(.018,.013,.018),C.BR,10,6)
        # Rearward offset arch clears the lid and the raised bread crate.
        m.beam((sx*.64,.43,.32),(sx*.76,.61,.78),.042,.05,C.IR)
        m.beam((sx*.76,.61,.78),(sx*.76,.61,1.78),.042,.05,C.IR)
        m.beam((sx*.76,.61,1.78),(0,.61,2.12),.042,.05,C.IR)
    m.rod((0,.61,2.12),(0,0,2.42),.030,C.IR,16)
    m.obj('Burgundy boards, forged hanger and corner rivets',r,.008)
    # Two real loading leaves let hands reach the low crate without crossing
    # an opaque front wall. They are locked shut while the basket travels.
    for sign in [-1,1]:
        gate=C.root('Freight loading gate '+str(sign),(sign*.64,-.43,0),r);gm=C.Mesh()
        for z in [.09,.25,.41,.57]:gm.box((-sign*.32,0,z),(.62,.06,.147),C.RD,wood=True,seed=int(z*100))
        gm.box((-sign*.57,-.045,.32),(.045,.025,.61),C.IR)
        gm.obj('Loading leaf ironwork',gate,.006)
        pin=C.Mesh();pin.rod((sign*.64,-.43,.03),(sign*.64,-.43,.66),.020,C.BR,12);pin.obj('Vertical loading gate hinge',r,.003)
    lid=C.root('Freight lid hinge',(0,.43,.65),r);lm=C.Mesh()
    for j in range(7):lm.box((-.56+j*.187,-.43,.01),(.177,.90,.055),C.RD,wood=True,seed=15+j)
    for x in [-.43,.43]:lm.box((x,-.43,.046),(.055,.93,.029),C.IR)
    lm.box((0,-.91,.02),(.16,.035,.09),C.BR);lm.obj('Freight lid with straps',lid,.006)
    for x in [-.43,.43]:
        hm=C.Mesh();hm.rod((x-.075,0,0),(x+.075,0,0),.027,C.BR,16);hm.obj('Lid hinge pin',C.root('Hinge socket',(x,.43,.65),r),.003)
    coil=[(-.12+.24*j/120,.43+.038*math.cos(j*math.tau/12),.65+.038*math.sin(j*math.tau/12)) for j in range(121)]
    C.curve('Visible lid torsion spring',coil,.007,C.BR,r)
    stop=C.Mesh();stop.box((.17,.47,.70),(.08,.12,.08),C.IR);stop.obj('Lid hinge travel stop',r,.003)
    trolley=C.root('Carrier trolley',(0,0,CARRIER_CONTACT_Z),r)
    trolley.rotation_euler.z=CABLE_HEADING;tm=C.Mesh()
    # Two actual grooved wheels ride above the bearing cable.  Their axles,
    # bearings and outside cheeks stay outside its central running groove.
    for y in [-.13,.13]:
        roll=C.root('Carrier roller '+('front' if y>0 else 'rear'),(0,y,.105),trolley);rm=C.Mesh()
        for x in [-.026,.026]:rm.torus((x,0,0),.080,.012,C.BR,Matrix.Rotation(math.pi/2,3,'Y'),28)
        rm.torus((0,0,0),.080,.009,C.IR,Matrix.Rotation(math.pi/2,3,'Y'),28)
        rm.rod((-.075,0,0),(.075,0,0),.016,C.IR,12)
        rm.obj('Carrier grooved roller',roll,.002)
        for x in [-.075,.075]:
            tm.box((x,y,.018),(.035,.06,.18),C.IR)
            tm.rod((x-.017,y,.105),(x+.017,y,.105),.025,C.BR,12)
    for x in [-.075,.075]:tm.box((x,0,-.065),(.045,.39,.04),C.IR)
    tm.box((0,0,-.075),(.17,.09,.04),C.IR)
    # A forged traction arm meets the offset haul rope from below.
    tm.beam((.075,0,-.065),(HAUL_OFFSET,0,-.065),.035,.04,C.IR)
    tm.box((HAUL_OFFSET,0,-.035),(.07,.09,.06),C.BR)
    tm.obj('Trolley bearing cheeks and traction arm',trolley,.004)
    r['contact_height']=CARRIER_CONTACT_Z;r['cable_heading']=CABLE_HEADING
    return r

def crate():
    r=C.root('One persistent bread crate');m=C.Mesh()
    m.box((0,0,.025),(.96,.60,.05),C.WO,wood=True)
    for sign in [-1,1]:
        for z in [.12,.27]:
            m.box((0,sign*.30,z),(.96,.045,.135),C.WO,wood=True,seed=int(z*99))
            m.box((sign*.48,0,z),(.045,.58,.135),C.WO,wood=True)
        for y in [-.26,.26]:m.box((sign*.45,y,.20),(.06,.055,.39),C.DK,wood=True)
        # Exterior grips are shared by hand-target constraints in the timeline.
        m.rod((sign*.51,-.16,.23),(sign*.51,.16,.23),.026,C.DK,12)
    m.obj('Dovetailed bread crate and carrying handles',r,.007)
    for i in range(3):
        for j in range(2):
            x=-.30+i*.30;y=-.14+j*.28;b=C.Mesh()
            b.ellipsoid((x,y,.15),(.125,.12,.085),C.BD,24,10);b.obj('Crusty morning loaf',r,0)
            for k in [-1,0,1]:C.curve('Bread scoring',[(x-.05,y+k*.06-.02,.218),(x,y+k*.06,.237),(x+.045,y+k*.06+.02,.218)],.005,C.CL,r)
    lid=C.root('Bread crate lid',(0,.30,.40),r);lm=C.Mesh()
    for j in range(6):lm.box((-.40+j*.16,-.30,0),(.153,.62,.035),C.WO,wood=True,seed=j+50)
    for x in [-.32,.32]:lm.box((x,-.30,.025),(.045,.63,.025),C.DK)
    lm.obj('Bread box opening lid',lid,.005)
    return r
