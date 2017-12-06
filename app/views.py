from flask import render_template, flash, redirect, url_for, session, request, g, send_from_directory, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .forms import LoginForm, AdminForm, CreateForm
from .models import Users, Alarms, Lists, Numbers, Included_numbers
from sqlalchemy import or_, update, delete
from .sms_config import Sms

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
    '''
    Главная страница.
    :return:
    '''

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
            print('Create ALARM')
            alarm = Alarms(form.name.data, user.id)
            db.session.add(alarm)
            db.session.commit()
            flash('Создано новое оповещение ' + form.name.data)
            return redirect(url_for('index'))

        return redirect(url_for('index'))


    return render_template('create.html', form=form, action=action, title='Создать.. ', user=user)

# Маршрут логина
@app.route('/login', methods = ['GET', 'POST'])
def login():
    '''
    Путь для Логина. Рисует форму входа для неавторизованных. остальных возвращает на главную.
    :return:
    '''
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
    '''
    Выход из сессии. Редиректит на главную.
    :return:
    '''
    logout_user()
    return redirect(url_for('index'))

@app.before_request
def before_request():
    '''
    При любом запросе, получаем в глобальную переменную пользователя
    :return:
    '''
    g.user = current_user

@lm.user_loader
def load_user(id):
    '''
    Загрузка параметров пользователя.
    :param id:
    :return:
    '''
    return Users.query.get(int(id))


@app.route('/numbers', methods=['POST', 'GET'])
@login_required
def numbers():
    user = g.user

    return render_template('numbers.html', user = user)


@app.route('/admin', methods= ['GET', 'POST'])
@login_required
def admin():
    '''
    Форма администрирования.
    :return:
    '''
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
                           form = form,
                           user = user
                           )

@app.route('/static/<path:path>')
# Статику отдаем без авторизации
# @login_required
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
        data['addList'] = get_numbers_data(user.id)
        return jsonify(data)

    if data['updateList']:
        print(len(data['updateList']))
        data_line = data['updateList'][0]
        db.session.query(Numbers).filter_by(id=data_line['id']).update({
            'number': data_line['number'],
            'comment': data_line['comment']
        })
        db.session.commit()
        # Numbers.query.filter_by(id=data_line['id']).update({'number': data_line['number']})
        data['updateList'] = get_numbers_data(user.id)
        return jsonify(data)
        #return jsonify(get_numbers_data(user.id))
    else:
        print("Update is empty")


    if data['deleteList']:
        data_line = data['deleteList'][0]
        #number = Numbers.query.filter_by(id=data_line['id'])
        db.session.query(Numbers).filter_by(id=data_line['id']).delete()
        #db.session.delete(number)
        db.session.commit()
        data['deleteList'] = get_numbers_data(user.id)
        return jsonify(data)
        #return jsonify(get_numbers_data(user.id))


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

# @app.route('/modify_list/<list_id>', methods=['POST', 'GET'])
@app.route('/list/<action>/<list_id>', methods=['POST', 'GET'])
@login_required
def modify_list(action, list_id):
    user = g.user
    lists = Lists.query.filter_by(id=list_id).first()

    def delete_list(list_id):
        db.session.query(Included_numbers).filter_by(list=list_id).delete()
        db.session.commit()
        return None

    if action == 'modify':
        if request.method == 'POST':
            data = request.get_json(force=True)

            # дропаем все номера в списке
            delete_list(list_id)
            # Занести обновленный список в БД





            for elem in data['list']:
                print(elem)
                inc_num = Included_numbers(list_id, elem)
                db.session.add(inc_num)
                db.session.commit()

            # Если имя изменилось, то обновить в БД

            if lists.name != data['name']:

                db.session.query(Lists).filter_by(id=list_id).update({
                                                                    'name': data['name']
                                                                   })
                db.session.commit()


            flash("Список сохранен")
            # Надо будет сделать проверку. Если что не так, вернуть другой ответ.
            return json_response(200)
        else:
            # Получить список всех номеров. Кроме тех, что в списке
            numbers = Numbers.query.filter_by(user=user.id)


            # Получить название списка по ID

            # По ID списка, получить ID номеров.
            user_list = db.session.query(Numbers.id, Numbers.number, Numbers.comment).filter(Included_numbers.list == list_id).\
                filter(Numbers.id == Included_numbers.number).all()

            result_numbers = [
                numbers.__dict__ for numbers in numbers.all()
            ]
            i = 0
            # Пробежаться по массиву номеров
            for num in result_numbers:
                # Отсеять номера, которые уже есть в этом списке
                for num_in_list in user_list:
                    # Если номер в списке, то удалить из массива номеров элемент.
                    if num['number'] == num_in_list[1]:

                        result_numbers.remove(num)
                        i -= 1

                i += 1
            # По ID номеров, получить номера в списке.

            return (render_template('list.html',
                                    list_name=lists.name,
                                    numbers=result_numbers,
                                    user_list=user_list,
                                    list_id=list_id,
                                    user=user

                                    )
                    )


    elif action == 'delete':
        delete_list(list_id)
        db.session.query(Lists).filter_by(id=list_id).delete()
        db.session.commit()
        flash('Список  удален')
        return redirect(url_for('index'))


@app.route('/alert_send/<alert_id>', methods=['POST'])
@login_required
def alert_send(alert_id):
    sms = Sms()
    data = request.get_json(force=True)

    # Выбрать параметры тревоги из БД
    alert = Alarms.query.filter_by(id=alert_id).first()
    # alert = db.session.query(Alarms.name).filter(Alarms.id == alert_id)
    #alert_r = [alert for alert in alert.name]
    #alert_r = ''.join(alert_r)
    # alert_r = 'Тревога! Сигнал:' + alert_r
    #alert_r = "Тест"
    # print(alert_r)
    # Для каждого списка, отправить оповещение
    for elem in data['list']:
        user_list = db.session.query(Numbers.number).filter(
            Included_numbers.list == elem). \
            filter(Numbers.id == Included_numbers.number)

        for num in user_list:
            print('Number to alert: ' + str(num))

            sms.send(alert.__repr__(), str(num[0]))
            # Отправить на номер смс!


    return json_response(200)

@app.route('/help')
@login_required
def help():
    user = g.user
    return render_template('help.html', user=user)


@app.route('/alarm/<action>/<id>', methods=['POST'])
@login_required
def alarm(action,id):

    '''
    Функция операции над оповещением.
    :param action: принимает действие: modify или delete
    :return: Возвращает обратно на главную старнницу.
    '''
    user = g.user
    data = request.get_json(force=True)

    if action == 'modify':
        # изменить имя тревоги.
        try:
            db.session.query(Alarms).filter_by(id=id).update({
                'name': data['name']
            })
            db.session.commit()
        except SQLAlchemyError:
            return json_response(501)

        flash('Оповещение  изменено')
        return json_response(200)

    elif action == 'delete':
        # Удалить тревогу.
        try:
            db.session.query(Alarms).filter_by(id=id).delete()
            db.session.commit()
        except SQLAlchemyError:
            return json_response(501)

        flash('Оповещение  удалено')
        return json_response(200)
