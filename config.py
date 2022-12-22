import os


class Config:
    DEBUG = True
    SECRET_KEY = "i6xn3PHKsn5vRW3tozEuUj3fVfpB11fP"

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.getcwd(), 'db', 'data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static')
