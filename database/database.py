from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from .models import Base

class Database:
    def __init__ (self, database_url: str):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(bind = self.engine, autoflush = False, autocommit = False, expire_on_commit=False)

    def create_tables(self):
        try:
            Base.metadata.create_all(bind = self.engine)
            return True
        except SQLAlchemyError as e:
            print("Ошибка при создании таблиц")
            return False
        except Exception as e:
            print("Неизвестная ошибка при создании таблиц")
            return False

    def get_session(self):
        return self.SessionLocal()

    def test_connection(self)->bool:
        try:
            with self.engine.connect() as connection:
                connection.execute(text('SELECT 1'))
                return True
        except SQLAlchemyError as e:
            print("ошибка подключения к бд")
            return False
        except Exception as e:
            print("Неизвестная ошибка подключения к бд")
            return False