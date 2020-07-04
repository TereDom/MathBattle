from flask import Flask, render_template, url_for, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

import os
import os.path as op

from data import db_session

from data.__all_models import *
from data.__all_forms import *

from admin import *

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


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/main', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    param = dict()
    param['form'] = form
    param['title'] = 'MathBattle'
    param['base_style_way'] = url_for('static', filename='css/style.css')
    param['style_way'] = url_for('static', filename='css/main.css')
    param['calculate_script_way'] = url_for('static', filename='js/calculate.js')
    param['template_name_or_list'] = 'main.html'
    param['search'] = True
    param['new_task'] = True
    param['calculate'] = True
    param['bootstrap'] = False
    session = db_session.create_session()
    if form.validate_on_submit():
        tasks = session.query(ForumTask).all()
        param['tasks'] = list()
        for task in tasks:
            task.answers = len(list(session.query(ForumAnswer).filter(ForumAnswer.task_id == task.id)))
            session.commit()
            if form.search_field.data.lower() in task.title.lower():
                param['tasks'] .append(task)
        print(param['tasks'])
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
    param['search'] = False
    param['new_task'] = False
    param['calculate'] = False
    param['bootstrap'] = True
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
    param['search'] = False
    param['new_task'] = False
    param['calculate'] = False
    param['bootstrap'] = True
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
    param['search'] = False
    param['new_task'] = False
    param['calculate'] = True
    param['bootstrap'] = True
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
        task.str_id = str(task.id).rjust(4, '0')
        session.commit()
        # return redirect(f'/task/{task.id}')
        return redirect('/')
    return render_template(**param)


@app.route('/task/<task_id>', methods=['GET', 'POST'])
def task(task_id):
    form = NewAnswerForm()
    session = db_session.create_session()
    task = session.query(ForumTask).filter(ForumTask.id == task_id).first()
    if not task:
        return redirect('/')
    param = dict()
    param['form'] = form
    param['title'] = task.title
    param['base_style_way'] = url_for('static', filename='css/style.css')
    param['style_way'] = url_for('static', filename='css/task.css')
    param['calculate_script_way'] = url_for('static', filename='js/calculate.js')
    param['template_name_or_list'] = 'task.html'
    param['search'] = False
    param['new_task'] = True
    param['calculate'] = True
    param['bootstrap'] = False
    param['task'] = task
    param['answers'] = session.query(ForumAnswer).filter(ForumAnswer.task_id == task_id)
    task.answers = len(list(param['answers']))
    task.views += 1
    session.commit()
    if form.validate_on_submit():
        data = dict()
        data['user_id'] = current_user.id
        data['content'] = form.answer_field.data
        data['task_id'] = task_id
        answer = ForumAnswer(**data)
        session.add(answer)
        session.commit()
        return redirect(f'/task/{task_id}#{answer.id}')
    return render_template(**param)


@app.route('/task/<task_id>/edit_answer/<answer_id>', methods=['POST', 'GET'])
@login_required
def edit(task_id, answer_id):
    form = NewAnswerForm()
    session = db_session.create_session()
    task = session.query(ForumTask).filter(ForumTask.id == task_id).first()
    answer = session.query(ForumAnswer).filter(ForumAnswer.id == answer_id).first()
    if answer.user_id != current_user.id or not answer:
        return redirect(f'/task/{task_id}')
    if not task:
        return redirect('/')
    param = dict()
    param['title'] = task.title
    param['base_style_way'] = url_for('static', filename='css/style.css')
    param['style_way'] = url_for('static', filename='css/task.css')
    param['calculate_script_way'] = url_for('static', filename='js/calculate.js')
    param['template_name_or_list'] = 'task.html'
    param['search'] = False
    param['new_task'] = True
    param['calculate'] = True
    param['bootstrap'] = False
    param['task'] = task
    param['answers'] = session.query(ForumAnswer).filter(ForumAnswer.task_id == task_id)
    task.answers = len(list(param['answers']))
    task.views += 1
    session.commit()
    if form.validate_on_submit():
        param['form'] = form
        answer.content = form.answer_field.data
        session.commit()
        return redirect(f'/task/{task_id}#{answer.id}')
    form.answer_field.data = answer.content
    param['form'] = form
    return render_template(**param)


@app.route('/task/<task_id>/delete_answer/<answer_id>', methods=['GET', 'POST'])
def delete(task_id, answer_id):
    session = db_session.create_session()
    answer = session.query(ForumAnswer).filter(ForumAnswer.id == answer_id).first()
    if not answer or (current_user.id != answer.user_id and 'admin' not in current_user.status):
        return redirect(f'/task/{task_id}')
    if not task:
        return redirect('/')
    session.delete(answer)
    session.commit()
    return redirect(f'/task/{task_id}')


if __name__ == '__main__':
    app.register_blueprint(api.blueprint)

    session = db_session.create_session()

    admin = Admin(app, index_view=MyAdminIndexView())

    path = op.join(op.dirname(__file__), '')
    try:
        os.mkdir(path)
    except OSError:
        pass
    admin.add_view(fileadmin.FileAdmin(path, '', name='all'))

    admin.add_view(MyUserAdmin(session))
    admin.add_view(MyTaskAdmin(session))
    admin.add_view(MyAnswerAdmin(session))
    admin.add_view(MyForumTaskAdmin(session))
    admin.add_view(MyForumAnswerAdmin(session))

    main()
