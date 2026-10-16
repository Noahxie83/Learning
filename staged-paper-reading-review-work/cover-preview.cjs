const {chromium}=require('C:/Users/noahx/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('node:fs');
(async()=>{
const previewPath='D:/Learning/staged-paper-reading-review-work/cover-preview.html';
fs.writeFileSync(previewPath,'<!doctype html><meta charset="utf-8"><style>body{margin:0;padding:20px;background:#fff}main{max-width:980px;margin:auto}img{width:100%;height:auto;display:block}</style><main><img alt="Staged Paper Reading" src="file:///D:/Learning/staged-paper-reading-review/assets/cover.png"></main>');
const browser=await chromium.launch({channel:'msedge',headless:true});
try{
const page=await browser.newPage();
for(const width of [1020,390]){
 await page.setViewportSize({width,height:650});
 await page.goto('file:///'+previewPath);
 const state=await page.locator('img').evaluate(el=>({loaded:el.complete&&el.naturalWidth>0,w:el.naturalWidth,h:el.naturalHeight,displayWidth:el.getBoundingClientRect().width,overflow:document.documentElement.scrollWidth>innerWidth}));
 if(!state.loaded||state.overflow) throw new Error(JSON.stringify(state));
 console.log(width,JSON.stringify(state));
 await page.screenshot({path:`D:/Learning/staged-paper-reading-review-work/cover-preview-${width}.png`});
}
}finally{await browser.close();}
})().catch(error=>{console.error(error);process.exit(1);});
