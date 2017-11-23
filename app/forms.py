from flask.ext.wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(Form):
    login = StringField('login', validators = [DataRequired()])
    password = PasswordField('password', validators = [DataRequired()])

class AdminForm(Form):
    login = StringField('login')
    password = PasswordField('password')
    organization = StringField('organization')
    role = StringField('role')


