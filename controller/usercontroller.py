from flask_restful import reqparse
from database import db
from models.userprofile import UserProfile
from service.validation import email, password


def create_user(name_first, name_last, email, password):
    user = UserProfile(name_first=name_first, name_last=name_last, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user

def user_instance(id):
    cur_user = UserProfile.query.get_or_404(UserProfile.id == id)
    return cur_user


user_parser = reqparse.RequestParser()

user_parser.add_argument(
    'name_first', dest='name_first',
    required=True, help='The current user\'s first name'
)

user_parser.add_argument(
    'name_last', dest='name_last',
    required=True, help='The current user\'s last name'
)

user_parser.add_argument(
    'email', dest='email', type=email,
    required=True, help='The current user\'s email'
)

user_parser.add_argument(
    'password', dest='password', type=password,
    required=True, help='The current user\'s password'
)