from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from academy.core.database import Base, get_db
import academy.core.models

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
))

Base.metadata.create_all(bind=TestingSessionLocal.kw["bind"])
engine = TestingSessionLocal.kw["bind"]


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
