/* Consumer session transport. Runtime activation requires verified concrete
 * provider identities, configuration and end-to-end TEST. Account provenance is verified within consumer scope; no legacy proxy fallback. */
const ORIGIN='https://backend.composio.dev';
const KINDS=new Set(['stripe','gmail','googledrive']);
const same=(a,b)=>JSON.stringify([...a].sort())===JSON.stringify([...b].sort());
export class ConsumerSession {
 constructor(env,policy,fetcher=fetch,proxyMode=false){
  this.proxyMode=proxyMode;
  this.env=env;this.fetcher=fetcher;this.policy=structuredClone(policy);this.checked=false;
  if(!/^(?:org|ok)_[A-Za-z0-9_-]+$/.test(env.COMPOSIO_ORG_ID||'')||!/^(?:proj|pr)_[A-Za-z0-9_-]+$/.test(env.COMPOSIO_CONSUMER_PROJECT_ID||'')||!env.COMPOSIO_USER_API_KEY||!env.COMPOSIO_USER_ID)throw Error('CONSUMER_SCOPE_REQUIRED');
  if(!policy||!same(Object.keys(policy),[...KINDS]))throw Error('CONSUMER_POLICY_REQUIRED');
  this.toolToKind=new Map();
  for(const [kind,p] of Object.entries(policy)){
   if(!Array.isArray(p.tools)||(!proxyMode&&!p.tools.length)||p.tools.length>20||typeof p.account!=='string'||!/^(?:ca|coup)_[A-Za-z0-9_-]+$/.test(p.account))throw Error('CONSUMER_ACCOUNT_OR_TOOLS_INVALID');
   for(const tool of p.tools){if(!/^[A-Z][A-Z0-9_]+$/.test(tool)||tool.startsWith('COMPOSIO_')||this.toolToKind.has(tool))throw Error('CONSUMER_TOOL_INVALID');this.toolToKind.set(tool,kind);}
  }
 }
 headers(){return{'content-type':'application/json','x-user-api-key':this.env.COMPOSIO_USER_API_KEY,'x-org-id':this.env.COMPOSIO_ORG_ID,'x-project-id':this.env.COMPOSIO_CONSUMER_PROJECT_ID};}
 async request(path,method,body){
  const response=await this.fetcher(ORIGIN+'/api/v3.1/tool_router/session'+path,{method,headers:this.headers(),redirect:'error',signal:AbortSignal.timeout(25000),...(body?{body:JSON.stringify(body)}:{})});
  if(!response.ok)throw Error('CONSUMER_HTTP_'+response.status);
  return response.json();
 }
 creationBody(){return{user_id:this.env.COMPOSIO_USER_ID,toolkits:{enable:[...KINDS]},connected_accounts:Object.fromEntries(Object.entries(this.policy).map(([k,v])=>[k,[v.account]])),tools:Object.fromEntries(Object.entries(this.policy).map(([k,v])=>[k,{enable:v.tools}])),instant:false,manage_connections:{enable:false},workbench:{enable:false},proxy_execute:{enable:this.proxyMode},search:{enable:false},execute:{enable_multi_execute:false},preload:{tools:[...this.toolToKind.keys()]},experimental:{no_elicitation_support_fallback:'deny'}};}
 verifyConfig(config){
  if(!config||config.user_id!==this.env.COMPOSIO_USER_ID||config.instant!==false||config.manage_connections?.enabled!==false||config.workbench?.enable!==false||config.proxy_execute?.enable!==this.proxyMode||config.search?.enable!==false||config.execute?.enable_multi_execute!==false)throw Error('CONSUMER_CONFIG_DRIFT');
  if(!Array.isArray(config.toolkits?.enabled)||!same(config.toolkits.enabled,[...KINDS])||!same(Object.keys(config.tools||{}),[...KINDS])||!same(Object.keys(config.connected_accounts||{}),[...KINDS]))throw Error('CONSUMER_SCOPE_DRIFT');
  for(const [kind,p] of Object.entries(this.policy))if(!Array.isArray(config.tools[kind]?.enabled)||Object.hasOwn(config.tools[kind],'disabled')||!Array.isArray(config.connected_accounts[kind])||!same(config.tools[kind].enabled,p.tools)||!same(config.connected_accounts[kind],[p.account]))throw Error('CONSUMER_TOOL_OR_ACCOUNT_DRIFT');
 }
 async createForSetup(){
  // Explicit setup operation only; never automatically recreates expired sessions.
  const response=await this.request('','POST',this.creationBody());
  if(!/^trs_[A-Za-z0-9_-]+$/.test(response.session_id||''))throw Error('CONSUMER_SESSION_INVALID');
  this.verifyConfig(response.config);return{session_id:response.session_id};
 }
 async verifySession(){
  const id=this.env.COMPOSIO_CONSUMER_SESSION_ID;
  if(!/^trs_[A-Za-z0-9_-]+$/.test(id||''))throw Error('CONSUMER_SESSION_REQUIRED');
  const response=await this.request('/'+id,'GET');
  if(response.session_id!==id)throw Error('CONSUMER_SESSION_MISMATCH');
  this.verifyConfig(response.config);this.checked=true;
 }
 async execute(tool,arguments_){
  const kind=this.toolToKind.get(tool);if(!kind)throw Error('CONSUMER_TOOL_NOT_ALLOWED');
  if(!arguments_||typeof arguments_!=='object'||Array.isArray(arguments_))throw Error('CONSUMER_ARGUMENTS_INVALID');
  await this.verifySession();
  const response=await this.request('/'+this.env.COMPOSIO_CONSUMER_SESSION_ID+'/execute','POST',{tool_slug:tool,arguments:arguments_,account:this.policy[kind].account,enable_auto_workbench_offload:false});
  if(response.result_type==='input_required')throw Error('CONSUMER_APPROVAL_REQUIRED');
  if(response.result_type!=='completed'||response.error||response.instant_charge)throw Error('CONSUMER_EXECUTION_FAILED');
  return response.data;
 }
}
