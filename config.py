from database import db

def configure():
    from models import UserProfile, Token, ExpiringToken
    db.drop_all()
    db.create_all()