from flask_restful import fields
from database import db
from service.constants import Constants
from service.customtypes import ChoiceType

class UserMessageRelationship(db.Model):
    """Relates users and keeps track of messages sent."""

    __tablename__ = 'user_message_rel'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    owner = db.relationship('UserProfile', backref=db.backref('owner_message_rel'), foreign_keys=[owner_id])

    contact_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    contact = db.relationship('UserProfile', backref=db.backref('contact_message_rel'), foreign_keys=[contact_id])

    connection_status = db.Column(ChoiceType(Constants.MessageRelConstants))


    def __init__(self, owner, contact, connection_status = Constants.MessageRelConstants.REQUESTED):
        self.owner_id = owner.id
        self.owner = owner
        self.contact_id = contact.id
        self.contact = contact
        self.connection_status = connection_status

    def __repr__(self):
        return f'Owner: {self.owner} | Contact: {self.contact}'


user_message_rel_fields = {
    'id': fields.Integer,
    'owner_id': fields.Integer,
    'contact_id': fields.Integer,
    'connection_status': fields.String
}
