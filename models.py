from flask_login import UserMixin
from sqlalchemy.orm import relationship

from app import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    login = db.Column(db.String, nullable=True, unique=True)
    email = db.Column(db.String, nullable=True, unique=True)
    password = db.Column(db.String, nullable=True)
    is_admin = db.Column(db.Boolean, nullable=True, default=False)

    @staticmethod
    def add(login, email, password):
        user = User()
        user.login = login
        user.email = email
        user.password = password

        db.session.add(user)
        db.session.commit()


class Good(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    manufacturer = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    photo = db.Column(db.String, nullable=False)

    likes = relationship("Like")

    @staticmethod
    def add(name, description, category, manufacturer, price, photo):
        good = Good()
        good.name = name
        good.description = description
        good.category = category
        good.manufacturer = manufacturer
        good.price = price
        good.photo = photo

        db.session.add(good)
        db.session.commit()


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    good_id = db.Column(db.Integer(), db.ForeignKey('good.id'))
    score = db.Column(db.Integer())

    @staticmethod
    def add(user_id, good_id, score):
        like = Like()
        like.user_id = user_id
        like.good_id = good_id
        like.score = score

        db.session.add(like)
        db.session.commit()


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    good_id = db.Column(db.Integer(), db.ForeignKey('good.id'))
    comment = db.Column(db.String(), nullable=False)
    user = db.relationship('User', backref='User')

    @staticmethod
    def add(user_id, good_id, comment):
        comment_model = Comment()
        comment_model.user_id = user_id
        comment_model.good_id = good_id
        comment_model.comment = comment

        db.session.add(comment_model)
        db.session.commit()
