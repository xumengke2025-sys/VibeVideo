const fs = require('fs');
const path = require('path');
const cp = require('child_process');
const sharp = require('C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const out = __dirname;
const ink = '#49392f';
const text = (x,y,s,size=36,color=ink,weight=700,anchor='middle') => `<text x="${x}" y="${y}" font-size="${size}" fill="${color}" font-weight="${weight}" text-anchor="${anchor}">${s}</text>`;
const leaf = (x,y,k=1) => `<g transform="translate(${x} ${y}) scale(${k})"><path d="M0 100 Q-70 65 -42 12 Q5 -25 27 25 Q83 38 43 81 Z" fill="#719879" stroke="#fdf8eb" stroke-width="10"/><path d="M0 110 Q3 67 0 28" stroke="#536e50" stroke-width="4" fill="none"/></g>`;
function child(x,y,color,dir,name) {
  return `<g transform="translate(${x} ${y})"><ellipse cx="0" cy="271" rx="96" ry="15" fill="#a18f74" opacity=".19"/><g transform="scale(${dir} 1)" stroke="${ink}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">
  <g stroke="#fffdf5" stroke-width="21"><path d="M-35 167 L-61 213 L-95 226 M24 165 L49 202 L78 252" fill="none"/><path d="M-40 95 L-69 142 L-91 119 M38 96 L65 131 L91 95" fill="none"/><path d="M-39 86 Q0 67 39 87 L43 169 Q0 186 -43 169 Z" fill="none"/><ellipse cx="0" cy="33" rx="58" ry="64" fill="#fffdf5"/></g>
  <path d="M-35 167 L-61 213 L-95 226" fill="none" stroke="#374960" stroke-width="28"/><path d="M24 165 L49 202 L78 252" fill="none" stroke="#374960" stroke-width="28"/>
  <path d="M-90 215 Q-127 229 -112 245 L-67 243 Q-61 229 -76 217 Z" fill="#f7ead5"/><path d="M63 244 Q60 263 79 270 L111 270 Q118 256 89 248 Z" fill="#f7ead5"/>
  <path d="M-40 95 L-69 142 L-91 119" fill="none" stroke="${color}" stroke-width="24"/><circle cx="-93" cy="115" r="14" fill="#eebf99"/>
  <path d="M38 96 L65 131 L91 95" fill="none" stroke="${color}" stroke-width="24"/><circle cx="94" cy="92" r="14" fill="#eebf99"/>
  <path d="M-39 86 Q0 67 39 87 L43 169 Q0 186 -43 169 Z" fill="${color}"/><path d="M-34 141 Q0 154 35 141" stroke="#fff7e3" opacity=".6" fill="none"/>
  <rect x="-11" y="62" width="25" height="26" rx="9" fill="#eebf99"/>
  <ellipse cx="0" cy="29" rx="56" ry="61" fill="#f4caa4"/><circle cx="52" cy="37" r="12" fill="#f4caa4"/>
  <path d="M-53 30 Q-76 -30 -23 -42 Q43 -61 56 0 Q25 -23 4 -6 Q-15 -9 -25 -23 Q-27 8 -53 30 Z" fill="#58412f"/>
  <path d="M-28 27 Q-22 19 -15 24 M11 20 Q18 12 26 18" fill="none" stroke-width="4"/>
  <ellipse cx="-15" cy="34" rx="5" ry="7" fill="${ink}"/><ellipse cx="25" cy="29" rx="5" ry="7" fill="${ink}"/>
  <ellipse cx="-30" cy="48" rx="11" ry="6" fill="#e9957b" stroke="none" opacity=".7"/><ellipse cx="38" cy="43" rx="11" ry="6" fill="#e9957b" stroke="none" opacity=".7"/>
  <path d="M-5 50 Q12 66 26 46" fill="#fff8ea" stroke-width="4"/>
  </g><rect x="-58" y="102" width="116" height="55" rx="16" fill="#fffaf0" stroke="${ink}" stroke-width="3"/>${text(0,142,name,34,color)}</g>`;
}
const bus = `<g transform="translate(120 802)" stroke="${ink}" stroke-linejoin="round" stroke-width="5">
 <ellipse cx="424" cy="298" rx="420" ry="26" fill="#7b6c57" opacity=".22" stroke="none"/>
 <path d="M11 238 L11 75 Q17 14 99 6 L727 6 Q811 13 824 62 L824 244 Z" fill="#fffdf3" stroke="#fffdf3" stroke-width="24"/>
 <path d="M11 238 L11 75 Q17 14 99 6 L727 6 Q811 13 824 62 L824 244 Z" fill="#edba54"/>
 <path d="M14 175 L823 175 L823 242 L14 242 Z" fill="#e59d40" stroke="none"/>
 <path d="M89 35 Q49 40 42 87 L42 143 L155 143 L155 35 Z" fill="#bbd9d7"/>
 ${[183,309,435,561,687].map(x=>`<rect x="${x}" y="38" width="101" height="100" rx="14" fill="#c4dedb"/><path d="M${x+14} 58 L${x+49} 58 L${x+14} 93" fill="#e6f1e8" stroke="none"/>`).join('')}
 <path d="M104 40 L104 137" fill="none" stroke="#739395" stroke-width="4"/>
 <circle cx="43" cy="200" r="17" fill="#fff3b6"/><rect x="781" y="187" width="15" height="35" rx="5" fill="#bd6146"/>
 <path d="M40 224 Q55 239 75 220" fill="none" stroke-width="4"/>
 <path d="M2 241 L835 241" stroke="#f7df9b" stroke-width="17"/>
 ${[160,666].map(x=>`<circle cx="${x}" cy="252" r="46" fill="#403c3c"/><circle cx="${x}" cy="252" r="25" fill="#faf0d6"/><circle cx="${x}" cy="252" r="10" fill="#82715d"/><path d="M${x} 231 V273 M${x-21} 252 H${x+21}" stroke="#d2c0a5" stroke-width="4"/>`).join('')}
 <rect x="307" y="157" width="284" height="64" rx="18" fill="#fff6df" stroke-width="3"/>${text(449,202,'长长巴士',40)}
 <path d="M33 13 Q371 -11 789 22" fill="none" stroke="#ffdd84" stroke-width="9"/>
</g>`;
const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">
<defs>
 <filter id="shadow" x="-30%" y="-30%" width="160%" height="180%"><feDropShadow dx="0" dy="12" stdDeviation="13" flood-color="#776241" flood-opacity=".13"/></filter>
 <pattern id="grain" width="70" height="70" patternUnits="userSpaceOnUse"><circle cx="5" cy="8" r=".9" fill="#856342" opacity=".11"/><circle cx="49" cy="26" r=".7" fill="#856342" opacity=".11"/><path d="M13 45 l9 -1 M36 59 l6 2" stroke="#856342" stroke-width=".7" opacity=".11"/></pattern>
 <clipPath id="world"><rect x="40" y="440" width="1000" height="1138" rx="80"/></clipPath>
</defs>
<g font-family="Microsoft YaHei, SimHei, sans-serif">
<rect width="1080" height="1920" fill="#f5ecd9"/>
<rect x="53" y="47" width="974" height="1826" rx="48" fill="none" stroke="#d9c9ad" stroke-width="2"/>
${text(540,111,'一辆巴士 · 两个跑步伙伴',28,'#86725d',500)}
${text(540,215,'长长巴士的',84)}
${text(540,317,'相遇谜案',106,'#bd6346')}
${text(540,393,'同一辆车，怎么一个6秒，一个2秒？',34,ink,500)}
<rect x="40" y="440" width="1000" height="1138" rx="80" fill="#e0eadc" filter="url(#shadow)"/>
<g clip-path="url(#world)">
 <rect x="40" y="440" width="1000" height="650" fill="#dae8e1"/>
 <circle cx="863" cy="576" r="68" fill="#edc972"/><circle cx="844" cy="560" r="60" fill="#f4dca0"/>
 <path d="M-100 915 Q145 550 485 831 Q710 516 1190 872 L1190 1150 L-100 1150 Z" fill="#adc7ac"/>
 <path d="M-100 973 Q327 689 697 917 Q1010 726 1190 995 L1190 1150 L-100 1150 Z" fill="#94b894"/>
 <g fill="#f4f2e6"><ellipse cx="209" cy="565" rx="71" ry="20"/><ellipse cx="250" cy="549" rx="43" ry="27"/><ellipse cx="707" cy="656" rx="67" ry="21"/></g>
 <g transform="translate(778 733)"><path d="M0 70 V-18 H113 V70" fill="#f5d59f" stroke="#7d735c" stroke-width="4"/><path d="M-14 -16 L56 -65 L126 -16 Z" fill="#bd7355" stroke="#7d735c" stroke-width="4"/><rect x="18" y="7" width="24" height="31" fill="#abc9c6"/><rect x="67" y="7" width="24" height="31" fill="#abc9c6"/></g>
 ${leaf(91,737,1.2)}${leaf(983,799,.85)}
 <path d="M40 1028 Q540 1001 1040 1028 V1207 H40 Z" fill="#8f9990"/>
 <path d="M40 1043 Q540 1020 1040 1043" fill="none" stroke="#e9e3cf" stroke-width="6"/>
 <path d="M0 1130 H1150" stroke="#eee6cf" stroke-width="10" stroke-dasharray="66 70"/>
 <rect x="40" y="1200" width="1000" height="385" fill="#e9ddbd"/>
 <path d="M40 1200 H1040" stroke="#f9f0d7" stroke-width="22"/>
 <path d="M40 1360 H1040 M40 1520 H1040 M170 1200 V1360 M550 1200 V1360 M930 1200 V1360 M360 1360 V1520 M740 1360 V1520" stroke="#d5c7a7" stroke-width="3"/>
 ${bus}
 ${child(293,1245,'#c87057',1,'小乙')}
 ${child(790,1245,'#4c849b',-1,'小甲')}
 <g stroke="${ink}" stroke-width="3" fill="#fffaf0"><path d="M90 1158 Q90 1136 115 1136 H457 Q482 1136 482 1161 V1193 Q482 1218 457 1218 H327 L290 1240 L297 1218 H115 Q90 1218 90 1193 Z"/><path d="M588 1128 Q588 1104 614 1104 H960 Q985 1104 985 1128 V1161 Q985 1188 960 1188 H824 L786 1216 L794 1188 H614 Q588 1188 588 1161 Z"/></g>
 ${text(285,1193,'哇，一下就过去啦！',30)}${text(787,1160,'咦，怎么还没过去？',30)}
 <g fill="none" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"><path d="M190 1540 H393 L371 1520 M393 1540 L371 1560" stroke="#c87057"/><path d="M890 1540 H687 L709 1520 M687 1540 L709 1560" stroke="#4c849b"/></g>
 <path d="M143 757 H942 M143 741 V773 M942 741 V773" stroke="#a58245" stroke-width="4"/>
 <rect x="429" y="712" width="229" height="65" rx="25" fill="#fff7df" stroke="#a58245" stroke-width="3"/>${text(543,758,'车身长15米',35)}
</g>
<g filter="url(#shadow)"><rect x="104" y="1630" width="872" height="192" rx="33" fill="#fffaf0" stroke="#e2d0ad" stroke-width="2"/></g>
${text(540,1705,'让巴士当尺子，把相遇看明白',40)}
${text(540,1772,'同向：多赶上多少？   迎面：一起靠近多少？',29,'#82715e',500)}
<rect width="1080" height="1920" fill="url(#grain)" pointer-events="none"/>
</g></svg>`;
fs.writeFileSync(path.join(out,'concept-v1.svg'), svg);
async function main() {
  await sharp(Buffer.from(svg)).png().toFile(path.join(out,'concept-v1.png'));
  const v=18*1000/3600, L=15, a=v-L/6, b=L/2-v;
  // Positive x = west. Origin is A at the instant the bus rear passes A.
  const at = t => ({rear:v*t,front:v*t+L,A:a*t,B:240-b*t});
  const tEnd=32, gap=at(tEnd).B-at(tEnd).A, answer=gap/(a+b);
  const checks={units:v===5,A:a===2.5,B:b===2.5,meet_B_front:at(30).front===at(30).B,pass_B_rear:at(32).rear===at(32).B,gap:gap===80,answer:answer===16,meet_runners:at(48).A===at(48).B,pass_A_start:at(-6).front===at(-6).A,pass_A_end:at(0).rear===at(0).A};
  if(Object.values(checks).some(x=>!x))throw new Error('Math contract failed');
  fs.writeFileSync(path.join(out,'math-verification.json'),JSON.stringify({checks,model:'x increases westward; rear=5t; front=5t+15; A=2.5t; B=240-2.5t',states:[-6,0,30,32,48].map(t=>({t,...at(t)})),answer},null,2));
  const ff=path.resolve(out,'../../node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe');
  fs.mkdirSync(path.join(out,'reference-study'),{recursive:true});
  const refs=[{id:'cel-boil',file:path.resolve(out,'../../reference-sources/upstream-videos/mg-styles-15/05-cel-boil.mp4'),times:[1,3,5,7]}, {id:'paper-popup',file:path.resolve(out,'../../reference-sources/upstream-videos/lemo-opuscar/paper-popup.mp4'),times:[12,12.25,12.5,12.75]}];
  for (const ref of refs) {
    const frames=[];
    for(let i=0;i<ref.times.length;i++){
      const f=path.join(out,'reference-study',`${ref.id}-${i}.png`);
      cp.execFileSync(ff,['-v','error','-ss',String(ref.times[i]),'-i',ref.file,'-frames:v','1','-vf','scale=640:360','-y',f],{timeout:60000,windowsHide:true,stdio:'pipe'});
      frames.push({input:f,left:i%2*640,top:Math.floor(i/2)*360});
    }
    await sharp({create:{width:1280,height:720,channels:3,background:'#f6eedc'}}).composite(frames).png().toFile(path.join(out,'reference-study',`${ref.id}-contact.png`));
  }
  console.log(JSON.stringify({concept:path.join(out,'concept-v1.png'),math:'10 assertions passed',references:refs.map(r=>({id:r.id,times:r.times}))}));
}
main().catch(e=>{console.error(e.message);process.exitCode=1});
