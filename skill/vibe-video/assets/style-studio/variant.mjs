// A deliberately different extreme at index 1 catches stale MAX/label assumptions.
import fs from 'node:fs';
const p=JSON.parse(fs.readFileSync(new URL('./clips/dataviz-proof.json',import.meta.url),'utf8'));
p.id='dataviz-variant';p.title='改变输入后的重建验证';
p.data.values=[94,32,58,17,49,83,45,61];p.data.maximum=100;
p.events.find(e=>e.id==='highlight').result='索引1值94由输入计算';
fs.writeFileSync(new URL('./clips/dataviz-variant.json',import.meta.url),JSON.stringify(p,null,2));
console.log('Written dataviz-variant: maximum moved from index 7 / 74 to index 1 / 94.');
