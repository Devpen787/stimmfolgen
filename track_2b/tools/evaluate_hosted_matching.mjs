// Real provider evaluation. Gold IDs are compared only AFTER inference, never prompted.
// Usage: node track_2b/tools/evaluate_hosted_matching.mjs CASES_JSON OUT_DIR TOKEN_FILE
import{readFile,writeFile,mkdir}from'node:fs/promises';
import{MODEL,completion,promptFrom,modelAvailable,composeAnswer}from'../hosted/qa.mjs';
import{planErrors,normalizePlan,candidates,directnessErrors,directnessPrompt}from'../hosted/retrieval.mjs';
const[caseFile,out,keyFile]=process.argv.slice(2);if(!caseFile||!out||!keyFile)throw Error('Need CASES_JSON OUT_DIR TOKEN_FILE');
const b=JSON.parse(await readFile(new URL('../hosted/public-bundle.json',import.meta.url))),q=b.hosted_query,cases=JSON.parse(await readFile(caseFile)),token=(await readFile(keyFile,'utf8')).trim();await mkdir(out,{recursive:false});await modelAvailable(token);let passed=0;
for(const reference of cases){let traces=[],plan,result;const start=Date.now();
 const capture=async(url,options)=>{await new Promise(r=>setTimeout(r,1800));const response=await fetch(url,options),raw=await response.clone().text();let body;try{body=JSON.parse(raw)}catch{body={raw_response_text:raw}}traces.push({request:JSON.parse(options.body),status:response.status,response:body});return response};
 try{plan=await completion(token,promptFrom(q.planner_template,reference.question),350,q.planner_system,capture,()=>{},q.plan_schema);plan=normalizePlan(plan);if(planErrors(plan).length)throw Error('Invalid query plan');
 const ids=[];for(const id of candidates(b.case,plan)){if(ids.length>=plan.limit)break;const card=b.case.cards.find(c=>c.id===id),check=await completion(token,directnessPrompt(b.case,reference.question,card,plan.focus),80,q.directness_system,capture,()=>{},q.directness_schema);if(directnessErrors(check).length)throw Error('Invalid directness check');if(check.direct)ids.push(id)}
 result={ids,pass:plan.kind===reference.kind&&JSON.stringify([...ids].sort())===JSON.stringify([...reference.ids].sort()),answer:composeAnswer(b.case,plan,ids)};
 }catch(error){result={pass:false,error:error.message}}passed+=Number(result.pass);await writeFile(out+'/'+reference.id+'.json',JSON.stringify({contract:q.contract,model:MODEL,reference,plan,result,traces,elapsed_seconds:(Date.now()-start)/1000},null,2)+'\n');console.log(JSON.stringify({id:reference.id,pass:result.pass,ids:result.ids,error:result.error}));}
await writeFile(out+'/summary.json',JSON.stringify({passed,total:cases.length,contract:q.contract},null,2)+'\n');console.log(passed+'/'+cases.length);
