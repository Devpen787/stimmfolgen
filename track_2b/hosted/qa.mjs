// Model output chooses references only; all published wording comes from reviewed case data.
export const MODEL='swiss-ai/apertus-v1.5-8b';
export const LIMITS=Object.freeze({lifetime:200,daily:80,promptBytes:16000,responseBytes:262144});
export function selectionErrors(s,caseData){
 if(!s||typeof s!=='object'||Array.isArray(s)||Object.keys(s).sort().join(',')!=='fact_ids,kind')return ['invalid_selection_shape'];
 const known=new Set(caseData.cards.map(c=>c.id)),ids=s.fact_ids;
 if(!['EVIDENCE','VOTING_ADVICE','OUTSIDE_EVIDENCE'].includes(s.kind))return ['invalid_selection_kind'];
 if(!Array.isArray(ids)||ids.length>known.size||ids.some(i=>typeof i!=='string'||!known.has(i)))return ['unknown_evidence_reference'];
 if(new Set(ids).size!==ids.length)return ['duplicate_evidence_reference'];
 if(Boolean(ids.length)!==(s.kind==='EVIDENCE'))return ['selection_kind_conflict'];
 return [];
}
export function matchReviewErrors(review,selection){
 if(!review||typeof review!=='object'||Array.isArray(review)||Object.keys(review).join(',')!=='fact_ids'||!Array.isArray(review.fact_ids))return ['invalid_relevance_review'];
 review=review.fact_ids;
 if(review.length>selection.fact_ids.length)return ['invalid_relevance_review'];
 if(review.some(i=>typeof i!=='string'||!selection.fact_ids.includes(i)))return ['unselected_evidence_reference'];
 if(new Set(review).size!==review.length)return ['duplicate_evidence_reference'];
 return [];
}
export function composeAnswer(caseData,selection,reviewedIds,scope=null){
 const facts=new Map(caseData.cards.map(c=>[c.id,c]));
 const claims=reviewedIds.map(id=>({text:facts.get(id).statement,fact_ids:[id],citations:facts.get(id).citations,evidence_kinds:[facts.get(id).kind]}));
 if(claims.length)return {outcome:'EVIDENCE_MATCH',answer_mode:'REVIEWED_EVIDENCE',claims,unknowns:[],statements_human_reviewed:true};
 const advice=selection.kind==='VOTING_ADVICE';
 const scoped=scope==='OTHER_PROPOSAL'?'This question appears to concern another proposal. Live analysis here covers '+caseData.title+'. Open the other vote to inspect its available sources.':scope==='LATER_EVENTS'?'This live analysis uses the historical evidence frame shown below. For later events, open Updates.':null;
 return {outcome:'INSUFFICIENT_EVIDENCE',answer_mode:advice?'SERVICE_LIMIT':'EVIDENCE_LIMIT',claims:[],unknowns:[scoped||(advice?'StimmFolgen does not recommend how to vote. You can explore the sources and perspectives to form your own view.':'No matching reviewed answer was found in this historical AHV evidence. This does not mean the event or effect did not happen. For later information, open Updates.')],statements_human_reviewed:false};
}
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
export function promptFrom(template,question,selection){
 let result=template;
 if(selection!==undefined)result=result.replace('{"__CANDIDATE__": true}',()=>JSON.stringify(selection));
 result=result.replace('"__QUESTION__"',()=>JSON.stringify(question));
 if(new TextEncoder().encode(result).length>LIMITS.promptBytes)throw Error('Prompt too large');
 return result;
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
export async function completion(token,prompt,maxTokens,system,fetcher=fetch,onResponse=()=>{},schema=null){
 const response=await fetcher('https://api.publicai.co/v1/chat/completions',{method:'POST',headers:{Authorization:'Bearer '+token,'Content-Type':'application/json','User-Agent':'StimmFolgen/0.4'},redirect:'manual',signal:AbortSignal.timeout(120000),body:JSON.stringify({model:MODEL,temperature:0,max_tokens:maxTokens,stream:false,...(schema?{response_format:{type:'json_schema',json_schema:{name:'bounded_match',strict:true,schema}}}:{}),messages:[{role:'system',content:system},{role:'user',content:prompt}]})});
 const raw=await responseJSON(response);
 if(raw.model===MODEL&&raw.choices?.length)onResponse();
 return parseCompletion(raw);
}

export function executionMatches(payload,expectedHash){
 return payload.live_inference_performed_for_this_request!==true||payload.execution_contract_sha256===expectedHash;
}
