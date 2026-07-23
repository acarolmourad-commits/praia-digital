#!/usr/bin/env python3
"""
litoral_whatsapp_bot.py
Bot autônomo de WhatsApp para Litoral Prime: responde leads e qualifica sozinho.
Uso: python litoral-prime-imoveis/automation/litoral_whatsapp_bot.py
"""
import json
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parents[1]
CHAT_LOG = BASE / 'docs/chat-log-litoral-prime.json'
CHAT_LOG.parent.mkdir(parents=True, exist_ok=True)

RESPOSTAS = {
    'oi': 'Olá! Bem-vindo à Litoral Prime. Qual seu interesse: comprar, alugar ou vender?',
    'comprar': 'Temos ótimas opções de compra no litoral de SP. Qual cidade/bairro você prefere?',
    'alugar': 'Qual tipo de imóvel você busca: apto, casa, flat? E em qual cidade?',
    'vender': 'Faça uma avaliação gratuita! Envie o endereço do imóvel.',
    'preço': 'Qual seu orçamento? Assim filtramos as melhores opções.',
    'visita': 'Perfeito! Envie seu nome e telefone que agendamos em 15 min.',
}

def registrar_mensagem(remetente, mensagem, resposta):
    hoje = datetime.now().strftime('%Y-%m-%d')
    registro = {
        'data': datetime.now().isoformat(),
        'remetente': remetente,
        'mensagem': mensagem,
        'resposta': resposta,
    }
    if CHAT_LOG.exists():
        historico = json.loads(CHAT_LOG.read_text(encoding='utf-8'))
    else:
        historico = []
    historico.append(registro)
    CHAT_LOG.write_text(json.dumps(historico, ensure_ascii=False, indent=2), encoding='utf-8')

def responder_cliente(mensagem):
    chave = next((k for k in RESPOSTAS if k in mensagem.lower()), None)
    resposta = RESPOSTAS.get(chave, 'Entendi! Um especialista vai te responder em instantes.')
    registrar_mensagem('cliente', mensagem, resposta)
    return resposta

def main():
    print('[WhatsApp Bot Litoral Prime] Iniciando atendimento autônomo...')
    testes = [
        'oi',
        'comprar',
        'alugar',
        'vender',
        'preço',
        'visita',
    ]
    for msg in testes:
        resp = responder_cliente(msg)
        print(f'Cliente: {msg}')
        print(f'Bot: {resp}')
        print('-' * 40)
    print(f'[WhatsApp Bot Litoral Prime] Atendimentos registrados: {len(testes)}')

if __name__ == '__main__':
    main()
