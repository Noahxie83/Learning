// Use the running application's own validated API; preserve registry revisions.
import { createRequire } from 'node:module';
import { readFile } from 'node:fs/promises';
const require = createRequire('D:/Project/Process Monitoring/package.json');
const { chromium } = require('playwright');
const [port] = (await readFile('C:/Users/noahx/AppData/Roaming/TrainingMonitor/DevToolsActivePort','utf8')).split(/\r?\n/);
const browser = await chromium.connectOverCDP(`http://127.0.0.1:${port}`);
const page = browser.contexts().flatMap(x=>x.pages()).find(x=>x.url().includes('/renderer/index.html') && !x.url().includes('view=gpu'));
if (!page) throw new Error('Training monitor main page not found');
const mode=process.argv[2] || 'inspect';
if(mode==='configure') {
  console.log(JSON.stringify(await page.evaluate(async()=>{
    const registry=await window.monitor.getRegistry();
    const task=registry.tasks.find(x=>x.taskId==='hdps_main_20261111');
    if(!task || task.hostId!=='lab-campus') throw new Error('Expected task not registered');
    const root='/data2/cy/xzn/Code/HDPS/repro_outputs/hdps_main_20261111';
    task.label='HDPS 论文主实验'; task.algorithm='flow';
    task.entryPaths=[root+'/run_experiments.py'];
    task.sources=[{sourceId:'hdps-paper-progress-log',path:root+'/logs/monitor.log',kind:'log'},
                  {sourceId:'hdps-paper-status',path:root+'/monitor_status.json',kind:'status_json'}];
    task.checkpointDirectories=[root+'/checkpoints'];
    return await window.monitor.saveRegistry(registry);
  })));
} else if(mode==='quit') {
  const session=await browser.newBrowserCDPSession();
  await session.send('Browser.close').catch(()=>{});
} else {
  console.log(JSON.stringify(await page.evaluate(async()=>{
    const s=await window.monitor.getSnapshot();
    return {hosts:s.hosts.map(h=>({hostId:h.hostId,connection:h.connection,error:h.errorCode})),
            tasks:s.tasks.map(t=>({taskId:t.taskId,lifecycle:t.lifecycle,reason:t.reason,main:t.processes.main,
                                   progress:t.progress,checkpoint:t.checkpoint})),sources:s.sources};
  })));
}
process.exit(0);
