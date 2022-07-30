from flask import Response, request
from flask_restful import Resource, marshal_with
from models.userprofile import UserProfile
from models.message import message_fields
from service.authentication import token_to_userprofile
from controller.messagecontroller import retrieve_messages, send_message, \
    send_message_request, update_message_request


class SendMessageRequest(Resource):

    def post(self, id):
        try:
            cur_user = token_to_userprofile(request)
            user = UserProfile.query.filter(UserProfile.id == id).first()

            if user.id == cur_user.id:
                raise ValueError

            message_rel = send_message_request(cur_user, user)
            return message_rel, 201
        except ValueError:
            return Response(status=400)


class AcceptMessageRequest(Resource):

    def post(self, id):
        try:
            cur_user = token_to_userprofile(request)
            user = UserProfile.query.filter(UserProfile.id == id).first()
            update_message_request(cur_user, user)
            return Response(status=200)
        except ValueError:
            return Response(status=400)


class DeclineMessageRequest(Resource):

    def post(self, id):
        try:
            cur_user = token_to_userprofile(request)
            user = UserProfile.query.filter(UserProfile.id == id).first()
            update_message_request(cur_user, user, declined=True)
            return Response(status=200)
        except ValueError:
            return Response(status=400)


class MessageRequests(Resource):

    @marshal_with(message_fields)
    def get(self, id):
        try:
            cur_user = token_to_userprofile(request)
            user = UserProfile.query.filter(UserProfile.id == id).first()
            messages = retrieve_messages(cur_user, user)
            return messages, 200
        except ValueError:
            return Response(status=400)

    def post(self, id):
        try:
            request_data = request.get_json()
            message = request_data['message']
            cur_user = token_to_userprofile(request)
            user = UserProfile.query.filter(UserProfile.id == id).first()

            send_message(cur_user, user, message)
            return Response(status=200)
        except ValueError:
            return Response(status=400)
