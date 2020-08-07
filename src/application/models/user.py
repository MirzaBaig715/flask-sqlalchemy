from marshmallow import fields, validate, pre_load
from sqlalchemy.sql import func
from .database import ma, db, bcrypt


class User(db.Model):
    """ Database Model for user management """

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, index=True)
    password = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __init__(self, email=None, password=None, username=None, created_at=None):
        self.email = email
        self.password = User.generate_password(password)
        self.username = username
        self.created_at = created_at

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def verify_password(user, password):
        return bcrypt.check_password_hash(user.password, password)

    @staticmethod
    def generate_password(password):
        return bcrypt.generate_password_hash(password, 10).decode("utf-8", "ignore")


class UserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=False)
    email = fields.String(required=True, validate=validate.Email())
    password = fields.String(required=True, validate=[validate.Length(min=6, max=36)])

    @pre_load
    def process_input(self, data, *args, **kwargs):
        """
        Clean data before loading the schema
        :param data: user data
        :param args:
        :param kwargs:
        :return: cleaned data
        """
        data["email"] = data.get("email", "").lower().strip()
        return data

    class Meta:
        fields = ('id', 'email', 'password', 'username', 'created_at')
