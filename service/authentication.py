from models.token import ExpiringToken


def token_to_userprofile(request):
    """
    Function for simplifying token to user_profile association
    """
    # Assigning UserProfile object associated with authenticated Token
    # get token straight from headers
    try:
        print(request.headers)
        tok = request.headers.get('Authorization').split()
        cur_token = ExpiringToken.query.filter(ExpiringToken.token_key == tok[1]).first()
        has_expired = cur_token.expired()
        if not has_expired:
            return cur_token.user
        else:
            return
    except Exception as e:
        print(e)
        return
