import {assess,briefing,followup} from './core.mjs';
const byId=id=>document.getElementById(id);
const listing=byId('listing');
const output=byId('output');
function show(value){output.value=value;byId('status').textContent='Resultado pronto para revisão. Nenhuma mensagem foi enviada.';output.focus();}
listing.addEventListener('submit',event=>{event.preventDefault();try{show(briefing(Object.fromEntries(new FormData(listing))));}catch(error){byId('status').textContent=error.message;}});
byId('diagnose').addEventListener('click',()=>{const result=assess(Object.fromEntries(new FormData(listing)));show(`REVISÃO DE COMPLETUDE\n${result.filled} de ${result.total} campos preenchidos.\n\n${result.missing.length?'Confirmar:\n'+result.missing.map(x=>'• '+x).join('\n'):'Todos os campos estão preenchidos. Confira a veracidade com a fonte.'}\n\nEste checklist não avalia qualidade comercial, SEO, documentação ou preço de mercado. Um campo preenchido ainda pode estar incorreto.`);});
byId('followup').addEventListener('submit',event=>{event.preventDefault();try{show(followup(Object.fromEntries(new FormData(event.target))));}catch(error){byId('status').textContent=error.message;}});
byId('copy').addEventListener('click',async()=>{if(!output.value){byId('status').textContent='Gere um resultado antes de copiar.';return;}try{await navigator.clipboard.writeText(output.value);byId('status').textContent='Texto copiado. Revise antes de usar.';}catch{output.focus();output.select();byId('status').textContent='Selecionei o texto. Use a opção Copiar do seu dispositivo.';}});
byId('download').addEventListener('click',()=>{if(!output.value){byId('status').textContent='Gere um resultado antes de baixar.';return;}const url=URL.createObjectURL(new Blob([output.value],{type:'text/plain;charset=utf-8'}));const a=document.createElement('a');a.href=url;a.download='praia-digital-briefing.txt';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);byId('status').textContent='Arquivo preparado para download.';});
byId('clear').addEventListener('click',()=>{listing.reset();byId('followup').reset();output.value='';byId('status').textContent='Campos e resultado limpos.';});
