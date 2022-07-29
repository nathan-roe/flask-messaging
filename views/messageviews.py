from controller.messagecontroller import send_message_request
from flask import Response, request
from flask_restful import Resource
from models.userprofile import UserProfile
from service.authentication import token_to_userprofile


class SendMessageRequest(Resource):

    def post(self, id):
        try:
            cur_user = token_to_userprofile(request)
            user = UserProfile.query.filter(UserProfile.id == id).first()
            print(cur_user, user)
            send_message_request(cur_user, user)
            return Response(status=200, mimetype='application/json')
        except ValueError:
            return Response(status=400, mimetype='application/json')
