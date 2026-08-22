from __future__ import annotations

import pytest

from academy.core.lead_segmentation import (
    LeadInterest,
    LeadOrigin,
    LeadSegment,
    segment_lead,
    whatsapp_message_for,
    INTEREST_KEYWORDS,
    SOURCE_KEYWORDS,
)


class TestInterestClassification:
    def test_imoveis(self):
        segment = segment_lead(raw_text="Quero comprar um apartamento no litoral")
        assert segment.interest is LeadInterest.IMOVEIS

    def test_temporada(self):
        segment = segment_lead(raw_text="Quero colocar minha casa para aluguel de temporada")
        assert segment.interest is LeadInterest.TEMPORADA

    def test_airbnb_booking(self):
        segment = segment_lead(raw_text="Quero alugar por Airbnb e Booking")
        assert segment.interest is LeadInterest.AIRBNB_BOOKING

    def test_fotografia_edicao(self):
        segment = segment_lead(raw_text="Preciso de fotografia profissional e edição de fotos")
        assert segment.interest is LeadInterest.FOTOGRAFIA_EDICAO

    def test_marketing_digital(self):
        segment = segment_lead(raw_text="Quero fazer marketing digital e SEO para minha imobiliária")
        assert segment.interest is LeadInterest.MARKETING_DIGITAL

    def test_cursos(self):
        segment = segment_lead(raw_text="Quero fazer um curso na Academy")
        assert segment.interest is LeadInterest.CURSOS

    def test_investidor(self):
        segment = segment_lead(raw_text="Sou investidor e quero flipping de imóveis")
        assert segment.interest is LeadInterest.INVESTIDOR

    def test_administracao(self):
        segment = segment_lead(raw_text="Preciso de uma administradora para meu condomínio")
        assert segment.interest is LeadInterest.ADMINISTRACAO

    def test_unknown_when_no_signal(self):
        segment = segment_lead(raw_text="Olá, tudo bem?")
        assert segment.interest is LeadInterest.UNKNOWN

    def test_unknown_when_empty(self):
        segment = segment_lead()
        assert segment.interest is LeadInterest.UNKNOWN

    def test_multiple_interests_returns_highest_score(self):
        segment = segment_lead(raw_text="Quero comprar um apartamento e fazer um curso")
        assert segment.interest in {LeadInterest.IMOVEIS, LeadInterest.CURSOS}

    def test_signals_are_recorded(self):
        segment = segment_lead(raw_text="Quero comprar um apartamento")
        assert "apartamento" in segment.raw_signals


class TestOriginClassification:
    def test_form_origin(self):
        segment = segment_lead(source="form-contato")
        assert segment.origin is LeadOrigin.FORM

    def test_whatsapp_origin(self):
        segment = segment_lead(source="whatsapp-link")
        assert segment.origin is LeadOrigin.WHATSAPP

    def test_landing_origin(self):
        segment = segment_lead(source="landing-page")
        assert segment.origin is LeadOrigin.LANDING

    def test_checkout_origin(self):
        segment = segment_lead(source="checkout-academy")
        assert segment.origin is LeadOrigin.CHECKOUT

    def test_blog_origin(self):
        segment = segment_lead(source="blog-post")
        assert segment.origin is LeadOrigin.BLOG

    def test_unknown_origin(self):
        segment = segment_lead(source="evento")
        assert segment.origin is LeadOrigin.OUTRO

    def test_empty_origin(self):
        segment = segment_lead()
        assert segment.origin is LeadOrigin.OUTRO


class TestSegmentIntegration:
    def test_service_mapping(self):
        segment = segment_lead(raw_text="Quero comprar um apartamento")
        assert segment.service == "imobiliario"

    def test_context_is_deterministic(self):
        segment = segment_lead(raw_text="Quero comprar um apartamento")
        assert "interest=imoveis" in segment.context
        assert "apartamento" in segment.context

    def test_full_segment_structure(self):
        segment = segment_lead(
            name="João",
            email="joao@example.com",
            phone="11999999999",
            source="form-contato",
            magnet="imovel",
            raw_text="Quero comprar um apartamento no litoral",
        )
        assert isinstance(segment, LeadSegment)
        assert segment.interest is LeadInterest.IMOVEIS
        assert segment.origin is LeadOrigin.FORM
        assert segment.service == "imobiliario"
        assert segment.context


class TestWhatsAppMessage:
    def test_known_interest_message(self):
        segment = segment_lead(raw_text="Quero comprar um apartamento")
        message = whatsapp_message_for(segment)
        assert "imóveis" in message.lower()

    def test_unknown_interest_fallback(self):
        segment = segment_lead(raw_text="Olá")
        message = whatsapp_message_for(segment)
        assert "especialista" in message.lower() or "conte" in message.lower()

    def test_marketing_message(self):
        segment = segment_lead(raw_text="Quero fazer marketing digital")
        message = whatsapp_message_for(segment)
        assert "marketing digital" in message.lower()

    def test_cursos_message(self):
        segment = segment_lead(raw_text="Quero fazer um curso")
        message = whatsapp_message_for(segment)
        assert "cursos" in message.lower()


class TestSegmentationFailSafe:
    def test_none_name_does_not_crash(self):
        segment = segment_lead(name=None)
        assert segment.interest is LeadInterest.UNKNOWN

    def test_non_string_fields_do_not_crash(self):
        segment = segment_lead(name=123, email=True)
        assert segment.interest is LeadInterest.UNKNOWN

    def test_empty_string_fields(self):
        segment = segment_lead(name="", email="", phone="")
        assert segment.interest is LeadInterest.UNKNOWN

    def test_unicode_text(self):
        segment = segment_lead(raw_text="Quero comprar um apartamento no litoral norte 🌴")
        assert segment.interest is LeadInterest.IMOVEIS


class TestSegmentationReproducibility:
    def test_deterministic_for_same_input(self):
        text = "Quero comprar um apartamento no litoral"
        first = segment_lead(raw_text=text)
        second = segment_lead(raw_text=text)
        assert first == second

    def test_case_insensitive(self):
        upper = segment_lead(raw_text="QUERO COMPRAR UM APARTAMENTO")
        lower = segment_lead(raw_text="quero comprar um apartamento")
        assert upper.interest == lower.interest
