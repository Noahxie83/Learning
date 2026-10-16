const {chromium}=require('C:/Users/noahx/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
const browser=await chromium.launch({channel:'msedge',headless:true});
try{
 const page=await browser.newPage({viewport:{width:1440,height:1200}});
 await page.goto('https://github.com/Noahxie83/staged-paper-reading',{waitUntil:'domcontentloaded',timeout:45000});
 const article=page.locator('article.markdown-body').first();
 await article.waitFor({state:'visible',timeout:20000});
 await page.waitForFunction(()=>{
  const imgs=[...document.querySelectorAll('article.markdown-body img')].filter(img=>/nav-|reading-flow/.test(img.src));
  return imgs.length===5&&imgs.every(img=>img.complete&&img.naturalWidth>0);
 },null,{timeout:20000});
 console.log('GitHub rendered all four button assets and animated SVG.');
 const nav=article.locator('a:has(img[src*="nav-start.svg"])');
 await nav.click();
 await page.waitForFunction(()=>location.hash==='#start');
 await page.waitForFunction(()=>{
  const el=document.querySelector('#user-content-start, #start');
  return el&&el.getBoundingClientRect().top>=-2&&el.getBoundingClientRect().top<=innerHeight;
 },null,{timeout:5000});
 const target=await page.locator('#user-content-start, #start').first().evaluate(el=>el.getBoundingClientRect().top);
 if(target<-2||target>1200) throw new Error('Live navigation failed: '+target);
 await article.locator('a:has(img[src*="nav-workflow.svg"])').click();
 await page.waitForFunction(()=>location.hash==='#workflow');
 await page.waitForTimeout(6500);
 await page.screenshot({path:'D:/Learning/staged-paper-reading-review-work/readme-github-live.png'});
 const details=article.locator('summary').filter({hasText:'展开完整阅读流程与可选分支'});
 await details.click();
 const expanded=await details.evaluate(el=>el.parentElement.open);
 if(!expanded) throw new Error('Live details does not expand');
 console.log('GitHub navigation and full-flow disclosure passed.');
}finally{await browser.close();}
})().catch(error=>{console.error(error);process.exit(1);});
