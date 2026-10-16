import {JSDOM} from 'jsdom';
import {readFileSync} from 'node:fs';
const dom=new JSDOM('<!doctype html><html><body></body></html>');
globalThis.window=dom.window;
globalThis.document=dom.window.document;
const {default:mermaid}=await import('mermaid');
mermaid.initialize({startOnLoad:false,securityLevel:'strict'});
for(const item of JSON.parse(readFileSync(new URL('./diagrams.json',import.meta.url),'utf8'))){
  await mermaid.parse(item.source);
  console.log('PASS',item.path);
}
