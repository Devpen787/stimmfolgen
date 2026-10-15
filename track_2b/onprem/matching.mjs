import{matchQuestion}from'../hosted/matching.mjs';
export function requestsVotingAdvice(question){
 return /\b(how (?:should|do|to) (?:i )?vote|should i vote|recommend (?:a|my|the|which) (?:vote|side)|which side is right|tell me (?:how|which way) to vote)\b/i.test(question)||/\b(wie soll ich (?:abstimmen|stimmen)|soll ich (?:ja|nein) stimmen|comment (?:dois-je|voter))\b/i.test(question);
}
export function requestsLaterObservation(question,cutoff){
 const observed=/\b(actually|happened|observed|in force|implemented|current law|today)\b/i.test(question);
 const years=question.match(/\b20\d{2}\b/g)||[];
 return observed&&(years.some(y=>Number(y)>Number(cutoff.slice(0,4)))||/\b(today|current law|in force)\b/i.test(question));
}
export async function matchLocalQuestion(c,k,q,call){
 const scope=requestsVotingAdvice(q)?'VOTING_ADVICE':requestsLaterObservation(q,c.as_of)?'LATER_EVENTS':null;
 if(scope)return{plan:{kind:scope==='VOTING_ADVICE'?'VOTING_ADVICE':'OUTSIDE_EVIDENCE',intent:'NONE',focus:'',limit:0},ids:[],tasks:[],scope:{scope}};
 return matchQuestion(c,k,q,call);
}
