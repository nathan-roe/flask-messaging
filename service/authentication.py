from models.token import ExpiringToken


def token_to_userprofile(request):
    """
    Function for simplifying token to user_profile association
    """
    # Assigning UserProfile object associated with authenticated Token
    # get token straight from headers
    try:
        print(request.META)
        tok = request.META.get('HTTP_AUTHORIZATION').split()
        cur_token = ExpiringToken.filter(token_key=tok[1])
        has_expired = ExpiringToken.expired(cur_token)
        if not has_expired:
            return cur_token.user
        else:
            return
    except:
        return
