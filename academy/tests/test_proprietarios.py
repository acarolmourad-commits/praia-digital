import pytest

from academy.core.database import Base


def _create_owner(client, payload):
    r = client.post("/proprietarios", json=payload)
    assert r.status_code == 200, r.text
    return r.json()["codigo"]


def test_create_proprietario(client):
    payload = {
        "nome_completo": "Joao Silva",
        "cpf_cnpj": "12345678900",
        "email": "joao@example.com",
        "whatsapp": "11999999999",
        "tipo_proprietario": "fisica",
        "cidade": "Santos",
        "tipo_imovel": "apartamento",
        "valor_anunciado": 800000,
        "valor_liquido_desejado": 720000,
        "declaracao_aceite": True,
    }
    r = client.post("/proprietarios", json=payload)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["codigo"] == "PD-000001"
    assert data["status"] == "AGUARDANDO_ANALISE"
    assert data["valor_anunciado"] == 800000
    assert data["valor_liquido_desejado"] == 720000

    r2 = client.get(f"/proprietarios/{data['codigo']}")
    assert r2.status_code == 200
    assert r2.json()["codigo"] == data["codigo"]


def test_valor_liquido_nao_pode_ser_maior_que_anunciado(client):
    payload = {
        "nome_completo": "Maria",
        "cpf_cnpj": "98765432100",
        "email": "maria@example.com",
        "whatsapp": "11988888888",
        "valor_anunciado": 100000,
        "valor_liquido_desejado": 200000,
        "declaracao_aceite": True,
    }
    r = client.post("/proprietarios", json=payload)
    assert r.status_code == 400


def test_fluxo_aprovado_e_publicacao(client):
    owner = {
        "nome_completo": "Carlos",
        "cpf_cnpj": "11122233344",
        "email": "carlos@example.com",
        "whatsapp": "11977777777",
        "cidade": "Santos",
        "tipo_imovel": "apartamento",
        "valor_anunciado": 800000,
        "valor_liquido_desejado": 720000,
        "declaracao_aceite": True,
    }
    r = client.post("/proprietarios", json=owner)
    assert r.status_code == 200
    codigo = r.json()["codigo"]

    files_doc = [("file", ("doc.jpg", b"fakeimagebytes", "image/jpeg"))]
    files_foto1 = [("file", ("foto1.jpg", b"fakeimagebytes", "image/jpeg"))]
    files_foto2 = [("file", ("foto2.jpg", b"fakeimagebytes2", "image/jpeg"))]
    r_doc = client.post(f"/proprietarios/{codigo}/documentos", files=files_doc, data={"tipo_documento": "identidade"})
    assert r_doc.status_code == 200
    r_foto1 = client.post(f"/proprietarios/{codigo}/fotos", files=files_foto1)
    assert r_foto1.status_code == 200
    r_foto2 = client.post(f"/proprietarios/{codigo}/fotos", files=files_foto2)
    assert r_foto2.status_code == 200

    r_analise = client.post(f"/proprietarios/{codigo}/analisar")
    assert r_analise.status_code == 200
    data = r_analise.json()
    assert data["status"] == "APROVADO"

    r_pub = client.post(f"/proprietarios/{codigo}/publicar")
    assert r_pub.status_code == 200
    pub = r_pub.json()
    assert pub["status"] == "PUBLICADO"
    assert pub["pagina_url"].startswith("https://praia.digital/proprietarios/")

    assert Base.metadata.tables is not None


def test_pendencia_e_correcao(client):
    owner = {
        "nome_completo": "Bia",
        "cpf_cnpj": "55566677788",
        "email": "bia@example.com",
        "whatsapp": "11966666666",
        "declaracao_aceite": True,
    }
    r = client.post("/proprietarios", json=owner)
    assert r.status_code == 200
    codigo = r.json()["codigo"]

    r_analise = client.post(f"/proprietarios/{codigo}/analisar")
    assert r_analise.status_code == 200
    data = r_analise.json()
    assert data["status"] == "PENDENCIA"

    r_corrigir = client.post(f"/proprietarios/{codigo}/corrigir", json={"campos": {"cidade": "Santos", "tipo_imovel": "casa"}})
    assert r_corrigir.status_code == 200
    assert r_corrigir.json()["status"] == "REANALISE"
