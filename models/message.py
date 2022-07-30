from flask_restful import fields
from database import db

class Message(db.Model):
    """Message model to keep track of messages sent within a UserMessageRelationship instance."""

    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String(1000))

    message_group_id = db.Column(db.Integer, db.ForeignKey('user_message_rel.id'))
    message_group = db.relationship('UserMessageRelationship', backref=db.backref('messages'))

    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    sender = db.relationship('UserProfile', backref=db.backref('sender_message_rel'), foreign_keys=[sender_id])

    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    receiver = db.relationship('UserProfile', backref=db.backref('receiver_message_rel'), foreign_keys=[receiver_id])

    def __init__(self, message, message_group, sender, receiver):
        self.message = message
        self.message_group = message_group
        self.message_group_id = message_group.id

        self.sender = sender
        self.sender_id = sender.id
        self.receiver = receiver
        self.receiver_id = receiver.id


    def __repr__(self):
        return f'ID: {self.id} | message: {self.message} | message group: {self.message_group}'


message_fields = {
    'id': fields.Integer,
    'message': fields.String,
    'message_group_id': fields.Integer,
    'sender_id': fields.Integer,
    'receiver_id': fields.Integer
}
