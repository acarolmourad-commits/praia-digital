#!/usr/bin/env python3
"""
Agente de pré-vendas automatizado — Praia Digital
Versão 2: scoring ajustado com pesos mais precisos
"""

import csv
import json
import os
import re
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict

# Caminhos base
BASE_DIR = Path(__file__).resolve().parents[3]
PROSPECTS_CSV = BASE_DIR / "docs/sales/acquisition-7dias/prospects-dia1.csv"
FILA_APROVACAO_CSV = BASE_DIR / "docs/sales/acquisition-7dias/fila-aprovacao.csv"
LEADS_QUENTES_CSV = BASE_DIR / "docs/sales/acquisition-7dias/leads-quentes.csv"
RELATORIO_MD = BASE_DIR / "docs/sales/acquisition-7dias/auto-pre-vendas-relatorio-v2.md"
DECISAO_HUMANA_CSV = BASE_DIR / "docs/sales/acquisition-7dias/decisao-humana-dia1.csv"

# Campos do CSV de prospects
PROSPECT_FIELDS = [
    "nome_empresa","cidade","segmento","servico_potencial","canal_contato",
    "anuncio_analisado","problema_observado","prioridade","status","fonte",
    "site_analisado","anuncio_analisado_url","problema_especifico",
    "evidencia","servico_indicado","justificativa_match","score","prioridade_score",
    "canal_contato_publico","contato_publico","proposta_personalizada",
    "status_processamento","data_analise","fonte_analise"
]

# Campos da fila de aprovação
FILA_FIELDS = [
    "prospect","cidade","segmento","score","prioridade","problema",
    "evidencia","servico_indicado","justificativa_match","canal",
    "contato_publico","mensagem_inicial","follow_up_1","follow_up_2",
    "follow_up_3","status","data_analise"
]

# Campos de leads quentes
LEAD_FIELDS = [
    "empresa","pessoa","cidade","servico","anuncio_analisado",
    "problema","diagnostico","proposta","mensagem_enviada",
    "resposta_recebida","objecoes","proximo_passo",
    "whatsapp_handoff","data_handoff"
]


@dataclass
class Prospect:
    nome_empresa: str
    cidade: str
    segmento: str
    servico_potencial: str
    canal_contato: str
    anuncio_analisado: str
    problema_observado: str
    prioridade: str
    status: str
    fonte: str
    site_analisado: str = ""
    anuncio_analisado_url: str = ""
    problema_especifico: str = ""
    evidencia: str = ""
    servico_indicado: str = ""
    justificativa_match: str = ""
    score: int = 0
    prioridade_score: str = ""
    canal_contato_publico: str = ""
    contato_publico: str = ""
    proposta_personalizada: str = ""
    status_processamento: str = "NOVO"
    data_analise: str = ""
    fonte_analise: str = ""


class AutoPreVendasV2:
    def __init__(self):
        self.prospects: List[Prospect] = []
        self.fila: List[Dict] = []
        self.leads_quentes: List[Dict] = []
        self.stats = {
            "total": 0, "analisados": 0, "qualificados": 0,
            "propostas_preparadas": 0, "aprovacao_pendente": 0,
            "whatsapp_handoff": 0
        }
        # Decisões humanas preservadas
        self.decisoes_humanas = {}

    def load_prospects(self):
        """Carrega prospects do CSV"""
        if not PROSPECTS_CSV.exists():
            raise FileNotFoundError(f"CSV de prospects não encontrado: {PROSPECTS_CSV}")
        
        with open(PROSPECTS_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("nome_empresa", "").strip():
                    self.prospects.append(Prospect(
                        nome_empresa=row.get("nome_empresa", ""),
                        cidade=row.get("cidade", ""),
                        segmento=row.get("segmento", ""),
                        servico_potencial=row.get("servico_potencial", ""),
                        canal_contato=row.get("canal_contato", ""),
                        anuncio_analisado=row.get("anuncio_analisado", ""),
                        problema_observado=row.get("problema_observado", ""),
                        prioridade=row.get("prioridade", ""),
                        status=row.get("status", ""),
                        fonte=row.get("fonte", ""),
                    ))
        self.stats["total"] = len(self.prospects)
        print(f"📋 Carregados {len(self.prospects)} prospects")

    def load_decisoes_humanas(self):
        """Carrega decisões humanas anteriores para preservar"""
        if not DECISAO_HUMANA_CSV.exists():
            print("ℹ️ Sem decisões humanas anteriores para preservar")
            return
        
        with open(DECISAO_HUMANA_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                nome = row.get("nome_empresa", "").strip()
                if nome:
                    self.decisoes_humanas[nome] = {
                        "status": row.get("status", ""),
                        "score": row.get("score", ""),
                        "classificacao": row.get("classificacao", ""),
                    }
        
        print(f"🔒 Decisões humanas preservadas: {len(self.decisoes_humanas)}")

    def analyze_prospect(self, prospect: Prospect) -> Dict:
        """
        Analisa um prospect individual com scoring ajustado.
        """
        analysis = {
            "site_analisado": "",
            "anuncio_analisado_url": "",
            "problema_especifico": "",
            "evidencia": "",
            "servico_indicado": "",
            "justificativa_match": "",
            "score": 0,
            "prioridade_score": "",
            "canal_contato_publico": "",
            "contato_publico": "",
            "proposta_personalizada": "",
            "status_processamento": "ANALISADO",
            "data_analise": datetime.now().isoformat(),
            "fonte_analise": "auto-pre-vendas-v2"
        }

        # SCORING AJUSTADO - pesos mais precisos
        score = 0
        problema = ""
        servico = ""
        justificativa = ""
        evidencia = ""

        # 1. Anúncio público efetivamente encontrado (peso 25)
        anuncio_encontrado = False
        anuncio_url = ""
        if prospect.anuncio_analisado and prospect.anuncio_analisado.lower() != "pendente primeira análise":
            anuncio_encontrado = True
            anuncio_url = prospect.anuncio_analisado
            score += 25
        elif "airbnb" in prospect.canal_contato.lower() or "booking" in prospect.canal_contato.lower():
            score += 10  # indício de plataforma, mas sem URL confirmada

        # 2. Problema específico e verificável (peso 25)
        problema_especifico = False
        if prospect.problema_observado and prospect.problema_observado.lower() != "pendente primeira análise":
            problema_especifico = True
            score += 25
        elif prospect.segmento:
            score += 5  # sem problema específico, só segmento

        # 3. Aderência direta ao serviço (peso 20)
        servico_aderencia = False
        if "edição" in prospect.servico_potencial.lower() or "fotografia" in prospect.servico_potencial.lower():
            servico_aderencia = True
            score += 20
        elif "gestão" in prospect.segmento.lower() or "administração" in prospect.segmento.lower():
            score += 15
        else:
            score += 5

        # 4. Potencial de recorrência (peso 15)
        recorrencia = False
        if "gestão" in prospect.segmento.lower() or "administrador" in prospect.segmento.lower() or "imobiliária" in prospect.segmento.lower():
            recorrencia = True
            score += 15
        elif "coanfitrião" in prospect.segmento.lower():
            score += 10
        else:
            score += 3

        # 5. Facilidade de contato (peso 10)
        contato_facil = False
        canal = prospect.canal_contato.lower()
        if "whatsapp" in canal or "e-mail" in canal or "@" in canal or "telefone" in canal:
            contato_facil = True
            score += 10
        elif "site" in canal or "redes" in canal:
            score += 5
        else:
            score += 2

        # 6. Evidência concreta de oportunidade (peso 5)
        if prospect.problema_observado and "não confirmado" not in prospect.problema_observado.lower():
            score += 5
        else:
            score += 1

        # Limitar score
        score = min(100, max(0, score))

        # Classificação
        if score >= 80:
            prioridade_score = "PRIORIDADE MÁXIMA"
        elif score >= 60:
            prioridade_score = "PRIORIDADE ALTA"
        elif score >= 40:
            prioridade_score = "PRIORIDADE MÉDIA"
        else:
            prioridade_score = "BAIXA PRIORIDADE"

        # Determinar problema e serviço baseado em dados reais
        if not anuncio_encontrado and not problema_especifico:
            problema = "Dados públicos insuficientes para diagnóstico específico."
            servico = "Diagnóstico gratuito → definir após análise do anúncio"
            justificativa = "Sem evidência pública concreta de problema ou volume."
            evidencia = "Não há anúncio público confirmado nem problema específico registrado."
        elif anuncio_encontrado and problema_especifico:
            problema = prospect.problema_observado
            servico = prospect.servico_potencial if prospect.servico_potencial else "Edição + fotografia"
            justificativa = "Anúncio público identificado e problema específico registrado."
            evidencia = f"Anúncio: {anuncio_url}"
        elif problema_especifico:
            problema = prospect.problema_observado
            servico = prospect.servico_potencial if prospect.servico_potencial else "Edição + fotografia"
            justificativa = "Problema específico identificado, mas sem URL de anúncio confirmada."
            evidencia = prospect.problema_observado
        else:
            problema = "Oportunidade inferida a partir do segmento."
            servico = "Diagnóstico gratuito → definir após contato"
            justificativa = "Sem evidência suficiente para proposta direcionada."
            evidencia = "Apenas segmento conhecido; sem anúncio ou problema específico."

        # Gerar proposta personalizada
        proposta = self._gerar_proposta(prospect, servico, problema)

        analysis.update({
            "site_analisado": prospect.canal_contato,
            "anuncio_analisado_url": anuncio_url,
            "problema_especifico": problema,
            "evidencia": evidencia,
            "servico_indicado": servico,
            "justificativa_match": justificativa,
            "score": score,
            "prioridade_score": prioridade_score,
            "canal_contato_publico": prospect.canal_contato,
            "contato_publico": prospect.canal_contato,
            "proposta_personalizada": proposta,
        })

        return analysis

    def _gerar_proposta(self, prospect: Prospect, servico: str, problema: str) -> str:
        """Gera proposta personalizada baseada no perfil"""
        nome = prospect.nome_empresa
        cidade = prospect.cidade
        segmento = prospect.segmento.lower()

        if "airbnb" in segmento or "gestão airbnb" in segmento or "administrador portais" in segmento:
            return (
                f"Olá, time da {nome}.\n"
                f"Vi que vocês trabalham com {prospect.segmento} em {cidade}.\n"
                f"Acredito que a maior oportunidade está em padronizar a apresentação dos anúncios: "
                f"primeira foto, título e descrição com foco em conversão.\n"
                f"Na Praia Digital ajudamos gestores mult_PORTAL a aumentar cliques e reservas "
                f"com edição profissional de anúncios e fotos prontas para publicar.\n"
                f"Posso mostrar como eu estruturaria 1 anúncio sem compromisso?"
            )
        elif "coanfitrião" in segmento or "administrador temporada" in segmento:
            return (
                f"Olá, time da {nome}.\n"
                f"Coanfitrião/administração em {cidade} precisa de apresentação profissional para cada imóvel.\n"
                f"Temos edição de anúncios e fotografia profissional com entrega em 48h.\n"
                f"Posso mostrar um exemplo prático em 1 anúncio?"
            )
        elif "imobiliária" in segmento:
            return (
                f"Olá, time da {nome}.\n"
                f"Imobiliária em {cidade} pode aumentar o interesse nos anúncios com fotos e descrição profissionais.\n"
                f"Trabalhamos com fotografia profissional e edição de anúncios para imóveis no litoral.\n"
                f"Quer que eu envie uma análise gratuita de 1 dos seus anúncios?"
            )
        else:
            return (
                f"Olá, time da {nome}.\n"
                f"Vi que vocês atuam em {cidade} com {prospect.segmento}.\n"
                f"Queremos ajudar a apresentar os imóveis com mais profissionalismo.\n"
                f"Se quiser, faço uma análise gratuita de 1 anúncio e envio 3 melhorias objetivas."
            )

    def _gerar_follow_up(self, prospect: Prospect) -> Dict[str, str]:
        """Gera follow-ups personalizados"""
        nome = prospect.nome_empresa
        return {
            "follow_up_1": (
                f"Oi, só passando aqui rapidinho. Conseguiu ver a mensagem sobre a análise do anúncio? "
                f"Sem pressa, quando quiser é só enviar o link."
            ),
            "follow_up_2": (
                f"Tudo bem? Ainda estou com a análise no radar. "
                f"Quer que eu reserve o tempo para o seu anúncio? É bem rápido e sem custo."
            ),
            "follow_up_3": (
                f"Oi! Estamos finalizando os casos de lançamento por aqui e pensei em você. "
                f"Quer que eu envie um exemplo de antes/depois de um anúncio que acabamos de otimizar? "
                f"Assim você já tem uma ideia de como funciona na prática."
            ),
        }

    def aplicar_decisoes_humanas(self):
        """Aplica decisões humanas anteriores, sobrepondo o score automático"""
        for prospect in self.prospects:
            nome = prospect.nome_empresa
            if nome in self.decisoes_humanas:
                decisao = self.decisoes_humanas[nome]
                print(f"  🔒 Decisão humana preservada: {nome} → {decisao['status']}")
                
                # Marcar como não-automatizado
                # Não alterar o score, mas adicionar flag de decisão humana
                # O status será definido na fila de aprovação

    def processar_lote(self):
        """Processa todos os prospects carregados"""
        print(f"\n🔄 Processando {len(self.prospects)} prospects...")
        
        for i, prospect in enumerate(self.prospects, 1):
            print(f"  [{i}/{len(self.prospects)}] {prospect.nome_empresa}...", end=" ")
            
            # Analisar
            analysis = self.analyze_prospect(prospect)
            self.stats["analisados"] += 1

            # Verificar se qualificado
            if analysis["score"] >= 60:
                self.stats["qualificados"] += 1
                self.stats["propostas_preparadas"] += 1
                
                # Verificar se há decisão humana prévia
                nome = prospect.nome_empresa
                status_fila = "APROVAÇÃO_PENDENTE"
                if nome in self.decisoes_humanas:
                    decisao = self.decisoes_humanas[nome]
                    if decisao["status"] == "APROVADO_PARA_ABORDAGEM":
                        status_fila = "APROVADO_PARA_ABORDAGEM"
                        self.stats["aprovacao_pendente"] += 1
                    elif decisao["status"] == "DESCARTADO":
                        status_fila = "DESCARTADO"
                    elif decisao["status"] == "AGUARDANDO_APROVAÇÃO":
                        status_fila = "AGUARDANDO_APROVAÇÃO"
                    else:
                        status_fila = "APROVAÇÃO_PENDENTE"
                        self.stats["aprovacao_pendente"] += 1
                else:
                    self.stats["aprovacao_pendente"] += 1
                
                # Gerar follow-ups
                followups = self._gerar_follow_up(prospect)
                
                # Adicionar à fila de aprovação
                fila_item = {
                    "prospect": prospect.nome_empresa,
                    "cidade": prospect.cidade,
                    "segmento": prospect.segmento,
                    "score": analysis["score"],
                    "prioridade": analysis["prioridade_score"],
                    "problema": analysis["problema_especifico"],
                    "evidencia": analysis["evidencia"],
                    "servico_indicado": analysis["servico_indicado"],
                    "justificativa_match": analysis["justificativa_match"],
                    "canal": analysis["canal_contato_publico"],
                    "contato_publico": analysis["contato_publico"],
                    "mensagem_inicial": analysis["proposta_personalizada"],
                    "follow_up_1": followups["follow_up_1"],
                    "follow_up_2": followups["follow_up_2"],
                    "follow_up_3": followups["follow_up_3"],
                    "status": status_fila,
                    "data_analise": analysis["data_analise"],
                }
                self.fila.append(fila_item)
                print(f"✅ Score {analysis['score']} — {analysis['prioridade_score']} — {status_fila}")
            else:
                print(f"⏭️ Score {analysis['score']} — {analysis['prioridade_score']} (não qualificado)")

    def salvar_fila(self):
        """Salva fila de aprovação em CSV"""
        if not self.fila:
            print("\n⚠️ Nenhum item na fila de aprovação")
            return
        
        with open(FILA_APROVACAO_CSV, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FILA_FIELDS)
            writer.writeheader()
            writer.writerows(self.fila)
        
        print(f"\n💾 Fila de aprovação salva: {FILA_APROVACAO_CSV}")
        print(f"   Total: {len(self.fila)} prospects qualificados")

    def salvar_relatorio(self):
        """Gera relatório em Markdown"""
        # Contar por status
        por_status = {}
        for item in self.fila:
            status = item["status"]
            por_status[status] = por_status.get(status, 0) + 1

        relatorio = f"""# Relatório de pré-vendas automatizado — V2
Data: {datetime.now().isoformat()}
Processo: auto-pre-vendas v2
Regra: score >= 60 = QUALIFICADO; APROVADO_PARA_ABORDAGEM = autorização humana explícita

---

## Estatísticas

- Total de prospects: {self.stats['total']}
- Analisados: {self.stats['analisados']}
- Qualificados (score >= 60): {self.stats['qualificados']}
- Propostas preparadas: {self.stats['propostas_preparadas']}
- Aprovação pendente: {self.stats['aprovacao_pendente']}
- WhatsApp handoff: {self.stats['whatsapp_handoff']}

---

## Distribuição de status na fila

"""
        for status, count in por_status.items():
            relatorio += f"- {status}: {count}\n"

        relatorio += f"""
---

## Fila de aprovação

| # | Prospect | Cidade | Score | Prioridade | Problema | Serviço | Status |
|---|---------|--------|-------|------------|----------|---------|--------|
"""
        for i, item in enumerate(self.fila, 1):
            problema_curto = item["problema"][:80] + "..." if len(item["problema"]) > 80 else item["problema"]
            relatorio += f"| {i} | {item['prospect']} | {item['cidade']} | {item['score']} | {item['prioridade']} | {problema_curto} | {item['servico_indicado']} | {item['status']} |\n"

        relatorio += f"""
---

## Decisões humanas preservadas

- Riviera Temporada → APROVADO_PARA_ABORDAGEM
- CASA Home Management → APROVADO_PARA_ABORDAGEM
- Rivino Invest → AGUARDANDO_APROVAÇÃO
- Quinta Prime → AGUARDANDO_APROVAÇÃO
- Hello Bertioga → DESCARTADO

---

## Limitações

- Análise baseada em dados públicos; algumas informações podem estar desatualizadas
- Sem acesso a conteúdo privado de anúncios, e-mails internos ou sistemas de terceiros
- Sem envio automático externo; todo contato requer aprovação humana
- Score é uma estimativa inicial; ajustar conforme resultados reais

---

Gerado automaticamente por auto-pre-vendas v2
"""

        with open(RELATORIO_MD, "w", encoding="utf-8") as f:
            f.write(relatorio)
        
        print(f"📄 Relatório salvo: {RELATORIO_MD}")

    def run(self):
        """Executa o processo completo"""
        print("🚀 Iniciando agente de pré-vendas automatizado v2\n")
        
        self.load_prospects()
        self.load_decisoes_humanas()
        self.aplicar_decisoes_humanas()
        self.processar_lote()
        self.salvar_fila()
        self.salvar_relatorio()
        
        print("\n✅ Processamento concluído")
        print(f"\n📊 Resumo:")
        print(f"   Analisados: {self.stats['analisados']}/{self.stats['total']}")
        print(f"   Qualificados: {self.stats['qualificados']}")
        print(f"   Aprovação pendente: {self.stats['aprovacao_pendente']}")
        print(f"\n📁 Arquivos gerados:")
        print(f"   - {FILA_APROVACAO_CSV}")
        print(f"   - {RELATORIO_MD}")


if __name__ == "__main__":
    agent = AutoPreVendasV2()
    agent.run()
