# app/database/database_manager.py
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

Base = declarative_base()


class DatabaseManager:
    def __init__(self, database_url=None):
        self.database_url = database_url or os.getenv("DATABASE_URL",
                                                      "postgresql://admin:password@localhost:5432/bitcoin_tracker")
        if not self.database_url:
            raise ValueError("DATABASE_URL is not set and no database_url provided")
        self.engine = create_engine(self.database_url)
        self.SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=self.engine)
        Base.metadata.bind = self.engine
        Base.metadata.create_all(bind=self.engine)

    def get_session(self):
        return self.SessionLocal()

    def get_engine(self):
        return self.engine

    def create_tables(self):
        Base.metadata.create_all(bind=self.engine)
