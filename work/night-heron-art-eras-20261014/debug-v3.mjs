import{chromium}from'../sand-journey-20261010/node_modules/playwright-core/index.mjs';
const b=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
const p=await b.newPage();p.on('pageerror',e=>console.log('PAGEERROR '+e.message));p.on('console',m=>{if(m.type()==='error')console.log('CONSOLE '+m.text())});
await p.goto('http://127.0.0.1:8146/rebuild-v3.html?render');
console.log(await p.evaluate(()=>Object.keys(window.SCENES)));try{await p.waitForFunction(()=>window.__ready,null,{timeout:90000});console.log(await p.evaluate(()=>({ready:__ready,assets:__assetsLoaded,state:__state})));await p.screenshot({path:'work/night-heron-art-eras-20261014/out/debug-v3.png'});}catch(e){console.log(e.message)}
await b.close();
