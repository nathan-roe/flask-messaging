

from models.messagegroup import UserMessageRelationship
from database import db

def send_message_request(cur_user, contact_user):
    message_rel = UserMessageRelationship(cur_user, contact_user)

    db.session.add(message_rel)
    db.session.commit()

    return message_rel