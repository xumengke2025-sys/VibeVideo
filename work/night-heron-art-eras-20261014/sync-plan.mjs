import fs from 'node:fs';
const f=new URL('production-plan.json',import.meta.url),p=JSON.parse(fs.readFileSync(f));
p.direction.promise='同一只夜鹭经过十六种艺术史意象，以同一节拍和动作偷吃身边动物已经捕获、放在地上的鱼。';
p.direction.alternatives[1].event='同一编舞，每时代更换画风与鱼的主人';
for(const s of p.timeline.shots){s.camera={subjectId:'heron_main',method:'固定侧视构图，保持身体、鱼和旁边动物的屏幕锚点；背景轻微横移与脚步表现行进意象。',worldPath:'未实现真实世界长距离跟拍；以同一构图匹配跨时代。',relativeOffset:'保持侧视距离，叼鱼处不切机位。',lookAt:'统一构图中以伸颈与鱼移动交接注意力。',screenRegions:{heron:[.1,.45,.68,.76],opponent:[.69,.40,.98,.65],fish:[.58,.62,.78,.72]}};}
p.implementation={concept:'out/concept-v3/styleboard.jpg',sample:'out/sample-v1/video.mp4',sampleDuration:6.75,conceptFeedback:'用户已授权执行并补充统一动作；效果图已在对话展示，未将沉默记作认可。',renderMethod:'原生Canvas可寻址时间轴、逐帧输出、FFmpeg合成',historicalScope:'艺术史意象而非考古、动物栖息地或名画精确复原'};
p.audio={clock:'全片固定106.6667 BPM，每时代2.25秒4拍；视觉接触和合成木质音均在时代起点后1.035秒。',design:'原创程序合成拨弦动机、低音、钟音、笛音和刷奏噪声；整片同一节拍，无旁白、无动物抵抗音效。',reuse:'未复用旧片录音或外部音乐。',license:'本工程原创声音代码与编排。',evidence:'audio/events.json记录事件和峰值/RMS；真实听音未完成。'};
p.workflow=[{name:'代码研究',status:'complete',deliverable:'research/contact.jpg 与 coverage.json，实际范围如实记录。'},{name:'效果图先行',status:'complete',deliverable:'concept-v3，已展示代表竖屏图，用户授权连续执行。'},{name:'动作与转场样段',status:'complete',deliverable:'sample-v1，6.75秒正式画幅：埃及→黑绘陶→马赛克。'},{name:'扩展16时代',status:'complete',deliverable:'40秒正式竖屏片，960帧。'},{name:'基本工程检查',status:'complete',deliverable:'全片解码、1080×1920/24fps/40秒/960帧/双声道AAC及确定寻址。'},{name:'AI审核一轮',status:'in_progress',deliverable:'唯一审片者实际检查成片；最多一次修复及必要复核；如实记录音频工具限制。'}];
p.openQuestions=['完整审核实际覆盖与剩余问题见qa/film-v1；不能以音频技术检查替代听音。'];
p.phases=p.workflow.map((s,i)=>({step:i+1,...s,done:s.status==='complete'}));p.openItems=p.openQuestions;
p.visualSystem.styleRules='每风格使用同一骨架与节拍，分别实现轮廓、线条、色板、纹理与场景；未复用旧PNG。';
p.visualSystem.transitions='每个时代边界以3帧横向遮罩切换完整风格场景，主体保持匹配姿态；不是连续几何形变。';
fs.writeFileSync(f,JSON.stringify(p,null,2));
