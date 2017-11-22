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
    password = db.Column(db.String(45), index = True, unique = True)
    organization = db.Column(db.String(90), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    # Отношение пользователя к спискам оповещений
    lists = db.relationship('Lists', backref = 'user', lazy = 'dynamic')

class Numbers(db.Model):
    '''
        Описание таблицы номеров
    '''
    id = db.Column(db.Integer, primary_key = True)
    # user = db.Column(db.Integer, index = True)
    user = db.Column(db.Integer, db.ForeignKey('users.id'))
    number = db.Column(db.Integer, index = True)


class Lists(db.Model):
    '''
        Описание таблицы списков
    '''
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(45), index = True)

class Included_numbers(db.Model):
    '''
        Описание таблицы отношения номеров к спискам
    '''
    id = db.Column(db.Integer, primary_key = True)
    lists = db.Column(db.String(45), index = True)
    number = db.Column(db.Integer, index = True)

class Alarms(db.Model):
    '''
        Описание таблицы тревог
    '''
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(45), index = True)

class Included_alarms(db.Model):
    '''
        Описание таблицы отношения номеров к спискам
    '''
    id = db.Column(db.Integer, primary_key = True)
    lists = db.Column(db.String(45), index = True)
    alarm = db.Column(db.Integer, index = True)

    def __repr__(self):
        return '<User %r' % (self.login)
