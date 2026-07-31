(function(){
  const target = document.querySelector('main .container');
  if (!target) return;
  if (document.getElementById('trust-block')) return;
  const block = document.createElement('section');
  block.id = 'trust-block';
  block.style.cssText = 'margin-top:18px;padding:16px;border:1px solid rgba(15,118,110,.18);border-radius:14px;background:#f0fdfa';
  block.innerHTML = `
<h2 style="margin-top:0">Conte com atendimento rápido</h2>
<div style="display:flex;flex-wrap:wrap;gap:10px">
  <a class="btn btn-primary" href="https://wa.me/5511954346288?text=Ol%C3%A1!%20Quero%20atendimento%20sobre%20este%20im%C3%B3vel." target="_blank" rel="noopener">Falar no WhatsApp agora</a>
</div>
<p style="margin:10px 0 0;color:#334155">Resposta direta, curadoria humana e conteúdo atualizado dia a dia no litoral de SP.</p>`;
  target.appendChild(block);
})();
