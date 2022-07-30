import bcrypt
from flask_restful import fields
import bcrypt
from database import db

class UserProfile(db.Model):
    """Model used to store user data."""

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_first = db.Column(db.String(50))
    name_last = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True)
    email_verified = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(255))

    def __init__(self, name_first, name_last, email, password):
        self.name_first = name_first
        self.name_last = name_last
        self.email = email
        if isinstance(password, str):
            password = bytes(password, 'utf-8')
        self.password = str(bcrypt.hashpw(password, bcrypt.gensalt()), 'utf8')

    def verified_password(self, password_to_check):
        if isinstance(password_to_check, str):
            password_to_check = bytes(password_to_check, 'utf-8')
        password = bytes(self.password, 'utf8')
        return bcrypt.hashpw(password_to_check, password) == password

    def __repr__(self):
        return f'<User {self.name_first} {self.name_last} | {self.email}>'


user_fields = {
    'id': fields.Integer,
    'name_first': fields.String,
    'name_last': fields.String,
    'email': fields.String,
    'email_verified': fields.Boolean,
}
