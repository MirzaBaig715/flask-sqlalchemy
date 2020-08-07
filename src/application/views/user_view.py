"""This is where the user blueprints and controllers are"""

from functools import wraps
from flask import request, Blueprint, jsonify
from werkzeug.exceptions import abort
from utils.api.response import CustomResponse
from utils.constants import Constant
from ..services import UserService
from ..authentication import JwtAuth


api = Blueprint('resource', __name__)


def jwt_permission(func):
    """
    Decorator for JWT required for anonymous users for some functions

    :param func:
    :return: check for the token in incoming request header
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_token = request.headers.environ.get('HTTP_AUTHORIZATION', '').split(' ')
        if len(auth_token) < 2:
            abort(403, "Authentication fails")

        JwtAuth.decode_auth_token(auth_token[1])
        return func(*args, **kwargs)
    return wrapper


@api.route('/user/<int:pk>', methods=['GET'])
@jwt_permission
def get_user(pk):
    """
    Get a single user.

    :param: pk
    :return: user object
    """
    user = UserService(user=pk).get_user_by_id()
    return CustomResponse(data=user).response()


@api.route('/user/<int:pk>', methods=['PUT'])
@jwt_permission
def update_user(pk):
    """
    Update a username.

    :param: pk
    :return: success message
    """
    data = request.json
    UserService(user=pk, data=data).update_user()
    return CustomResponse(
        message=Constant.response.OPERATION_SUCCESS.format(object='User', operation='updated')
    ).response()


@api.route('/user/<int:pk>', methods=['DELETE'])
@jwt_permission
def delete_user(pk):
    """
    Delete a user.

    :param: pk
    :return: success message
    """
    UserService(user=pk).delete_user()
    return CustomResponse(
        message=Constant.response.OPERATION_SUCCESS.format(object='User', operation='deleted')
    ).response()


@api.route('/register', methods=['POST'])
def register():
    """
    User data to register on application

    :param: email, username (optional), password
    :return: User object
    """
    # Validate and deserialize input
    json_data = request.get_json()
    if not json_data:
        return CustomResponse(
            message=Constant.response.NO_INPUT_DATA
        ).response()

    user = UserService(data=json_data).create_user()
    return CustomResponse(data=user).response()


@api.route('/login', methods=['POST'])
def login():
    """
    Login in application

    :param: email, password
    :return: user object with token
    """
    # Validate and deserialize input
    json_data = request.get_json()
    if not json_data:
        return CustomResponse(
            message=Constant.response.NO_INPUT_DATA
        ).response()
    user_service = UserService(data=json_data, attr=json_data.get('email'))
    check_password = user_service.pass_verification()

    if check_password:
        user_data = user_service.get_user_by_attr()
        auth_token = JwtAuth.encode_auth_token(user_data.get('id'))
        if auth_token:
            user_data.update({'token': auth_token.decode()})
            return CustomResponse(data=user_data).response()
    return CustomResponse(message=Constant.response.INCORRECT_USER).response()


@api.errorhandler(400)
def resource_bad_request(error_msg):
    """Handle the bad error"""
    return jsonify(error=str(error_msg))


@api.errorhandler(403)
def resource_forbidden_request(error_msg):
    """Handle the forbidden error"""
    return jsonify(error=str(error_msg))


@api.errorhandler(404)
def resource_not_found(error_msg):
    """Handle the not found error"""
    return jsonify(error=str(error_msg))


@api.errorhandler(500)
def internal_server_error(error_msg):
    """Handle the internal server error"""
    return jsonify(error=str(error_msg))
