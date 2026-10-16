// Keep a delayed answer tied to the exact public case the reader opened.
export function answerFitsCase(answer,source){
 if(answer.case_id&&answer.case_id!==source.case_id)return false;
 if(answer.source_sha256&&answer.source_sha256!==source.source_sha256)return false;
 if(!answer.claims?.length)return true;
 if(answer.case_id!==source.case_id||answer.source_sha256!==source.source_sha256)return false;
 return answer.claims.every(claim=>Array.isArray(claim.fact_ids)&&claim.fact_ids.length===1&&source.cards.some(card=>card.id===claim.fact_ids[0]&&card.statement===claim.text&&JSON.stringify(claim.evidence_kinds)===JSON.stringify([card.kind])));
}
