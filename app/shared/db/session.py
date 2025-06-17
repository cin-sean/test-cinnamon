from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.shared.settings import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class DBSession:
    def __init__(self):
        self.session = None

    def __enter__(self):
        self.session = SessionLocal()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
