from config import configure
from flask_restful import Api
from views import SendMessageRequest, ResendVerifyEmail, SignUp, VerifyEmail, SignIn
from database import app

api = Api(app)
configure()


# Auth
api.add_resource(SignUp, '/')
api.add_resource(SignIn, '/signin')
api.add_resource(VerifyEmail, '/verify-email')
api.add_resource(ResendVerifyEmail, '/resend-email')

# Messaging
api.add_resource(SendMessageRequest,'/message/request/<int:id>')


if __name__ == '__main__':
    app.run(debug=True)
