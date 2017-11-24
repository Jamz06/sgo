from flask.ext.wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(Form):
    '''
    Класс, описывающий форму входа
    '''
    login = StringField('login', validators = [DataRequired()])
    password = PasswordField('password', validators = [DataRequired()])

class AdminForm(Form):
    '''
    Класс описывающий форму администратора, по добавлению юзеров
    '''
    login = StringField('login')
    password = PasswordField('password')
    organization = StringField('organization')
    role = StringField('role')

class CreateForm(Form):
    name = StringField('name', validators = [DataRequired()])


