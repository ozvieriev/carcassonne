from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from ..core import config


engine = create_engine(
    config.connectionString,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

def getDb() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()