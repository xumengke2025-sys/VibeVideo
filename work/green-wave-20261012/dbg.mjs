import {chromium} from '../sand-journey-20261010/node_modules/playwright-core/index.mjs';
import {createServer} from './server.mjs';
const server=createServer();await new Promise(r=>server.listen(0,'127.0.0.1',r));
const b=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true,args:['--use-angle=d3d11','--enable-gpu','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:540,height:960}});
p.on('pageerror',e=>console.log('PAGEERROR:',e.message));
p.on('console',m=>{if(m.type()==='error')console.log('CONSOLE:',m.text().slice(0,400))});
await p.goto('http://127.0.0.1:'+server.address().port+'/?render&width=540');
await new Promise(r=>setTimeout(r,7000));
console.log('__ready =',await p.evaluate(()=>window.__ready));
try{const d=await p.evaluate(()=>window.renderAt(0,'image/png',.9));console.log('renderAt OK, len',d.length)}catch(e){console.log('renderAt threw:',e.message.slice(0,300))}
await b.close();await new Promise(r=>server.close(r));
