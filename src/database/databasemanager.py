from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.user import Base as UserBase
from models.message import Base as MessageBase
from models.contact import Base as ContactBase


class DatabaseManager:
    def __init__(self, db_url="sqlite:///messenger.db"):
        self.engine = create_engine(db_url, echo=False, future=True)
        self.SessionLocal = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)

    def create_tables(self):
        UserBase.metadata.create_all(self.engine)
        MessageBase.metadata.create_all(self.engine)
        ContactBase.metadata.create_all(self.engine)

    def get_session(self):
        return self.SessionLocal()
if __name__=='__main__':
    db = DatabaseManager()
    db.create_tables()