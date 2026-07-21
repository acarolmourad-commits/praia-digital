(function(){
  const form = document.getElementById('b2bLeadFormPlan');
  if (!form) return;
  form.addEventListener('submit', async function(e){
    e.preventDefault();
    const nome = document.getElementById('b2bNomePlan').value.trim();
    const fone = document.getElementById('b2bFonePlan').value.trim();
    const cidade = document.getElementById('b2bCidadePlan').value.trim();
    const perfil = document.getElementById('b2bPerfilPlan').value;
    const plano = document.getElementById('b2bPlanoPlan').value;
    const subject = encodeURIComponent('Solicita proposta B2B');
    const body = encodeURIComponent(`Nome: ${nome}\nTelefone: ${fone}\nCidade: ${cidade}\nPerfil: ${perfil}\nPlano: ${plano}\n`);
    window.location.href = `mailto:comercial@praia.digital?subject=${subject}&body=${body}`;
    try {
      const endpoint = '/praia-digital/backend/api/leads/b2b.js';
      const res = await fetch(endpoint, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({nome,telefone:fone,cidade,perfil,plano}) });
      const feedback = document.getElementById('b2bFeedbackPlan');
      if (feedback) { feedback.style.display='block'; feedback.textContent='Interesse registrado! Abra seu e-mail para enviar.'; }
    } catch {
      const feedback = document.getElementById('b2bFeedbackPlan');
      if (feedback) { feedback.style.display='block'; feedback.textContent='Interesse registrado! Abra seu e-mail para enviar.'; }
    }
  });
})();
