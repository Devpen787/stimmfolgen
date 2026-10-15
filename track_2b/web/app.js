import {PrivateVault} from './vault.js';
const vault = new PrivateVault();
const drafts = new Map();
function lockPrivate() { vault.lock(); drafts.clear(); }
let liveStatus={configured:false}, liveQuestion='', liveResult=null, livePending=false, refreshLive=()=>{};
let catalog, analysis, sessions = [], currentVote = null, idleTimer, searchQuery = '';
const screen = document.getElementById('screen');
const dialog = document.getElementById('dialog');
const body = document.getElementById('dialog-body');
const labels = {DIRECT_PROVISION:'Defined in the proposal',COST_PROJECTION:'Government projection',UNRESOLVED:'Unresolved financing',ATTRIBUTED_PREDICTION:'Council / Parliament argument'};
const $ = id => document.getElementById(id);
const entries = () => vault.unlocked ? vault.entries : vault.exists ? [] : sessions;
const saved = id => entries().find(item => item.id === id);
const vote = id => catalog.votes.find(item => item.id === id);
const card = id => analysis.cards.find(item => item.id === id);
function el(tag,text,cls) { const node=document.createElement(tag); if(text!==undefined)node.textContent=text; if(cls)node.className=cls; return node; }
function icon(name) { const node=el('img'); node.src='/assets/'+name+'.svg'; node.alt=''; return node; }
function button(text,action,cls='text-button') { const node=el('button',text,cls); node.type='button'; node.addEventListener('click',action); return node; }
function link(text,url,cls='') { const node=el('a',text,cls); node.href=url; return node; }
function date(value) { return new Intl.DateTimeFormat('en-GB',{day:'numeric',month:'long',year:'numeric',timeZone:'Europe/Zurich'}).format(new Date(value.length===10?value+'T12:00:00+01:00':value)); }
function future(v) { const p=Object.fromEntries(new Intl.DateTimeFormat('en-CA',{timeZone:'Europe/Zurich',year:'numeric',month:'2-digit',day:'2-digit'}).formatToParts(new Date()).map(p=>[p.type,p.value])); return v.date>p.year+'-'+p.month+'-'+p.day; }
function notify(text) { $('notice').textContent=text; $('notice').hidden=false; }
function openDialog(title,nodes) { $('dialog-title').textContent=title; body.replaceChildren(...nodes); if(!dialog.open)dialog.showModal(); }
function go(id,tab='meaning') { location.hash=id==='my'||id==='upcoming'||id==='search'?'#'+id:'#vote/'+id+'/'+tab; }
function sourceLink(reference,text='View source') { const ref=catalog.sources[reference]; const node=link(text,ref.url,'source-link'); node.target='_blank'; node.rel='noopener noreferrer'; node.append(icon('arrow-top-right-on-square')); return node; }
function checkedNote() { return el('p','Catalogue checked '+date(catalog.checked_date)+'. Five selected federal proposals; this is not the full Swiss vote register.','date-note'); }
function modelLink() {
 const node=button('',showApertus,'model-link'); const text=el('span'); text.append(el('span',liveStatus.configured?'Explore with live Apertus':'Prepared with Apertus v1.5'),el('br'),el('span','Reviewed historical analysis'));
 node.append(icon('document-text'),text,icon('chevron-right')); return node;
}
function showApertus() {
 openDialog('How Apertus helps',[
  el('p','Apertus v1.5 ran locally to find original booklet passages, extract candidate values and identify who made an argument.'),
  el('p','Independent source and meaning checks, followed by human review, produced this published AHV explanation.'),
  el('p','The overview contains reviewed recorded results. Ask Apertus sends your explicit public question for a fresh answer using this reviewed AHV evidence.'),
  el('p',liveStatus.configured?'Live service: '+liveStatus.model+' · '+liveStatus.provider+'. No model download is needed in your browser.':'Live Apertus is not configured on this installation. The reviewed explanation remains available.'),
  el('p','Fresh answers are AI-generated and are not human reviewed. A separate pass by the same model checks meaning; it can still make mistakes. Original source text and dates remain available.'),
  el('p','Your choices and notes are not part of public analysis requests. On-device encryption, not the model, protects saved private data.'),
  el('p','Other catalogue entries have official source references, but do not yet have reviewed Apertus analysis.','plain-note')]);
}
function sourceStatement(id) {
 const c=card(id),nodes=[el('p',labels[c.kind]+' · reviewed statement'),el('p',c.statement),el('p','Historical evidence frame: '+date(analysis.as_of),'source-date')];
 for(const ref of c.citations) {
  nodes.push(el('blockquote',ref.text)); const a=link('Original booklet, page '+ref.pdf_page,'/api/booklet.pdf#page='+ref.pdf_page); a.target='_blank';a.rel='noopener';nodes.push(a);
  nodes.push(el('p','Source: '+(ref.actor==='GOVERNMENT'?(c.kind==='ATTRIBUTED_PREDICTION'?'Federal Council / Parliament argument section':'Federal Council explanation'):'Initiative committee'),'source-date'));
  const detail=el('details');detail.append(el('summary','Reference details'),el('code','Span '+ref.span_id+' · SHA-256 '+ref.text_sha256));nodes.push(detail);
 }
 if(id==='P01') { const a=link('Proposed legal text, page 18','/api/booklet.pdf#page=18');a.target='_blank';a.rel='noopener';nodes.push(a); }
 const hash=el('details');hash.append(el('summary','Document and dates'),el('code',analysis.source_sha256),el('p','Content cutoff: '+date(analysis.content_cutoff)+'. Public availability established by '+date(analysis.available_by)+'.'));nodes.push(hash);
 openDialog(c.title,nodes);
}
function updateCard(v) {
 if(!v.updates.length) { const box=el('div',undefined,'update-card');box.append(icon('information-circle'),el('p','No verified updates recorded for this vote in the current catalogue.','plain-note'));return box; }
 const u=v.updates[0],ref=catalog.sources[u.source],box=el('article',undefined,'update-card');const ico=icon('information-circle');ico.className='update-icon';box.append(ico);
 const text=el('div');text.append(el('h3','Official update'),el('div',date(u.date),'source-date'),el('p',u.title),el('div',ref.publisher,'source-date'),sourceLink(u.source,'Source: '+new URL(ref.url).hostname));box.append(text);return box;
}
function relatedCard(relation) {
 const v=vote(relation.id);const node=button('',()=>go(v.id),'related'),text=el('div');text.append(el('div','Related vote','small-label'),el('h3',v.title));const meta=el('div',undefined,'meta');meta.append(el('span',date(v.date)),el('span',future(v)?'Upcoming':'Past vote','tag'+(future(v)?' future':'')));text.append(meta);node.append(text,icon('chevron-right'));return node;
}
function voteCard(v,tracked=false) {
 const box=el('article',undefined,'vote-card'),row=el('div',undefined,'title-row');row.append(el('h2',v.title));const toggle=button(saved(v.id)?'Tracked':'Track',()=>toggleTrack(v),'track-button');toggle.setAttribute('aria-label',saved(v.id)?'Untrack '+v.title:'Track '+v.title);toggle.setAttribute('aria-pressed',String(Boolean(saved(v.id))));toggle.append(icon(saved(v.id)?'bookmark':'plus'));row.append(toggle);box.append(row);
 const meta=el('div',undefined,'meta');meta.append(el('span',date(v.date)),el('span',future(v)?'Upcoming':'Past vote','tag'+(future(v)?' future':'')));box.append(meta,el('p',v.summary,'summary'));
 const open=button(tracked?'Explore my vote':'Explore vote',()=>go(v.id),'primary');open.append(icon('arrow-right'));box.append(open);
 if(v.analysis_case_id)box.append(modelLink());else box.append(el('p','Official source available · Apertus analysis not reviewed yet.','plain-note'));
 return box;
}
function findVote() { const a=link('','#search','find');a.append(icon('magnifying-glass'),el('span','Find another vote'),icon('chevron-right'));return a; }
function renderMy() {
 screen.append(el('h1','My votes'),el('p','Your votes, with context.','subtitle'));
 if(vault.exists&&!vault.unlocked) { const box=el('div',undefined,'empty');box.append(el('h2','Your private votes are locked'),el('p','Unlock them on this device. You can still browse public votes without unlocking.'),button('Unlock my votes',showDevice,'primary'));screen.append(box,findVote());return; }
 if(!entries().length) { const box=el('div',undefined,'empty');box.append(el('h2','Keep the votes you want to understand'),el('p','Find a vote and tap Track. Your vote choice is optional and is never inferred.'),button('Find a vote',()=>go('search'),'primary'),button('Explore the AHV example',()=>go('ahv13')));screen.append(box); }
 for(const entry of entries()) {
  const v=vote(entry.id);if(!v) { screen.append(el('p','A tracked vote is no longer in this catalogue. Your private record is retained.'));continue; }
  const grid=el('div',undefined,'my-grid');grid.append(voteCard(v,true));const updates=el('div',undefined,'updates-column');updates.append(updateCard(v));for(const relation of v.related)updates.append(relatedCard(relation));grid.append(updates);screen.append(grid);
 }
 if(entries().length){screen.append(findVote());if(!vault.exists)screen.append(button('Save my votes on this device',showDevice,'secondary'));}
 screen.append(el('p',vault.unlocked?'Saved encrypted on this device. Your passphrase is needed after reload.':'Tracking stays in this visit only. Use On this device to save encrypted private votes.','plain-note'),checkedNote());
}
function renderCatalogue(which) {
 screen.append(el('h1',which==='search'?'Search votes':'Upcoming votes'),el('p',which==='search'?'Find a vote. Keep the ones that matter to you.':'See what is on the next federal ballot.','subtitle'));
 let input;if(which==='search'){const field=el('div',undefined,'search-box');field.append(icon('magnifying-glass'));input=el('input');input.type='search';input.placeholder='Search by topic or date';input.value=searchQuery;input.setAttribute('aria-label','Search votes');field.append(input);screen.append(field);}
 const results=el('div',undefined,'results');screen.append(results);
 const draw=()=>{results.replaceChildren();const q=(input?.value||'').trim().toLocaleLowerCase();let list=catalog.votes.filter(v=>which!=='upcoming'||future(v));list=list.filter(v=>(v.title+' '+v.official_title+' '+v.date+' '+date(v.date)).toLocaleLowerCase().includes(q));
  for(const v of list)results.append(voteCard(v));if(!list.length)results.append(el('p','No matching votes in this selected catalogue. Try AHV, pensions or a date.','plain-note'));};
 input?.addEventListener('input',()=>{searchQuery=input.value;draw();});draw();screen.append(checkedNote());
}
function renderLive(container) {
 const box=el('section',undefined,'live-panel');box.setAttribute('aria-labelledby','live-heading');
 const heading=el('h2','Ask Apertus');heading.id='live-heading';box.append(heading,
  el('p','Your question. A fresh answer, connected to the original evidence.','subtitle'),
  el('p','Historical AHV booklet only · before 3 March 2024. For later events, see Updates.','plain-note'));
 if(!liveStatus.configured){box.append(el('p','Live Apertus is unavailable on this installation. You can still explore the reviewed explanation and sources.','plain-note'));container.append(box);return;}
 box.append(el('p',liveStatus.model+' · '+liveStatus.provider+' · no download required','source-date'));
 const form=el('form'),label=el('label','What would you like to understand?'),input=el('textarea');input.id='public-question';label.htmlFor=input.id;input.maxLength=700;input.required=true;input.minLength=3;input.value=liveQuestion;input.placeholder='For example: what remained unknown about financing?';input.rows=3;input.disabled=livePending;
 const privacy=el('p','This question goes to the Apertus service. Do not include names, salary or private notes. Your saved votes and notes are never attached.','plain-note');privacy.id='question-privacy';input.setAttribute('aria-describedby',privacy.id);
 const send=el('button',livePending?'Apertus is reading and checking…':'Ask Apertus','primary');send.type='submit';send.disabled=livePending;
 const output=el('div',undefined,'live-result');output.setAttribute('role','status');output.setAttribute('aria-live','polite');
 function draw(){output.replaceChildren();if(livePending){output.append(el('p','Reading the historical evidence, then checking the answer. This can take about a minute.'));return;}if(!liveResult)return;
  if(liveResult.error)output.append(el('p',liveResult.error,'unknown'));
  if(liveResult.live_inference_performed_for_this_request)output.append(el('p','Fresh Apertus answer · '+date(liveResult.answered_at)+' · '+liveResult.latency_seconds+' seconds','source-date'));
  if(liveResult.outcome==='INSUFFICIENT_EVIDENCE')output.append(el('h3','The evidence does not establish a complete answer'));
  for(const claim of liveResult.claims||[]){const section=el('section',undefined,'analysis-row');section.append(el('p',claim.text));for(const id of claim.fact_ids)section.append(button('Source and dates · '+card(id).title,()=>sourceStatement(id)));output.append(section);}
  for(const unknown of liveResult.unknowns||[])output.append(el('p',unknown,'unknown'));
  if(liveResult.live_inference_performed_for_this_request){output.append(el('p','AI-generated, not human reviewed. Source references are authenticated; the separate meaning check uses the same model and can miss errors.','plain-note'));const details=el('details');details.append(el('summary','Answer evidence'),el('p','Historical frame: '+date(liveResult.as_of)),el('code','Source SHA-256: '+liveResult.source_sha256),el('code','Answer receipt: '+liveResult.receipt));output.append(details);}
 }
 input.addEventListener('input',()=>{liveQuestion=input.value;});
 form.addEventListener('submit',async event=>{event.preventDefault();if(livePending)return;liveQuestion=input.value.trim();if(liveQuestion.length<3)return;livePending=true;liveResult=null;input.disabled=true;send.disabled=true;send.textContent='Apertus is reading and checking…';draw();
  try{const response=await fetch('/api/live/question',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:liveQuestion}),signal:AbortSignal.timeout(280000)});liveResult=await response.json();}
  catch{liveResult={error:'Apertus did not respond. Your question was not saved. Try again; reviewed sources remain available.'};}
  finally{livePending=false;refreshLive();}
 });
 const suggestions=el('div',undefined,'question-suggestions');for(const q of ['What changes for pension recipients?','What remains unknown for workers?','Who made the taxes or spending-cuts argument?'])suggestions.append(button(q,()=>{input.value=q;liveQuestion=q;input.focus();},'secondary'));
 form.append(label,input,privacy,send);box.append(form,suggestions,output);refreshLive=()=>{input.disabled=livePending;send.disabled=livePending;send.textContent=livePending?'Apertus is reading and checking…':'Ask Apertus';draw();};draw();container.append(box);
}
function renderVote(v,tab) {
 currentVote=v;screen.append(link('Back to My votes','#my','back'));const header=el('div',undefined,'detail-header');header.append(el('h1',v.title),el('div',date(v.date)+' · '+(future(v)?'Upcoming vote':'Past vote'),'meta'));screen.append(header);
 const actions=el('div',undefined,'flex-actions');actions.append(button(vault.exists&&!vault.unlocked?'Unlock to track':saved(v.id)?'Tracked':'Track this vote',()=>toggleTrack(v),'secondary'));screen.append(actions);
 const nav=el('div',undefined,'section-nav');nav.setAttribute('role','tablist');nav.setAttribute('aria-label','Explore vote');for(const [id,text] of [['meaning','What it means'],['updates','Updates'],['related','Related votes'],['perspectives','Perspectives'],['private','My choice & notes']]){const b=button(text,()=>go(v.id,id));b.id='tab-'+id;b.setAttribute('role','tab');b.setAttribute('aria-controls','vote-panel');b.setAttribute('aria-selected',String(tab===id));b.tabIndex=tab===id?0:-1;b.addEventListener('keydown',event=>{const ids=['meaning','updates','related','perspectives','private'];let next=ids.indexOf(id);if(event.key==='ArrowRight')next=(next+1)%ids.length;else if(event.key==='ArrowLeft')next=(next+ids.length-1)%ids.length;else if(event.key==='Home')next=0;else if(event.key==='End')next=ids.length-1;else return;event.preventDefault();if(ids[next]===tab){b.focus();return;}window.addEventListener('hashchange',()=>document.getElementById('tab-'+ids[next])?.focus(),{once:true});go(v.id,ids[next]);});nav.append(b);}screen.append(nav);
 const content=el('section');content.id='vote-panel';content.setAttribute('role','tabpanel');content.setAttribute('aria-labelledby','tab-'+tab);screen.append(content);
 if(tab==='meaning') {
  if(v.analysis_case_id) {
   renderLive(content);
   content.append(modelLink(),el('p','Historical evidence frame · '+date(analysis.as_of)+'. Later official updates have a separate tab.','plain-note'));
   for(const c of analysis.cards) {
    const row=el('section',undefined,'analysis-row');
    const nodes=[el('div',labels[c.kind],'kind'),el('p',c.statement),button('Source and dates',()=>sourceStatement(c.id))];
    if(c.origin==='REVIEWED_REFERENCE_CONTEXT')nodes.push(el('p','Reviewed source context; this figure was not extracted in the final model trial.','plain-note'));
    if(c.id==='P01'||c.id==='P04'){row.append(el('h2',c.title),...nodes);}
    else {const more=el('details');more.append(el('summary',c.title),...nodes);row.append(more);}
    content.append(row);
   }
  } else {content.append(el('h2','Official proposal reference'),el('p',v.summary),el('p','A reviewed Apertus explanation is not available for this vote yet.','plain-note'));for(const ref of v.sources){const source=catalog.sources[ref];content.append(sourceLink(ref),el('p',source.publisher+' · '+(source.published_at?'Published '+date(source.published_at)+'. ':'Publication date not established. ')+'Checked '+date(source.retrieved_at)+'.','source-date'));}}
 } else if(tab==='updates') {
  content.append(el('h2',future(v)?'Updates before the vote':'Updates since the vote'),updateCard(v));
  for(const u of v.updates){content.append(el('p','Official publisher information, not a new Apertus analysis. Published '+date(u.date)+'; checked '+date(catalog.sources[u.source].retrieved_at)+'.','plain-note'));}
  content.append(el('p','No updates recorded means no verified update in this catalogue, not proof that nothing happened.','plain-note'));
 } else if(tab==='related') {
  content.append(el('h2','Related votes'));if(!v.related.length)content.append(el('p','No sourced related vote is recorded in this catalogue.','plain-note'));
  for(const relation of v.related){content.append(relatedCard(relation),el('p',relation.reason,'plain-note'),sourceLink(relation.source,'Relationship source'),el('p','Relationship source checked '+date(catalog.sources[relation.source].retrieved_at)+'.','source-date'));}
 } else if(tab==='perspectives') renderPerspectives(v,content);
 else renderPrivate(v,content);
}
function renderPerspectives(v,container=screen) {
 container.append(el('h2','Look at it from a different perspective'),el('p','Choose a factual situation, for you or someone else. Nothing is sent as a private profile.','plain-note'));
 if(!v.analysis_case_id){container.append(el('p','Reviewed perspectives are not available for this vote yet.','plain-note'));return;}
 const scope=el('div',undefined,'perspectives'),detail=el('div');container.append(scope,detail);
 function show(which){scope.querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.scope===which)));detail.replaceChildren();
  if(which==='nation'){detail.append(el('h3','Projected national expenditure'),el('p',card('P02').statement),el('p','An attributed historical forecast, not an observed outcome.','plain-note'),button('Source and dates',()=>sourceStatement('P02')));return;}
  const label=el('label',which==='me'?'Which situation do you want to understand?':'Which situation applies to the other person?');const select=el('select');select.setAttribute('aria-label',which==='me'?'My factual situation':'Other person’s factual situation');
  select.append(new Option('Working-age person','worker'),new Option('AHV old-age pension recipient','recipient'));const result=el('div',undefined,'analysis-row');detail.append(label,select,result);
  const draw=()=>{result.replaceChildren();const id=select.value==='recipient'?'P01':'P04';result.append(el('h3',id==='P01'?'The proposed annual supplement':'A definite personal charge was not established'),el('p',card(id).statement),button('Source and dates',()=>sourceStatement(id)));
   if(id==='P04'){const gap=el('div',undefined,'unknown');gap.append(el('p','The original initiative did not settle the financing method and rate. Unknown does not mean zero.'));result.append(gap);}else result.append(el('p','This statement concerns AHV old-age pensions; it does not establish every individual eligibility condition.','plain-note'));};select.addEventListener('change',draw);draw();
 }
 for(const [id,text] of [['me','Me'],['others','Others'],['nation','Switzerland']]){const b=button(text,()=>show(id),'secondary');b.dataset.scope=id;b.setAttribute('aria-pressed','false');scope.append(b);}show('me');renderLive(container);
}
async function store(entry) { if(vault.exists&&!vault.unlocked)throw Error('Unlock your private votes first.');if(vault.unlocked)await vault.save(entry);else sessions=sessions.filter(item=>item.id!==entry.id).concat(entry); }
function newEntry(v) {return {id:v.id,choice:'NOT_RECORDED',notes:'',pinnedVersion:v.analysis_case_id?analysis.source_sha256+'@'+analysis.as_of:catalog.checked_at,savedAt:new Date().toISOString(),viewedUpdate:''};}
async function toggleTrack(v) {
 if(vault.exists&&!vault.unlocked){showDevice();return;}
 const existing=saved(v.id);
 if(existing&&(existing.notes||existing.choice!=='NOT_RECORDED'||drafts.get(v.id)?.notes||drafts.get(v.id)?.choice&&drafts.get(v.id).choice!=='NOT_RECORDED')){
  openDialog('Remove this private vote?',[el('p','Removing '+v.title+' also removes its saved choice and notes from this browser. Download an encrypted backup first if you want to keep them.'),button('Keep my vote',()=>dialog.close(),'primary'),button('Remove vote and its notes',async()=>{try{if(vault.unlocked)await vault.remove(v.id);else sessions=sessions.filter(item=>item.id!==v.id);drafts.delete(v.id);dialog.close();render();notify('Private vote removed from this device.');}catch(e){notify(e.message);}},'secondary')]);return;
 }
 try {if(saved(v.id)){if(vault.unlocked)await vault.remove(v.id);else sessions=sessions.filter(item=>item.id!==v.id);drafts.delete(v.id);notify('Vote untracked on this device.');}else{await store(newEntry(v));notify(vault.unlocked?'Vote saved encrypted on this device.':'Vote tracked for this visit. Use On this device to keep it after reload.');}render();}catch(e){notify(e.message);}
}
function renderPrivate(v,container=screen) {
 container.append(el('h2','My choice and notes'),el('p','Tracking a vote does not record how you voted. These fields are optional and stay on your device.','plain-note'));
 if(vault.exists&&!vault.unlocked){container.append(button('Unlock private votes',showDevice,'primary'));return;}
 const entry=saved(v.id)||newEntry(v),form=el('form'),choice=el('select');choice.id='private-choice';for(const [value,text] of [['NOT_RECORDED','Not recorded'],['YES','I voted Yes'],['NO','I voted No'],['ABSTAIN','I abstained']])choice.append(new Option(future(v)?({'YES':'Yes (planned)','NO':'No (planned)','ABSTAIN':'Abstain (planned)'}[value]||text):text,value));choice.value=drafts.get(v.id)?.choice??entry.choice;
 const label=el('label','My self-recorded choice (optional)');label.htmlFor=choice.id;form.append(label,choice);const notes=el('textarea');notes.id='private-notes';notes.value=drafts.get(v.id)?.notes??entry.notes;notes.placeholder='My questions and reflections';notes.maxLength=16000;const nlabel=el('label','My private notes');nlabel.htmlFor=notes.id;form.append(nlabel,notes);
 const save=el('button',vault.unlocked?'Save privately on this device':'Keep for this visit','primary');save.type='submit';form.append(save);
 const keepDraft=()=>drafts.set(v.id,{choice:choice.value,notes:notes.value});notes.addEventListener('input',keepDraft);choice.addEventListener('change',keepDraft);
 form.addEventListener('submit',async event=>{event.preventDefault();save.disabled=true;try{await store({...entry,choice:choice.value,notes:notes.value});drafts.delete(v.id);notify(vault.unlocked?'Choice and notes saved encrypted on this device.':'Choice and notes kept in this visit only; reload clears them.');}catch(e){notify(e.message);}finally{save.disabled=false;}});container.append(form,el('p',vault.unlocked?'Drafts stay while you browse this app. Save before reloading or locking. Saved notes are encrypted on this device.':'Drafts stay while you browse this app. Reload clears visit-only notes. Use On this device to save encrypted notes after reload.','plain-note'));
 const source=el('details');source.append(el('summary','The version attached to this private record'),el('code',entry.pinnedVersion));container.append(source);
}
function download(text,name) {const url=URL.createObjectURL(new Blob([text],{type:'application/json'}));const a=link('',url);a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
function showDevice() {
 if(vault.unlocked){openDialog('Private votes on this device',[el('p','Your saved choices and notes are encrypted in this browser. They are not sent to the backend or Apertus.'),
  button('Lock my votes',()=>{lockPrivate();dialog.close();render();notify('Private votes locked.');},'primary'),button('Download encrypted backup',()=>download(vault.backup(),'stimmfolgen-private-backup.json'),'secondary'),
  el('p','Keep your passphrase safe. Encryption protects stored data, not an unlocked browser or compromised device. No account or cross-device sync.','plain-note')]);return;}
 const nodes=[el('p',vault.exists?'Enter your passphrase to unlock your private votes.':'Browse freely. To keep private votes after reload, create an encrypted vault with a passphrase.')];
 const form=el('form'),input=el('input');input.type='password';input.id='vault-passphrase';input.autocomplete=vault.exists?'current-password':'new-password';input.minLength=12;input.required=true;const label=el('label','Passphrase');label.htmlFor=input.id;const submit=el('button',vault.exists?'Unlock my votes':'Create private vault','primary');submit.type='submit';const error=el('p',undefined,'error');error.setAttribute('role','alert');form.append(label,input,el('p','At least 12 characters. This app cannot recover a forgotten passphrase.','plain-note'),submit,error);
 form.addEventListener('submit',async event=>{event.preventDefault();submit.disabled=true;try{if(vault.exists)await vault.unlock(input.value);else{await vault.create(input.value);for(const item of sessions)await vault.save(item);sessions=[];}input.value='';dialog.close();render();notify('Private votes unlocked on this device.');resetIdle();}catch(e){input.value='';error.textContent=e.message;}finally{submit.disabled=false;}});nodes.push(form);
 if(!vault.exists)nodes.push(button('Keep tracking for this visit',()=>dialog.close(),'secondary'));
 const file=el('input');file.type='file';file.accept='application/json,.json';file.id='backup-file';const filelabel=el('label','Restore an encrypted backup');filelabel.htmlFor=file.id;file.addEventListener('change',async()=>{if(!file.files[0])return;try{if(file.files[0].size>1000000)throw Error('Backup is too large.');const backup=JSON.parse(await file.files[0].text());const f=el('form'),pass=el('input');pass.type='password';pass.id='restore-passphrase';pass.required=true;const l=el('label','Backup passphrase');l.htmlFor=pass.id;const submit=el('button','Restore private backup','primary');submit.type='submit';const err=el('p',undefined,'error');f.append(l,pass,submit,err);f.addEventListener('submit',async e=>{e.preventDefault();submit.disabled=true;try{await vault.unlock(pass.value,backup);pass.value='';sessions=[];dialog.close();render();notify('Encrypted backup restored on this device.');resetIdle();}catch(x){pass.value='';err.textContent=x.message;}finally{submit.disabled=false;}});openDialog('Restore private backup',[el('p','Restoring replaces this browser’s encrypted vault. The backup is not uploaded.'),f]);}catch(e){error.textContent=e.message;}});nodes.push(filelabel,file);openDialog(vault.exists?'Unlock my votes':'Keep my votes private',nodes);
}
function resetIdle(){clearTimeout(idleTimer);if(vault.unlocked)idleTimer=setTimeout(()=>{lockPrivate();if(dialog.open)dialog.close();render();notify('Private votes locked after five minutes without activity.');},300000);}
function render(){screen.replaceChildren();currentVote=null;const parts=(location.hash||'#my').slice(1).split('/');const section=['my','upcoming','search'].includes(parts[0])?parts[0]:'my';document.querySelectorAll('[data-nav]').forEach(a=>a.setAttribute('aria-current',a.dataset.nav===section?'page':'false'));
 if(parts[0]==='vote'){const v=vote(parts[1]);if(v)renderVote(v,['meaning','updates','related','perspectives','private'].includes(parts[2])?parts[2]:'meaning');else screen.append(el('h1','Vote not found'),findVote());}
 else if(section==='my')renderMy();else renderCatalogue(section);
 document.title='StimmFolgen — '+(currentVote?.title||({my:'My votes',upcoming:'Upcoming votes',search:'Search'}[section]));
}
$('device').addEventListener('click',showDevice);$('close-dialog').addEventListener('click',()=>dialog.close());window.addEventListener('hashchange',()=>{if(catalog){$('notice').hidden=true;render();$('main').focus({preventScroll:true});window.scrollTo(0,0);}});
for(const event of ['pointerdown','keydown'])document.addEventListener(event,resetIdle,{passive:true});
document.addEventListener('visibilitychange',()=>{if(document.hidden&&vault.unlocked){lockPrivate();if(dialog.open)dialog.close();if(catalog)render();}});
window.addEventListener('storage',event=>{if(event.key==='stimmfolgen.private.v1'){lockPrivate();if(catalog)render();notify('Private data changed in another tab. Unlock it again.');}});
Promise.all([fetch('/api/catalog').then(r=>{if(!r.ok)throw Error();return r.json();}),fetch('/api/case').then(r=>{if(!r.ok)throw Error();return r.json();}),fetch('/api/live/status').then(r=>r.ok?r.json():{configured:false}).catch(()=>({configured:false}))]).then(([c,a,l])=>{catalog=c;analysis=a;liveStatus=l;render();}).catch(()=>screen.replaceChildren(el('h1','The verified catalogue is unavailable'),el('p','Please refresh. No unverified answer is substituted.')));
