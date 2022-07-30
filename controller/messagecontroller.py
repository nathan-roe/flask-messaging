from models.message import Message
from models.messagegroup import UserMessageRelationship
from database import db
from service.constants import Constants


def send_message_request(cur_user, contact_user):
    cur_message_rels = get_related_message_group(cur_user, contact_user)

    if cur_message_rels.count() > 0:
        raise ValueError("A message request has already been sent.")

    message_rel = UserMessageRelationship(cur_user, contact_user)

    db.session.add(message_rel)
    db.session.commit()

    return message_rel


def update_message_request(cur_user, owner, declined = False):
    message_rel = UserMessageRelationship.query.filter(
        (UserMessageRelationship.owner == owner)
        & (UserMessageRelationship.contact == cur_user)
    ).first()

    status = Constants.MessageRelConstants.DECLINED \
        if declined else Constants.MessageRelConstants.CONNECTED
    
    message_rel.status = status

    db.session.add(message_rel)
    db.session.commit()

    return message_rel


def send_message(cur_user, receiver, message):
    message_rel = get_related_message_group(cur_user, receiver).first()

    message = Message(
        message=message, 
        message_group=message_rel,
        sender=cur_user,
        receiver=receiver
    )

    db.session.add(message)
    db.session.commit()

    return message


def retrieve_messages(cur_user, receiver):
    message_rel = get_related_message_group(cur_user, receiver).first()
    messages = Message.query.filter(Message.message_group == message_rel).all()

    return messages


def get_related_message_group(cur_user, contact):
    message_rels = UserMessageRelationship.query.filter(
        ((UserMessageRelationship.owner == contact) & (UserMessageRelationship.contact == cur_user))
        | ((UserMessageRelationship.owner == cur_user) & (UserMessageRelationship.contact == contact))
    )

    return message_rels