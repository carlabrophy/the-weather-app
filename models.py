from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User table"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(12), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    weather = db.relationship('Weather', backref='user')


    @classmethod
    def register(cls, username, pwd):
        """register with hashed password and return user"""

        hashed = bcrypt.generate_password_hash(pwd)

        #turns bytestering into normal (unicode utf8 pwd)
        hashed_utf = hashed.decode("utf8")

        #return the instance of user with username and hashed password
        return cls(username=username, password=hashed_utf)


    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exist $password is correct.
        Return user if valid; else, return False"""

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False


    




class Weather(db.Model):
    """Weather table"""
    __tablename__ = 'weathers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Text, nullable=False)
    location = db.Column(db.Text, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    created = created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


   