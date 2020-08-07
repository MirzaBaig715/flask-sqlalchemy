"""This is the where the user related logic is written"""

from werkzeug.exceptions import abort

from utils.modules.utils_methods import UtilsMethods
from utils.constants import Constant
from ..models.database import db
from ..models.user import UserSchema, User


user_schema = UserSchema()


class UserService:
    """
    For the user operations
    """

    def __init__(self, **kwargs):
        self.user = kwargs.get('user')
        self.data = kwargs.get('data')
        self.attr = kwargs.get('attr')

    def get_user_by_id(self):
        """
        Get user by user id
        :return:
        """
        user = UtilsMethods.get_object_or_raise_404(User, self.user)
        return user_schema.dump(user)

    def get_user_by_attr(self):
        """

        :return: user object
        """
        user = UtilsMethods.get_object_or_raise_404(User, self.attr, filter_by=True)
        return user_schema.dump(user)

    def update_user(self):
        """
        Update username of a user
        :return: user object
        """
        user = UtilsMethods.get_object_or_raise_404(User, self.user)
        user.username = self.data.get('username', user.username)
        db.session.commit()
        return user_schema.dump(user)

    def delete_user(self):
        """
        User will be search and deleted here
        :return: none
        """
        user = UtilsMethods.get_object_or_raise_404(User, self.user)
        db.session.delete(user)
        db.session.commit()

    def create_user(self):
        """
        User creation and schema loading will be here
        :return: user object
        """
        self.data = UtilsMethods.load_schema(user_schema, self.data)
        if self.check_user_exists():
            abort(400, description=Constant.response.EMAIL_ALREADY_IN_USE)
        user = User(
            email=self.data.get('email'),
            password=self.data.get('password'),
            username=self.data.get('username')
        )
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user)

    def load_user_data(self):
        """
        Load schema for users
        :return: loaded schema
        """
        return UtilsMethods.load_schema(user_schema, self.data)

    def pass_verification(self):
        """
        Verify password for login
        :return: boolean
        """
        self.data = self.load_user_data()
        user = UtilsMethods.get_object_or_raise_404(User, self.data.get('email'), filter_by=True)
        return User.verify_password(user, self.data.get('password'))

    def check_user_exists(self):
        """
        Filter user by email
        :return: boolean
        """
        return db.session.query(User.id).filter_by(
            email=self.data.get('email')
        ).scalar() is not None
