import re
from time import time


from db import db

CONFIRMATION_EXPIRATION_DELTA = 1800 # 2 minutes

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(128))
    repeat_password = db.Column(db.String(128))
    number = db.Column(db.String(128))
    expire_at = db.Column(db.Integer, nullable=False)
    activated = db.Column(db.Boolean, default=False)


    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.expire_at = int(time()) + CONFIRMATION_EXPIRATION_DELTA

    @property
    def expired(self) -> bool:
        return time() > self.expire_at

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


    @classmethod    
    def find_by_username(cls, username):
            return cls.query.filter_by(username=username).first()
    
    @classmethod    
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_phone(cls, phone):
        return cls.query.filter_by(phone=phone).first()

    @classmethod
    def find_by_number(cls, number):
        return cls.query.filter_by(number=number).first()


    @classmethod
    def check_username(cls, username):
        if not  username.strip():
            return True

    @classmethod
    def check_name(cls, name):
        if not  name.strip():
            return True
    
    @classmethod
    def check_email(cls,email): 
        match=re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9.]*\.*[com|org|edu]{3}$)",email)
        if not match:
            return True
    @classmethod
    def check_phone(cls,phone): 
        match=re.search(r"(09(1[0-9]|3[1-9]|2[1-9])-?[0-9]{3}-?[0-9]{4}$)",phone)
        if not match:
            return True
    @classmethod
    def check_password(cls, password): 
        if not  password.strip():
            return True


    @classmethod 
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
    @classmethod
    def find_all(cls):
        return db.session.query(cls.id, cls.username, cls.email, cls.phone, cls.name).all()
        
