"""One terrain function shared by masonry, streets and animation. Metres."""
import math
def smooth(u):
 u=max(0,min(1,u));return u*u*(3-2*u)
def interp(a,points):
 for (x,z),(xx,zz) in zip(points,points[1:]):
  if a<=xx:return z+(zz-z)*smooth((a-x)/(xx-x))
 return points[-1][1]
def ground_z(x,y):
 a=abs(x)
 if a<26:return 2.25
 yy=y
 if x<0:
  h=interp(a,[(26,0),(34,4),(48,9),(68,18),(82,23),(102,32),(116,38),(136,46),(150,50),(180,61),(214,70),(280,85),(390,115),(650,160)])
 else:
  h=interp(a,[(26,0),(54,0),(68,5),(82,10),(102,18),(116,23),(136,31),(150,37),(180,48),(220,62),(280,80),(390,110),(650,155)])
 # A broad lower pass allows the mail road to cross the city without a steep grade.
 h*=smooth((abs(yy-18)-10)/38)
 h*=.80+.20*smooth((yy+75)/230)
 h+=smooth((a-45)/70)*smooth((yy-180)/360)*(17+12*math.sin(yy*.008+a*.009))
 # Cathedral terrace sits on a rock shoulder, with a lower ceremonial forecourt.
 if x<0:
  weight=smooth((x+65)/7)*smooth((-22-x)/6)*smooth((y-25)/9)*smooth((115-y)/10)
  platform=17+15*smooth((y-58.5)/.6)
  h=h*(1-weight)+(platform-2.25)*weight
  # Recess the western switchback stair into the hillside; quay remains clear.
  stair=smooth((x+74)/1.2)*smooth((-63-x)/1.2)*smooth((y-26)/2)*smooth((43-y)/2)
  h*=1-stair
 return 2.25+h
def plot_z(x,y,w,d):
 return max(ground_z(x+dx,y+dy) for dx in [-w/2,0,w/2] for dy in [-d/2,0,d/2])+.08
def carriage_road_z(x,y):return ground_z(x,y)
