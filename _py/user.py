from flask import current_app
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, email):
        self.email = email
        self.password = ""
        self.active = True
    
    def get_id(self):
        return self.email
    
    @property
    def is_active(self):
        return self.active

def get_user(email):
    user = User(email)
    return user