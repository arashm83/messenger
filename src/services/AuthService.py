from hashlib import sha256
from repositories.UserRepository import UserRepository
from models.user import User
import re

class AuthService:

    def __init__(self):
        self.user_repo = UserRepository()

    def validate_username(self, user_name) -> bool:
        if re.fullmatch(r'^[a-zA-Z][a-zA-Z0-9_]{3,19}$', user_name):
            return True
        return False
    
    def validate_password(self, passwd) -> bool:
        if re.fullmatch(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$", passwd):
            return True
        return False

    def validate_phone_number(self, phone_number) -> bool:
        if len(phone_number) != 11:
            return False
        return True
    
    def get_hash(self, passwd) -> str:
        return sha256(passwd.encode()).hexdigest()
    
    def _validate(self, user_name, passwd, phone_number) -> tuple[bool, str]:
        if not re.fullmatch(r'^[a-zA-Z][a-zA-Z0-9_]{3,19}$', user_name):
            return False, "Invalid Username"
        if not re.fullmatch(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$", passwd):
            return False, "Invalid Psssword"
        if len(phone_number) != 11:
            return False, "Invalid Phone number"
        return True, None
    
    def register(self, user_name, passwd, phone_number) -> tuple[bool, str]:
        validate, err = self._validate(user_name, passwd, phone_number)
        if validate:
            if self.user_repo.get_user(user_name):
                return False, "Username Already Exists"
            
            if self.user_repo.add_user(User(user_name=user_name, passwd_hash=self.get_hash(passwd), phone_number=phone_number)):
                return True, 'Registeration Succesfull'
        return False, err
        
    def sign_in(self, user_name, passwd) -> User | None:
        try:
            user = self.user_repo.get_user(user_name)
            if user.passwd_hash == self.get_hash(passwd):
                return user
        except:
            return None