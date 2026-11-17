from academy.tests._shared_test_db import Base, get_db, override_get_db, TestingSessionLocal, engine
import pytest


@pytest.fixture()
def owner_publication_sandbox(tmp_path, monkeypatch):
    """Keep example listings, uploads and sitemaps outside the public checkout."""
    from academy.core import publication_service, owner_email_service
    monkeypatch.chdir(tmp_path)
    public_dir = tmp_path / "proprietarios"
    public_dir.mkdir()
    monkeypatch.setattr(publication_service, "PUBLIC_DIR", str(public_dir))
    monkeypatch.setattr(owner_email_service, "send_email", lambda *args, **kwargs: True)
    (tmp_path / "sitemap.xml").write_text(
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>',
        encoding="utf-8",
    )
    return tmp_path


@pytest.fixture(autouse=True)
def _reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
def client():
    from fastapi.testclient import TestClient
    from academy.main import app
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture()
def db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
