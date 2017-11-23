from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import generate_password_hash, check_password_hash
from flask.ext.login import LoginManager

app = Flask(__name__)
# Подключить конфиг
app.config.from_object('config')
# Подключить БД
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
# Куда отправлять неавторизованных
lm.login_view = 'login'


from app import views, models


