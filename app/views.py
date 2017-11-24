from flask import render_template, flash, redirect, url_for, session, request, g, send_from_directory
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .forms import LoginForm, AdminForm, CreateForm
from .models import Users, Alarms, Lists, Numbers
from sqlalchemy import or_

from flask_json import FlaskJSON, JsonError, json_response, as_json
FlaskJSON(app)

@app.route('/')
@app.route('/index', methods=['GET'])
@login_required
def index():
    # user = { 'nickname': 'Lihoded' }
    user = g.user

    # Передать массив тревог на страницу:
    alarms = Alarms.query.filter(or_(Alarms.user==None, Alarms.user==user.id))
    lists = Lists.query.filter_by(user=user.id)

    return render_template('index.html',
                           title = 'Система голосового оповещения',
                           user = user,
                           alarms = alarms,
                           lists = lists
                           )

@app.route('/create/<string:action>', methods=['POST', 'GET'])
@login_required
def create(action):
    '''
    Маршрут создания тревоги или списка
    :param action: принять действие по созданию списка или тревоги
    :return: Возвращает форму создания
    '''
    form = CreateForm()
    user = g.user

    if form.validate_on_submit():

        if action == 'list':
            list = Lists(form.name.data, user.id)
            db.session.add(list)
            db.session.commit()
            flash('Создан новый список ' + form.name.data )
            return redirect(url_for('index'))
        elif action == 'alarm':
            alarm = Alarms(form.name.data, user.id)
            db.session.add(alarm)
            db.session.commit()
            flash('Создано новое оповещение ' + form.name.data)
            return redirect(url_for('index'))

        return redirect(url_for('index'))


    return render_template('create.html', form=form, action=action, title='Создать.. ')

# Маршрут логина
@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(login=form.login.data).first()

        if user is not  None and user.check_password(form.password.data):
            username = {'nickname': form.login.data}
            # flash('login ="' + form.login.data + '", password="' + str(form.password.data))
            login_user(user)
            if user.role == 1:
                return  redirect(url_for('admin'))
            return redirect(url_for('index'))

    return render_template('login.html',
        title = 'Войти',
        form = form,
    )

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.before_request
def before_request():
    g.user = current_user

@lm.user_loader
def load_user(id):
    return Users.query.get(int(id))


@app.route('/numbers', methods=['POST', 'GET'])
@login_required
def numbers():
    user = g.user

    return render_template('numbers.html')


@app.route('/admin', methods= ['GET', 'POST'])
@login_required
def admin():
    user = g.user
    if user.role != 1:
        return redirect(url_for('index'))
    form = AdminForm()
    if form.validate_on_submit():
        foo = Users.hash_password(form.password.data)
        flash('login ="' + form.login.data + '", password="' + str(foo))
        me = Users(form.login.data, str(foo), form.organization.data, int(form.role.data))
        db.session.add(me)
        db.session.commit()
        return redirect('/admin')

    return render_template('admin.html',
                           form = form
                           )

@app.route('/static/<path:path>')
@login_required
def send_js(path):
    # Отладочный вывод с информацией о запросе файла
    # flash("path is: " + path)
    return send_from_directory('static', path)


@app.route('/numbers_batch', methods=['POST', 'GET'])
# @login_required
def numbers_batch():
    '''
        Принять JSON от таблицы
    :return: Ответить хз чем пока
    '''
    user = g.user

    data = request.get_json(force=True)

    print(dict.keys(data))
    # print(data['addList'])
    if data['addList']:
        print(len(data['addList'][0]))
        print(data['addList'][0]['ik_num'])
        data_line = data['addList'][0]
        number = Numbers(user.id, data_line['ik_num'], data_line['comment'])
        db.session.add(number)
        db.session.commit()

    if data['updateList']:
        print("update len: " + len(data['updateList']))
    else:
        print("Update is empty")


    if data['deleteList']:
        pass


    return  json_response(200)


