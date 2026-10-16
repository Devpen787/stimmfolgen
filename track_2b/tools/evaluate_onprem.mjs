// Explicit authored-public-question evaluation only; never production note logging.
import{readFile,mkdir,writeFile}from'node:fs/promises';
import{localCompletion}from'../onprem/adapter.mjs';
import{matchLocalQuestion}from'../onprem/matching.mjs';import{composeAnswer}from'../hosted/qa.mjs';
const[file,out,candidateFile]=process.argv.slice(2),b=JSON.parse(await readFile(new URL('../hosted/public-bundle.json',import.meta.url))),cases=JSON.parse(await readFile(file)),localContract=JSON.parse(await readFile(new URL('../onprem/query-contract.json',import.meta.url)));if(candidateFile)b.cases={...(b.cases||{ahv13:b.case}),'home-tax':JSON.parse(await readFile(candidateFile))};await mkdir(out,{recursive:false});
for(const item of cases){const c=(b.cases||{ahv13:b.case})[item.case||'ahv13'],traces=[];let result;
 try{const m=await matchLocalQuestion(c,localContract,item.question,(prompt,max,system,schema)=>localCompletion('http://127.0.0.1:8768/v1',prompt,max,system,schema,item.question,t=>traces.push(t)));result={plan:m.plan,ids:m.ids,pass:m.plan.kind===item.kind&&JSON.stringify([...m.ids].sort())===JSON.stringify([...item.ids].sort()),answer:composeAnswer(c,m.plan,m.ids,m.scope.scope)};}catch(e){result={pass:false,error:e.message}}
 await writeFile(out+'/'+item.id+'.json',JSON.stringify({reference:item,result,traces},null,2));console.log(item.id,result.pass,result.ids,result.error||'');}
