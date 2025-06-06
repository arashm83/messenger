from hashlib import sha256
from repositories.UserRepository import UserRepository
from models.user import User
import re

class AuthService:

    def __init__(self):
        self.user_repo = UserRepository()

    def validate_username(self, user_name):
        if not re.fullmatch(r'[A-Za-z0-9_.]{3:}', user_name):
            return False
        return True
    
    def validate_password(self, passwd):
        if not re.fullmatch(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$", passwd):
            return False, None
        return True, sha256(passwd)

    def validate_phone_number(self, phone_number):
        if len(phone_number) != 11:
            return False
        return True
    
    def get_hash(self, passwd):    
        return sha256(passwd)
    
    def _validate(self, user_name, passwd, phone_number):
        if not re.fullmatch(r'[A-Za-z0-9_.]{3:}', user_name):
            return False, "Invalid Username"
        if not re.fullmatch(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$", passwd):
            return False, "Invalid Psssword"
        if len(phone_number) != 11:
            return False, "Invalid Phone number"
        return True, None
    
    def register(self, user_name, passwd, phone_number):
        validate, err = self._validate(user_name, passwd, phone_number)
        if validate:
            if self.user_repo.get_user(user_name):
                return False, "Username Already Exists"
            
            self.user_repo.add_user(User(user_name, sha256(passwd), phone_number))
            return True, None
        return False, err
        
    def sign_in(self, user_name, passwd):
        try:
            user = self.user_repo.get_user(user_name)
            if user.passwd_hash == sha256(passwd):
                return user
        except:
            return False
        
    