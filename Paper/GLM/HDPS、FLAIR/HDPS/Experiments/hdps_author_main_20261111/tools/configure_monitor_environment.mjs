// Explicit maintenance helper; normal launches use the existing monitor form.
import {createRequire} from 'node:module';
import {readFile} from 'node:fs/promises';
const require=createRequire('D:/Project/Process Monitoring/package.json');
if(!process.argv.includes('--apply'))throw new Error('Use the existing monitor form; pass --apply only for an intentional configuration update.');
const {chromium}=require('playwright');
const [port]=(await readFile('C:/Users/noahx/AppData/Roaming/TrainingMonitor/DevToolsActivePort','utf8')).split(/\r?\n/);
const browser=await chromium.connectOverCDP(`http://127.0.0.1:${port}`);
const page=browser.contexts().flatMap(x=>x.pages()).find(x=>x.url().includes('/renderer/index.html')&&!x.url().includes('view=gpu'));
if(!page)throw new Error('Training monitor main page not found');
const task=await page.evaluate(async()=>{
  const registry=await window.monitor.getRegistry();
  const task=registry.tasks.find(x=>x.taskId==='hdps_author_main_20261111');
  if(!task||task.hostId!=='lab-campus')throw new Error('Expected registered task not found');
  const root='/data2/cy/xzn/Code/HDPS/repro_outputs/hdps_author_main_20261111';
  task.label='HDPS 作者实现主实验';
  task.algorithm='HDPS';
  task.logFormat='flow';
  task.entryPaths=[root+'/start.py'];
  task.sources=[{sourceId:'hdps-author-console',path:root+'/logs/console.log',kind:'log'},
                {sourceId:'hdps-author-status',path:root+'/status.json',kind:'status_json'}];
  task.checkpointDirectories=[root+'/checkpoints'];
  task.autoStart={execution:'server_tmux',enabled:false,armId:crypto.randomUUID(),gpuDeviceIds:[],
                  idleSeconds:60,maxUtilizationPercent:5,maxMemoryMiB:1024,
                  launch:{pythonPath:'/data2/cy/xzn/envs/hdps_repro/bin/python',entryPath:root+'/start.py',
                          cwd:'/data2/cy/xzn/Code/HDPS',arguments:'',logSourceId:'hdps-author-console'}};
  const saved=await window.monitor.saveRegistry(registry);
  return {revision:saved.revision,task:saved.tasks.find(x=>x.taskId===task.taskId)};
});
console.log(JSON.stringify(task));
process.exit(0);
