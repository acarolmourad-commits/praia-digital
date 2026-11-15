/** Synchronous authorization at the last local boundary before provider I/O.
 * A Promise is never permission. Production callers supply a one-use ledger
 * guard; isolated transport tests may supply an explicit fixture guard. */
export function requireWriteGuard(guard) {
 if(typeof guard!=='function'||guard.constructor?.name==='AsyncFunction')throw Error('SYNCHRONOUS_WRITE_GUARD_REQUIRED');
 return guard;
}
export function checkWriteGuard(guard) {
 const decision=requireWriteGuard(guard)();
 if(decision!==true){
  // Do not await an asynchronous decision or leave a rejected Promise unhandled.
  if(decision instanceof Promise)decision.catch(()=>{});
  throw Error('SYNCHRONOUS_WRITE_GUARD_REJECTED');
 }
}
