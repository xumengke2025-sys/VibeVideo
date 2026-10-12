const {chromium}=require('C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright-core');
const fs=require('fs');
(async()=>{
  const results=[];
  for(const [label,args] of [['upstream-wsl-flags',['--use-gl=angle','--use-angle=gl','--disable-accelerated-2d-canvas','--ignore-gpu-blocklist','--enable-gpu-rasterization']],['windows-d3d11',['--use-gl=angle','--use-angle=d3d11']]]){
    let browser;
    try{
      browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true,args,timeout:20000});
      const page=await browser.newPage();
      const info=await page.evaluate(()=>{
        const gl=document.createElement('canvas').getContext('webgl2');
        if(!gl)return {webgl2:false};
        const ext=gl.getExtension('WEBGL_debug_renderer_info');
        return {webgl2:true,renderer:ext?gl.getParameter(ext.UNMASKED_RENDERER_WEBGL):gl.getParameter(gl.RENDERER),vendor:ext?gl.getParameter(ext.UNMASKED_VENDOR_WEBGL):gl.getParameter(gl.VENDOR)};
      });
      results.push({label,args,...info});
    }catch(e){results.push({label,error:e.message.slice(0,600)});}
    finally{if(browser)await browser.close();}
  }
  fs.writeFileSync(__dirname+'/gpu.json',JSON.stringify(results,null,2));
  console.log(JSON.stringify(results));
})();
