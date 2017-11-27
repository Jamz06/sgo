from werkzeug.security import check_password_hash, generate_password_hash

from app import db


ROLE_USER = 0
ROLE_ADMIN = 1

# ToDO: Присвоить связи таблицам
class Users(db.Model):
    '''
        Описание таблицы пользователей
    '''
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(45), index = True, unique = True)
    password = db.Column(db.String(256), index = True, unique = True)
    organization = db.Column(db.String(90), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    # Отношение пользователя к спискам оповещений
    # lists = db.relationship('Lists', backref = 'user', lazy = 'dynamic')

    def __init__(self, login, password, organization, role):
        self.login = login
        self.password =password
        self.organization = organization
        self.role = role

    def __repr__(self):
        return '<User %r>' % (self.login)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):

        return str(self.id)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

class Numbers(db.Model):
    '''
        Описание таблицы номеров
    '''
    id = db.Column(db.Integer, primary_key = True)
    # user = db.Column(db.Integer, index = True)
    user = db.Column(db.Integer, db.ForeignKey('users.id'))
    number = db.Column(db.String(11), index = True)
    comment = db.Column(db.String(90), index = True)

    def __init__(self, user, number, comment):
        self.user = user
        self.number = number
        self.comment = comment

class Lists(db.Model):
    '''
        Описание таблицы списков
    '''
    id = db.Column(db.Integer, primary_key = True)
    user = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(45), index = True)

    def __init__(self, name, user):
        self.name = name
        self.user = user

    def __repr__(self):

        return self.name

class Alarms(db.Model):
    '''
        Описание таблицы тревог
    '''
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(45), index = True)
    user = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name, user):
        self.name = name
        self.user = user

class Included_numbers(db.Model):
    '''
        Описание таблицы отношения номеров к спискам
    '''
    id = db.Column(db.Integer, primary_key = True)
    list = db.Column(db.String(45), db.ForeignKey('lists.id'))
    number = db.Column(db.Integer, db.ForeignKey('numbers.id'))

    def __init__(self, list, number):
        self.list = list
        self.number = number

class Included_alarms(db.Model):
    '''
        Описание таблицы отношения номеров к спискам
    '''
    id = db.Column(db.Integer, primary_key = True)
    list = db.Column(db.String(45), db.ForeignKey('lists.id'))
    alarm = db.Column(db.Integer, db.ForeignKey('alarms.id'))

    def __init__(self, list, alarm):
        self.list = list
        self.alarm = alarm

