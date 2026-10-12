"""Independent double-precision RK4 checks of the orbit equation used for illustration."""
from pathlib import Path
import math,json
def cross(p,v):return p[0]*v[1]-p[1]*v[0]
def norm(v):return math.hypot(*v)
def ray(b):
    state=[-100.,b,1.,0.];L=cross(state[:2],state[2:]);L2=L*L
    E2=norm(state[2:])**2-L2/norm(state[:2])**3
    maxL=maxE=0.;rmin=norm(state[:2]);captured=False
    def derivative(s):
        r=norm(s[:2]);q=-1.5*L2/r**5
        return [s[2],s[3],q*s[0],q*s[1]]
    def shifted(s,k,h):return [a+h*c for a,c in zip(s,k)]
    for n in range(100000):
        r=norm(state[:2]);rmin=min(rmin,r)
        if r<=1.01:captured=True;break
        if state[0]>100 or (r>130 and n>100):break
        h=min(.07,max(.002,r*.007));k1=derivative(state);k2=derivative(shifted(state,k1,h/2));k3=derivative(shifted(state,k2,h/2));k4=derivative(shifted(state,k3,h))
        state=[a+h*(v1+2*v2+2*v3+v4)/6 for a,v1,v2,v3,v4 in zip(state,k1,k2,k3,k4)]
        maxL=max(maxL,abs(cross(state[:2],state[2:])-L));maxE=max(maxE,abs(norm(state[2:])**2-L2/norm(state[:2])**3-E2))
    return {'initial_offset_rs':b,'captured':captured,'minimum_radius_rs':rmin,'outgoing_angle_radians':math.atan2(state[3],state[2]),'weak_field_leading_angle_2rs_over_b':2/b,'max_angular_momentum_absolute_error':maxL,'max_energy_squared_absolute_error':maxE,'steps':n+1}
results=[ray(b) for b in [2.5,2.8,10.,30.]]
assert results[0]['captured'] and not results[1]['captured']
assert not results[2]['captured'] and not results[3]['captured']
assert abs(abs(results[3]['outgoing_angle_radians'])-2/30)<.009
assert all(x['max_angular_momentum_absolute_error']<1e-5 for x in results)
out=Path(__file__).parent/'out'/'orbit-check.json'
out.write_text(json.dumps({'rs':1,'equation':'r_vector_ddot = -1.5 * rs * L^2 * r_vector / |r|^5','purpose':'Checks equation and limiting behavior; does not validate GPU discretization, radiative transfer, or the stylized disk texture','passed':True,'results':results},indent=2),encoding='utf-8')
print(json.dumps({'passed':True,'rays':results},ensure_ascii=False))
