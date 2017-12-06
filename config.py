import os
# Базовый путь проекта
basedir = os.path.abspath(os.path.dirname(__file__))
# настройки для БД
# Это путь к файлу с  базой данных
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://sgo_man:12345678@localhost/sgo-lab?charset=utf8mb4'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# Активирует предотвращение поддельных межсайтовых запросов.
CSRF_ENABLED = True
# Используется для создания криптографического токена, который используется при валидации формы
SECRET_KEY = 'mxP7U87p6htYeCgJNR9k'



