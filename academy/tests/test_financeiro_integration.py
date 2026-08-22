from fastapi.testclient import TestClient
from academy.main import app
from academy.core.database import Base, get_db
from academy.tests._shared_test_db import override_get_db, TestingSessionLocal, engine as test_engine

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)
Base.metadata.create_all(bind=test_engine)

def test_financeiro_routers_registered():
    paths = [r.path for r in app.routes if hasattr(r, 'path') and '/financeiro' in r.path]
    assert '/financeiro/registros' in paths
    assert '/financeiro/registros/{registro_id}' in paths
    assert '/financeiro/registros/{registro_id}/comprovante' in paths
    assert '/financeiro/registros/{registro_id}/validar' in paths
    print('ROUTER_OK', paths)

def test_financeiro_create_requires_auth():
    r = client.post('/financeiro/registros', json={"customer_name": "Fernanda Lima", "amount_expected": 1200})
    assert r.status_code == 401
    print('AUTH_OK', r.status_code)
