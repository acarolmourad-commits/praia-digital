#!/usr/bin/env python3
import webbrowser
import subprocess
import sys

LEADS = [
    ("Porto da Lua Prime", "(11) 90000-0001", "Olá! Quero apresentar uma parceria com ferramentas de IA e captação para Porto da Lua."),
    ("Praia Grande Site View", "(11) 90000-0002", "Olá! Quero apresentar uma parceria com ferramentas de IA e captação para Praia Grande."),
    ("Porto da Lua Blue", "(11) 90000-0003", "Olá! Quero apresentar uma parceria com ferramentas de IA e captação para Porto da Lua."),
    ("Prime Imóveis Centro", "(11) 90000-0004", "Olá! Quero apresentar uma parceria com ferramentas de IA e captação para o Centro."),
    ("Costa Verde Imóveis", "(11) 90000-0005", "Olá! Quero apresentar uma parceria com ferramentas de IA e captação para Costa Verde."),
]

for nome, telefone, mensagem in LEADS:
    url = f"https://wa.me/55{telefone.replace('(','').replace(')','').replace('-','').replace(' ','')}?text={mensagem.replace(' ', '%20')}"
    print(f"Abrindo WhatsApp para: {nome}")
    webbrowser.open(url)
