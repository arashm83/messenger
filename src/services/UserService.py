from services.AuthService import AuthService
from repositories.UserRepository import UserRepository
from models.user import User

class UserService:

    def __init__(self):
        self.user_repo = UserRepository()
        self.auth_service = AuthService()

    def sign_in(self, user_name: str, passwd: str) -> User | None:
        return self.auth_service.sign_in(user_name, passwd)
    
    def sign_up(self, user_name: str, passwd: str, phone_number: str):
        return self.auth_service.register(user_name, passwd, phone_number)
    
    def update(self, user: User, new_username=None, new_passwd=None, new_phone=None, new_pic = None):
        try:
            if new_username and not self.auth_service.validate_username(new_username):
                return False, 'invalid username format'
            if new_passwd and not self.auth_service.validate_password(new_passwd):
                return False, 'invalid password format'
            if new_phone and not self.auth_service.validate_phone_number(new_phone):
                return False, 'invalid phone number format'

            updated_username = new_username if new_username else user.username
            updated_passwd_hash = self.auth_service.get_hash(new_passwd) if new_passwd else user.passwd_hash
            updated_phone = new_phone if new_phone else user.phone_number
            updated_pic = new_pic if new_pic else user.profile_pic

            # Check for username and phone uniqueness
            if updated_username != user.user_name and self.user_repo.get_user(updated_username):
                return False, 'username already exists'
            if updated_phone != user.phone_number and self.user_repo.get_user_by_phone(updated_phone):
                return False, 'phone number already exists'

            # Update user fields
            user.user_name = updated_username
            user.passwd_hash = updated_passwd_hash
            user.phone_number = updated_phone
            user.profile_pic = updated_pic

            self.user_repo.update_user(user)
            return True, 'user info updated succesfully'
        except Exception as e:
            return False, f'an error happend while updating user info : {e}'

    def find_user(self, user_name: str) -> User | None:
        try:
            user = self.user_repo.get_user(user_name)
            if user:
                return user
            else:
                return None
        except Exception:
            return None

    def find_user_by_phone(self, phone_number: str):
        try:
            user = self.user_repo.get_user_by_phone(phone_number)
            if user:
                return user
            else:
                return None
        except Exception:
            return None
        
    def add_contact(self, user: User, contact: User) -> bool:
        return self.user_repo.add_contact(user, contact)
        
    def get_contact(self, user: User) -> list[User]:
        return self.user_repo.get_contacts(user)