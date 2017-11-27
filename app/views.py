from flask import render_template, flash, redirect, url_for, session, request, g, send_from_directory, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .forms import LoginForm, AdminForm, CreateForm
from .models import Users, Alarms, Lists, Numbers, Included_numbers
from sqlalchemy import or_, update, delete

from flask_json import FlaskJSON, JsonError, json_response, as_json
FlaskJSON(app)

def get_numbers_data(user_id):
    '''
    Функция загрузки номеров пользователя
    :param user_id:  ИД пользователя
    :return: массив с номерами пользователя
    '''
    numbers = Numbers.query.filter_by(user=user_id)

    # print(json_numbers[0])
    json_numbers = []
    for number in numbers:
        print(number.number)
        json_numbers.append(
            {
                'id': number.id,
                'number': number.number,
                'comment': number.comment
            }
        )
    return json_numbers



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


@app.route('/numbers_batch', methods=['POST'])
@login_required
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
        print(data['addList'][0]['number'])
        data_line = data['addList'][0]
        number = Numbers(user.id, data_line['number'], data_line['comment'])
        db.session.add(number)
        db.session.commit()
        return jsonify(get_numbers_data(user.id))

    if data['updateList']:
        print(len(data['updateList']))
        data_line = data['updateList'][0]
        db.session.query(Numbers).filter_by(id=data_line['id']).update({
            'number': data_line['number'],
            'comment': data_line['comment']
        })
        db.session.commit()
        # Numbers.query.filter_by(id=data_line['id']).update({'number': data_line['number']})
        return jsonify(get_numbers_data(user.id))
    else:
        print("Update is empty")


    if data['deleteList']:
        data_line = data['deleteList'][0]
        #number = Numbers.query.filter_by(id=data_line['id'])
        db.session.query(Numbers).filter_by(id=data_line['id']).delete()
        #db.session.delete(number)
        db.session.commit()
        return jsonify(get_numbers_data(user.id))


    return  json_response(200)


@app.route('/numbers_data', methods=['GET'])
@login_required
def numbers_data():
    '''
    Функция-маршрут для отдачи номеров пользователя.
    :return: JSON с номерами пользователя
    '''

    user = g.user
    json_numbers = get_numbers_data(user.id)

    return jsonify(data=json_numbers)

@app.route('/modify_list/<list_id>', methods=['POST', 'GET'])
@login_required
def modify_list(list_id):
    user = g.user

    if request.method == 'POST':
        data = request.get_json(force=True)

        # дропаем все номера в списке
        db.session.query(Included_numbers).filter_by(list=list_id).delete()
        db.session.commit()
        # Занести обновленный список в БД
        for elem in data['list']:
            print(elem)
            inc_num = Included_numbers(list_id, elem)
            db.session.add(inc_num)
            db.session.commit()

        flash("Список сохранен")
        # Надо будет сделать проверку. Если что не так, вернуть другой ответ.
        return json_response(200)
    else:
        # Получить список всех номеров.
        numbers = Numbers.query.filter_by(user=user.id)

        # Получить название списка по ID
        lists = Lists.query.filter_by(id=list_id).first()
        # По ID списка, получить ID номеров.
        user_list = []
        # По ID номеров, получить номера в списке.

        return (render_template('list.html',
                                list_name=lists.name,
                                numbers=numbers,
                                user_list=user_list,
                                list_id=list_id

                                )
                )



