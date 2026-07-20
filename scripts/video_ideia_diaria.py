#!/usr/bin/env python3
"""Ideia de video diaria (Proptech) — seleciona roteiro do dia a partir do JSON.
Imprime a sugestao do dia para o cron enviar no Telegram.
Uso: python video_ideia_diaria.py
"""
import json, os
from datetime import date
REPO=r"C:/Users/Carolina/praia-digital"
J=os.path.join(REPO,"docs/content/roteiros-video-diario.json")
def main():
    d=json.load(open(J,encoding="utf-8"))
    rot=d["roteiros"]
    dia=date.today().day
    r=rot[(dia-1)%len(rot)]
    print(f"🎬 Vídeo do dia ({dia}): {r['titulo']}")
    print("Roteiro:")
    for passo in r["roteiro"]: print("  -",passo)
    print(f"Ferramenta: {r['ferramenta']}")
if __name__=="__main__": main()
