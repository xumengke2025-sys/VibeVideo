"""Narrow masonry footings and connected door approaches for the shared world.

Usage, after film_world.build() assemblies and roads exist, before saving:
    import world_grounding as G
    report = G.add_grounding()

Does not clear or rebuild the world. XY layout is never silently changed.
Run with system Python to write the numeric-only report, without Blender:
    python src/world_grounding.py
All footprint dimensions are metres, relative to asset ground roots; -Y is front.
"""
from pathlib import Path
import ast
import json
import math
import heapq
import hashlib
from datetime import datetime, timezone
from types import SimpleNamespace

R = Path(__file__).resolve().parents[1]
# Rectangles: local centre x/y, width/depth. Include low attached structures.
FOOTPRINTS = {
    'inn': [(0, 0, 6.7, 5.4), (4.1, .85, 2.8, 4.5), (0, -3.36, 6.4, 1.45)],
    'workshop': [(0, 0, 4.6, 5.2), (2.79, .11, 1.03, 3.68)],
    'grocer': [(0, 0, 5.7, 4.7), (0, -2.94, 5.2, 1.25)],
    'cottage': [(0, 0, 4.25, 4.6), (-2.68, .5, 1.1, 3.2)],
    'chapel': [(0, 0, 4.9, 8.4)],
    'tower': [(0, 0, 3.8, 3.8)],
    'bakery': [(0, 0, 7.0, 5.9)],
}
# Door x, facade y, width; inn approach begins beyond its covered porch.
DOORS = {'inn': (0, -4.13, 1.25), 'workshop': (1.49, -2.77, 1.0),
         'grocer': (.65, -3.60, 1.05), 'cottage': (1.12, -2.46, 1.0),
         'chapel': (0, -4.39, 1.65), 'tower': (0, -2.07, 1.2),
         'bakery': (0, -3.12, 1.3)}


def _ground_function():
    """Compile only the authoritative pure terrain functions; no bpy import."""
    tree = ast.parse((R/'src/alpine_environment.py').read_text(encoding='utf8'))
    selected = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in ('smooth', 'ground')]
    env = {'math': math}
    exec(compile(ast.Module(body=selected, type_ignores=[]), 'ground-extract', 'exec'), env)
    return env['ground']


ground = _ground_function()


def world_xy(item, x, y):
    c, s = math.cos(item['rotation']), math.sin(item['rotation'])
    sc = item['scale']
    return (item['x']+sc*(c*x-s*y), item['y']+sc*(s*x+c*y))


def local_xy(item, x, y):
    dx, dy = x-item['x'], y-item['y']
    c, s = math.cos(item['rotation']), math.sin(item['rotation'])
    return ((c*dx+s*dy)/item['scale'], (-s*dx+c*dy)/item['scale'])


def placements():
    tree = ast.parse((R/'src/film_world.py').read_text(encoding='utf8'))
    values = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in ('placements', 'houses'):
                    values[target.id] = ast.literal_eval(node.value)
    items=[]
    for typ, (x,y,rot) in values['placements'].items():
        items.append(dict(name='ARCH_'+typ.upper(), type=typ, x=x, y=y, rotation=rot, scale=1.0))
    items.append(dict(name='Hill bakery', type='bakery', x=-15, y=26, rotation=0.0, scale=1.0))
    for i,(typ,x,y,rot,sc) in enumerate(values['houses']):
        items.append(dict(name='Neighbourhood '+str(i), type=typ, x=x, y=y, rotation=rot, scale=sc))
    return items


def road_samples():
    tree=ast.parse((R/'src/film_world.py').read_text(encoding='utf8'))
    fn=next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name=='roadpath')
    points=ast.literal_eval(next(n.value for n in fn.body if isinstance(n, ast.Assign) and any(isinstance(t,ast.Name) and t.id=='pts' for t in n.targets)))
    out=[]
    for i in range(len(points)-1):
        pp=[points[max(0,i-1)],points[i],points[i+1],points[min(len(points)-1,i+2)]]
        for j in range(44):
            t=j/44
            out.append(tuple(.5*(2*pp[1][k]+(-pp[0][k]+pp[2][k])*t+(2*pp[0][k]-5*pp[1][k]+4*pp[2][k]-pp[3][k])*t*t+(-pp[0][k]+3*pp[1][k]-3*pp[2][k]+pp[3][k])*t*t*t) for k in (0,1)))
    out.append(points[-1])
    return out


def distance(item, point):
    x,y=local_xy(item,*point)
    return min(math.hypot(max(abs(x-cx)-w/2,0),max(abs(y-cy)-d/2,0))*item['scale'] for cx,cy,w,d in FOOTPRINTS[item['type']])


def footprint_grid(item):
    for cx,cy,w,d in FOOTPRINTS[item['type']]:
        for j in range(7):
            for i in range(7):
                yield world_xy(item,cx-w/2+w*i/6,cy-d/2+d*j/6)


def envelopes_overlap(a,b,margin=.30):
    """Separating-axis test of compound rotated ground rectangles."""
    for acx,acy,aw,ad in FOOTPRINTS[a['type']]:
        pa=[world_xy(a,acx+sx*aw/2,acy+sy*ad/2) for sx,sy in [(-1,-1),(1,-1),(1,1),(-1,1)]]
        for bcx,bcy,bw,bd in FOOTPRINTS[b['type']]:
            pb=[world_xy(b,bcx+sx*bw/2,bcy+sy*bd/2) for sx,sy in [(-1,-1),(1,-1),(1,1),(-1,1)]]
            separated=False
            for angle in [a['rotation'],a['rotation']+math.pi/2,b['rotation'],b['rotation']+math.pi/2]:
                c,s=math.cos(angle),math.sin(angle)
                aa=[x*c+y*s for x,y in pa];bb=[x*c+y*s for x,y in pb]
                if max(aa)+margin<min(bb) or max(bb)+margin<min(aa):separated=True;break
            if not separated:return True
    return False


def network_samples():
    result=road_samples()
    # Extract production polylines so layout corrections also move entrances.
    for name,points,width in side_lanes():
        for a,b in zip(points,points[1:]):
            result.extend((a[0]+(b[0]-a[0])*i/100,a[1]+(b[1]-a[1])*i/100) for i in range(101))
    for i in range(41):
        result.extend([(-6+18*i/40,-4.5),(-6+18*i/40,6.5),(-6,-4.5+11*i/40),(12,-4.5+11*i/40)])
    # Pedestrian stair is also part of the existing public network.
    result.extend((3.5,7+i*.4) for i in range(37))
    return result


def source_literal(name,default=None):
    tree=ast.parse((R/'src/film_world.py').read_text(encoding='utf8'))
    for n in ast.walk(tree):
        if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets):
            return ast.literal_eval(n.value)
    return default


def side_lanes():
    updated=source_literal('side_lanes')
    if updated is not None:return updated
    return [('Upper bakery lane',[(-26,21),(-5,22)],2.5),
            ('Eastern market lane',[(13,-13),(17,24)],2.5),
            ('Western craftsmen lane',[(-23,5),(-18,16)],2.1)]


def station_checks(obstacles, resident_paths, road):
    """Capture only landing()'s CPU geometry, using the actual current algorithm."""
    boxes=[]
    class MeshCapture:
        def box(self, centre, size, material, **kwargs):
            boxes.append((tuple(centre),tuple(size)))
        def beam(self, *args, **kwargs):pass
        def obj(self, *args, **kwargs):pass
    tree=ast.parse((R/'src/film_world.py').read_text(encoding='utf8'))
    fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='landing')
    env={'E':SimpleNamespace(ground=ground),'C':SimpleNamespace(Mesh=MeshCapture,ST=None,DK=None,WO=None)}
    exec(compile(ast.Module(body=[fn],type_ignores=[]),'landing-numeric-capture','exec'),env)
    stations=[]
    origins=[(ast.literal_eval(n.args[0]),ast.literal_eval(n.args[1])) for n in ast.walk(tree)
             if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='landing']
    for name,xy in origins:
        boxes.clear();platform=env['landing'](name,xy)
        # Production treads have a 1.5m walking width; footings are .405m squares.
        stairs=[(p,s) for p,s in boxes if abs(s[1]-1.5)<1e-6]
        footings=[(p,s) for p,s in boxes if abs(s[0]-.405)<1e-6 and abs(s[1]-.405)<1e-6]
        def distance_box(p,centre,size):
            return math.hypot(max(abs(p[0]-centre[0])-size[0]/2,0),max(abs(p[1]-centre[1])-size[1]/2,0))
        walking=stairs+[((xy[0]+.65,xy[1],platform[2]),(6,4.4,.26))]
        resident_hits=[]
        for resident,points in resident_paths:
            clear=min(distance_box(p,c,s) for p in points for c,s in walking)-.30
            if clear<0:resident_hits.append({'resident':resident,'body_edge_clearance_m':round(clear,4)})
        building_hits=[]
        for ob in obstacles:
            # Dense per-rectangle surface samples also cover long attached stairs.
            clear=min(distance(ob,(c[0]+s[0]*(i/4-.5),c[1]+s[1]*(j/8-.5))) for c,s in walking for i in range(5) for j in range(9))
            if clear<=.001:building_hits.append(ob['name'])
        first,first_size=stairs[0];last,last_size=stairs[-1]
        tops=[p[2]+s[2]/2 for p,s in stairs]
        stair_road=min(distance_box(p,c,s) for p in road for c,s in stairs)-2.2
        footing_gaps=[p[2]-s[2]/2-ground(p[0]+sx*s[0]/2,p[1]+sy*s[1]/2) for p,s in footings for sx in [-1,1] for sy in [-1,1]]
        stations.append({'name':name,'origin_xy':xy,'geometry_source':'actual film_world.landing extracted and executed with pure CPU box capture',
                         'treads':len(stairs),'first_tread_xy':list(first[:2]),'first_tread_top_above_local_terrain_m':round(tops[0]-ground(*first[:2]),4),
                         'riser_min_m':round(min(b-a for a,b in zip(tops,tops[1:])),4),'riser_max_m':round(max(b-a for a,b in zip(tops,tops[1:])),4),
                         'last_tread_to_gallery_height_error_m':round(tops[-1]-(platform[2]+.4),6),
                         'tread_to_gallery_horizontal_gap_m':round(last[0]-last_size[0]/2-(xy[0]+3.65),6),
                         'maximum_footing_corner_gap_above_terrain_m':round(max(footing_gaps),4),
                         'stair_to_carriage_road_edge_clearance_m':round(stair_road,4),
                         'building_footprint_intersections':building_hits,'resident_path_conflicts':resident_hits})
    return stations


def cpu_spatial_checks(items):
    """Frame-time path envelopes and terrain heights; never imports Blender."""
    obstacles=items+[dict(name='Waterwheel house',type='cottage',x=-27.8,y=15,rotation=math.pi/2,scale=.68)]
    source_lanes=source_literal('lanes',[])
    resident_lanes=[(-3,-5,1,0,2)]+source_lanes
    residents=[];resident_paths=[]
    for index,(x,y,dx,dy,span) in enumerate(resident_lanes):
        phase=0 if index==0 else (index-1)*1.731
        points=[(x+dx*span*math.sin((math.floor(j/24*12)/12)*.14+phase),
                 y+dy*span*math.sin((math.floor(j/24*12)/12)*.14+phase)) for j in range(2161)]
        hits=[];minimum=1e9
        for ob in obstacles:
            clearance=min(distance(ob,p) for p in points)
            minimum=min(minimum,clearance)
            if clearance<.30:hits.append({'building':ob['name'],'centre_to_footprint_m':round(clearance,4)})
        residents.append({'name':'Resident %02d'%index,'base_xy':[x,y],'axis':[dx,dy],'span':span,
                          'body_radius_assumption_m':.30,'minimum_body_clearance_m':round(minimum-.30,4),'building_conflicts':hits})
        resident_paths.append(('Resident %02d'%index,points))
    lane_checks=[]
    for name,poly,width in side_lanes():
        points=[(a[0]+(b[0]-a[0])*j/100,a[1]+(b[1]-a[1])*j/100) for a,b in zip(poly,poly[1:]) for j in range(101)]
        hits=[];minimum=1e9
        for ob in obstacles:
            clear=min(distance(ob,p) for p in points)-width/2
            minimum=min(minimum,clear)
            if clear<0:hits.append({'building':ob['name'],'lane_edge_clearance_m':round(clear,4)})
        lane_checks.append({'name':name,'polyline_xy':poly,'width_m':width,'minimum_building_clearance_m':round(minimum,4),'building_conflicts':hits})
    road=road_samples();dist=0;segments=[]
    for a,b in zip(road,road[1:]):
        planar=math.dist(a,b);dz=ground(*b)-ground(*a);dist+=math.hypot(planar,dz)
        segments.append({'grade':abs(dz/planar),'distance':dist,'xy':[(a[0]+b[0])/2,(a[1]+b[1])/2]})
    maxgrade=max(segments,key=lambda p:p['grade']);used=[p for p in segments if 8<=p['distance']<=51.2]
    road_hits=[{'building':ob['name'],'road_edge_clearance_m':round(min(distance(ob,p) for p in road)-2.2,4)} for ob in obstacles if min(distance(ob,p) for p in road)<2.2]
    stations=station_checks(obstacles,resident_paths,road)
    return {'verification_type':'independent pure CPU numeric checks; not independent audiovisual review',
            'resident_time_range_s':[0,90],'resident_time_samples':2161,
            'residents':residents,'side_lanes':lane_checks,
            'carriage_road':{'length_m':round(dist,4),'maximum_grade_percent':round(maxgrade['grade']*100,3),'maximum_grade_xy':maxgrade['xy'],
                             'animation_travel_distance_m':[8,51.2],'actual_used_maximum_grade_percent':round(max(p['grade'] for p in used)*100,3),
                             'building_conflicts_including_waterwheel_house':road_hits},
            'station_construction':stations,
            'station_check_limit':'CPU box capture excludes rail beams, hand contact, exact triangles and audiovisual assessment. Building intersections use dense rectangle samples.'}


def _route(start, target, obstacles):
    """Short 0.65m grid search avoiding every other building envelope."""
    step=.65
    def cell(p): return (round(p[0]/step),round(p[1]/step))
    def pos(p): return (p[0]*step,p[1]*step)
    a,b=cell(start),cell(target);front=[(0,a)];came={};cost={a:0};done=set()
    for _ in range(6500):
        if not front: break
        _,u=heapq.heappop(front)
        if u in done: continue
        done.add(u)
        if math.dist(pos(u),target)<.9:
            path=[target,pos(u)]
            while u in came:
                u=came[u];path.append(pos(u))
            return [start]+list(reversed(path))[1:]
        for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]:
            v=(u[0]+dx,u[1]+dy);p=pos(v)
            if abs(p[0]-start[0])>30 or abs(p[1]-start[1])>30: continue
            if any(distance(ob,p)<.63 for ob in obstacles):continue
            new=cost[u]+math.hypot(dx,dy)
            if new<cost.get(v,1e30):
                cost[v]=new;came[v]=u;heapq.heappush(front,(new+math.dist(p,target)/step,v))
    return None


def analyze():
    items=placements();road=road_samples();network=network_samples();records=[];conflicts=[]
    for item in items:
        heights=[ground(*p) for p in footprint_grid(item)]
        floor=max(heights)+.08
        record={**item,'original_floor_z':ground(item['x'],item['y']), 'floor_z':floor,
                'lift_m':floor-ground(item['x'],item['y']), 'max_foundation_exposure_m':floor-min(heights)}
        minimum=min(distance(item,p) for p in road)
        record['road_edge_clearance_m']=minimum-2.2
        if minimum<2.2:
            recommendation=None
            # Keep a full 20 cm buffer outside the 4.4m carriage corridor.
            for ring in range(1,21):
                candidates=[]
                for j in range(32):
                    angle=j*math.tau/32;dx=.5*ring*math.cos(angle);dy=.5*ring*math.sin(angle)
                    candidate={**item,'x':item['x']+dx,'y':item['y']+dy}
                    clearance=min(distance(candidate,p) for p in road)-2.2
                    if clearance>=.20:
                        if any(envelopes_overlap(candidate,ob) for ob in items if ob['name']!=item['name']):continue
                        candidates.append((abs(dy)*.2,dict(x=round(candidate['x'],3),y=round(candidate['y'],3),dx=round(dx,3),dy=round(dy,3),road_edge_clearance_m=round(clearance,3))))
                if candidates:
                    recommendation=min(candidates,key=lambda p:p[0])[1];break
            conflicts.append({'name':item['name'],'clearance_m':round(minimum-2.2,3),'recommendation_xy':recommendation,'applied':False})
        door=DOORS[item['type']];entry=world_xy(item,door[0],door[1]-.32)
        # Start the public connector after an independent 1.5m door stair.
        start=world_xy(item,door[0],door[1]-.32-1.50/item['scale'])
        other=items
        targets=sorted(network,key=lambda p:math.dist(start,p))[:80:8]
        route=None
        for target in targets:
            if any(distance(ob,target)<.65 for ob in other):continue
            route=_route(start,target,other)
            if route:break
        record['door_entry_xy']=entry;record['stair_end_xy']=start
        record['approach_path_xy']=route
        record['approach_status']='connected_numeric_grid' if route else 'requires_layout_adjustment'
        records.append(record)
    overlaps=[(a['name'],b['name']) for i,a in enumerate(items) for b in items[i+1:] if envelopes_overlap(a,b,0)]
    return {'status':'numeric_only_not_rendered','source':'AST extraction of film_world placements/houses/roadpath and alpine_environment.ground',
            'generated_utc':datetime.now(timezone.utc).isoformat(),
            'source_sha256':{name:hashlib.sha256((R/'src'/name).read_bytes()).hexdigest() for name in ['film_world.py','alpine_environment.py','world_grounding.py']},
            'road_width_m':4.4,'building_count':len(items),'road_conflicts':conflicts,'buildings':records,
            'building_footprint_overlaps':overlaps,
            'cpu_spatial_checks':cpu_spatial_checks(items),
            'limitations':['Footprint OBB distance to dense spline samples, not exact triangle collision. Roof overhangs are excluded from ground-road checks.',
             'Building roots will be lifted. Production film_world emits chimney smoke after grounding; this numeric report does not verify emitter-to-mesh contact.',
             'Waterwheel house is excluded: moving its root requires moving its separate axle/wheel together.',
             'No GPU render or aesthetic/animation acceptance was performed. XY recommendations are not applied.']}


def add_grounding(roots=None, report_path=None):
    """Apply footings to existing scene roots; return JSON-serializable evidence.

    roots may be a name->Blender-object mapping; omitted finds named scene roots.
    Repeated calls are safe: original floors are stored on the building roots,
    generated GROUNDING meshes are replaced, not accumulated. No XY mutation.
    """
    import bpy
    import craft as C
    from mathutils import Matrix,Vector
    result=analyze();built=[];missing=[]
    for ob in list(bpy.data.objects):
        if ob.get('world_grounding_generated'):bpy.data.objects.remove(ob,do_unlink=True)
    for record in result['buildings']:
        root=(roots or {}).get(record['name']) if roots is not None else bpy.data.objects.get(record['name'])
        if root is None:missing.append(record['name']);continue
        # Actual XY may have been manually adjusted according to the report.
        item={**record,'x':root.location.x,'y':root.location.y,'rotation':root.rotation_euler.z,'scale':root.scale.x}
        floor=max(ground(*p) for p in footprint_grid(item))+.08
        if 'grounding_original_z' not in root:root['grounding_original_z']=float(root.location.z)
        root.location.z=floor;root['grounding_floor_z']=floor
        mesh=C.Mesh();sc=item['scale']
        def emit(local,faces,material):mesh.add(local,faces,material)
        # A 22cm thick wall, subdivided into individually fitted courses.
        # Each wall bottom follows terrain; no broad rectangular terrain plinth.
        for cx,cy,w,d in FOOTPRINTS[item['type']]:
            for a,b in [((cx-w/2,cy-d/2),(cx+w/2,cy-d/2)),((cx+w/2,cy-d/2),(cx+w/2,cy+d/2)),((cx+w/2,cy+d/2),(cx-w/2,cy+d/2)),((cx-w/2,cy+d/2),(cx-w/2,cy-d/2))]:
                length=math.dist(a,b);n=max(1,math.ceil(length/.54));dx=(b[0]-a[0])/length;dy=(b[1]-a[1])/length
                for j in range(n):
                    u=j/n;v=(j+1)/n;px=a[0]+(b[0]-a[0])*(u+v)/2;py=a[1]+(b[1]-a[1])*(u+v)/2
                    level=(ground(*world_xy(item,px,py))-floor)/sc-.07
                    courses=max(1,math.ceil((-level+.025)/.23))
                    for k in range(courses):
                        lo=level+k*(-level+.025)/courses;hi=level+(k+1)*(-level+.025)/courses
                        rot=Matrix.Rotation(math.atan2(dy,dx),3,'Z')
                        mesh.box((px,py,(lo+hi)/2),(length/n-.012,.24,hi-lo-.012),C.ST,rot,jitter=.004,seed=j+13*k)
        foundation=mesh.obj('GROUNDING | '+root.name+' | fitted masonry',root,.010)
        foundation['world_grounding_generated']=True
        # Door stair, world coordinates, with steps meeting the existing terrain.
        dx,dy,dw=DOORS[item['type']];entry=world_xy(item,dx,dy-.32);end=world_xy(item,dx,dy-.32-1.50/sc)
        top=floor+.025;bottom=ground(*end)+.15;n=max(1,math.ceil(max(0,top-bottom)/.17));run=1.50/n
        steps=C.Mesh();rot=Matrix.Rotation(item['rotation'],3,'Z')
        for j in range(n):
            t=(j+.5)/n;xx=entry[0]+(end[0]-entry[0])*t;yy=entry[1]+(end[1]-entry[1])*t
            high=top+(bottom-top)*(j/n);base=min(ground(xx,yy)-.05,high-.06)
            steps.box((xx,yy,(base+high)/2),(max(1.05,dw*sc),run+.012,high-base),C.ST,rot)
        stair=steps.obj('GROUNDING | '+root.name+' | doorstep stair',None,.012);stair['world_grounding_generated']=True
        # Recompute connector after any approved layout edits. Avoid buildings.
        other=[item if o['name']==root.name else o for o in placements()]
        targets=sorted(network_samples(),key=lambda p:math.dist(end,p))[:100:10];route=None
        for target in targets:
            if any(distance(ob,target)<.65 for ob in other):continue
            route=_route(end,target,other)
            if route:break
        if route:
            pathmesh=C.Mesh()
            for a,b in zip(route,route[1:]):
                length=math.dist(a,b)
                if length<.001:continue
                rot=Matrix.Rotation(math.atan2(b[1]-a[1],b[0]-a[0])+math.pi/2,3,'Z')
                for j in range(max(1,math.ceil(length/.28))):
                    t=(j+.5)/max(1,math.ceil(length/.28));xx=a[0]+(b[0]-a[0])*t;yy=a[1]+(b[1]-a[1])*t
                    for side in [-1,0,1]:
                        v=rot@Vector((side*.30,0,0));x=xx+v.x;y=yy+v.y
                        pathmesh.box((x,y,ground(x,y)+.145),(.285,length/max(1,math.ceil(length/.28))+.015,.10),C.ST,rot)
            path=pathmesh.obj('GROUNDING | '+root.name+' | connected cleared footway',None,.008);path['world_grounding_generated']=True
        built.append({'name':root.name,'floor_z':floor,'lift_m':floor-float(root['grounding_original_z']),'approach_connected':bool(route)})
    result['status']='applied_in_existing_blender_scene_not_rendered';result['applied']=built;result['missing_roots']=missing
    path=Path(report_path) if report_path else R/'render/grounding-report.json'
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    return result


if __name__=='__main__':
    report=analyze();path=R/'render/grounding-report.json';path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps({'report':str(path),'buildings':report['building_count'],'road_conflicts':report['road_conflicts'],
                      'missing_approaches':[b['name'] for b in report['buildings'] if not b['approach_path_xy']]},ensure_ascii=False))
