from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = 'sqlite:///weather.db'

engine = create_engine(
    DATABASE_URL,
    connect_args={'check_same_thread': False}
)

Base = declarative_base()

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


def init_db():
    import models

    Base.metadata.create_all(bind=engine)
    print('Таблицы базы данных созданы или уже существуют.')