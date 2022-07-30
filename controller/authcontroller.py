from database import db
from models.token import ExpiringToken
from models.userprofile import UserProfile

# Function used to create an expiring token
def create_token(user, reset = False):
    # Remove previous token(s) if reset is True
    if reset:
        ExpiringToken.query.filter(ExpiringToken.user == user).delete()
        db.session.commit()

    token = ExpiringToken(user_id=user.id)
    db.session.add(token)
    db.session.commit()
    return token


# Function used to send an email with a verification token. NOTE: Currently mocked and logged to console.
def mock_email_token(token):
    print(token.token_key)
    return token


# Function used to verify an email based on a verification token.
def verify_email(token):
    cur_user = UserProfile.query.filter(UserProfile.tokens.any(token_key=token)).first()
    
    if not cur_user:
        raise ValueError(f'The UserProfile with the token: {token} doesn\'t exist.')

    token_instance = ExpiringToken.query.filter(ExpiringToken.user == cur_user).first()
    if token_instance.expired():
        db.session.delete(token_instance)
        raise PermissionError(f'The current token has expired.')
    
    cur_user.email_verified = True
    db.session.add(cur_user)
    db.session.delete(token_instance)
    db.session.commit()


# Function used to create a new ExpiringToken as part of the resend verification email process.
def update_access_token(cur_user, token, access_log):
    if token:
        db.session.delete(token)
        
    token = ExpiringToken(cur_user.id)
    db.session.add(token)

    # Log successful login attempt data
    access_log.success_user = cur_user
    access_log.attempt_successful = True
    db.session.add(access_log)

    db.session.commit()
    return token