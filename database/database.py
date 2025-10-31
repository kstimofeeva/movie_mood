from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .models import *

class Database:
    def __init__ (self, database_url: str):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(bind = self.engine, autoflush = False, autocommit = False)
        return

    def create_tables(self):
        self.metadata.create_all(bind = self.engine)
        return

    def get_session(self):
        return self.SessionLocal()