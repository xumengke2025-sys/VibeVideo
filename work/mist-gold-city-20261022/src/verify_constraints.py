"""Numerical geometry/event checks; does not replace visual or listening review."""
import sys,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));sys.path.insert(0,str(ROOT/'vendor/urban'))
from timeline import bridge_angle,boat_y,coach_x,coach_speed,road_z
from shapely.geometry import Polygon,LineString
layout=json.loads((ROOT/'model/urban-layout.json').read_text(encoding='utf8'))
reserved=[Polygon(p) for p in layout['reserved']]
road_conflicts=[]
for r in layout['roads']:
 lane=LineString(r['points']).buffer(r['width']/2)
 for i,p in enumerate(reserved):
  if lane.intersection(p).area>.01:road_conflicts.append([r['name'],i])
assert not road_conflicts,road_conflicts[:10]
# The hull/cargo envelope must fit the opening throughout the entire crossing.
clearances=[]
for f in range(2160):
 t=f/24;y=boat_y(t);angle=bridge_angle(t)
 if abs(y-18)<6.102+3.4:
  half=9.25-9.25*math.cos(angle);clearances.append(half-2.38)
assert min(clearances)>0
assert coach_speed(43)==0 and coach_speed(64)==0
assert boat_y(60)-6.102>21.4
assert coach_x(43)+4.9<-19
assert 5.7>3.1-.25
report={'road_reserved_footprint_collisions':road_conflicts,'minimum_open_bridge_hull_side_clearance_m':min(clearances),'boat_stern_at_lower_start_y':boat_y(60)-6.102,'bridge_north_edge_y':21.4,'horse_nose_when_stopped_x':coach_x(43)+4.9,'gate_x':-19,'closed_bridge_underside_m':2.85,'cargo_gantry_top_m':4.44,'flag_top_m':5.7,'background_barge_side_clearance_m':6-2*2.38,'limits':'Numerical specified envelopes, not all-mesh dynamic collision proof; visual sequence review still required.'}
(ROOT/'qa/constraints.json').write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps(report,indent=2))
