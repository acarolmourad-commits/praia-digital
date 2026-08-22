from __future__ import annotations

import json
import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class LeadInterest(str, Enum):
    IMOVEIS = "imoveis"
    TEMPORADA = "temporada"
    AIRBNB_BOOKING = "airbnb_booking"
    FOTOGRAFIA_EDICAO = "fotografia_edicao"
    MARKETING_DIGITAL = "marketing_digital"
    CURSOS = "cursos"
    INVESTIDOR = "investidor"
    ADMINISTRACAO = "administracao"
    UNKNOWN = "unknown"


class LeadOrigin(str, Enum):
    FORM = "form"
    WHATSAPP = "whatsapp"
    LANDING = "landing"
    CHECKOUT = "checkout"
    BLOG = "blog"
    OUTRO = "outro"


INTEREST_KEYWORDS: dict[LeadInterest, list[str]] = {
    LeadInterest.IMOVEIS: ["imovel", "apartamento", "casa", "cobertura", "venda", "compra", "lancamento", "pronto"],
    LeadInterest.TEMPORADA: ["temporada", "aluguel temporada", "locacao temporada", "verao", "ferias", "aluguel"],
    LeadInterest.AIRBNB_BOOKING: ["airbnb", "booking", "rental", "aluguel curto", "curta estadia", "plataforma"],
    LeadInterest.FOTOGRAFIA_EDICAO: ["foto", "fotografia", "edicao", "imagem", "tour virtual"],
    LeadInterest.MARKETING_DIGITAL: ["marketing", "midia", "instagram", "facebook", "ads", "seo", "redes sociais", "conversao"],
    LeadInterest.CURSOS: ["curso", "academy", "treinamento", "capacitacao", "aula", "certificado"],
    LeadInterest.INVESTIDOR: ["investidor", "investimento", "patrimonio", "retorno", "renda", "flipping"],
    LeadInterest.ADMINISTRACAO: ["administradora", "administracao", "gestao", "condominio", "imobiliaria"],
}

SOURCE_KEYWORDS: dict[LeadOrigin, list[str]] = {
    LeadOrigin.FORM: ["form", "cadastro", "contato", "lead-form"],
    LeadOrigin.WHATSAPP: ["whatsapp", "wa.me", "zap", "mensagem"],
    LeadOrigin.LANDING: ["landing", "pagina", "pagina unica"],
    LeadOrigin.CHECKOUT: ["checkout", "pagamento", "assinatura", "plano"],
    LeadOrigin.BLOG: ["blog", "artigo", "post"],
}


@dataclass(frozen=True)
class LeadSegment:
    interest: LeadInterest
    origin: LeadOrigin
    service: str
    context: str
    raw_signals: list[str]


def _normalize_text(value: Optional[str]) -> str:
    if not isinstance(value, str):
        return ""
    return re.sub(r"\s+", " ", value).strip().lower()


def _classify_interest(text: str) -> tuple[LeadInterest, list[str]]:
    text = _normalize_text(text)
    if not text:
        return LeadInterest.UNKNOWN, []

    best_interest = LeadInterest.UNKNOWN
    best_score = 0
    best_signals: list[str] = []

    for interest, keywords in INTEREST_KEYWORDS.items():
        score = 0
        signals: list[str] = []
        for keyword in keywords:
            if keyword in text:
                score += 1
                signals.append(keyword)
        if score > best_score:
            best_score = score
            best_interest = interest
            best_signals = signals

    return best_interest, best_signals


def _classify_origin(source: Optional[str], context: Optional[str]) -> tuple[LeadOrigin, list[str]]:
    text = _normalize_text(" ".join(filter(None, [source, context])))
    if not text:
        return LeadOrigin.OUTRO, []

    best_origin = LeadOrigin.OUTRO
    best_score = 0
    best_signals: list[str] = []

    for origin, keywords in SOURCE_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in text)
        signals = [keyword for keyword in keywords if keyword in text]
        if score > best_score:
            best_score = score
            best_origin = origin
            best_signals = signals

    return best_origin, best_signals


def _service_for(interest: LeadInterest) -> str:
    return {
        LeadInterest.IMOVEIS: "imobiliario",
        LeadInterest.TEMPORADA: "temporada",
        LeadInterest.AIRBNB_BOOKING: "airbnb_booking",
        LeadInterest.FOTOGRAFIA_EDICAO: "fotografia_edicao",
        LeadInterest.MARKETING_DIGITAL: "marketing_digital",
        LeadInterest.CURSOS: "academy",
        LeadInterest.INVESTIDOR: "investidor",
        LeadInterest.ADMINISTRACAO: "administracao",
        LeadInterest.UNKNOWN: "geral",
    }[interest]


def segment_lead(
    *,
    name: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    city: Optional[str] = None,
    source: Optional[str] = None,
    magnet: Optional[str] = None,
    context: Optional[str] = None,
    raw_text: Optional[str] = None,
) -> LeadSegment:
    def _to_str(value: object) -> str:
        if isinstance(value, str):
            return value
        if isinstance(value, (int, float, bool)):
            return str(value)
        return ""

    text = " ".join(
        _to_str(v)
        for v in [name, email, phone, city, source, magnet, context, raw_text]
        if v is not None
    )
    interest, interest_signals = _classify_interest(text)
    origin, origin_signals = _classify_origin(source, context)

    context_parts = [
        f"interest={interest.value}",
        f"origin={origin.value}",
    ]
    if interest_signals:
        context_parts.append(f"interest_signals={','.join(interest_signals)}")
    if origin_signals:
        context_parts.append(f"origin_signals={','.join(origin_signals)}")

    return LeadSegment(
        interest=interest,
        origin=origin,
        service=_service_for(interest),
        context="; ".join(context_parts),
        raw_signals=interest_signals + origin_signals,
    )


def whatsapp_message_for(segment: LeadSegment) -> str:
    interest_label = {
        LeadInterest.IMOVEIS: "imóveis",
        LeadInterest.TEMPORADA: "locação de temporada",
        LeadInterest.AIRBNB_BOOKING: "Airbnb/Booking",
        LeadInterest.FOTOGRAFIA_EDICAO: "fotografia e edição",
        LeadInterest.MARKETING_DIGITAL: "marketing digital",
        LeadInterest.CURSOS: "cursos",
        LeadInterest.INVESTIDOR: "investimento",
        LeadInterest.ADMINISTRACAO: "administração de imóveis",
        LeadInterest.UNKNOWN: "atendimento geral",
    }[segment.interest]

    if segment.interest == LeadInterest.UNKNOWN:
        return (
            "Olá! Recebemos seu contato e vamos direcionar para um especialista. "
            "Conte um pouco mais sobre o que você precisa?"
        )

    return (
        f"Olá! Identificamos seu interesse em {interest_label}. "
        f"Já vamos conectar você com a solução mais adequada."
    )
