from models.user import User

class UserRepository:


    def get_user(user_name):
        ...

    def add_user():
        ...

    def get_contacts(user: User) -> list['User']:
        ...
