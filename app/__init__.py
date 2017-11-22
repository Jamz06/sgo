from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
app = Flask(__name__)
# Подключить конфиг
app.config.from_object('config')
# Подключить БД
db = SQLAlchemy(app)

from app import views, models


