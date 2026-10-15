import {DurableObject} from 'cloudflare:workers';
import bundleText from './public-bundle.json' with {type:'text'};
import expectedHash from './bundle-hash.mjs';
import {MODEL,LIMITS,composeAnswer,questionPayload,promptFrom,modelAvailable,completion,boundedText,executionMatches} from './qa.mjs';
import {planErrors,normalizePlan,candidates,directnessErrors,directnessPrompt} from './retrieval.mjs';
const bundle=JSON.parse(bundleText);
export const headers={'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store','X-Content-Type-Options':'nosniff','Referrer-Policy':'no-referrer','Content-Security-Policy':"default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'"};
const json=(data,status=200)=>new Response(JSON.stringify(data),{status,headers});
export const digest=async text=>[...new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(text)))].map(b=>b.toString(16).padStart(2,'0')).join('');
const authenticated=digest(bundleText).then(hash=>hash===expectedHash&&bundle.case.gate.gate0_status==='PASS_BOUNDED_AHV');
const configured=env=>env.LIVE_ENABLED==='true'&&Boolean(env.PUBLICAI_TOKEN);

export class DemoGate extends DurableObject{
 constructor(ctx,env){super(ctx,env);this.ctx=ctx;this.env=env;this.busy=false;this.clients=new Map();this.salt=crypto.randomUUID();this.ready=ctx.blockConcurrencyWhile(async()=>{this.usage=await ctx.storage.get('usage')||{total:0,day:'',today:0};});}
 async fetch(request){
  await this.ready;
  if(new URL(request.url).pathname==='/status')return json({remaining:Math.max(0,LIMITS.lifetime-this.usage.total),daily_remaining:Math.max(0,LIMITS.daily-(this.usage.day===new Date().toISOString().slice(0,10)?this.usage.today:0))});
  if(!configured(this.env))return json({outcome:'SERVICE_UNAVAILABLE',error:'Live Apertus is not enabled.',live_inference_performed_for_this_request:false},503);
  let data;try{data=await request.json();if(!questionPayload(data))throw Error();}catch{return json({error:'Send one public question without private fields.'},400);}
  if(this.busy)return json({outcome:'BUSY',error:'Apertus is answering another visitor. Please try again shortly.',live_inference_performed_for_this_request:false},429);
  this.busy=true;
  const start=Date.now();let result={outcome:'SERVICE_UNAVAILABLE',claims:[],unknowns:[],live_inference_performed_for_this_request:false,human_reviewed:false,publication_state:'REVIEWED_STATEMENTS_WITH_UNREVIEWED_MODEL_MATCH',as_of:bundle.case.as_of,source_sha256:bundle.case.source_sha256,model:MODEL,contract:bundle.hosted_query.contract,execution_contract_sha256:expectedHash,directness_checks_performed:0,provider:'PUBLIC_AI',hosting:'CLOUDFLARE_GLOBAL_NOT_SWISS_SOVEREIGN',model_identity_basis:'PROVIDER_REPORTED_NOT_WEIGHT_ATTESTED',semantic_check:'IMMUTABLE_REVIEWED_WORDING_AND_BM25F_WITH_SAME_MODEL_DIRECTNESS_CHECK'};
  try{
   const now=Date.now(),day=new Date(now).toISOString().slice(0,10),network=await digest(this.salt+request.headers.get('X-Network'));
   for(const [k,v] of this.clients)if(now-v.start>300000)this.clients.delete(k);
   const client=this.clients.get(network)||{start:now,count:0};
   if(client.count>=6||this.clients.size>=4096)return json({...result,outcome:'LIMIT_REACHED',error:'Please wait a few minutes before another question.'},429);
   if(this.usage.day!==day)this.usage={...this.usage,day,today:0};
   if(this.usage.total>=LIMITS.lifetime||this.usage.today>=LIMITS.daily)return json({...result,outcome:'LIMIT_REACHED',error:'The free demo allowance is used up. Reviewed sources remain available.'},429);
   // Lifetime reservations never reset on redeploy. No questions or IPs are stored.
   this.usage.total++;this.usage.today++;client.count++;this.clients.set(network,client);
   await this.ctx.storage.put('usage',this.usage);
   await modelAvailable(this.env.PUBLICAI_TOKEN);
   const question=data.question.trim();
   const contract=bundle.hosted_query;
   const plan=normalizePlan(await completion(this.env.PUBLICAI_TOKEN,promptFrom(contract.planner_template,question),350,contract.planner_system,fetch,()=>{result.live_inference_performed_for_this_request=true;},contract.plan_schema));
   if(planErrors(plan).length)throw Error('Invalid query plan');
   const reviewedIds=[],retrieved=candidates(bundle.case,plan);
   for(const id of retrieved){
    if(reviewedIds.length>=plan.limit)break;
    const card=bundle.case.cards.find(c=>c.id===id);
    const check=await completion(this.env.PUBLICAI_TOKEN,directnessPrompt(bundle.case,question,card,plan.focus),80,contract.directness_system,fetch,()=>{result.directness_checks_performed++;},contract.directness_schema);
    if(directnessErrors(check).length)throw Error('Invalid directness check');
    if(check.direct)reviewedIds.push(id);
   }
   Object.assign(result,composeAnswer(bundle.case,plan,reviewedIds),{contract:contract.contract,model_tasks:['QUERY_INTERPRETATION',...(result.directness_checks_performed?['ORIGINAL_QUESTION_DIRECTNESS_CHECK']:[])],semantic_check:'IMMUTABLE_REVIEWED_WORDING_AND_BM25F_WITH_SAME_MODEL_DIRECTNESS_CHECK'});
  }catch(error){if(result.live_inference_performed_for_this_request)result.outcome='WITHHELD';result.failure_code=/^(Provider HTTP [0-9]{3}|Invalid model identity or completion|Invalid content|Required model or bounded pricing unavailable|Response too large)$/.test(error.message)?error.message:'PROVIDER_TRANSPORT_OR_FORMAT';result.error='Apertus is unavailable or the free credit is exhausted. No answer was substituted. Reviewed sources remain available.';}
  finally{this.busy=false;}
  result.latency_seconds=Math.round((Date.now()-start)/10)/100;result.answered_at=new Date().toISOString();result.receipt=await digest(JSON.stringify(result));
  return json(result,result.outcome==='SERVICE_UNAVAILABLE'?503:200);
 }
}

export default{
 async fetch(request,env){
  const url=new URL(request.url),path=url.pathname;
  if(!path.startsWith('/api/')){
   const response=await env.ASSETS.fetch(request);const h=new Headers(response.headers);for(const [k,v] of Object.entries(headers))if(k!=='Content-Type')h.set(k,v);return new Response(response.body,{status:response.status,headers:h});
  }
  if(!await authenticated)return json({error:'Authenticated evidence bundle unavailable'},503);
  if(request.method==='GET'){
   if(path==='/api/case')return json(bundle.case);
   if(path==='/api/catalog')return json(bundle.catalog);
   if(path==='/api/health')return json({status:'ok',gate0:bundle.case.gate.gate0_status,mode:'REVIEWED_RECORDED_CASE'});
   if(path==='/api/live/status')return json({configured:configured(env),scope:'AHV historical reviewed evidence only',model:MODEL,provider:'Public AI · website on Cloudflare (global hosting)',private_notes_sent:false,limited_free_demo:true,hosting:'NOT_SWISS_SOVEREIGN'});
   if(path==='/api/booklet.pdf')return Response.redirect(bundle.source_url+url.hash,302);
   return json({error:'Not found'},404);
  }
  if(request.method!=='POST'||path!=='/api/live/question')return json({error:'Not found'},404);
  if(request.headers.get('Origin')&&request.headers.get('Origin')!==url.origin)return json({error:'Cross-origin requests are not accepted'},400);
  if(!request.headers.get('Content-Type')?.startsWith('application/json'))return json({error:'Use application/json'},400);
  let text;try{text=await boundedText(request.body,4096);if(new TextEncoder().encode(text).length>4096||!questionPayload(JSON.parse(text)))throw Error();}catch{return json({error:'Send one public question (3–700 characters), without private fields.'},400);}
  const gate=env.DEMO_GATE.get(env.DEMO_GATE.idFromName('global-free-demo-v1'));
  const response=await gate.fetch(new Request('https://internal/question',{method:'POST',headers:{'Content-Type':'application/json','X-Network':request.headers.get('CF-Connecting-IP')||'local-test'},body:text}));
  const payload=await response.clone().json();
  // Workers and Durable Objects can update at different times. Never publish
  // inference produced under a different evidence/prompt contract.
  if(!executionMatches(payload,expectedHash))return json({outcome:'SERVICE_UNAVAILABLE',error:'Apertus is updating to the current evidence contract. Please retry shortly. Reviewed sources remain available.',live_inference_performed_for_this_request:false},503);
  return response;
 }
};
