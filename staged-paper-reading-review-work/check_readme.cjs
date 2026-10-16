const {chromium}=require('C:/Users/noahx/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('node:fs');
const work='D:/Learning/staged-paper-reading-review-work/';
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true});
 try{
  const page=await browser.newPage({viewport:{width:1040,height:1500}});
  await page.goto('file:///'+work+'readme-preview.html');
  await page.waitForFunction(()=>[...document.images].every(img=>img.complete&&img.naturalWidth>0));
  await page.screenshot({path:work+'readme-desktop.png'});
  const nav=page.locator('a:has(img[src*="nav-"])');
  if(await nav.count()!==4) throw new Error('Navigation button count');
  for(const id of ['workflow','start','notes','files']){
   await page.locator('a[href="#'+id+'"]').click();
   const target=await page.locator('#'+id).evaluate(el=>el.getBoundingClientRect().top);
   if(target<-1||target>1500) throw new Error('Broken nav '+id+': '+target);
  }
  await page.setViewportSize({width:390,height:844});
  await page.goto('file:///'+work+'readme-preview.html');
  await page.waitForFunction(()=>[...document.images].every(img=>img.complete&&img.naturalWidth>0));
  await page.screenshot({path:work+'readme-mobile.png'});
  if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth)) throw new Error('Mobile overflow');
  const rows=await nav.evaluateAll(els=>els.map(el=>Math.round(el.getBoundingClientRect().top)));
  if(new Set(rows).size!==2) throw new Error('Buttons should wrap in two rows on mobile');
  await page.goto('file:///D:/Learning/staged-paper-reading-review/assets/reading-flow.svg');
  await page.setViewportSize({width:960,height:356});
  await page.evaluate(()=>document.getAnimations().forEach(a=>{a.pause();a.currentTime=0;}));
  const beginning=await page.screenshot();
  await page.evaluate(()=>document.getAnimations().forEach(a=>{a.currentTime=6500;}));
  const final=await page.screenshot({path:work+'reading-flow-final.png'});
  if(beginning.equals(final)) throw new Error('Animation does not change');
  const timing=await page.evaluate(()=>document.getAnimations().map(a=>a.effect.getTiming()));
  if(timing.some(t=>t.iterations!==1)) throw new Error('Animation repeats');
  await page.emulateMedia({reducedMotion:'reduce'});
  if(await page.evaluate(()=>document.getAnimations().length)!==0) throw new Error('Reduced motion failed');
  const visible=await page.locator('.ink').evaluateAll(els=>els.every(el=>getComputedStyle(el).opacity==='1'));
  if(!visible) throw new Error('Reduced motion hides content');
  const overflow=await page.evaluate(()=>[...document.querySelectorAll('text')].some(el=>{const b=el.getBBox();return b.x<0||b.x+b.width>960||b.y<0||b.y+b.height>356;}));
  if(overflow) throw new Error('Diagram text overflow');
  console.log('PASS: all images, four navigation links, mobile two-row buttons, single-play animation, reduced-motion fallback, SVG text bounds.');
 }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exit(1);});
