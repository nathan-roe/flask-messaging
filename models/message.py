from flask_restful import fields
from database import db

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String(1000))

    message_group_id = db.Column(db.Integer, db.ForeignKey('user_message_rel.id'))
    message_group = db.relationship('UserMessageRelationship', backref=db.backref('messages'))

    def __init__(self, message, message_group):
        self.message = message
        self.message_group = message_group
        self.message_group_id = message_group.id

    def __repr__(self):
        return f'ID: {self.id} | message: {self.message} | message group: {self.message_group}'


user_fields = {
    'id': fields.Integer,
    'message': fields.String,
    'message_group_id': fields.Integer
}
