import test from'node:test';import assert from'node:assert/strict';import{adaptQuery}from'../../onprem/adapter.mjs';
test('native adapter composes routing metadata but cannot supply an answer ID or text',()=>{
 assert.deepEqual(adaptQuery({focus:'library fees',voting_advice:false},'What is the fee?'),{kind:'EVIDENCE',intent:'CONTENT',focus:'library fees What is the fee?',limit:1});
 assert.equal(adaptQuery({focus:'opening and future budgets',voting_advice:false},'Compare both budgets').limit,2);
 assert.deepEqual(adaptQuery({focus:'anything',voting_advice:true},'Tell me my vote'),{kind:'VOTING_ADVICE',intent:'NONE',focus:'',limit:0});
 for(const value of [{focus:'fee',voting_advice:'false'},{focus:'fee',voting_advice:false,text:'invented'},{focus:'fee',voting_advice:false,fact_ids:['H01']}])assert.throws(()=>adaptQuery(value,'question'));
});

import{requestsVotingAdvice,requestsLaterObservation}from'../../onprem/matching.mjs';
test('local service policy distinguishes advice from factual voting questions and historical forecasts',()=>{
 for(const q of ['Tell me how to vote and which side is right.','Should I vote yes?','Wie soll ich abstimmen?'])assert.equal(requestsVotingAdvice(q),true);
 for(const q of ['What did people vote on?','Who made the budget forecast?'])assert.equal(requestsVotingAdvice(q),false);
 assert.equal(requestsLaterObservation('What actually happened in 2026?','2024-03-02'),true);assert.equal(requestsLaterObservation('What did they forecast for 2026?','2024-03-02'),false);
});
