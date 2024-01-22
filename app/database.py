import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение URL для подключения к базе данных из переменных окружения
DATABASE_URL = os.getenv("DATABASE_URL")

# Создание подключения к базе данных
engine = create_engine(DATABASE_URL)

# Создание сессии базы данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание базового класса для моделей SQLAlchemy
Base: DeclarativeMeta = declarative_base()
