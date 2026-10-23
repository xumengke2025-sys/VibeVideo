"""One addressable route, metre units, +Y bicycle forward. No Blender dependency."""
import math,bisect
DURATION=90.0
NODES=[(0,-1,-34),(4,-1,-30),(8,-1,-22),(12,-1,-10),(17,-1,5),(19,-1,10),(23,-1.5,23),(25,0,32),(27,6,36),(31,22.8,37),(34,22.8,47),(37,22.8,63),(40,22.8,81),(44,22.8,102),(46,17,103),(49,0,103),(53,-30,103),(55,-47,104),(58,-47,118),(62,-47,131),(64,-46,137),(66,-45.5,138),(69.8,-45.5,138),(70.6,-44.8,138.9),(71.5,-43.5,138.2),(72.4,-43.7,136.6),(73.5,-45,133),(74.5,-47,127),(75.5,-43,124),(76.7,-31,122.4),(77.4,-25,122.7),(78,-20,124),(81,-1,124),(84,-1,143),(90,-1,179)]
TIMES=[p[0] for p in NODES]
def velocity(i):
    a=NODES[max(0,i-1)];b=NODES[min(len(NODES)-1,i+1)];p=NODES[i]
    # Align the last approach tangent with the stop chord, avoiding a tiny
    # reverse before stopping that used to flip yaw by about ninety degrees.
    if p[0]==64:return tuple((NODES[i+1][k]-p[k])/(NODES[i+1][0]-p[0]) for k in [1,2])
    if (i and p[1:]==a[1:]) or (i<len(NODES)-1 and p[1:]==b[1:]):return (0.,0.)
    return tuple(0. if (i and p[k]==a[k]) or (i<len(NODES)-1 and p[k]==b[k]) else (b[k]-a[k])/(b[0]-a[0]) for k in [1,2])
TANGENTS=[velocity(i) for i in range(len(NODES))]
def position(t):
    t=max(0,min(DURATION,t));i=min(len(NODES)-2,max(0,bisect.bisect_right(TIMES,t)-1));a,b=NODES[i:i+2];dt=b[0]-a[0];u=(t-a[0])/dt
    h00=2*u**3-3*u*u+1;h10=u**3-2*u*u+u;h01=-2*u**3+3*u*u;h11=u**3-u*u
    return tuple(h00*a[k+1]+h10*dt*TANGENTS[i][k]+h01*b[k+1]+h11*dt*TANGENTS[i+1][k] for k in range(2))
ARC=[0.]
for i in range(1,10801):
    a=position((i-1)/120);b=position(i/120);ARC.append(ARC[-1]+math.dist(a,b))
def distance(t):
    x=max(0,min(10800,t*120));i=min(10799,int(x));return ARC[i]+(ARC[i+1]-ARC[i])*(x-i)
def ramp(t,a,b):
    x=max(0,min(1,(t-a)/(b-a)));return x*x*(3-2*x)
def pulse(t,a,b,c,d):return ramp(t,a,b)*(1-ramp(t,c,d))
def state(t):
    x,y=position(t);a=position(t-.04);b=position(t+.04);dx=(b[0]-a[0])/.08;dy=(b[1]-a[1])/.08;speed=math.hypot(dx,dy)
    if speed<.02:
        a=position(65.8);b=position(66);dx=b[0]-a[0];dy=b[1]-a[1]
    yaw=math.atan2(-dx,dy)
    earlier=position(t-.16);later=position(t+.16);bend=dx*(later[1]-2*y+earlier[1])-dy*(later[0]-2*x+earlier[0]);lean=max(-.14,min(.14,bend*.15))
    quay=ramp(x,20.5,22.5) if 34<y<107 else 0
    temple=ramp(y,125.5,127.5)*(1-ramp(x,-29.5,-28)) if x<-28 else 0
    height=.10+1.055*quay+.18*temple
    return {'t':t,'position':[x,y,height],'yaw':yaw,'speed':speed,'distance':distance(t),'wheel_angle':-distance(t)/.36,'crank_angle':distance(t)/(.36*2.35),'lean':lean,'wave':max(pulse(t,12.5,13.1,14.7,15.4),pulse(t,35,35.7,37.5,38.2)),'hat_tip':pulse(t,67,67.7,69,69.7),'duck':max(pulse(t,39.2,39.7,41.3,41.8),.25*pulse(t,49.8,50.2,51.1,51.6)),'stop':pulse(t,64.5,66,69.8,71)}
