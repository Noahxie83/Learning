// Exercise the installed monitor's real parsers against CPU-only script output.
import {createRequire} from 'node:module';
import {execFileSync} from 'node:child_process';
import {writeFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
const root=fileURLToPath(new URL('..',import.meta.url));
const app='D:/Project/Process Monitoring';
const require=createRequire(app+'/package.json');
const {build}=require('esbuild');
const python=`import sys,json,io
from pathlib import Path
sys.path.insert(0,${JSON.stringify(root)})
from monitoring import Monitor
out=io.StringIO()
m=Monitor(Path('unused'),'hdps_author_main_20261111',93,50,
 {'status':'running','total_samples':2,'completed_samples':1},lambda *args:None,
 stream=out,start_thread=False,identity={'pid':123,'startTicks':'456','hostBootId':'fixture'})
m.update(55,sampling_step=5,sampling_steps=43);m.emit()
running=out.getvalue().splitlines()[-1];state=m._state()
m.update(93,status='completed');m.close()
print(json.dumps({'running':running,'state':state,'completed':out.getvalue().splitlines()[-1]}))`;
const fixture=JSON.parse(execFileSync('python',['-c',python],{encoding:'utf8'}));
const contents=`
import assert from 'node:assert/strict';
import {parseGenericRecord} from './src/parsers/generic.ts';
import {parseFlowRecord,flow} from './src/parsers/flow.ts';
import {parseBaselineStartupContent} from './src/domain/baseline.ts';
const fixture=${JSON.stringify(fixture)};
for(const parse of [parseGenericRecord,parseFlowRecord]) {
 const record=parse(fixture.running,'author-console');
 assert.equal(record.isTrainingOutput,true);
 assert.equal(record.sessionCompletedCount,5);
 assert.equal(record.sessionTargetCount,43);
 const completed=parse(fixture.completed);
 assert.equal(completed.sessionCompletedCount,43);
 assert.equal(completed.sessionTargetCount,43);
}
const baseline=parseBaselineStartupContent(JSON.stringify(fixture.state));
assert.equal(baseline.resumeCheckpointIndex,50);
assert.equal(baseline.targetCount,94);
assert.equal(baseline.targetMeaning,'exclusive_index');
const result=flow({b:baseline.resumeCheckpointIndex,T:baseline.targetCount,n:5});
assert.equal(result.lastStepIndex,55);
assert.equal(result.global.completedCount,56);
assert.equal(result.session.completedCount,5);
assert.equal(result.session.targetCount,43);
export default {generic_parser:'passed',flow_parser:'passed',status_baseline:'passed',
 flow_step_and_counts:'passed',fixture_type:'synthetic CPU-only',
 monitor_app_changed:false,gpu_query_performed:false,inference_started:false};`;
const bundled=await build({stdin:{contents,resolveDir:app,loader:'ts'},bundle:true,
 platform:'node',format:'esm',write:false});
const checked=await import('data:text/javascript;base64,'+Buffer.from(bundled.outputFiles[0].contents).toString('base64'));
await writeFile(new URL('../monitor_protocol_check.json',import.meta.url),JSON.stringify(checked.default,null,2)+'\n');
console.log(JSON.stringify(checked.default));
