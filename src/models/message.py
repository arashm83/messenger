from sqlalchemy import String, Integer, ForeignKey, DateTime
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base
import json


class Message(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(String, nullable=False)
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    receiver_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))

    def serialize(self) -> str:
        data = {
            "id": self.id,
            "content": self.content,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }
        return json.dumps(data)

    @staticmethod
    def deserialize(json_str: str):
        data = json.loads(json_str)
        return Message(
            id=data.get("id"),
            content=data.get("content"),
            sender_id=data.get("sender_id"),
            receiver_id=data.get("receiver_id"),
            timestamp=datetime.fromisoformat(data["timestamp"]) if data.get("timestamp") else None
        )