from database.databasemanager import DatabaseManager
from models.message import Message
from functions.singleton import singleton

@singleton
class MessageRepository:

    def __init__(self):
        self.db = DatabaseManager()

    def save_message(self, message: Message) -> bool:
        session = self.db.get_session()
        try:
            session.add(message)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            return False
        finally:
            session.close()

    def get_messages(self, user1_id: str, user2_id: str) -> list[Message]:
        session = self.db.get_session()
        messages = session.query(Message).filter(
                ((Message.sender_id == user1_id) & (Message.receiver_id == user2_id)) |
                ((Message.sender_id == user2_id) & (Message.receiver_id == user1_id))
            ).order_by(Message.timestamp).all()
        session.close()
        return messages