from hashlib import sha256
from repositories.UserRepository import get_user, add_user
from models.user import User
import re

class AuthServce:

    def __init__(self):
        pass

    def _validate(self, user_name, passwd, phone_number):
        if not re.fullmatch(r'[A-Za-z0-9_.]{3:}', user_name):
            raise Exception("Invalid Username")
        if not re.fullmatch(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$", passwd):
            raise Exception('Invalid Psssword')
        if len(phone_number) != 11:
            raise Exception('Invalid Phone number')
        return True
    
    def register(self, user_name, passwd, phone_number):
        if self._validate(user_name, passwd, phone_number):
            if get_user(user_name):
                raise Exception("Username Already Exists")
            
            add_user(User(user_name, sha256(passwd), phone_number))
            return True
        
    def sign_in(self, user_name, passwd):
        try:
            user = get_user(user_name)
            if user.passwd_hash == sha256(passwd):
                return user
        except:
            raise Exception('Incorrect Username or Password')
        
        