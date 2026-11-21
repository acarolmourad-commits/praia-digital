/* Provider adapters must never auto-retry Gmail create/send. They must pin all
 * connected account/tool IDs and verify exact recipient, package and message. */
export async function processOne(ledger,provider,id,token,now){
 let row=ledger.claim(id,token,now);if(!row)return 'NOT_CLAIMED';
 const update=(next,fields)=>{row=ledger.transition(row,next,fields);};
 try{
  let sent;try{sent=await provider.findVerifiedSent(row);}catch(_){update(row.state,{due:now+60000,error:'SENT_LOOKUP_FAILED'});return 'RETRY';}
  if(!Array.isArray(sent))throw Error('INVALID_PROVIDER_RESULT');
  if(sent.length>1){update('HELD',{error:'MULTIPLE_SENT_MESSAGES'});return 'HELD';}
  if(sent.length===1){ledger.recoverSent(id,sent[0].id);return 'SENT';}
  if(row.state==='UNCERTAIN'){update('HELD',{error:'UNKNOWN_EXTERNAL_RESULT'});return 'HELD';}
  if(row.revoked){update('REVOKED',{error:'REVOKED_BEFORE_SEND'});return 'REVOKED';}
  // Includes current payment/refund state AND current Drive owner-only/hash.
  let checked;try{checked=await provider.validateCurrentPaymentAndPackage(JSON.parse(row.payload));}catch(_){update(row.state,{due:now+60000,error:'VALIDATION_UNAVAILABLE'});return 'RETRY';}
  if(!checked||checked.ok!==true){update(checked?.revoked?'REVOKED':'HELD',{error:'VALIDATION_REJECTED'});return 'HELD';}
  if(row.state==='READY'){
   update('DRAFT_CREATING',{attempts:row.attempts+1});
   let draft;try{draft=await provider.createExactDraft(row,checked);}catch(_){update('UNCERTAIN',{error:'DRAFT_RESULT_UNKNOWN'});return 'UNCERTAIN';}
   if(!draft?.id){update('UNCERTAIN',{error:'DRAFT_RESULT_UNKNOWN'});return 'UNCERTAIN';}
   update('DRAFT_READY',{draft_id:draft.id,due:now+1000,error:null});return 'DRAFT_READY';
  }
  if(row.state!=='DRAFT_READY'){update('HELD',{error:'UNSUPPORTED_STATE'});return 'HELD';}
  let draftValid;try{draftValid=await provider.verifyExactDraft(row,checked);}catch(_){update(row.state,{due:now+60000,error:'DRAFT_LOOKUP_FAILED'});return 'RETRY';}
  if(draftValid!==true){update('HELD',{error:'DRAFT_MISMATCH'});return 'HELD';}
  update('SENDING'); // CAS fails here if a revocation occurred during API awaits.
  let message;try{message=await provider.sendExistingDraft(row.draft_id);}catch(_){update('UNCERTAIN',{error:'SEND_RESULT_UNKNOWN'});return 'UNCERTAIN';}
  if(!message?.id){update('UNCERTAIN',{error:'SEND_RESULT_UNKNOWN'});return 'UNCERTAIN';}
  // If a refund races AFTER the actual send began, preserve revocation flag and
  // record actual accepted Gmail message. Already sent attachment cannot revoke.
  ledger.recoverSent(id,message.id);return 'SENT';
 }finally{ledger.release(row);}
}
