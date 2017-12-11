#!/var/www/sgo/venv/bin/python3
# -*- coding: utf-8 -*-
from flask import Flask
import flask.ext
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import generate_password_hash, check_password_hash
from flask.ext.login import LoginManager

# Для gunicorn
from werkzeug.contrib.fixers import ProxyFix


app = Flask(__name__, static_url_path='')
# Подключить конфиг
app.config.from_object('config')
# Подключить БД
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
# Куда отправлять неавторизованных
lm.login_view = 'login'
# Для gunicorn
app.wsgi_app = ProxyFix(app.wsgi_app)

from app import views, models


