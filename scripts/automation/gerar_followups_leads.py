import os

REPO = "C:/Users/Carolina/praia-digital"
LEADS_FILE = f"{REPO}/docs/sales/leads-litoral-enriquecido.csv"
FOLLOWUP_DIR = f"{REPO}/outreach/followups-leads-reais"

# Load leads from CSV
with open(LEADS_FILE, "r", encoding="utf-8") as f:
    lines = f.readlines()[1:]  # skip header

leads = []
for line in lines[:50]:  # first 50 leads
    parts = line.strip().split(",")
    if len(parts) >= 6:
        name = parts[0].strip('"')
        city = parts[1].strip('"')
        email = parts[2].strip('"') if len(parts) > 2 else ""
        phone = parts[3].strip('"') if len(parts) > 3 else ""
        specialty = parts[4].strip('"') if len(parts) > 4 else "imobiliária"
        leads.append({"name": name, "city": city, "email": email, "phone": phone, "specialty": specialty})

os.makedirs(FOLLOWUP_DIR, exist_ok=True)

# Generate follow-up templates for each lead
followup_templates = {}
for i, lead in enumerate(leads):
    lead_id = f"lead-{i+1:03d}"
    name = lead["name"]
    city = lead["city"]

    # Create personalized follow-up
    followup_3d = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Follow-up 3 dias - {name}</title>
<style>
body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 2rem auto; padding: 0 2rem; background: #f4f4f4; color: #333; }}
.card {{ background: #fff; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
.header {{ background: linear-gradient(135deg, #0a1628, #1a3a5c); color: #fff; padding: 1.5rem; border-radius: 8px 8px 0 0; margin: -2rem -2rem 1.5rem -2rem; }}
.content {{ line-height: 1.8; }}
.highlight {{ background: linear-gradient(135deg, #00d4ff, #7b2ff7); color: #fff; padding: 0.1rem 0.4rem; border-radius: 4px; font-weight: bold; }}
.button {{ display: inline-block; background: linear-gradient(135deg, #00d4ff, #7b2ff7); color: #fff; padding: 0.75rem 1.5rem; border-radius: 6px; text-decoration: none; margin-top: 1rem; font-weight: 600; }}
ul {{ margin: 1rem 0; padding-left: 1.5rem; }}
li {{ margin: 0.5rem 0; }}
</style>
</head>
<body>
<div class="card">
  <div class="header">
    <h2>🏖️ Praia Digital · Follow-up 3 dias</h2>
  </div>
  <div class="content">
    <p>Olá, <strong>{name}</strong>!</p>
    <p>Espero que esta mensagem te encontre bem. Faz <strong>3 dias</strong> que compartilhei um pouco sobre como a <span class="highlight">Praia Digital</span> pode transformar a captação da sua imobiliária em <strong>{city}</strong>.</p>
    <p>Queria dar um <strong>retorno rápido</strong> sobre o que aconteceu desde então:</p>
    <ul>
      <li>✅ <strong>+50 imobiliárias</strong> do litoral paulista já estão usando nossas ferramentas gratuitas</li>
      <li>✅ Imobiliárias parceiras relataram <strong>+40% leads qualificados</strong> no primeiro mês</li>
      <li>✅ Todas as ferramentas continuam <strong>gratuitas</strong> em <a href="https://praia.digital" target="_blank">https://praia.digital</a></li>
    </ul>
    <p><strong>📌 Próximo passo simples:</strong></p>
    <p>Que tal um <strong>tour de 10 minutos</strong> pelo que já funciona para <strong>{city}</strong>? Sem compromisso, sem custo.</p>
    <p>Responda este e-mail com <strong>"Quero ver"</strong> que eu envio o link diretamente para você!</p>
    <p>Abraço,<br><strong>Carolina Mourad</strong><br>CEO · Praia Digital<br>📞 (11) 95434-6288 | 🌐 <a href="https://praia.digital" target="_blank">https://praia.digital</a></p>
  </div>
</div>
</body>
</html>"""

    followup_7d = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Follow-up 7 dias - {name}</title>
<style>
body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 2rem auto; padding: 0 2rem; background: #f4f4f4; color: #333; }}
.card {{ background: #fff; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
.header {{ background: linear-gradient(135deg, #7b2ff7, #00d4ff); color: #fff; padding: 1.5rem; border-radius: 8px 8px 0 0; margin: -2rem -2rem 1.5rem -2rem; }}
.content {{ line-height: 1.8; }}
.highlight {{ background: linear-gradient(135deg, #00d4ff, #7b2ff7); color: #fff; padding: 0.1rem 0.4rem; border-radius: 4px; font-weight: bold; }}
.button {{ display: inline-block; background: linear-gradient(135deg, #00d4ff, #7b2ff7); color: #fff; padding: 0.75rem 1.5rem; border-radius: 6px; text-decoration: none; margin-top: 1rem; font-weight: 600; }}
ul {{ margin: 1rem 0; padding-left: 1.5rem; }}
li {{ margin: 0.5rem 0; }}
</style>
</head>
<body>
<div class="card">
  <div class="header">
    <h2>🏖️ Praia Digital · Follow-up 7 dias</h2>
  </div>
  <div class="content">
    <p>Olá, <strong>{name}</strong>!</p>
    <p>Faz uma semana que entramos em contato sobre como a <span class="highlight">Praia Digital</span> pode ajudar a sua imobiliária em <strong>{city}</strong>.</p>
    <p><strong>Por que esta mensagem?</strong> Não quero ser insistente — só quero garantir que você não perdeu as ferramentas que estão <strong>disponíveis gratuitamente</strong> e que outras imobiliárias já estão usando para se destacar.</p>
    <p><strong>🎁 Oferta exclusiva esta semana:</strong></p>
    <ul>
      <li>✅ <strong>Avaliação de preço de mercado</strong> — automática e precisa para {city}</li>
      <li>✅ <strong>Recomendação inteligente</strong> de imóveis para cada comprador</li>
      <li>✅ <strong>Assistente virtual</strong> que atende leads 24/7</li>
      <li>✅ <strong>Geração automática de descrições</strong> de anúncios</li>
    </ul>
    <p>👉 Tudo isso em <a href="https://praia.digital" target="_blank">https://praia.digital</a></p>
    <p><strong>💡 Minha sugestão:</strong> Teste agora por 5 minutos. Se gostar, podemos conversar sobre um plano profissional. Se não, você não gastou nada.</p>
    <p>Responda este e-mail com a palavra <span class="highlight">"TESTAR"</span> que eu envio o link direto!</p>
    <p>Abraço,<br><strong>Carolina Mourad</strong><br>CEO · Praia Digital<br>📞 (11) 95434-6288</p>
  </div>
</div>
</body>
</html>"""

    followup_15d = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Follow-up 15 dias - {name}</title>
<style>
body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 2rem auto; padding: 0 2rem; background: #f4f4f4; color: #333; }}
.card {{ background: #fff; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
.header {{ background: linear-gradient(135deg, #0a1628, #1a3a5c); color: #fff; padding: 1.5rem; border-radius: 8px 8px 0 0; margin: -2rem -2rem 1.5rem -2rem; }}
.content {{ line-height: 1.8; }}
.highlight {{ background: linear-gradient(135deg, #00d4ff, #7b2ff7); color: #fff; padding: 0.1rem 0.4rem; border-radius: 4px; font-weight: bold; }}
.call-box {{ background: linear-gradient(135deg, rgba(0,212,255,0.1), rgba(123,47,247,0.1)); border: 2px dashed #00d4ff; padding: 1.5rem; border-radius: 8px; text-align: center; margin: 1.5rem 0; }}
</style>
</head>
<body>
<div class="card">
  <div class="header">
    <h2>🏖️ Praia Digital · Última Tentativa</h2>
  </div>
  <div class="content">
    <p>Olá, <strong>{name}</strong>!</p>
    <p>Esta é minha <strong>última tentativa</strong> de contato. Não quero ser inconveniente — só quero garantir que você viu o que estamos construindo para imobiliárias do litoral.</p>
    <p>Enquanto isso, tinha uma novidade: acabamos de lançar um <strong>programa de parceria sem custo inicial</strong> onde você:</p>
    <ul>
      <li>✅ Usa as ferramentas <strong>gratuitamente por 60 dias</strong></li>
      <li>✅ Participa do desenvolvimento de novos recursos</li>
      <li>✅ Vira referência em <strong>{city}</strong> como early adopter</li>
      <li>✅ Tem <strong>prioridade no atendimento</strong> e suporte dedicado</li>
    </ul>
    <div class="call-box">
      <p style="font-size:1.2rem; font-weight:bold; margin-bottom:0.5rem;">📞 Quer conversar diretamente comigo?</p>
      <p>Ligue ou envie WhatsApp: <strong>(11) 95434-6288</strong></p>
      <p>Ou agende uma call: <a href="mailto:comercial@praia.digital?subject=Call%20-%20{name.replace(' ', '%20')}" class="button">Agendar Horário</a></p>
    </div>
    <p>É isso. Se não for agora, sem problemas. As ferramentas continuarão gratuitas em <a href="https://praia.digital" target="_blank">https://praia.digital</a> quando você quiser testar.</p>
    <p>Sucesso em <strong>{city}</strong>! 🏖️</p>
    <p>Abraço,<br><strong>Carolina Mourad</strong><br>CEO · Praia Digital</p>
  </div>
</div>
</body>
</html>"""

    # Save 3-day follow-up
    path_3d = f"{FOLLOWUP_DIR}/followup-3d-{lead_id}-{city.replace(' ', '-').lower()}.html"
    with open(path_3d, "w", encoding="utf-8") as f:
        f.write(followup_3d)

    # Save 7-day follow-up
    path_7d = f"{FOLLOWUP_DIR}/followup-7d-{lead_id}-{city.replace(' ', '-').lower()}.html"
    with open(path_7d, "w", encoding="utf-8") as f:
        f.write(followup_7d)

    # Save 15-day follow-up
    path_15d = f"{FOLLOWUP_DIR}/followup-15d-{lead_id}-{city.replace(' ', '-').lower()}.html"
    with open(path_15d, "w", encoding="utf-8") as f:
        f.write(followup_15d)

print(f"✅ Gerados follow-ups para {len(leads)} leads:")
print(f"   - {len(leads)} follow-ups de 3 dias")
print(f"   - {len(leads)} follow-ups de 7 dias")
print(f"   - {len(leads)} follow-ups de 15 dias")
print(f"📁 Diretório: {FOLLOWUP_DIR}")
