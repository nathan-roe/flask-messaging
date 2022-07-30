from flask import Response, request
from flask_restful import Resource, marshal_with
from models.userprofile import UserProfile
from models.message import message_fields
from models.messagegroup import user_message_rel_fields
from service.authentication import token_to_userprofile
from controller.messagecontroller import get_all_related_message_groups, retrieve_messages, send_message, \
    send_message_request, update_message_request


class SendMessageRequest(Resource):
    """View used to send a message request to a user based on id."""

    @marshal_with(user_message_rel_fields)
    def post(self, id):
        """
        Sends a message request to a user.
        Expected Post Data: None
        """
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
    """View used to handle accepting a message request based on user id."""

    def post(self, id):
        """
        Accepts a message request based on user id.
        Expected Post Data: None
        """
        try:
            cur_user = token_to_userprofile(request)
            user = UserProfile.query.filter(UserProfile.id == id).first()
            update_message_request(cur_user, user)
            return Response(status=200)
        except ValueError:
            return Response(status=400)


class DeclineMessageRequest(Resource):
    """View used to handle declined a message request based on a user id."""

    def post(self, id):
        """
        Declined a message request based on user id.
        Expected Post Data: None
        """
        try:
            cur_user = token_to_userprofile(request)
            user = UserProfile.query.filter(UserProfile.id == id).first()
            update_message_request(cur_user, user, declined=True)
            return Response(status=200)
        except ValueError:
            return Response(status=400)


class MessageRequests(Resource):
    """View used to handle sending and retrieving messages."""

    @marshal_with(message_fields)
    def get(self, id):
        """
        Returns messages within a UserMessageRelationship based on user id.
        Expected Params: UserProfile ID
        """
        try:
            cur_user = token_to_userprofile(request)
            user = UserProfile.query.filter(UserProfile.id == id).first()
            messages = retrieve_messages(cur_user, user)
            return messages, 200
        except ValueError:
            return Response(status=400)

    @marshal_with(message_fields)
    def post(self, id):
        """
        Sends a message to a specified user based on user id.
        Expected Post Data: {"message": str}
        Expected Params: UserProfile ID
        """
        try:
            request_data = request.get_json()
            message = request_data['message']
            cur_user = token_to_userprofile(request)
            user = UserProfile.query.filter(UserProfile.id == id).first()

            message = send_message(cur_user, user, message)
            return message, 200
        except ValueError:
            return Response(status=400)


class MessageGroups(Resource):
    """View used to handle multiple message groups."""

    @marshal_with(user_message_rel_fields)
    def get(self):
        """
        Returns all related messages for the cur_user.
        Expected Params: None
        """
        try:
            cur_user = token_to_userprofile(request)

            message_rel = get_all_related_message_groups(cur_user)
            return message_rel, 200
        except ValueError:
            return Response(status=400)
