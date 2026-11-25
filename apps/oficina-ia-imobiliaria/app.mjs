import {assess,briefing,followup} from './core.mjs';
const byId=id=>document.getElementById(id);
const listing=byId('listing');
const output=byId('output');
const status=byId('status');
const resultKind=byId('result-kind');
let resultFile='praia-digital-texto-revisado.txt';
let resultSource=null;
let resultSnapshot='';
let generatedText='';
const snapshot=form=>JSON.stringify([...new FormData(form)]);
const isOutdated=()=>resultSource!==null && snapshot(resultSource)!==resultSnapshot;
const outdatedMessage='Os dados usados neste resultado foram alterados. Gere o resultado novamente antes de copiar ou baixar. O texto anterior foi preservado para revisão.';

function show(value,source,kind,file){
  if(output.value.trim() && output.value!==generatedText && !window.confirm('Substituir o texto que você editou? Se quiser guardá-lo, cancele e guarde sua revisão antes de gerar outro resultado.')) return;
  output.value=value;
  generatedText=output.value;
  if(resultKind) resultKind.textContent=kind;
  resultFile=file;
  resultSource=source;
  resultSnapshot=snapshot(source);
  status.textContent='Resultado pronto para revisão. Nenhuma mensagem foi enviada.';
  output.focus();
}

for(const form of [listing,byId('followup')]){
  const update=()=>{
    if(resultSource===form){
      status.textContent=isOutdated()?outdatedMessage:'Os campos voltaram aos valores usados no resultado. Revise o texto antes de usar.';
    }
  };
  form.addEventListener('input',update);
  form.addEventListener('change',update);
}

function canExport(action){
  if(isOutdated()){
    status.textContent=outdatedMessage;
    return false;
  }
  if(!output.value.trim()){
    status.textContent=`Gere um resultado antes de ${action}.`;
    return false;
  }
  return true;
}

listing.addEventListener('submit',event=>{event.preventDefault();try{show(briefing(Object.fromEntries(new FormData(listing))),listing,'Briefing e prompt','praia-digital-briefing.txt');}catch(error){status.textContent=error.message;}});
byId('diagnose').addEventListener('click',()=>{const result=assess(Object.fromEntries(new FormData(listing)));show(`REVISÃO DE COMPLETUDE\n${result.filled} de ${result.total} campos preenchidos.\n\n${result.missing.length?'Confirmar:\n'+result.missing.map(x=>'• '+x).join('\n'):'Todos os campos estão preenchidos. Confira a veracidade com a fonte.'}\n\nEste checklist não avalia qualidade comercial, SEO, documentação ou preço de mercado. Um campo preenchido ainda pode estar incorreto.`,listing,'Checklist de completude','praia-digital-checklist.txt');});
byId('followup').addEventListener('submit',event=>{
  event.preventDefault();
  try{
    const data=Object.fromEntries(new FormData(event.target));
    // Validate the stage before using it in the result label or file name.
    const text=followup(data);
    const stage=event.target.querySelector('select').selectedOptions[0].textContent;
    show(text,event.target,`Modelo de e-mail: ${stage}`,`praia-digital-email-${data.etapa}.txt`);
  }catch(error){status.textContent=error.message;}
});
byId('copy').addEventListener('click',async()=>{
  if(!canExport('copiar')) return;
  const text=output.value;
  try{
    await navigator.clipboard.writeText(text);
    // Do not overwrite a newer warning/result while clipboard permission is pending.
    if(!isOutdated() && output.value===text) status.textContent='Texto copiado. Revise antes de usar.';
  }catch{
    if(isOutdated()){status.textContent=outdatedMessage;return;}
    if(output.value!==text) return;
    output.focus();output.select();
    status.textContent='Selecionei o texto. Use a opção Copiar do seu dispositivo.';
  }
});
byId('download').addEventListener('click',()=>{if(!canExport('baixar'))return;const url=URL.createObjectURL(new Blob([output.value],{type:'text/plain;charset=utf-8'}));const a=document.createElement('a');a.href=url;a.download=resultFile;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);status.textContent='Arquivo preparado para download.';});
byId('clear').addEventListener('click',()=>{
  const hasWork=Boolean(output.value.trim()) || [...document.querySelectorAll('#listing input, #listing textarea, #followup input, #followup textarea')].some(control=>control.value.trim());
  if(hasWork && !window.confirm('Limpar todos os campos e o resultado? Esta ação não pode ser desfeita.')) return;
  listing.reset();
  byId('followup').reset();
  output.value='';
  if(resultKind) resultKind.textContent='Nenhum resultado gerado';
  resultFile='praia-digital-texto-revisado.txt';
  resultSource=null;
  resultSnapshot='';
  generatedText='';
  status.textContent='Campos e resultado limpos.';
  listing.querySelector('[name="tipo"]').focus();
});

// Enable local-only controls only after every handler above has been installed.
// method="dialog" also prevents native navigation if a handler fails to run.
for (const control of document.querySelectorAll('[data-oficina-control]')) control.disabled=false;
byId('startup-status').hidden=true;
