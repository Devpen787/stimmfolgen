#!/usr/bin/env node
// Explicit evaluation only: public authored questions, raw traces without auth headers.
// Production does not persist questions. Uses finite provider credit; never tops up.
import {parseArgs} from 'node:util';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {completion,MODEL,modelAvailable,selectionErrors,matchReviewErrors,composeAnswer,promptFrom} from '../hosted/qa.mjs';
const {values}=parseArgs({options:{cases:{type:'string'},'token-file':{type:'string'},out:{type:'string'}}});
if(!values.cases||!values['token-file']||!values.out)throw Error('Required: --cases PUBLIC_CASES.json --token-file PRIVATE_FILE --out NEW_DIRECTORY');
const cases=JSON.parse(await readFile(values.cases,'utf8'));
if(!Array.isArray(cases)||!cases.length||cases.length>32||cases.some(c=>!c.id?.match(/^[a-z0-9_-]+$/)||typeof c.question!=='string'||c.question.length>700||!Array.isArray(c.ids))||new Set(cases.map(c=>c.id)).size!==cases.length)throw Error('Invalid bounded public evaluation cases');
const bytes=await readFile(new URL('../hosted/public-bundle.json',import.meta.url),'utf8'),bundle=JSON.parse(bytes),token=(await readFile(values['token-file'],'utf8')).trim();
await mkdir(values.out);await modelAvailable(token);let passed=0;
for(const c of cases){
 const traces=[],start=Date.now();let result,selection,review=[];
 const save=()=>writeFile(values.out+'/'+c.id+'.json',JSON.stringify({evidence_class:'ACTUAL_PUBLIC_AI_SOURCE_MATCH_EVALUATION',contract:bundle.contract,bundle_sha256:createHash('sha256').update(bytes).digest('hex'),model:MODEL,source_sha256:bundle.case.source_sha256,as_of:bundle.case.as_of,evaluation_reference:c,selection,review,result,elapsed_seconds:(Date.now()-start)/1000,traces},null,2)+'\n');
 const fetcher=async(url,options)=>{const r=await fetch(url,options);traces.push({url,request:JSON.parse(options.body),status:r.status,response:await r.clone().json()});await save();return r;};
 try{
  selection=await completion(token,promptFrom(bundle.generation_template,c.question),250,bundle.generator_system,fetcher);
  let errors=selectionErrors(selection,bundle.case);if(errors.length)throw Error(errors.join(','));
  if(selection.kind==='EVIDENCE'){review=await completion(token,promptFrom(bundle.review_template,c.question,selection),250,bundle.review_system,fetcher);errors=matchReviewErrors(review,selection);if(errors.length)throw Error(errors.join(','));}
  const answer=composeAnswer(bundle.case,selection,selection.kind==='EVIDENCE'?review.fact_ids:[]),ids=answer.claims.flatMap(x=>x.fact_ids);
  result={answer,pass:selection.kind===c.kind&&JSON.stringify([...ids].sort())===JSON.stringify([...c.ids].sort())};
 }catch(error){result={pass:false,error:error.message};}
 await save();passed+=Number(result.pass);console.log(JSON.stringify({id:c.id,pass:result.pass,selection,review,error:result.error}));
}
console.log(JSON.stringify({exact_reference_matches:passed,total:cases.length,scope:'Authored development questions; not general accuracy or independent user research'}));
process.exitCode=passed===cases.length?0:2;
