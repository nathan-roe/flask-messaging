from datetime import datetime
import secrets
from flask_restful import fields
from database import db
from models.userprofile import UserProfile
from service.constants import Constants

class Token(db.Model):
    """General token used for authentication and authorization."""

    __tablename__ = 'tokens'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token_key = db.Column(db.String(50))
    created_date = db.Column('created_date', db.DateTime, default=datetime.utcnow())

    def __init__(self, user_id):
        self.token_key = secrets.token_urlsafe()
        self.user = UserProfile.query.filter(UserProfile.id == user_id).first()
        self.user_id = user_id

    def __repr__(self):
        return f'<Token {self.user!r}>'


class ExpiringToken(Token):
    """Extend Token to add expired method."""

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('UserProfile', backref=db.backref('tokens'))

    def expired(self):
        """Return boolean indicating token expiration."""
        now = datetime.utcnow()
        if self.created_date < now - Constants.TokenConstants.TOKEN_EXPIRE_TIME:
            return True
        return False


token_fields = {
    'id': fields.Integer,
    'token_key': fields.Integer
}