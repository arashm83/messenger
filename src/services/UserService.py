from AuthService import AuthService
from repositories.UserRepository import UserRepository
from models.user import User

class UserService:

    def __init__(self):
        self.user_repo = UserRepository()
        self.auth_service = AuthService()

    def sign_in(self, user_name, passwd):
        return self.auth_service.sign_in(user_name, passwd)
    
    def sign_up(self, user_name, passwd, phone_number):
        return self.auth_service.register(user_name, passwd, phone_number)
    
    def update(self, user: User, new_username=None, new_passwd=None, new_phone=None, new_pic = None):
        new_username = new_username if self.auth_service.validate_username(new_username) else user.username
        new_passwd_hash = self.auth_service.get_hash(new_passwd) if self.auth_service.validate_password(new_passwd) else user.passwd_hash
        new_phone = self.auth_service.validate_phone_number(new_phone) if new_phone else user.phone_number
        new_pic = new_pic if new_pic else user.profile_pic

        user.username = new_username
        user.passwd_hash = new_passwd_hash
        user.phone_number = new_phone
        user.profile_pic = new_pic

        self.user_repo.update_user(user)
            


    

    
