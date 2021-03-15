from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()
default_img = 'https://www.kindpng.com/picc/m/24-248253_user-profile-default-image-png-clipart-png-download.png'

def connect_db(app):

    db.app = app
    db.init_app(app)



class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    image_url = db.Column(
        db.Text,
        default=default_img
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    birthday = db.Column(
        db.Text,
        nullable = False
    )

    fav = db.Column(
        db.Text,
        
    )
    favs = db.relationship('Favorite' , backref = 'users')

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"
        
    @classmethod
    def signUp(cls ,username, email, password, image_url , birthday):
        hashed = bcrypt.generate_password_hash(password).decode('UTF-8')
        user = User(username=username,
            email=email,
            password=hashed,
            image_url=image_url or None,
            birthday = birthday)

        db.session.add(user)
        return user


    @classmethod
    def auth(cls , username , password):
        user = User.query.filter_by(username = username).first()
        if user:
            check = bcrypt.check_password_hash(user.password , password)
            if check:
                return user
        return False

class Favorite(db.Model):
    __tablename__ = 'user_fav'

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True,
    )

    fav_cocktail_id = db.Column(
        db.Integer,
        primary_key=True
    )
    fav_URL = db.Column(
        db.Text
    )
    fav_name = db.Column(
        db.Text
    )