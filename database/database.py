from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .models import Base

class Database:
    def __init__ (self, database_url: str):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(bind = self.engine, autoflush = False, autocommit = False, expire_on_commit=False)

    def create_tables(self):
        Base.metadata.create_all(bind = self.engine)
        return

    def get_session(self):
        return self.SessionLocal()