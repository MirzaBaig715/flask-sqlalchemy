import os
import datetime
import jwt
from werkzeug.exceptions import abort


class JwtAuth:

    @staticmethod
    def encode_auth_token(user):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=365),
                'iat': datetime.datetime.utcnow(),
                'sub': user
            }
            return jwt.encode(payload, os.getenv('SECRET_KEY', 'secret'), algorithm='HS256')
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: string
        """
        try:
            payload = jwt.decode(auth_token, os.getenv('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            abort(403, 'Signature expired. Please log in again.')
        except jwt.InvalidTokenError:
            abort(403, 'Invalid token. Please log in again.')

