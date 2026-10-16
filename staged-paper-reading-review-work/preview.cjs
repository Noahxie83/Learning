const {chromium}=require('C:/Users/noahx/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('node:fs');
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true});
 const page=await browser.newPage({viewport:{width:1280,height:440}});
 await page.goto('file:///D:/Learning/staged-paper-reading-review/assets/workflow.svg');
 await page.screenshot({path:'D:/Learning/staged-paper-reading-review-work/workflow-preview.png'});
 const overflow=await page.evaluate(()=>[...document.querySelectorAll('text')].some(el=>{const b=el.getBBox();return b.x<0||b.x+b.width>1280||b.y<0||b.y+b.height>440;}));
 if(overflow) throw new Error('SVG text overflow');
 await page.setViewportSize({width:1000,height:800});
 await page.goto('about:blank');
 await page.setContent(fs.readFileSync('D:/Learning/staged-paper-reading-review-work/example.html','utf8'));
 await page.locator('a[href="#fig1"]').click();
 const result=await page.evaluate(()=>({hash:location.hash,target:document.getElementById('fig1')?.getBoundingClientRect().top,figures:document.querySelectorAll('h4').length}));
 if(result.hash!=='#fig1'||result.target<0||result.target>800) throw new Error(JSON.stringify(result));
 console.log('SVG text fits the viewBox. Figure navigation passed:',JSON.stringify(result));
 await browser.close();
})().catch(error=>{console.error(error);process.exit(1);});
