from flask import render_template, flash, redirect, url_for, session, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db
from .forms import LoginForm, AdminForm
from .models import Users

@app.route('/')
@app.route('/index', methods=['GET'])
@login_required
def index():
    user = { 'nickname': 'Lihoded' }

    return render_template('index.html',
                           title = 'Home',
                           user = user
                           )


# Маршрут логина
@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(login=form.login.data).first()

        if user is not  None and user.check_password(form.password.data):
            username = {'nickname': form.login.data}
            # flash('login ="' + form.login.data + '", password="' + str(form.password.data))

            return redirect(url_for('index'))

    return render_template('login.html',
        title = 'Войти',
        form = form,
    )

@app.route('/admin', methods= ['GET', 'POST'])
def admin():
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