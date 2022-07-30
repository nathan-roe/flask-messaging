from datetime import timedelta

class Constants:
    """
    General constants used for models:
    UserMessageRelationship
    """

    class MessageRelConstants:
        REQUESTED = 1
        CONNECTED = 2
        DECLINED = 3

    class TokenConstants:
        TOKEN_EXPIRE_TIME = timedelta(minutes=15)
        LOGIN_SECONDS = 30
        LOGIN_MAX_FAILED = 5
        LOGIN_REQUESTS_ALLOWED = 3

    class AccessLogActionTypes:
        LOGIN = 1
        LOGOUT = 2