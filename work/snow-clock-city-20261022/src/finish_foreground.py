"""Close the foreground snowbank skirt so the reveal never sees under a sheet."""
import bpy,bmesh,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(R/'model/clock-city-production-v4.blend'))
ob=bpy.data.objects['Near snow bank'];me=ob.data
bm=bmesh.new();bm.from_mesh(me)
boundary=[e for e in bm.edges if e.is_boundary]
bottom={v:bm.verts.new((v.co.x,v.co.y,-2)) for e in boundary for v in e.verts}
for e in boundary:
 a,b=e.verts;bm.faces.new((a,b,bottom[b],bottom[a]))
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();me.update()
bpy.ops.wm.save_as_mainfile(filepath=str(R/'model/clock-city-production-v5.blend'))
print('CLOSED_BANK_READY',len(boundary),flush=True)
