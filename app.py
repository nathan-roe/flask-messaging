from config import configure
from flask_restful import Api
from views import SendMessageRequest, ResendVerifyEmail, SignUp, \
    VerifyEmail, SignIn, AcceptMessageRequest, DeclineMessageRequest
from database import app
from views.messageviews import MessageRequests


api = Api(app)
configure()


# Auth
api.add_resource(SignUp, '/')
api.add_resource(SignIn, '/signin')
api.add_resource(VerifyEmail, '/verify-email')
api.add_resource(ResendVerifyEmail, '/resend-email')

# Messaging
api.add_resource(SendMessageRequest,'/messages/request/<int:id>')
api.add_resource(AcceptMessageRequest,'/messages/accept/<int:id>')
api.add_resource(DeclineMessageRequest,'/messages/decline/<int:id>')
api.add_resource(MessageRequests,'/messages/<int:id>')


if __name__ == '__main__':
    app.run(debug=True)
