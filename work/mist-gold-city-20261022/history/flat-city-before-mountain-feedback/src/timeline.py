"""Absolute-time shared event clock. All positions have deterministic seeking."""
import math
def clamp(x):return max(0.,min(1.,x))
def smooth(x):x=clamp(x);return x*x*(3-2*x)
def smoother(x):x=clamp(x);return x*x*x*(x*(6*x-15)+10)
def bridge_angle(t):return math.radians(76)*(smoother((t-44)/5)-smoother((t-60)/4))
def boat_y(t):return 18+1.9*(t-54.5)
def coach_x(t):
 if t<40:return -32+(t-40)*2.7
 if t<43:
  u=(t-40)/3;return -32+8.1*(u-u*u/2)
 if t<65.5:return -27.95
 dt=t-65.5
 if dt<3:return -27.95+4.2*(dt*dt/6)
 return -27.95+6.3+4.2*(dt-3)
def coach_speed(t):
 if t<40:return 2.7
 if t<43:return 2.7*(1-(t-40)/3)
 if t<65.5:return 0
 return 4.2*clamp((t-65.5)/3)
def road_z(x):
 a=abs(x)
 if a<9.25:return 3.1
 if a<19:return 2.25+.85*(19-a)/9.75
 return 2.25
# Separate camera position and target trajectories; monotone cubic slopes avoid stops at every marker.
CAMERA=[
 (0,(20,-140,18.5),(-35,73,28),42),
 (4,(27,-128,46),(-20,79,19),42),
 (10,(66,-98,153),(0,82,10),42),
 (18,(65,-62,139),(-8,69,10),43),
 (25,(57,-32,109),(0,38,7),42),
 (32,(46,-26,78),(4,5,5),39),
 (40,(40,-28,58),(0,15,3),36),
 (46,(37,-28,56),(0,18,3),36),
 (53,(35,-25,55),(0,19,3),36),
 (60,(34,-22,55),(0,21,3),36),
 (65,(34,-21,57),(-5,20,3),36),
 (70,(39,-19,64),(-6,21,4),38),
 (76,(59,-47,102),(8,45,8),40),
 (84,(115,-151,221),(0,110,10),42),
 (90,(160,-235,316),(0,165,12),43)]
def sample_camera(t):
 i=next((j for j in range(len(CAMERA)-1) if CAMERA[j][0]<=t<CAMERA[j+1][0]),len(CAMERA)-2);a=CAMERA[i];b=CAMERA[i+1];dt=b[0]-a[0];u=clamp((t-a[0])/dt)
 def val(j,k):return list(CAMERA[j][1])+list(CAMERA[j][2])+[CAMERA[j][3]] if k is None else (list(CAMERA[j][1])+list(CAMERA[j][2])+[CAMERA[j][3]])[k]
 def slope(j,k):
  if j==0:return (val(1,k)-val(0,k))/(CAMERA[1][0]-CAMERA[0][0])
  if j==len(CAMERA)-1:return 0
  l=(val(j,k)-val(j-1,k))/(CAMERA[j][0]-CAMERA[j-1][0]);r=(val(j+1,k)-val(j,k))/(CAMERA[j+1][0]-CAMERA[j][0]);return 0 if l*r<=0 else 2*l*r/(l+r)
 out=[]
 for k in range(7):out.append((2*u**3-3*u*u+1)*val(i,k)+(u**3-2*u*u+u)*dt*slope(i,k)+(-2*u**3+3*u*u)*val(i+1,k)+(u**3-u*u)*dt*slope(i+1,k))
 return out[:3],out[3:6],out[6]
def slowed_time(t):
 # Peripheral motion stays alive; no global freeze at the bridge.
 return t
