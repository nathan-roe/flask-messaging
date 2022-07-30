from database import db
from models import *

# Configuration function used to update the database. NOTE: Only for local development.
def configure():
    # db.drop_all()
    db.create_all()
