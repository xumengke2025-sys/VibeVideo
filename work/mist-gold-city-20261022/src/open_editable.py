"""Launch Blender with the editable world and deterministic animated timeline.
blender --python src/open_editable.py
Animation is procedural (source editable), not baked simulation caches.
"""
import sys,os,runpy
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[1]
os.environ['FOG_PERCENT']='50'
sys.argv=['blender','--','editor']
ns=runpy.run_path(str(ROOT/'src/render_film.py'))
scene=bpy.context.scene
scene.frame_start=1;scene.frame_end=2160;scene.render.fps=24
def update_frame(scene,*args):
 ns['at']((scene.frame_current-1)/24,set_frame=False)
update_frame._fog_city=True
bpy.app.handlers.frame_change_post[:]=[h for h in bpy.app.handlers.frame_change_post if not getattr(h,'_fog_city',False)]
bpy.app.handlers.frame_change_post.append(update_frame)
scene.frame_set(1201)
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA'
print('Editable procedural film ready. Scrub frames 1–2160. Use source to change event timing.')
