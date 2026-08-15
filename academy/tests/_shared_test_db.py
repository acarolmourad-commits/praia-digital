from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.exc import OperationalError
import academy.core.models
import academy.core.database as _db

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
))
engine = TestingSessionLocal.kw["bind"]
try:
    _db.Base.metadata.create_all(bind=engine)
except OperationalError:
    pass

Base = _db.Base
get_db = _db.get_db


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
