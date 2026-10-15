import{rank,planErrors,directnessErrors,directnessPrompt}from'./retrieval.mjs';
export function scopePrompt(c,question){return JSON.stringify({question,open_proposal:c.title,evidence_as_of:c.as_of});}
export function queryPrompt(c,question){return 'QUESTION='+JSON.stringify(question)+'\nOPEN_PROPOSAL='+JSON.stringify(c.title)+'\nEVIDENCE_AS_OF='+JSON.stringify(c.as_of);}
export function oneField(x,key,valid){return x&&typeof x==='object'&&!Array.isArray(x)&&Object.keys(x).join(',')===key&&valid(x[key]);}
export function queryErrors(x){const errors=planErrors(x);return errors.length===1&&errors[0]==='query_kind_conflict'?[]:errors;}
export function contractErrors(c){return Object.entries({time_system:1800,query_system:6000,directness_system:2400}).filter(([key,max])=>typeof c?.[key]!=='string'||!c[key].trim()||c[key].length>max||/async\s+function|process\.argv|writeFile\(|parseCompletion\(/.test(c[key])).map(([key])=>'invalid_system_prompt:'+key);}
export async function matchQuestion(c,k,question,call){
 if(contractErrors(k).length)throw Error('Invalid matching contract');
 const raw=await call(queryPrompt(c,question),350,k.query_system,k.query_schema),tasks=['QUERY_INTERPRETATION'];
 if(queryErrors(raw).length)throw Error('Invalid query');
 if(raw.kind==='VOTING_ADVICE')return{plan:{kind:raw.kind,intent:'NONE',focus:'',limit:0},ids:[],tasks,scope:{scope:'VOTING_ADVICE'}};
 if(explicitOtherProposal(c,question))return{plan:{kind:'OUTSIDE_EVIDENCE',intent:'NONE',focus:'',limit:0},ids:[],tasks,scope:{scope:'OTHER_PROPOSAL'}};
 const time=await call(scopePrompt(c,question),80,k.time_system,k.time_schema);tasks.push('OBSERVED_TIME_CHECK');
 if(!oneField(time,'actual_later',v=>typeof v==='boolean'))throw Error('Invalid temporal scope');
 if(time.actual_later)return{plan:{kind:'OUTSIDE_EVIDENCE',intent:'NONE',focus:'',limit:0},ids:[],tasks,scope:{scope:'LATER_EVENTS'}};
 const plan={...raw,kind:'EVIDENCE'},ids=[];
 if(!plan.focus||plan.intent==='NONE'||!plan.limit)return{plan,ids,tasks,scope:{scope:'CURRENT_PROPOSAL'}};
 if(planErrors(plan).length)throw Error('Invalid query');
 // Only topical lexical support enters the shortlist. No model-only fallback.
 for(const {id}of rank(c,plan.focus).slice(0,3)){
  if(ids.length>=plan.limit)break;
  const card=c.cards.find(x=>x.id===id),check=await call(directnessPrompt(c,question,card,plan.focus),80,k.directness_system,k.directness_schema);
  if(directnessErrors(check).length)throw Error('Invalid directness check');
  if(!tasks.includes('ORIGINAL_QUESTION_DIRECTNESS_CHECK'))tasks.push('ORIGINAL_QUESTION_DIRECTNESS_CHECK');
  if(check.direct)ids.push(id);
 }
 return{plan,ids,tasks,scope:{scope:'CURRENT_PROPOSAL'}};
}

// Conservative name routing, independent of source/answer IDs. Unnamed questions
// retain the user's selected proposal. This is not a general proposal importer.
export function explicitOtherProposal(c,question){
 const normalize=s=>s.toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g,'');
 const aliases=new Set((normalize(c.title).match(/[\p{L}\p{N}]+/gu)||[]));
 const generic=new Set('the a an this that our original new current same proposed public federal national dieser diese dieses der die das den dem einer eine ein ursprunglich ursprungliche ursprunglichen ursprunglicher cette cet ce la le les'.split(' '));
 const q=normalize(question),names=[...q.matchAll(/([\p{L}\p{N}]+)[ -]+(?:initiative|proposal|reform|ban|referendum)\b/gu)].map(m=>m[1]);
 for(const m of q.matchAll(/\b([\p{L}\p{N}]{2,})(?:initiative)\b/gu))names.push(m[1]);
 return names.some(name=>!generic.has(name)&&!aliases.has(name));
}
