from PhongMach.models import  User
from PhongMach import db
from password_strength import PasswordPolicy

import hashlib

def auth_user(username, password):
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        return User.query.filter(User.username.__eq__(username.strip()),
                                User.password.__eq__(password)).first()

def register(name, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name, username=username.strip(), password=password, avatar=avatar)
    db.session.add(u)
    db.session.commit()

def PasswordStrong(password):
    policy = PasswordPolicy.from_names(
        length=8,  # min length: 8
        uppercase=1,  # need min. 2 uppercase letters
        numbers=1,  # need min. 2 digits
        special=1,  # need min. 2 special characters
    )
    return policy.test(password)



def get_user_by_id(user_id):
    return User.query.get(user_id)