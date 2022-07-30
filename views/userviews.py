from datetime import datetime, timedelta
from flask import request, Response
from flask_restful import Resource, marshal_with
from controller.authcontroller import create_token, mock_email_token, update_access_token, verify_email
from controller.usercontroller import create_user, user_parser
from models.logs import AccessLog
from models.token import ExpiringToken
from models.userprofile import UserProfile, user_fields
from service.constants import Constants


class SignUp(Resource):
    """View used to handle sign up."""

    @marshal_with(user_fields)
    def post(self):
        """
        Creates a user based on post data and sends a verification email.
        Expected Post Data:
        {
            "name_first": str,
            "name_last": str,
            "email": str,
            "password": str
        }
        """
        try:
            args = user_parser.parse_args()
            user = create_user(args.name_first, args.name_last, args.email, args.password)
            token = create_token(user)
            mock_email_token(token)
            return user, 200
        except ValueError:
            return Response(status=400)


class VerifyEmail(Resource):
    """View used to handle email verification as a part of the sign up process."""
    def post(self):
        """
        Verifies a user account based on token.
        Expected Post Data:
        {
            "token": str
        }
        """
        try:
            request_data = request.get_json()
            token = request_data['token']

            verify_email(token)

            return Response(status=200)
        except PermissionError:
            data = {'message': 'This token has expired. Please resend the verification email'}
            return data, 401
        except ValueError:
            return Response(status=400)


class ResendVerifyEmail(Resource):
    """View used to resend a verification email as a part of the sign up process."""

    def post(self):
        """
        Resended a verification email to the cur_user based on email.
        Expected Post Data:
        {
            "email": str
        }
        """
        try:
            request_data = request.get_json()
            email = request_data['email']
            user = UserProfile.query.filter(UserProfile.email == email).first()
            token = create_token(user, reset=True)
            mock_email_token(token)

            return Response(status=200)
        except ValueError:
            return Response(status=400)


class SignIn(Resource):
    """View used to sign in and create an authorization token."""

    def post(self):
        """
        Signs in the current user provided a valid email and password.
        Expected Post Data:
        {
            "email": str,
            "password": str
        }
        """
        try:
            user_data = request.get_json()

            # Only so many unsuccessful attempts within a given time period
            seconds_ago = datetime.utcnow() - timedelta(seconds=Constants.TokenConstants.LOGIN_SECONDS)

            if AccessLog.query.filter(
                (AccessLog.date_time >= seconds_ago) & (AccessLog.attempt_successful is False)
            ).count() > Constants.TokenConstants.LOGIN_REQUESTS_ALLOWED:
                return Response(status=429)
            
            access_log = AccessLog(attempt_user=user_data["email"])

            # Checks to ensure user has not been soft deleted, incoming data valid
            if UserProfile.query.filter(
                UserProfile.email == user_data['email'],
                UserProfile.email_verified == True
            ).first() is not None:
                
                cur_user = UserProfile.query.filter(UserProfile.email == user_data['email']).first()

                if cur_user and not cur_user.verified_password(user_data['password']):
                    raise ValueError("Incorrect username or password.")

                prev_token = ExpiringToken.query.filter(ExpiringToken.user == cur_user).first()

                token = update_access_token(cur_user, prev_token, access_log)

                return {'token': token.token_key}, 200

            # TODO: Uncomment code and add expiration logic
            # thirty_minutes_ago = timezone.now() - datetime.timedelta(minutes=30)
            # if AccessLog.query.filter(
            #     AccessLog.date_time >= thirty_minutes_ago and AccessLog.attempt_successful is False).count() \
            #         >= Constants.TokenConstants.LOGIN_MAX_FAILED and \
            #     AccessLog.query.filter(
            #         AccessLog.date_time >= thirty_minutes_ago and AccessLog.attempt_successful is False
            #     ).count() == 0:
            #     try:
            #         user: UserProfile = UserProfile.query.filter(UserProfile.email == user_data['email']).first()
            #         user.is_active = False
            #         db.session.add(user)
            #     except:
            #         pass

            # If user email is not verified
            return Response(status=401)
        except ValueError:
            return Response(status=400)
