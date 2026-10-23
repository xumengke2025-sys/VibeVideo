from pathlib import Path
R=Path(__file__).resolve().parent
p=(R/'package_source_v17.py').read_text(encoding='utf8').replace('v17','v18').replace('version=17','version=18').replace("'version':17","'version':18").replace("'17.0.0'","'18.0.0'")
p=p.replace('assets/bridges-v18','assets/bridges-v17').replace('PLAN-v18-continuity.md','PLAN-v17-continuity.md').replace("'inspect_sample_v18.py',",'')
p=p.replace("'build_continuity_v18.py',","'build_continuity_v18.py','build_continuity_v17.py','check_scale_v18.py',")
p=p.replace("files.add(R/'clean_matte_v18.py')","files.add(R/'clean_matte_v17.py')")
p=p.replace('- 整组重新注册坐姿，以首姿态锁住低位凳脚、坐垫和落脚区；不拆拼人物手臂，不叠加周期性全身摇摆。','- 以发顶到坐姿支撑点的高度统一缩放完整双人姿态，固定坐姿基线；不拆拼或单独拉伸手臂。\n- 黑底与白底分别补帧，再重建RGBA透明通道，保留手臂间的封闭透明空隙与白色服装。')
p=p.replace('Complete generated pairs with newly generated recovery poses; shared continuous actor timeline; exact actor endpoint handoff; room-only era mattes; fixed interior and exterior life','Whole-pair crown-to-seat scale registration; dual-matte RGBA reconstruction; continuous actor timeline and room-only era transitions')
p=p.replace("'qa/v18/*.json',","'qa/v18/*.json','qa/v18/scale-board-*.jpg','qa/v18/alpha-before-after.jpg',")
(R/'package_source_v18.py').write_text(p,encoding='utf8')
p=R/'verify_source_runtime_v18.py';p.write_text(p.read_text(encoding='utf8').replace("'version':17","'version':18"),encoding='utf8')
print('v18 packaging prepared')
