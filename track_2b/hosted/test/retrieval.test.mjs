import test from 'node:test';import assert from 'node:assert/strict';import{readFileSync}from'node:fs';
import{rank,retrieve,candidates,normalizePlan,planErrors,directnessErrors,directnessPrompt}from'../retrieval.mjs';
const bundle=JSON.parse(readFileSync(new URL('../public-bundle.json',import.meta.url))),p={kind:'EVIDENCE',intent:'CONTENT',focus:'annual supplement pension payment',limit:1};
test('query plan cannot publish factual prose or contradict its scope',()=>{
 assert.deepEqual(planErrors(p),[]);
 for(const x of [{...p,text:'invented'},{...p,fact_ids:['P01']},{...p,limit:true},{...p,focus:''},{...p,limit:0},{...p,intent:'NONE'},{...p,kind:'OUTSIDE_EVIDENCE'}])assert.ok(planErrors(x).length);
 assert.deepEqual(planErrors({kind:'OUTSIDE_EVIDENCE',intent:'NONE',focus:'',limit:0}),[]);
 for(const x of [{direct:1},{direct:true,text:'invented'},null,[]])assert.ok(directnessErrors(x).length);
 assert.deepEqual(directnessErrors({direct:false}),[]);
});
test('retrieval follows statement text after every ID is renamed and order reversed',()=>{
 const original=rank(bundle.case,p.focus),renamed={...bundle.case,cards:bundle.case.cards.map((c,i)=>({...c,id:'opaque-'+(11+i)})).reverse()};
 const result=retrieve(renamed,p);assert.equal(result.length,1);
 assert.equal(renamed.cards.find(c=>c.id===result[0]).statement,bundle.case.cards.find(c=>c.id===original[0].id).statement);
});
test('unrelated fictional case retrieves its own statements without AHV ID knowledge',()=>{
 const fictional={cards:[{id:'x8',title:'Library opening hours',statement:'The library opens on Sundays.'},{id:'k2',title:'Acoustic projection',statement:'The council projects increased noise.'},{id:'n4',title:'Funding unresolved',statement:'Individual charges remain unspecified.'}]};
 assert.deepEqual(retrieve(fictional,{...p,focus:'library Sunday opening hours'}),['x8']);assert.deepEqual(retrieve(fictional,{...p,focus:'noise acoustic projection'}),['k2']);
 assert.deepEqual(retrieve(fictional,{...p,focus:'volcano eruption'}),[]);
});
test('directness check binds original question to one immutable candidate, without an expected ID',()=>{
 const c=bundle.case.cards[4],question='Did someone else make that argument?';const prompt=JSON.parse(directnessPrompt(bundle.case,question,c));assert.equal(prompt.question,question);assert.equal(prompt.candidate.statement,c.statement);assert.equal(prompt.candidate.id,undefined);assert.deepEqual(prompt.candidate.actors,c.citations.map(x=>x.actor));
});

test('zero lexical overlap cannot become a model-only answer',()=>{
 const zero={...p,focus:'volcano eruption'};assert.deepEqual(retrieve(bundle.case,zero),[]);assert.deepEqual(candidates(bundle.case,zero),[]);assert.deepEqual(candidates(bundle.case,{kind:'OUTSIDE_EVIDENCE'}),[]);
});

test('refusal metadata can be discarded without changing scope or permitting retrieval',()=>{
 const raw={...p,kind:'OUTSIDE_EVIDENCE',limit:0};const normalized=normalizePlan(raw);assert.deepEqual(normalized,{kind:'OUTSIDE_EVIDENCE',intent:'NONE',focus:'',limit:0});assert.deepEqual(candidates(bundle.case,normalized),[]);assert.deepEqual(normalizePlan({...raw,text:'invented'}),{...raw,text:'invented'});assert.deepEqual(normalizePlan({...p,intent:'NONE'}),{...p,intent:'NONE'});
});
