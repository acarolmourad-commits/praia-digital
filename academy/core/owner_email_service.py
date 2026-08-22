import os
from academy.core.email_service import send_email


def send_pendencia(owner_email: str, codigo: str, pendencias: list[str], correction_url: str) -> bool:
    subject = f"Seu cadastro está quase pronto — {codigo}"
    body = f"""<p>Olá,</p>
<p>Recebemos seu cadastro <strong>{codigo}</strong>, mas precisamos de ajustes para continuar:</p>
<ul>
"""
    for p in pendencias:
        body += f"<li>{p}</li>\n"
    body += f"""</ul>
<p>Corrija pelo link seguro abaixo e retorne para análise:</p>
<p><a href="{correction_url}">Corrigir cadastro</a></p>
<p>Equipe Praia Digital</p>
"""
    return send_email(owner_email, subject, body, html=True)


def send_certificacao(owner_email: str, codigo: str, pagina_url: str, valor_anunciado: int, nivel: str) -> bool:
    subject = f"Seu imóvel foi aprovado e publicado — {codigo}"
    body = f"""<p>Parabéns, seu anúncio foi publicado.</p>
<ul>
  <li><strong>Código:</strong> {codigo}</li>
  <li><strong>URL pública:</strong> <a href="{pagina_url}">{pagina_url}</a></li>
  <li><strong>Valor divulgado:</strong> R$ {valor_anunciado:,.2f}</li>
  <li><strong>Nível de verificação:</strong> {nivel}</li>
</ul>
<p>Para atualizar informações, use o canal recebido.</p>
<p>Equipe Praia Digital</p>
"""
    return send_email(owner_email, subject, body, html=True)


def send_recebimento(owner_email: str, codigo: str) -> bool:
    subject = f"Cadastro recebido — {codigo}"
    body = f"""<p>Olá,</p>
<p>Recebemos seu cadastro <strong>{codigo}</strong> para análise.</p>
<p>Você receberá atualizações por e-mail.</p>
<p>Equipe Praia Digital</p>
"""
    return send_email(owner_email, subject, body, html=True)


def send_bloqueio(owner_email: str, codigo: str, motivo: str) -> bool:
    subject = f"Cadastro não aprovado — {codigo}"
    body = f"""<p>Olá,</p>
<p>Infelizmente não foi possível aprovar seu cadastro <strong>{codigo}</strong> no momento.</p>
<p><strong>Motivo:</strong> {motivo}</p>
<p>Se precisar, fale conosco para orientação.</p>
<p>Equipe Praia Digital</p>
"""
    return send_email(owner_email, subject, body, html=True)
