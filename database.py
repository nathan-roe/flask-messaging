import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Environment variable configuration.
from dotenv import load_dotenv

load_dotenv()

# Function used to fetch env variables and handle env not found exceptions.
def get_env(env_variable):
    try:
        return os.environ[env_variable]
    except KeyError as key_error:
        error_msg = f'Set the {env_variable} environment variable.'
        raise KeyError(error_msg) from key_error


# Configuration logic to handle connecting to database.
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'{get_env("ENGINE")}://{get_env("USER")}:'\
    f'{get_env("PASSWORD")}@{get_env("HOST")}:{get_env("PORT")}/{get_env("NAME")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initialize database session.
db = SQLAlchemy(app)
