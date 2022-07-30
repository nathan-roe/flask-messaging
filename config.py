from database import db
from models import *

def configure():
    # db.drop_all()
    db.create_all()