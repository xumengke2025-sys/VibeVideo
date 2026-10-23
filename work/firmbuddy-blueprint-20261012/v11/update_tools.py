from pathlib import Path
import json
R=Path(__file__).resolve().parent
old=R.parent/'v10'
s=(old/'check_layout.mjs').read_text(encoding='utf-8').replace('/v10/','/v11/').replace('layout-v10','layout-v11')
s=s.replace('try{\n browser=',"windows.forEach(w=>w.range=w.range.map(t=>t+8));windows[0].range=[11.1,11.5];windows.unshift({range:[1.5,3.3],texts:['商机收集耗时长','不知从何入手','信息归集不全','专业支持难找']},{range:[4.9,6.3],texts:['商机查询','治理整改','并购重组','股东减持','风险管理','上市与分拆']});\ntry{\n browser=")
(R/'check_layout.mjs').write_text(s,encoding='utf-8')
s=(old/'check_motion.mjs').read_text(encoding='utf-8').replace('motion-v10','motion-v11').replace('time:t,position','time:t+8,position')
(R/'check_motion.mjs').write_text(s,encoding='utf-8')
(R/'make_audio.py').write_text("from pathlib import Path\nimport runpy\nrunpy.run_path(str(Path(__file__).with_name('make_opening_audio.py')),run_name='__main__')\n",encoding='utf-8')
print('Updated V11 reading windows, camera checks and audio entry point')
