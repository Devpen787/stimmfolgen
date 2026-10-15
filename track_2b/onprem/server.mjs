// On-premise app: the same source matcher as hosted, no external inference fallback.
import http from 'node:http';
import {readFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {localCompletion} from './adapter.mjs';
import {matchLocalQuestion} from './matching.mjs';
import {composeAnswer,questionPayload} from '../hosted/qa.mjs';
const root=new URL('../',import.meta.url),bundleText=await readFile(new URL('hosted/public-bundle.json',root),'utf8');
const bundle=JSON.parse(bundleText),expected=(await import('../hosted/bundle-hash.mjs')).default;
const hash=x=>createHash('sha256').update(x).digest('hex');
if(hash(bundleText)!==expected||bundle.case.gate.gate0_status!=='PASS_BOUNDED_AHV')throw Error('Evidence bundle authentication failed');
const base=process.env.LOCAL_MODEL_URL||'http://host.docker.internal:8768/v1';
if(!['http://host.docker.internal:8768/v1','http://127.0.0.1:8768/v1'].includes(base))throw Error('Use the documented local model bridge');
const identity=JSON.parse(await readFile(process.env.LOCAL_IDENTITY_FILE||'/run/local-identity.json','utf8'));
if(identity.backing_checkpoint!=='swiss-ai/Apertus-v1.5-8B'||identity.artifacts?.['model.safetensors']?.sha256!=='d0478edeb06bf18e5f4f7b50db77d89b839730b2d16cb1020015e6099e42074b'||!identity.v1_5_verified)throw Error('Pinned local model inspection required');
const models=await(await fetch(base+'/models',{signal:AbortSignal.timeout(10000)})).json();
if(!models.data?.some(m=>m.id===identity.model_dir))throw Error('Local endpoint does not serve the inspected model');
const localContract=JSON.parse(await readFile(new URL('onprem/query-contract.json',root),'utf8'));
const executionHash=hash(bundleText+JSON.stringify(localContract));
const cases=()=>bundle.cases||{ahv13:bundle.case};
let busy=false;
const headers={'Cache-Control':'no-store','X-Content-Type-Options':'nosniff','Referrer-Policy':'no-referrer','Content-Security-Policy':"default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'"};
const server=http.createServer(async(req,res)=>{
 const send=(status,data,type='application/json; charset=utf-8')=>{const body=Buffer.isBuffer(data)?data:typeof data==='string'?data:JSON.stringify(data);res.writeHead(status,{...headers,'Content-Type':type});res.end(body);};
 try{
  const url=new URL(req.url,'http://localhost'),id=url.searchParams.get('case')||'ahv13',c=cases()[id];
  if(req.method==='GET'){
   if(url.pathname==='/api/cases')return send(200,cases());
   if(url.pathname==='/api/case')return c?send(200,c):send(404,{error:'Vote not found'});
   if(url.pathname==='/api/catalog')return send(200,bundle.catalog);
   if(url.pathname==='/api/health')return send(200,{status:'ok',gate0:bundle.case.gate.gate0_status,mode:'LOCAL_APERTUS_DOCKER_APP',bundle_sha256:expected});
   if(url.pathname==='/api/live/status')return send(200,{configured:true,model:identity.backing_checkpoint,provider:'Apertus on this computer',local:true,private_notes_sent:false});
   if(url.pathname==='/api/booklet.pdf'){
    if(!c)return send(404,{error:'Vote not found'});
    const pdf=await readFile('/sources/'+id+'.pdf');if(hash(pdf)!==c.source_sha256)throw Error('Source PDF authentication failed');return send(200,pdf,'application/pdf');
   }
   const path=url.pathname==='/'?'index.html':url.pathname.slice(1);
   if(!/^(index\.html|app\.js|vault\.js|answer\.js|style\.css|local\.html|judges\.html|assets\/[a-z0-9-]+\.svg)$/.test(path))return send(404,{error:'Not found'});
   const mime=path.endsWith('.js')?'text/javascript':path.endsWith('.css')?'text/css':path.endsWith('.svg')?'image/svg+xml':'text/html';return send(200,await readFile(new URL('web/'+path,root)),mime+'; charset=utf-8');
  }
  if(req.method!=='POST'||url.pathname!=='/api/live/question')return send(404,{error:'Not found'});
  if(!c)return send(404,{error:'Vote not found'});
  if(req.headers.origin&&new URL(req.headers.origin).host!==req.headers.host)return send(400,{error:'Use this app to ask a question'});
  if(!req.headers['content-type']?.startsWith('application/json'))return send(400,{error:'Send one public question'});
  let raw='';for await(const chunk of req){raw+=chunk;if(Buffer.byteLength(raw)>4096)return send(400,{error:'Question too long'});}
  let data;try{data=JSON.parse(raw);if(!questionPayload(data))throw Error();}catch{return send(400,{error:'Send one public question without private information'});}
  if(busy)return send(429,{outcome:'BUSY',error:'Apertus is answering another question. Please try again shortly.',live_inference_performed_for_this_request:false});
  busy=true;const started=Date.now();let performed=false;
  try{
   const matched=await matchLocalQuestion(c,localContract,data.question,(prompt,max,system,schema)=>localCompletion(base,prompt,max,system,schema,data.question,trace=>{if(trace.response?.choices?.length)performed=true;})
   );
   const result={...composeAnswer(c,matched.plan,matched.ids,matched.scope.scope),contract:localContract.contract,execution_contract_sha256:executionHash,source_bundle_sha256:expected,model:identity.backing_checkpoint,model_identity_basis:'PINNED_LOCAL_WEIGHTS',provider:'LOCAL_APERTUS',model_tasks:matched.tasks,live_inference_performed_for_this_request:performed,human_reviewed:false,case_id:c.case_id,as_of:c.as_of,source_sha256:c.source_sha256,answered_at:new Date().toISOString(),latency_seconds:(Date.now()-started)/1000};result.receipt=hash(JSON.stringify(result));return send(200,result);
  }catch{return send(503,{outcome:'SERVICE_UNAVAILABLE',error:'Apertus could not answer this question. You can still read the sources below.',live_inference_performed_for_this_request:performed});}finally{busy=false;}
 }catch{return send(503,{error:'This information is temporarily unavailable. Please try again.'});}
});
server.requestTimeout=300000;server.listen(Number(process.env.PORT||8770),'0.0.0.0',()=>console.log('StimmFolgen ready; local Apertus only. No request-body logging.'));
