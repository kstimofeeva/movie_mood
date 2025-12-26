'''
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
'''# database/database.py
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from .models import Base

class Database:
    def __init__(self, database_url: str):
        """Инициализация подключения к PostgreSQL"""
        try:
            print(f"🔧 Подключаемся к PostgreSQL: {database_url}")

            # Для PostgreSQL добавляем пул соединений
            self.engine = create_engine(
                database_url,
                pool_size=10,  # Размер пула
                max_overflow=20,  # Максимальное количество соединений
                pool_pre_ping=True,  # Проверка соединений перед использованием
                echo=False  # Логирование SQL
            )

            self.SessionLocal = sessionmaker(
                bind=self.engine,
                autoflush=False,
                autocommit=False,
                expire_on_commit=False
            )
            print("✅ Объект Database создан для PostgreSQL")

        except Exception as e:
            print(f"❌ Ошибка при создании Database: {e}")
            raise

    def test_connection(self) -> bool:
        """Проверяет подключение к PostgreSQL"""
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text('SELECT version()'))
                version = result.fetchone()
                print(f"✅ Подключено к PostgreSQL {version[0]}")
                return True

        except SQLAlchemyError as e:
            print(f"❌ Ошибка подключения к PostgreSQL: {e}")
            return False
        except Exception as e:
            print(f"❌ Неизвестная ошибка: {e}")
            return False

    # Остальные методы остаются такими же
    # create_tables, get_session и т.д.'''