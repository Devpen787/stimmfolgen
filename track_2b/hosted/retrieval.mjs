// BM25F relevance ranking only, never a truth/confidence score.
const STOP=new Set('a an the this that these those of to for in on at and or as is are was were would will could should can does do did be been being have has had by with from it its their they them under about what which who whose how whether specific individuals someone person people information amount initiative proposal current'.split(' '));
export function tokens(text){return (text.toLowerCase().normalize('NFKD').match(/[a-z0-9]+/g)||[]).filter(t=>!STOP.has(t)).map(t=>{if(t.length>4&&t.endsWith('ies'))t=t.slice(0,-3)+'y';else if(t.length>4&&t.endsWith('es'))t=t.slice(0,-2);else if(t.length>3&&t.endsWith('s'))t=t.slice(0,-1);if(t.length>5&&t.endsWith('ing'))t=t.slice(0,-3);else if(t.length>4&&t.endsWith('ed'))t=t.slice(0,-2);if(t.length>4&&t.endsWith('e'))t=t.slice(0,-1);return t;});}
export function rank(caseData,focus){
 const cards=caseData.cards;if(!cards.length)return [];
 const titles=cards.map(c=>tokens(c.title)),bodies=cards.map(c=>tokens(c.statement)),documents=titles.map((a,i)=>[...a,...bodies[i]]),df=new Map();
 for(const doc of documents)for(const t of new Set(doc))df.set(t,(df.get(t)||0)+1);
 const threshold=Math.max(3,Math.ceil(cards.length*.6)),query=[...new Set(tokens(focus))].filter(t=>(df.get(t)||0)<threshold).sort(),at=Math.max(1,titles.reduce((n,d)=>n+d.length,0)/cards.length),ab=Math.max(1,bodies.reduce((n,d)=>n+d.length,0)/cards.length);
 return cards.map((c,i)=>{let score=0;for(const term of query){const f=df.get(term)||0,idf=Math.log(1+(cards.length-f+.5)/(f+.5));for(const[field,avg,weight]of[[titles[i],at,5],[bodies[i],ab,1]]){const tf=field.filter(t=>t===term).length;if(tf)score+=weight*idf*tf*2.2/(tf+1.2*(.25+.75*field.length/avg));}}return{id:c.id,score:Math.round(score*1e8)/1e8};}).filter(x=>x.score>0).sort((a,b)=>b.score-a.score||(a.id<b.id?-1:a.id>b.id?1:0));
}
export function retrieve(caseData,plan){return plan.kind==='EVIDENCE'?rank(caseData,plan.focus).slice(0,plan.limit).map(x=>x.id):[];}
export function planErrors(p){
 if(!p||typeof p!=='object'||Array.isArray(p)||Object.keys(p).sort().join(',')!=='focus,intent,kind,limit')return ['invalid_query_plan'];
 if(!['EVIDENCE','VOTING_ADVICE','OUTSIDE_EVIDENCE'].includes(p.kind)||!['SPEAKER','CONTENT','NONE'].includes(p.intent)||typeof p.focus!=='string'||p.focus.length>500||!Number.isInteger(p.limit)||p.limit<0||p.limit>3)return ['invalid_query_plan'];
 if(p.kind==='EVIDENCE' ? (!p.focus.trim()||p.limit<1||p.intent==='NONE') : (p.focus!==''||p.limit!==0||p.intent!=='NONE'))return ['query_kind_conflict'];
 return [];
}
export function directnessErrors(check){return !check||typeof check!=='object'||Array.isArray(check)||Object.keys(check).join(',')!=='direct'||typeof check.direct!=='boolean'?['invalid_directness_check']:[];}
export function directnessPrompt(caseData,question,card,focus){return JSON.stringify({question,retrieval_focus:focus,open_proposal:caseData.title,as_of:caseData.as_of,candidate:{kind:card.kind,statement:card.statement,actors:card.citations.map(c=>c.actor)}});}
// No lexical match means no candidate; a model-only fallback was rejected.
export function candidates(caseData,plan){return retrieve(caseData,plan);}
// A refusal never uses retrieval metadata. Discard contradictory unused fields
// without changing the model's scope decision or turning a refusal into evidence.
export function normalizePlan(plan){
 return planErrors(plan).includes('query_kind_conflict')&&plan.kind!=='EVIDENCE'?{...plan,intent:'NONE',focus:'',limit:0}:plan;
}
