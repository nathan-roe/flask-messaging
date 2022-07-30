from datetime import datetime
from flask_restful import fields
from database import db
from service.constants import Constants
from service.customtypes import ChoiceType

class AccessLog(db.Model):
    """Model used to keep track of attempts to login or logout of an account."""
    
    __tablename__ = 'access_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    attempt_user = db.Column(db.String(128))
    success_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    success_user = db.relationship('UserProfile', backref=db.backref('success_user'), foreign_keys=[success_user_id])
    date_time = db.Column('created_date', db.DateTime, default=datetime.utcnow())
    attempt_successful = db.Column(db.Boolean, default=False)
    device = db.Column(db.String(128), nullable=True)
    browser = db.Column(db.String(128), nullable=True)
    ip = db.Column(db.String(128), nullable=True)

    action_type = db.Column(ChoiceType(Constants.AccessLogActionTypes))
    

    def __init__(self, attempt_user, success = False, action_type = Constants.AccessLogActionTypes.LOGIN):
        self.attempt_user = attempt_user
        self.attempt_successful = success
        self.action_type = action_type


    def __repr__(self):
        return f'attempt_user: {self.attempt_user} | success_user: {self.success_user_id} | successful: {self.attempt_successful}'


access_log_fields = {
    'id': fields.Integer,
    'attempt_user': fields.String,
    'success_user_id': fields.Integer,
    'action_type': fields.Integer
}
