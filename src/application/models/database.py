"""Initialize all the libraries"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow

# initialize our db
db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
