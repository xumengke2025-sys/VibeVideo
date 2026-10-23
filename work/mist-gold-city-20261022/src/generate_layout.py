"""Irregular urban fabric: connected lanes, curved arterials, perimeter parcels.
Source geometry is original. Historical aerial references inform morphology only.
"""
import sys,json,math,random
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'vendor/urban'))
import numpy as np
from scipy.spatial import Voronoi
from scipy.interpolate import CubicSpline
from shapely.geometry import Polygon,LineString,box,Point
from shapely.ops import unary_union,nearest_points
R=random.Random(180061)
def curve(points):
 p=np.array(points);t=np.r_[0,np.cumsum(np.linalg.norm(np.diff(p,axis=0),axis=1))];f=CubicSpline(t,p,axis=0,bc_type='natural');return f(np.linspace(0,t[-1],max(3,int(t[-1]/4)))).tolist()
arterials=[]
def road(name,p,w):arterials.append({'name':name,'points':curve(p),'width':w})
for s in [-1,1]:
 quay=19.3 if s<0 else 23
 road('Stone quay avenue '+str(s),[(s*quay,-170),(s*quay,400),(s*quay,1600)],5.8 if s<0 else 7)
 road('Mail road '+str(s),[(s*19,18),(s*95,18),(s*200,18)],7)
 for y in [-54,126,234,378]:road('Bridge approach '+str(s)+' '+str(y),[(s*16,y),(s*42,y),(s*74,y+R.uniform(-12,12)),(s*125,y+R.uniform(-30,30))],6)
 road('Old ridge high street '+str(s),[(s*38,-120),(s*66,-60),(s*102,-10),(s*118,70),(s*85,155),(s*108,205),(s*207,230),(s*197,340),(s*258,460),(s*292,640),(s*350,900),(s*405,1280),(s*420,1600)],8)
 road('Lower winding market street '+str(s),[(s*42,-150),(s*52,-35),(s*68,18),(s*82,110),(s*55,205),(s*90,300),(s*73,440),(s*95,590),(s*77,780),(s*104,1040),(s*116,1550)],5.7)
 road('Terrace contour lane '+str(s),[(s*145,-140),(s*180,-60),(s*226,50),(s*248,155),(s*288,205),(s*324,310),(s*319,450),(s*382,570),(s*415,760),(s*460,970),(s*517,1440)],5)
reserved=[box(-74,27,-22.8,105),box(-201,126,-119,200),box(27.3,-38,53,21),box(27.3,37,55,62),box(63,-37,86,-12)]
reserved.append(box(-30.5,-63,-25,14))
# Existing landmark footprints and gardens are preserved; the old street grid is not.
for x,y in [(-111,144),(143,183),(-179,267),(212,365),(-245,520),(314,695)]:reserved.append(Point(x,y).buffer(16,resolution=12))
reserved_union=unary_union(reserved)
# Every arterial respects the same protected building footprints as the lanes.
clear_arterials=[]
for a in arterials:
 line=LineString(a['points']).difference(reserved_union.buffer(a['width']/2+.5))
 parts=[line] if line.geom_type=='LineString' else list(getattr(line,'geoms',[]))
 for i,p in enumerate(parts):
  if p.geom_type=='LineString' and p.length>4:clear_arterials.append(dict(a,name=a['name']+(' segment '+str(i) if len(parts)>1 else ''),points=[list(v) for v in p.coords]))
arterials=clear_arterials
arterial_mask=unary_union([LineString(a['points']).buffer(a['width']/2+1.3,join_style=1) for a in arterials])
blocks=[];lanes=[];seen=set()
for side in [-1,1]:
 lo,hi=(29,620);ylo,yhi=-150,1620;pts=[]
 # Rejection-sampled sites form genuinely unequal blocks, independent of a grid.
 while len(pts)<240:
  p=(R.uniform(lo,hi),R.uniform(ylo,yhi));spacing=R.uniform(36,57)
  if all((p[0]-a)**2+(p[1]-b)**2>spacing**2 for a,b in pts):pts.append(p)
 pts.extend([(x,y) for x in [-100,800] for y in range(-400,2001,120)]+[(x,y) for y in [-400,2000] for x in range(-100,801,120)])
 vor=Voronoi(pts);bounds=box(lo,ylo,hi,yhi)
 for k in range(240):
  reg=vor.regions[vor.point_region[k]]
  if -1 in reg or not reg:continue
  poly=Polygon(vor.vertices[reg]).intersection(bounds)
  if poly.is_empty:continue
  coords=list(poly.exterior.coords)
  for a,b in zip(coords,coords[1:]):
   aa=(round(side*a[0],3),round(a[1],3));bb=(round(side*b[0],3),round(b[1],3));key=tuple(sorted([aa,bb]))
   if key in seen:continue
   seen.add(key);line=LineString([aa,bb]).difference(reserved_union.buffer(3.4))
   for l in ([line] if line.geom_type=='LineString' else getattr(line,'geoms',[])):
    if l.geom_type=='LineString' and l.length>3:lanes.append({'name':'Old town lane '+str(len(lanes)),'points':[list(p) for p in l.coords],'width':R.uniform(3.6,5.5)})
  poly=Polygon([(side*x,y) for x,y in coords]).buffer(-3.3,join_style=2)
  poly=poly.difference(arterial_mask).difference(reserved_union.buffer(.8))
  pieces=[poly] if poly.geom_type=='Polygon' else getattr(poly,'geoms',[])
  for piece in pieces:
   if piece.area<115:continue
   pp=piece.simplify(.9,preserve_topology=True)
   # Retain irregular perimeter, orient CCW for inward normals.
   from shapely.geometry.polygon import orient
   pp=orient(pp,1);co=[list(v) for v in list(pp.exterior.coords)[:-1]]
   blocks.append({'id':len(blocks),'polygon':co,'area':piece.area,'garden':R.random()<.075,'seed':R.randrange(100000)})
for block in blocks:
 poly=Polygon(block['polygon']);depth=R.uniform(10,16);inner=poly.buffer(-depth,join_style=2)
 while inner.is_empty and depth>4:depth-=1;inner=poly.buffer(-depth,join_style=2)
 block['parcels']=[]
 if inner.is_empty:continue
 co=block['polygon']
 for i,(a,b) in enumerate(zip(co,co[1:]+co[:1])):
  length=math.dist(a,b);n=max(1,round(length/R.uniform(7,12)))
  for k in range(n):
   t0=k/n;t1=(k+1)/n;p0=[a[j]+(b[j]-a[j])*t0 for j in range(2)];p1=[a[j]+(b[j]-a[j])*t1 for j in range(2)]
   q0=list(nearest_points(Point(p0),inner)[1].coords)[0];q1=list(nearest_points(Point(p1),inner)[1].coords)[0];quad=Polygon([p0,p1,q1,q0])
   if quad.is_valid and quad.area>18 and poly.buffer(.15).covers(quad):block['parcels'].append({'quad':[p0,p1,q1,q0],'height':R.uniform(9,20),'variant':R.randrange(100)})
layout={'description':'Organic old-city road graph and irregular perimeter blocks; all points in metres.','blocks':blocks,'roads':arterials+lanes,'reserved':[list(p.exterior.coords) for p in reserved]}
(ROOT/'model/urban-layout.json').write_text(json.dumps(layout,ensure_ascii=False,separators=(',',':')),encoding='utf8')
print('LAYOUT',len(blocks),'irregular blocks,',len(arterials+lanes),'connected road segments')
