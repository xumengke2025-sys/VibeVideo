import fs from 'node:fs';
const base=new URL('.',import.meta.url),file=new URL('production-plan.json',base);
const p=JSON.parse(fs.readFileSync(file));
if(!fs.existsSync(new URL('production-plan-v1.json',base)))fs.copyFileSync(file,new URL('production-plan-v1.json',base));
p.version='plan-v2-consistent-action';p.status='in_production';p.scope='按用户授权执行；16时代同一偷鱼动作，无争抢、对抗、追逐。';
p.brief.duration=40;p.brief.userConfirmed.push('执行计划','每个时代动作基本一致以保持连续性','从别的动物脚边或放置处偷走已捕获的鱼；无对抗');
p.brief.proposed=['40秒','每时代2.25秒，24fps'];
p.direction.selected='同一动作跨风格接力：夜鹭走近→伸颈叼鱼→抬头吞下→继续走；其他动物平静看向别处，少量自然呼吸。';
p.direction.ending='最后一时代仍完成相同偷吃动作；夜鹭满足地缩颈，回收片名。不加幼鸟抢鱼或追逐反转。';
p.direction.failureCondition='动作有争抢、打架或追逐；不同风格动作相位与角色身份断裂；只改背景色；看不出地上原本属于其他动物的鱼被夜鹭取走。';
p.timeline.opening={start:0,end:2,action:'夜鹭已在岸边，远处动物身旁放着捕获的鱼，短标题出现。'};
for(let i=0;i<p.timeline.shots.length;i++){const s=p.timeline.shots[i];s.start=2+i*2.25;s.end=s.start+2.25;s.action='走近→伸颈叼走旁边动物已经捕到并放下的鱼→抬喙吞下→继续走；对方不争抢、不追逐。';s.reads=[{what:'鱼放在别的动物身旁',from:s.start,readableAt:s.start+.2,to:s.start+.8},{what:'同一动作伸喙接触，鱼由地面绑定喙部',from:s.start+.8,readableAt:s.start+1.05,to:s.start+1.45},{what:'抬头吞下，回到下一个时代相同起始姿态',from:s.start+1.45,readableAt:s.start+1.7,to:s.end}];s.connectionToNext='夜鹭根部位置、脚底线、头部姿态和行动方向保持；同相位短遮罩切入下一画风。';s.camera.speedResponse='同一动作模板、相同接触时刻、同一画面区域，环境保留轻微视差。';}
p.timeline.ending={start:38,end:40,action:p.direction.ending};p.timeline.rhythm='16×2.25秒=36秒，加开头2秒与结尾2秒。跨风格沿用同一编舞和接触锚点。';
p.implementation.state='每段独立fishId；owner由opponent→heron→consumed。16段相同动作曲线，喙与鱼共享锚点。';
p.revisions=[{date:'2026-10-14',reason:'用户明确删去对抗并要求每个时代动作基本一致',changes:['统一编舞','40秒','其他动物自然站坐','取消抢夺、追逐和结尾反抢']}];
fs.writeFileSync(file,JSON.stringify(p,null,2));console.log('plan-v2: 40s, 16 eras, identical action');
