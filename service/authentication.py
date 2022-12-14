from models.token import ExpiringToken


def token_to_userprofile(request):
    """
    Function for simplifying token to user_profile association.
    Assigns UserProfile object associated with authenticated Token. Gets token from headers.
    """

    try:
        tok = request.headers.get('Authorization').split()
        cur_token = ExpiringToken.query.filter(ExpiringToken.token_key == tok[1]).first()
        has_expired = cur_token.expired()
        if not has_expired:
            return cur_token.user
        else:
            return
    except ValueError as ve:
        raise ValueError from ve
