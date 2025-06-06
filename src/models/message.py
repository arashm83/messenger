from sqlalchemy import String, Integer, ForeignKey, DateTime
from datetime import datetime, timezone
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()

class Message(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(String, nullable=False)
    sender: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    recever: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
