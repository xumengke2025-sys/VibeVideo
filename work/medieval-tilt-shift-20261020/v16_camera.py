"""A short river-palace reveal, while the same v15 cyclist keeps moving."""
from mathutils import Vector
import v15_motion
def camera(t):
 pose=v15_motion.camera(t)
 if 25<=t<31:
  u=v15_motion.route.ramp(t,25,31)
  pose.update(position=list(Vector((-60,0,95)).lerp(Vector((-52,-6,88)),u)),target=list(Vector((58,10,7)).lerp(Vector((60,12,8)),u)),lens=30,shot=9,progress=u)
 return pose
