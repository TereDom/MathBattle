from flask import Flask, render_template, url_for, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data import db_session

from data.__all_models import *
from data.__all_forms import *

from api import *
import api


db_session.global_init('db/DataBase.sqlite')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'elttaBhtaM'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    app.run(host='127.0.0.1', port=5000)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/')
@app.route('/index')
@app.route('/main')
def index():
    form = SearchForm()
    param = dict()
    param['form'] = form
    param['title'] = 'MathBattle'
    param['base_style_way'] = url_for('static', filename='css/style.css')
    param['style_way'] = url_for('static', filename='css/main.css')
    param['calculate_script_way'] = url_for('static', filename='js/calculate.js')
    param['template_name_or_list'] = 'main.html'
    session = db_session.create_session()
    if form.validate_on_submit():
        param['tasks'] = session.query(ForumTask).filter(form.search_field.data.lower() in ForumTask.name.lower())
        return render_template(**param)
    param['tasks'] = session.query(ForumTask)
    return render_template(**param)


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = RegisterForm()
    param = dict()
    param['form'] = form
    param['title'] = 'Регистрация'
    param['base_style_way'] = url_for('static', filename='css/style.css')
    param['style_way'] = url_for('static', filename='css/sign_up.css')
    param['template_name_or_list'] = 'sign_up.html'
    param['message'] = ''
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            param['message'] = "Пароли не совпадают"
            return render_template(**param)
        session = db_session.create_session()
        if session.query(User).filter(User.login == str(form.login.data)).first():
            param['message'] = "Такой пользователь уже есть"
            return render_template(**param)
        user = User(
            name=form.name.data,
            login=str(form.login.data)
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/sign_in')
    return render_template(**param)


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = LoginForm()
    param = dict()
    param['template_name_or_list'] = 'sign_in.html'
    param['title'] = 'Авторизация'
    param['form'] = form
    param['base_style_way'] = url_for('static', filename='css/style.css')
    param['style_way'] = url_for('static', filename='css/sign_in.css')
    param['message'] = ''
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        param['message'] = "Неправильный логин или пароль"
        return render_template(**param)
    return render_template(**param)


@app.route('/sign_out')
@login_required
def sign_out():
    logout_user()
    return redirect("/")


@app.route('/new_task', methods=['GET', 'POST'])
@login_required
def new_task():
    form = NewTaskForm()
    param = dict()
    param['form'] = form
    param['template_name_or_list'] = 'new_task.html'
    param['title'] = 'Новое обсуждение'
    param['base_style_way'] = url_for('static', filename='css/style.css')
    param['style_way'] = url_for('static', filename='css/new_task.css')
    param['calculate_script_way'] = url_for('static', filename='js/calculate.js')
    if form.validate_on_submit():
        session = db_session.create_session()
        data = dict()
        data['title'] = form.title.data
        data['content'] = form.content.data
        data['short_description'] = (form.short_description.data
                                     if form.short_description.data != '' else form.content.data)
        data['user_id'] = current_user.id
        task = ForumTask(**data)
        session.add(task)
        session.commit()
        print(task.id)
        task.str_id = str(task.id).rjust(4, '0')
        session.commit()
        # return redirect(f'/task{task.id}')
        return redirect('/')
    return render_template(**param)


if __name__ == '__main__':
    app.register_blueprint(api.blueprint)
    main()
