import {DurableObject} from 'cloudflare:workers';
import bundleText from './public-bundle.json' with {type:'text'};
import expectedHash from './bundle-hash.mjs';
import {MODEL,LIMITS,candidateErrors,reviewPass,questionPayload,promptFrom,citationsFor,modelAvailable,completion,boundedText} from './qa.mjs';
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
  const start=Date.now();let result={outcome:'SERVICE_UNAVAILABLE',claims:[],unknowns:[],live_inference_performed_for_this_request:false,human_reviewed:false,publication_state:'LIVE_AI_UNREVIEWED',as_of:bundle.case.as_of,source_sha256:bundle.case.source_sha256,model:MODEL,contract:bundle.contract,provider:'PUBLIC_AI',hosting:'CLOUDFLARE_GLOBAL_NOT_SWISS_SOVEREIGN',model_identity_basis:'PROVIDER_REPORTED_NOT_WEIGHT_ATTESTED',semantic_check:'SEPARATE_PASS_SAME_MODEL_NOT_INDEPENDENT_REVIEW'};
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
   const candidate=await completion(this.env.PUBLICAI_TOKEN,promptFrom(bundle.generation_template,question),850,bundle.generator_system,fetch,()=>{result.live_inference_performed_for_this_request=true;});
   result.live_inference_performed_for_this_request=true;
   if(candidateErrors(candidate,bundle.case).length){result.outcome='WITHHELD';result.error='Apertus could not produce a valid grounded answer. Read the reviewed explanation.';}
   else{
    const review=await completion(this.env.PUBLICAI_TOKEN,promptFrom(bundle.review_template,question,candidate),200,'Audit evidence support strictly. Return the requested JSON checks.');
    if(!reviewPass(review)){result.outcome='WITHHELD';result.error='The answer did not pass the separate meaning check. Read the reviewed explanation or try a narrower question.';}
    else Object.assign(result,{outcome:candidate.outcome,claims:citationsFor(candidate,bundle.case),unknowns:candidate.unknowns,checks:review});
   }
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
  return gate.fetch(new Request('https://internal/question',{method:'POST',headers:{'Content-Type':'application/json','X-Network':request.headers.get('CF-Connecting-IP')||'local-test'},body:text}));
 }
};
