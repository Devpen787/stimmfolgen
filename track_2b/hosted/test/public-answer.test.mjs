import test from'node:test';import assert from'node:assert/strict';import{answerFitsCase}from'../../web/answer.js';
test('late public answers cannot cross vote, wording or epistemic boundaries',()=>{
 const source={case_id:'fictional-A',source_sha256:'source-A',cards:[{id:'same-id',statement:'A forecast, not a guarantee.',kind:'ATTRIBUTED_PREDICTION'}]};
 const answer={case_id:source.case_id,source_sha256:source.source_sha256,claims:[{fact_ids:['same-id'],text:source.cards[0].statement,evidence_kinds:['ATTRIBUTED_PREDICTION']}]};
 assert.equal(answerFitsCase(answer,source),true);assert.equal(answerFitsCase({...answer,case_id:'fictional-B'},source),false);assert.equal(answerFitsCase({...answer,source_sha256:'source-B'},source),false);
 for(const claim of [{...answer.claims[0],text:'Invented'},{...answer.claims[0],evidence_kinds:['DIRECT_PROVISION']},{...answer.claims[0],fact_ids:['unknown-id']}])assert.equal(answerFitsCase({...answer,claims:[claim]},source),false);
 assert.equal(answerFitsCase({error:'Unavailable'},source),true);
});
