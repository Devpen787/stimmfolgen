// Shared response contract with the native app; fixtures never imply real inference.
export const MODEL='swiss-ai/apertus-v1.5-8b';
export const REVIEW_FIELDS=['entailed','actor_correct','time_correct','uncertainty_preserved','no_advice','answers_question'];
export const LIMITS=Object.freeze({lifetime:200,daily:80,promptBytes:16000,responseBytes:262144});
export function candidateErrors(a, caseData){
 const keys=(o,expected)=>o&&typeof o==='object'&&!Array.isArray(o)&&Object.keys(o).sort().join(',')===[...expected].sort().join(',');
 if(!keys(a,['outcome','claims','unknowns']))return ['invalid_answer_shape'];
 const errors=[], facts=new Set(caseData.cards.map(c=>c.id));
 if(!['SUPPORTED','INSUFFICIENT_EVIDENCE'].includes(a.outcome))errors.push('invalid_outcome');
 if(!Array.isArray(a.claims)||a.claims.length>4)return [...errors,'invalid_claims'];
 if(a.outcome==='SUPPORTED'&&!a.claims.length)errors.push('empty_supported_answer');
 if(!Array.isArray(a.unknowns)||a.unknowns.length>4||a.unknowns.some(x=>typeof x!=='string'||!x.length||x.length>400))errors.push('invalid_unknowns');
 if(a.outcome==='INSUFFICIENT_EVIDENCE'&&!a.unknowns?.length)errors.push('abstention_requires_reason');
 for(const c of a.claims){
  if(!keys(c,['text','fact_ids'])){errors.push('invalid_claim');continue;}
  if(typeof c.text!=='string'||!c.text.length||c.text.length>700)errors.push('invalid_text');
  if(!Array.isArray(c.fact_ids)||!c.fact_ids.length||c.fact_ids.length>5||c.fact_ids.some(i=>typeof i!=='string'||!facts.has(i)))errors.push('unknown_evidence_reference');
 }
 return errors;
}
export const reviewPass=r=>r&&typeof r==='object'&&!Array.isArray(r)&&Object.keys(r).sort().join(',')===[...REVIEW_FIELDS].sort().join(',')&&Object.values(r).every(v=>v===true);
export function questionPayload(value){
 return value&&typeof value==='object'&&!Array.isArray(value)&&Object.keys(value).join(',')==='question'&&typeof value.question==='string'&&value.question.trim().length>=3&&value.question.trim().length<=700;
}
export function parseCompletion(raw){
 if(!raw||raw.model!==MODEL||!Array.isArray(raw.choices)||raw.choices[0]?.finish_reason!=='stop')throw Error('Invalid model identity or completion');
 let text=raw.choices[0].message?.content;
 if(typeof text!=='string')throw Error('Invalid content');
 text=text.trim().replace(/^```(?:json)?\s*|\s*```$/gi,'');
 return JSON.parse(text);
}
export function promptFrom(template,question,candidate){
 let result=template;
 if(candidate!==undefined)result=result.replace('{"__CANDIDATE__": true}',()=>JSON.stringify(candidate));
 result=result.replace('"__QUESTION__"',()=>JSON.stringify(question));
 if(new TextEncoder().encode(result).length>LIMITS.promptBytes)throw Error('Prompt too large');
 return result;
}
export function citationsFor(candidate,caseData){
 const facts=new Map(caseData.cards.map(c=>[c.id,c]));
 return candidate.claims.map(c=>({...c,citations:[...new Map(c.fact_ids.flatMap(i=>facts.get(i).citations).map(s=>[s.span_id,s])).values()],evidence_kinds:[...new Set(c.fact_ids.map(i=>facts.get(i).kind))].sort()}));
}
export async function boundedText(body,limit){
 if(!body)throw Error('Empty body');
 const reader=body.getReader();let size=0,chunks=[];
 try{for(;;){const {done,value}=await reader.read();if(done)break;size+=value.length;if(size>limit)throw Error('Response too large');chunks.push(value);}}
 finally{await reader.cancel();}
 const bytes=new Uint8Array(size);let offset=0;for(const chunk of chunks){bytes.set(chunk,offset);offset+=chunk.length;}
 return new TextDecoder('utf-8',{fatal:true}).decode(bytes);
}
export async function responseJSON(response){
 if(!response.ok)throw Error('Provider HTTP '+response.status);
 return JSON.parse(await boundedText(response.body,LIMITS.responseBytes));
}
export async function modelAvailable(token,fetcher=fetch){
 const response=await fetcher('https://api.publicai.co/v1/models',{headers:{Authorization:'Bearer '+token,'User-Agent':'StimmFolgen/0.4'},redirect:'manual',signal:AbortSignal.timeout(20000)});
 const models=await responseJSON(response);const model=models.data?.find(m=>m.id===MODEL);
 if(!model||!model.pricing||typeof model.pricing.input!=='number'||typeof model.pricing.output!=='number'||model.pricing.input<0||model.pricing.output<0||model.pricing.input>0.1||model.pricing.output>0.2)throw Error('Required model or bounded pricing unavailable');
 return model;
}
export async function completion(token,prompt,maxTokens,system,fetcher=fetch,onResponse=()=>{}){
 const response=await fetcher('https://api.publicai.co/v1/chat/completions',{method:'POST',headers:{Authorization:'Bearer '+token,'Content-Type':'application/json','User-Agent':'StimmFolgen/0.4'},redirect:'manual',signal:AbortSignal.timeout(120000),body:JSON.stringify({model:MODEL,temperature:0,max_tokens:maxTokens,stream:false,messages:[{role:'system',content:system},{role:'user',content:prompt}]})});
 const raw=await responseJSON(response);
 if(raw.model===MODEL&&raw.choices?.length)onResponse();
 return parseCompletion(raw);
}
