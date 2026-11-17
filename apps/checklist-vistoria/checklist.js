'use strict';
(function(root){
const GROUPS = [
  {nome:'🌊 Maresia & Umidade (crítico no litoral)', items:[
    'Esquadrias sem corrosão (alumínio/anodizado)','Ferragens e dobradiças sem ferrugem','Ar-condicionado com serpentina protegida','Pintura/revestimento sem bolhas de umidade','Sem cheiro de mofo em armários e cantos','Balcão/guarda-corpo com altura ≥1,10 m e fixação firme (NBR 14.718)']},
  {nome:'🏗️ Estrutura & Construção', items:[
    'Sem trincas estruturais em paredes/teto','Piso nivelado, sem partes ocas','Telhado/laje sem infiltração','Impermeabilização de banheiros OK','Elétrica: disjuntores e tomadas funcionando','Fachada sem sinais de corrosão de armaduras (manchas alaranjadas)']},
  {nome:'🚿 Hidráulica', items:[
    'Pressão de água boa em todos os pontos','Sem vazamentos visíveis (torneiras, sifões)','Esgoto sem retorno de odor','Aquecimento (boiler/solar) funcionando']},
  {nome:'📄 Documentação', items:[
    'Matrícula atualizada sem ônus','IPTU quitado','Habite-se / averbação da construção','Condomínio: atas e inadimplência OK','Nada consta na prefeitura (regularização)','Laudo de inspeção predial do condomínio disponível e em dia (NBR 16.747 / Lei SP 16.642/2017)']},
  {nome:'📍 Entorno', items:[
    'Distância real da praia conferida','Rua/entorno sem alagamento em chuva','Comércio e serviços próximos','Vagas de garagem conforme anúncio']}
];
const KEY='pd-vistoria-v1';
const ALLOWED=new Set(GROUPS.flatMap((g,gi)=>g.items.map((_,ii)=>gi+'_'+ii)));
function createStore(access){
 let state=Object.create(null),session=false,status='As marcações serão salvas neste navegador se o armazenamento estiver disponível.';
 try{
  const raw=access().getItem(KEY);
  if(raw!==null){
   let parsed;
   try{parsed=JSON.parse(raw);}catch{session=true;}
   if(!session){
    if(parsed===null||typeof parsed!=='object'||Array.isArray(parsed))session=true;
    else for(const [key,value] of Object.entries(parsed)){
     if(ALLOWED.has(key)&&(value==='ok'||value==='bad'))state[key]=value;
     else session=true;
    }
   }
   status=session?'Modo sessão: há dados armazenados inválidos ou desconhecidos. Somente marcações válidas foram recuperadas. O conteúdo original não será sobrescrito; novas alterações ficam apenas nesta página. Use Recomeçar para autorizar sua remoção.':'Marcações anteriores recuperadas deste navegador.';
  }
 }catch{session=true;status='Modo sessão: não foi possível ler o armazenamento. Alterações ficam apenas nesta página e podem se perder ao recarregar.';}
 function snapshot(){return {state:{...state},session,status,total:ALLOWED.size};}
 function mark(key,value){
  if(!ALLOWED.has(key)||!['ok','bad'].includes(value))return snapshot();
  if(state[key]===value)delete state[key];else state[key]=value;
  if(!session){try{access().setItem(KEY,JSON.stringify(state));status='Marcações salvas neste navegador. Não há sincronização com outros dispositivos.';}
   catch{session=true;status='Modo sessão: não foi possível salvar esta alteração. As marcações atuais ficam apenas nesta página; dados anteriores podem reaparecer ao recarregar.';}}
  return snapshot();
 }
 function reset(){
  state=Object.create(null);
  try{access().removeItem(KEY);session=false;status='Marcações removidas deste navegador. O registro foi reiniciado.';}
  catch{session=true;status='Modo sessão: o registro foi limpo apenas nesta página. Não foi possível remover dados armazenados; eles podem reaparecer ao recarregar.';}
  return snapshot();
 }
 return {snapshot,mark,reset};
}
if(typeof module==='object'&&module.exports)module.exports={createStore,KEY,GROUPS};
if(!root.document)return;
const store=createStore(()=>root.localStorage),get=id=>root.document.getElementById(id);
function render(){
 const {state,total,status}=store.snapshot();
 get('groups').innerHTML=GROUPS.map((g,gi)=>`<div class="card"><h2>${g.nome}</h2>${g.items.map((t,ii)=>{
  const key=gi+'_'+ii,value=state[key];
  return `<div class="item ${value==='ok'?'ok':value==='bad'?'bad':''}"><span style="flex:1">${t}</span><div class="opts"><button type="button" aria-pressed="${value==='ok'}" onclick="mark('${key}','ok')">✓ OK</button><button type="button" aria-pressed="${value==='bad'}" onclick="mark('${key}','bad')">✗ Problema</button></div></div>`;
 }).join('')}</div>`).join('');
 const done=Object.keys(state).length,ok=Object.values(state).filter(v=>v==='ok').length,pct=Math.round(done/total*100);
 get('bar').style.width=pct+'%';get('score').textContent=pct+'%';get('score').style.color='#0369a1';
 get('verdict').textContent=`${done}/${total} itens registrados: ${ok} marcados OK, ${done-ok} com problema e ${total-done} sem marcação. Não é avaliação de segurança.`;
 get('storage-status').textContent=status;
}
root.mark=(key,value)=>{store.mark(key,value);render();};
root.resetAll=()=>{if(root.confirm('Limpar todas as marcações desta página e remover o registro salvo neste navegador, inclusive dados inválidos? Esta ação não pode ser desfeita.')){store.reset();render();}};
render();
})(typeof window==='undefined'?globalThis:window);
