import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from config import Config

if not os.path.exists(os.path.join(Config.UPLOAD_FOLDER, 'photos')):
    os.makedirs(os.path.join(Config.UPLOAD_FOLDER, 'photos'))

if not os.path.exists(os.path.join(os.getcwd(), 'db')):
    os.makedirs(os.path.join(os.getcwd(), 'db'))
    open(Config.SQLALCHEMY_DATABASE_URI, 'wt').close()

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
login_manager = LoginManager(app)

import views

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
