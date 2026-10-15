// Real workerd/Durable Object execution with a SYNTHETIC provider; no inference claim.
import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join,dirname} from 'node:path';
import {Miniflare,Response,convertV4MiniflareOptions} from 'miniflare';
import {MODEL,LIMITS} from '../qa.mjs';
const compiled=process.env.WORKER_BUILD;
const good={kind:'EVIDENCE',intent:'CONTENT',focus:'annual supplement pension payment',limit:1};
test('actual Worker validates privacy, serialises requests and persists its quota across restart',{skip:!compiled},async()=>{
 const directory=await mkdtemp(join(tmpdir(),'stimmfolgen-worker-test-'));
 let calls=0,gate,release,mode='valid';
 const outbound=async request=>{
  assert.equal(new URL(request.url).hostname,'api.publicai.co');
  if(new URL(request.url).pathname==='/v1/models')return Response.json({data:[{id:MODEL,pricing:{input:.1,output:.2}}]});
  calls++;const body=await request.json();assert.equal(body.model,MODEL);
  if(gate){const wait=gate;gate=null;await wait;}
  const candidate=mode==='invented'?{...good,text:'made up'}:good;
  const content=body.messages[0].content.includes('Judge whether a candidate')?{direct:mode!=='reject'}:candidate;
  return Response.json({model:MODEL,choices:[{finish_reason:'stop',message:{content:mode==='malformed'?'not JSON':JSON.stringify(content)}}]});
 };
 const options={resourcePersistencePath:directory,workers:[{name:"fixture",modules:true,scriptPath:compiled,modulesRoot:dirname(compiled),compatibilityDate:'2026-10-15',bindings:{LIVE_ENABLED:'true',PUBLICAI_TOKEN:'synthetic-not-a-key'},durableObjects:{DEMO_GATE:{className:'DemoGate',useSQLite:true}},serviceBindings:{ASSETS:()=>new Response('static fixture')},outboundService:outbound}]};
 let mf=new Miniflare(convertV4MiniflareOptions(options));
 const send=async(body,origin='https://demo.test')=>mf.dispatchFetch('https://demo.test/api/live/question',{method:'POST',headers:{Origin:origin,'Content-Type':'application/json','CF-Connecting-IP':String(Math.random())},body:JSON.stringify(body)});
 const status=async()=>{const ns=await mf.getDurableObjectNamespace('DEMO_GATE');return (await ns.get(ns.idFromName('global-free-demo-v1')).fetch('https://internal/status')).json();};
 try{
  const asset=await mf.dispatchFetch('https://demo.test/app.js');assert.equal(asset.headers.get('Cache-Control'),'no-store');assert.ok(asset.headers.get('Content-Security-Policy').includes("script-src 'self'"));
  assert.equal((await send({question:'What changes?',notes:'private'})).status,400);
  assert.equal((await send({question:'x'.repeat(5000)})).status,400);
  assert.equal((await send({question:'What changes?'},'https://other.test')).status,400);assert.equal(calls,0);
  gate=new Promise(resolve=>{release=resolve;});
  const first=send({question:'What changes?'});
  // Wait until provider call is deliberately blocked, then exercise the same DO.
  for(let n=0;calls===0&&n<100;n++)await new Promise(resolve=>setTimeout(resolve,10));
  const concurrent=await (await send({question:'Concurrent request?'})).json();assert.equal(concurrent.outcome,'BUSY');release();
  const result=await (await first).json();assert.equal(result.outcome,'EVIDENCE_MATCH');assert.equal(result.human_reviewed,false);assert.match(result.execution_contract_sha256,/^[a-f0-9]{64}$/);assert.ok(result.claims[0].citations[0].span_id);assert.equal(calls,2);
  mode='invented';assert.equal((await (await send({question:'Invented quote fixture?'})).json()).outcome,'WITHHELD');assert.equal(calls,3);mode='malformed';const malformed=await (await send({question:'Malformed completion fixture?'})).json();assert.equal(malformed.outcome,'WITHHELD');assert.equal(malformed.live_inference_performed_for_this_request,true);mode='reject';const rejected=await (await send({question:'Rejected relevance fixture?'})).json();assert.equal(rejected.outcome,'INSUFFICIENT_EVIDENCE');assert.deepEqual(rejected.claims,[]);assert.equal(rejected.directness_checks_performed,1);mode='valid';
  await mf.dispose();mf=new Miniflare(convertV4MiniflareOptions(options));assert.equal((await status()).remaining,LIMITS.lifetime-4);
  for(let n=4;n<LIMITS.daily;n++)assert.equal((await (await send({question:'Quota fixture '+n})).json()).outcome,'EVIDENCE_MATCH');
  const before=calls;assert.equal((await (await send({question:'Over daily quota?'})).json()).outcome,'LIMIT_REACHED');assert.equal(calls,before);
  await mf.dispose();mf=new Miniflare(convertV4MiniflareOptions(options));assert.equal((await status()).daily_remaining,0);assert.equal((await status()).remaining,LIMITS.lifetime-LIMITS.daily);
 }finally{release?.();await mf.dispose();await rm(directory,{recursive:true,force:true});}
});
