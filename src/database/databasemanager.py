from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from  models.base import Base
import models.user
import models.message
import models.contact
from functions.singleton import singleton


@singleton
class DatabaseManager:
    def __init__(self, db_url="sqlite:///src/database/messenger.db"):
        self.engine = create_engine(db_url, echo=False, future=True)
        self.SessionLocal = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)

    def create_tables(self):
        Base.metadata.create_all(self.engine)


    def get_session(self):
        return self.SessionLocal()