import os

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, inspect, MetaData
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker, DeclarativeBase, registry

load_dotenv()


class Connection:
    """Управление/инициализация БД и модели"""

    _instance = None
    connected = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Connection, cls).__new__(cls)
        return cls._instance


    def __init__(
        self,
    ):
        if self.connected:
            return

        self.url_object = URL.create(
            drivername="postgresql+psycopg2",
            username=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD", "456852"),
            host=os.getenv("DB_HOST", "db"),
            database=os.getenv("POSTGRES_DB", "postgres"),
            port=int(os.getenv("DB_PORT", "5432")),
        )

        self.engine = create_engine(
            self.url_object,
            echo=True,
            client_encoding="utf8",
        )
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        self.inspector: Inspector | None = inspect(subject=self.engine)
        self.inspector.clear_cache()
        self.connected = True


