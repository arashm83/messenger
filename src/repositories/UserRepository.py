from models.user import User
from models.contact import Contact
from database.databasemanager import DatabaseManager
from functions.singleton import singleton


@singleton
class UserRepository:

    def __init__(self):
        self.db = DatabaseManager()

    def get_user(self, user_name) -> User | None:
        session = self.db.get_session()
        user = session.query(User).filter(User.user_name == user_name).first()
        session.close()
        return user

    def add_user(self, user: User) -> bool:
        session = self.db.get_session()
        try:
            session.add(user)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            return False
        finally:
            session.close()

    def get_contacts(self, user: User) -> list[User]:
        session = self.db.get_session()
        contacts = (
            session.query(User)
            .join(Contact, Contact.contact_id == User.id)
            .filter(Contact.user_id == user.id)
            .all()
        )
        session.close()
        return contacts

    def update_user(self, user: User) -> bool:
        session = self.db.get_session()
        try:
            session.merge(user)
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False
        finally:
            session.close()

    def get_user_by_phone(self, phone_number) -> User | None:
        session = self.db.get_session()
        user = session.query(User).filter(User.phone_number == phone_number).first()
        session.close()
        return user
    
    def get_user_by_id(self, id) -> User | None:
        session = self.db.get_session()
        user = session.query(User).filter(User.id == id).first()
        session.close()
        return user
    
    def add_contact(self, user: User, contact: User):
        session = self.db.get_session()
        con = Contact(user_id = user.id, contact_id = contact.id)
        try:
            session.add(con)
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False
        finally:
            session.close()
