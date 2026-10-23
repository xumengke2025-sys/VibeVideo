from pathlib import Path
R=Path(__file__).resolve().parent
for name in ['film/index-v18.html','film/sequences-v18.js','render-v18.mjs','render-batched-v18.mjs','preview-v18.mjs','finalize_v18.py','inspect_transitions_v18.py','inspect_bridges_v18.py','check_assets_v18.py','verify_source_runtime_v18.py']:
    text=(R/name).read_text(encoding='utf8').replace('v18','v19').replace("'version':18","'version':19")
    (R/name.replace('v18','v19')).write_text(text,encoding='utf8')
p=R/'film/sequences-v19.js';s=p.read_text(encoding='utf8').replace('whole-pair crown-to-seat scale registration and dual-matte RGBA on a shared continuous actor timeline','independent infant skull-arc size registration with protected adult face and seamless shared-contact mapping; dual-matte RGBA');p.write_text(s,encoding='utf8')
p=R/'CHECKPOINT.md';p.write_text('''# v19：单独修复婴儿大小变化（进行中）

- 用户明确指出v18婴儿仍忽大忽小，要求彻底修复。上一版仅锁定妈妈坐姿高度，不足以约束婴儿；不再以妈妈高度当宝宝验收指标。
- 沿用40秒、20时代、1080×1920、9:16、24fps、有意无声；delivery_mode=ai_review_once历史预算已用完，不新增审片角色。
- 新测量measure_infant_v19.py：拟合婴儿头发外侧不透明边界上弧，排除衣领、手、奶瓶；初次暗色整块和单纯肤色宽度方法不可靠，已替换。
- build_infant_v19.py对婴儿单独校准，完整连续坐标场保护透明空隙和接触；母亲面部固定区。样场0/4/16/17/18/19正在二次试验。最终需全片动作、连接、边界和编码后检查，不能仅看妈妈大小宣布通过。
- 下一步：查看样场与动态参数，完整重建/渲染v19，打包源码，记录实际范围与剩余问题。

'''+p.read_text(encoding='utf8'),encoding='utf8')
print('v19 renderer entries and checkpoint ready')
