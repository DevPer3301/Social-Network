from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_restful import Api
from flask_jwt_extended import JWTManager
from uuid import uuid4


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///social_network.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = str(uuid4().hex)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db, render_as_batch=True)
api = Api(app)
jwt = JWTManager(app)

from routes import *
from models import *
from routes_api import *

if __name__ == "__main__":
    app.run(debug=True)