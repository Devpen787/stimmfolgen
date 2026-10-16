import test from'node:test';import assert from'node:assert/strict';import{readFileSync}from'node:fs';
import{matchQuestion,contractErrors,queryErrors,queryPrompt,explicitOtherProposal}from'../matching.mjs';
const b=JSON.parse(readFileSync(new URL('../public-bundle.json',import.meta.url))),k=b.hosted_query;
function query(focus,kind='EVIDENCE'){return{kind,intent:'CONTENT',focus,limit:1};}
test('system prompts reject leaked evaluator code before inference',async()=>{
 assert.deepEqual(contractErrors(k),[]);const bad={...k,directness_system:k.directness_system+'\nasync function call(){writeFile(out,c.ids)}'};assert.ok(contractErrors(bad).length);let called=false;await assert.rejects(matchQuestion(b.case,bad,'A question?',async()=>{called=true}),/Invalid matching contract/);assert.equal(called,false);
});
test('query planning receives neither source answers nor gold data',()=>{
 const prompt=queryPrompt(b.case,'A public question');assert.ok(!b.case.cards.some(c=>prompt.includes(c.statement)));for(const c of b.case.cards)assert.ok(!prompt.includes(c.id));assert.ok(queryErrors({...query('budget'),text:'invented'}).length);
});
test('pay/charge search works on a fictional definite fee with arbitrary IDs',async()=>{
 const c={title:'Fictional club reform',as_of:'2020',cards:[{id:'opaque-x',title:'Public budget',kind:'COST_PROJECTION',statement:'The system would spend 900 tokens.',citations:[]},{id:'opaque-y',title:'Membership fee',kind:'DIRECT_PROVISION',statement:'Each member has a personal charge of 12 tokens.',citations:[]}]},seen=[];
 const r=await matchQuestion(c,k,'Do members pay?',async(prompt,max,system,schema)=>{seen.push(prompt);if(schema.properties.focus)return query('Do members pay?');if(schema.properties.actual_later)return{actual_later:false};return{direct:true};});assert.deepEqual(r.ids,['opaque-y']);assert.ok(!JSON.stringify(seen).includes('opaque-y'));
});
test('a different proposal is refused independently of the query generator kind',async()=>{
 let n=0;const r=await matchQuestion(b.case,k,'What about airport reform?',async(prompt,max,system,schema)=>{n++;if(schema.properties.focus)return query('economic effects of airport reform');throw Error('Other proposal must not search')});assert.equal(r.plan.kind,'OUTSIDE_EVIDENCE');assert.equal(r.scope.scope,'OTHER_PROPOSAL');assert.deepEqual(r.ids,[]);assert.equal(n,1);
});
test('query scope cannot override same-proposal and observed-time checks for a missing topic',async()=>{
 let n=0;const r=await matchQuestion(b.case,k,'Are lunar effects established?',async(prompt,max,system,schema)=>{n++;if(schema.properties.focus)return query('Whether lunar effects are established','OUTSIDE_EVIDENCE');if(schema.properties.actual_later)return{actual_later:false};throw Error('Generic establish/effect words should not match a source')});assert.equal(r.plan.kind,'EVIDENCE');assert.deepEqual(r.ids,[]);assert.equal(n,2);
});
test('later observations and voting advice never reach the source matcher',async()=>{
 let n=0;const later=await matchQuestion(b.case,k,'What actually happened later?',async(prompt,max,system,schema)=>{n++;if(schema.properties.focus)return query('later events');return{actual_later:true}});assert.equal(n,2);assert.equal(later.scope.scope,'LATER_EVENTS');assert.deepEqual(later.ids,[]);
 let calls=0;const advice=await matchQuestion(b.case,k,'Choose my vote',async()=>{calls++;return{kind:'VOTING_ADVICE',intent:'NONE',focus:'',limit:0}});assert.equal(calls,1);assert.equal(advice.plan.kind,'VOTING_ADVICE');
});

test('proposal name routing uses the selected title, not known vote names',()=>{
 const c={title:'Lunar observatory initiative'};
 for(const q of ['What does this initiative mean?','What is the lunar initiative?','Who made the forecast?'])assert.equal(explicitOtherProposal(c,q),false,q);
 for(const q of ['What does the airport initiative change?','Does the fisheries ban apply?','Was bedeutet die Flughafeninitiative?'])assert.equal(explicitOtherProposal(c,q),true,q);
 assert.equal(explicitOtherProposal({title:'Airport initiative'},'What does the airport initiative change?'),false);
});
