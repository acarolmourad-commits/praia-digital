import os,re,glob
NEW = '<script>(function(){var form=document.getElementById("leadForm");if(!form)return;var WA="5511954346288";function collect(){var d={};var els=form.querySelectorAll("input,select,textarea");for(var i=0;i<els.length;i++){var el=els[i];if(!el.id)continue;var v=(el.value||"").trim();if(v)d[el.id]=v;}return d;}function send(data){var st=document.getElementById("formStatus");try{var leads=JSON.parse(localStorage.getItem("pd_leads")||"[]");leads.push(Object.assign({ts:new Date().toISOString(),page:location.pathname},data));localStorage.setItem("pd_leads",JSON.stringify(leads));}catch(e){}try{window.dispatchEvent(new CustomEvent("lead_pre_qualificado",{detail:data}));}catch(e){}var ctrl=new AbortController();var to=setTimeout(function(){ctrl.abort();},3500);fetch("https://academy.praia.digital/leads",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(data),signal:ctrl.signal}).then(function(r){clearTimeout(to);if(r.status===200){if(st)st.textContent="Recebido! Entraremos em contato.";return;}throw new Error("st");}).catch(function(){clearTimeout(to);var rot={"name":"Nome","email":"E-mail","phone":"WhatsApp","city":"Cidade","magnet":"Interesse","faixa_preco":"Faixa de preco","prazo_interesse":"Prazo","source":"Origem"};var partes=[];for(var k in data){if(k==="source")continue;partes.push((rot[k]||k)+": "+data[k]);}var msg="Ola! Quero receber informacoes."+(partes.length?" "+partes.join(" | "):"");window.open("https://wa.me/"+WA+"?text="+encodeURIComponent(msg),"_blank","noopener");if(st)st.textContent="Abrindo seu WhatsApp para concluir o envio. Se preferir, fale conosco: (11) 95434-6288.";});}form.addEventListener("submit",function(e){e.preventDefault();send(collect());});})();</script>'
pat = re.compile(r"<script>[^<]*?academy\.praia\.digital/leads.*?</script>", re.S)
changed=[]
for p in glob.glob("**/*.html", recursive=True):
    t=open(p,encoding="utf-8",errors="replace").read()
    if "academy.praia.digital/leads" not in t: continue
    t2,n=pat.subn(NEW,t)
    if n==0:
        print("SEM BLOCO",p); continue
    if t2!=t:
        open(p,"w",encoding="utf-8").write(t2); changed.append(p)
print("corrigidos:",len(changed))
