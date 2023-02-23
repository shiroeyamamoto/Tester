from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_admin import Admin
from flask_babelex import Babel
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)
app.secret_key = '*^!@7489123*!@#!^@$0!(&382168610!&*236'

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/babyshark?charset=utf8mb4" % quote(
    'Admin@123')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

cloudinary.config(cloud_name='djrvkcesw', api_key='731634529784673', api_secret='siW---jWhBMnUHDwX_vJLp3BT9w')


db = SQLAlchemy(app=app)

admin = Admin(app=app, name='QUẢN TRỊ PHÒNG MẠCH', template_mode='bootstrap4')

login = LoginManager(app=app)

babel = Babel(app=app)


@babel.localeselector
def get_locale():
    return 'vi'
