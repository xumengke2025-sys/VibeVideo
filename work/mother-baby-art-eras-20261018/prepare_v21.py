from pathlib import Path
import re
R=Path(__file__).resolve().parent
for name in ['film/index-v20.html','film/sequences-v20.js','render-v20.mjs','render-batched-v20.mjs','preview-v20.mjs']:
    text=(R/name).read_text(encoding='utf8').replace('v20','v21')
    # The environment and stationary cushions retain their verified v20 assets.
    if name.startswith('film/'):
        text=text.replace('environment-life-v21.js','environment-life-v20.js').replace('ENV_LIFE_V21','ENV_LIFE_V20')
        text=text.replace('../assets/motion-v21/cushions-atlas.png','../assets/motion-v20/cushions-atlas.png')
    if name.endswith('sequences-v20.js'):
        text=re.sub(r'function caption\(.*?\n','',text)
        text=text.replace("if(transition)caption(transition.p<.5?transition.from:transition.to,Math.abs(2*transition.p-1));else caption(i);",'')
        text=text.replace("await Promise.all([document.fonts.load('500 30px \"Microsoft YaHei\"'),document.fonts.load('22px Georgia')]);await document.fonts.ready;",'')
        text=text.replace('*(end-start))*47)', '*(end-start))*47)') # explicit replacements below
        text=text.replace('clamp((absolute-start)/(end-start))*47','clamp((absolute-start)/(end-start))*(sequences[i].info.frames-1)')
        text=text.replace('hash(sequences[k-1],47)','hash(sequences[k-1],sequences[k-1].info.frames-1)')
        text=text.replace("route:'v19 infant size retained byte-for-byte above support; independently fixed cushion layer; local rooted environment motion'","route:'text-free; exact-clock optical-flow resampling; local hand/prop matte repair; fixed infant scale and independent cushion'")
    (R/name.replace('v20','v21')).write_text(text,encoding='utf8')
(R/'qa/v21').mkdir(parents=True,exist_ok=True)
p=R/'CHECKPOINT.md';old=p.read_text(encoding='utf8')
p.write_text('''# v21：去文字与动作局部修复（制作中）

- objective: 去除全部入镜文字；修复递扇、喝奶等手/道具拖影及动作跳帧；检查结尾放杯换手。
- aspect_ratio=9:16; width=1080; height=1920; fps=24; duration=40; 20时代；有意无声。
- delivery_mode=ai_review_once；历史一轮已耗尽，本次为主制作角色定向检查，不新增独立角色。
- baseline: v20成片与源码保留。已实际查看20时代各5姿态和递扇/喝奶/结尾各24连续编码帧。
- findings: 48姿态被取整压入不同长动作段，跳过的步长交替；双底补间手/道具有局部透明拖影；结尾杯子跨手太快。
- protection: 宝宝头部尺度、固定坐垫与大地毯、既有背景局部活动、人物连续连接和画幅。
- next: 在正式尺寸验证手/道具局部修复和按实际可用时长重新采样，随后全片导出、解码及源码打包。尚未声称问题已解决。

'''+old,encoding='utf8')
print('v21 entries prepared')
