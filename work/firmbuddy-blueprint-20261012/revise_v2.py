from pathlib import Path
import json
R=Path(__file__).resolve().parent
f=R/'film.js'
s=f.read_text(encoding='utf-8')
a=s.index('function task()'); b=s.index('function opportunity()',a)
s=s[:a]+'''function task(){at(...centers.task,()=>{sect('01','专业支持，随时进入','VISIT / QUESTIONS / OPPORTUNITIES',0);
const cards=[['拜访准备','客户情况 · 沟通重点','document'],['业务答疑','有问题，随时问','shield'],['商机查询','找线索 · 看来源','chart']];
cards.forEach(([title,note,kind],i)=>{const x=-590+i*410,a=p(T,.05+i*.55,.65+i*.55);R(x,-230,370,350,a,.9,2.3);icon(kind,x+185,-135,85,a);mono('0'+(i+1),x+25,-190,23,a,{v:.6});TX(title,x+185,0,45,p(T,.4+i*.55,1+i*.55),{align:'center'});TX(note,x+185,65,26,p(T,.7+i*.55,1.3+i*.55),{align:'center',v:.8});route([[x+185,120],[x+185,205],[0,205]],2+i*.3,3+i*.3)});
label('从不同需求，找到专业支持',-340,242,680,p(T,3.3,3.8),34);route([[0,205],[640,205],[720,260]],5.6,7.2);
})}
''' +s[b:]
s=s.replace("compact?'客户议题':'客户拜访议题'", "compact?'业务问题':'当前业务问题'")
s=s.replace("'精选商机','SIGNAL / NOT YET VERIFIED'", "'主动查询商机','FIND SIGNALS / CHECK SOURCES'")
s=s.replace("'专家协同会商','ONE QUESTION / MANY PERSPECTIVES'", "'有疑问，问专家','QUESTIONS / EXPERT PERSPECTIVES'")
s=s.replace("'查证后，再形成沟通要点'", "'查规则、找依据，再作判断'")
s=s.replace("'形成拜访准备','FROM EVIDENCE TO ACTION'", "'按需形成业务成果','FROM SUPPORT TO ACTION'")
s=s.replace("'VISIT STRATEGY / Q-01'", "'EXAMPLE / VISIT PREPARATION'")
s=s.replace("'本次拜访的行动蓝图'", "'拜访 · 答疑 · 商机查询'")
s=s.replace("'让专业协同，走进客户经营'", "'专业支持，贯穿日常业务'")
a=s.index('export const captions=');b=s.index('function subtitle()',a)
s=s[:a]+'''export const captions=[
[.2,3.2,'准备拜访，有业务疑问'],[3.2,6.6,'或者想找商机，都能打开 FirmBuddy'],
[8.1,11.9,'主动查询商机，发现值得研判的线索'],[12,16.1,'查看来源，再核实机会'],
[18.4,22.7,'遇到问题，随时向专家提问'],[23,27.8,'从企业画像到资本运作，汇集专业视角'],
[30.6,34.3,'查规则、找资料，打开知识档案'],[34.4,39,'让判断有来源，有依据'],
[41.6,47.15,'按需形成业务成果，例如拜访策略包'],[47.2,51,'确认后，再创建跟进任务'],
[52.3,55.8,'拜访、答疑、商机查询'],[56,60,'FirmBuddy，专业支持，随时在场']];
''' +s[b:]
s=s.replace('window.stateAt=t=>({time:t,camera:cameraAt(t)', 'window.stateAt=t=>({time:t,camera:cameraAt(t*1.25)')
s=s.replace('caption:captions.find(s=>t>=s[0]&&t<s[1])','caption:captions.find(s=>t*1.25>=s[0]&&t*1.25<s[1])')
s=s.replace('T=clamp(t/60)*60','T=clamp(t/48)*60')
s=s.replace("+' / 60'","+' / 48'").replace('base>=60','base>=48').replace('Math.min(60,base+','Math.min(48,base+').replace('if(t>=60)','if(t>=48)')
f.write_text(s,encoding='utf-8')
f=R/'index.html';s=f.read_text(encoding='utf-8').replace('max="60"','max="48"').replace('0.00 / 60','0.00 / 48');f.write_text(s,encoding='utf-8')
f=R/'render.mjs';s=f.read_text(encoding='utf-8').replace('Number(args.duration||23):60','Number(args.duration||23):48').replace('3.5,12.5,25.5,35.5,45.5,50.5,56.7,59','3.5,10,20.4,28.4,36.4,40.4,45.4,47.2');f.write_text(s,encoding='utf-8')
entries=[(.2,3.15,'准备拜访，有业务疑问。'),(3.2,6.45,'或者想找商机，都能打开Firm Buddy。'),(8.1,11.9,'主动查询商机，发现值得研判的线索。'),(12,16,'查看来源，再核实机会。'),(18.4,22.7,'遇到问题，随时向专家提问。'),(23,27.7,'从企业画像到资本运作，汇集专业视角。'),(30.6,34.3,'查规则、找资料，打开知识档案。'),(34.4,38.9,'让判断有来源，有依据。'),(41.6,47,'按需形成业务成果，例如拜访策略包。'),(47.2,51,'确认后，再创建跟进任务。'),(52.3,55.8,'拜访、答疑、商机查询。'),(56,59.9,'Firm Buddy，专业支持，随时在场。')]
entries=[(round(a/1.25,3),round(b/1.25,3),c) for a,b,c in entries]
(R/'audio/script-v2.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2),encoding='utf-8-sig')
f=R/'make_audio.py';s=f.read_text(encoding='utf-8');a=s.index('entries=[');b=s.index('async def synth',a);s=s[:a]+"entries=json.loads((ROOT/'audio/script-v2.json').read_text(encoding='utf-8-sig'))\n"+s[b:];s=s.replace('n=sr*60','n=sr*48').replace('np.arange(.4,59,.625)','np.arange(.32,47,.5)').replace('add(fx,t,a)','add(fx,t/1.25,a)').replace("'duration':60","'duration':48");f.write_text(s,encoding='utf-8')
f=R/'make_voice.ps1';s=f.read_text(encoding='utf-8-sig');a=s.index('$texts = @(');b=s.index('for ($i=',a);s=s[:a]+"$entries = Get-Content -LiteralPath (Join-Path $voiceRoot 'script-v2.json') -Raw -Encoding UTF8 | ConvertFrom-Json\n$texts = @($entries | ForEach-Object { [string]$_[2] })\n"+s[b:];s=s.replace('$voice.Rate = $(if($i -eq 1){3}else{1})','$voice.Rate = 2\nif($i -eq 1){$voice.Rate = 4}\n$texts[$i] = $texts[$i].Replace(\'Firm Buddy\',\'<voice required="Language=409">Firm Buddy</voice><voice required="Language=804"></voice>\')');s=s.replace('$(if($i -eq 11){8}else{0})','8');f.write_text(s,encoding='utf-8-sig')
print('V2 content, 48-second timeline, and voice scripts updated')
