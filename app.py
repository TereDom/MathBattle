from flask import Flask, render_template, url_for, redirect
# from flask_login import LoginManager
from data import db_session

from data.__all_models import *
from data.__all_forms import *


db_session.global_init('db/DataBase.sqlite')
app = Flask(__name__)
# login_manager = LoginManager()
# login_manager.init_app(app)


def main():
    app.run()


# @login_manager.user_loader
# def load_user(user_id):
#     session = db_session.create_session()
#     return session.query(User).get(user_id)


@app.route('/')
@app.route('/index')
@app.route('/main')
def index():
    pass


@app.route('sign_up', methods=['GET', 'POST'])
def sign_up():
    form = RegisterForm()
    param = dict()
    param['form'] = form
    param['title'] = 'Регистрация'
    param['base_style_way'] = url_for('static', filename='css/style.css')
    param['style_way'] = url_for('static', filename='css/sign_up.css')
    param['template_name_or_list'] = 'sign_up.html'
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            param['message'] = "Пароли не совпадают"
            return render_template(**param)
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            param['message'] = "Такой пользователь уже есть"
            return render_template(**param)
        user = User(
            name=form.name.data,
            login=form.login.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template(**param)


# @app.route('/sign_in', methods=['GET', 'POST'])
# def sign_in():
#     pass


if __name__ == '__main__':
    app.register_blueprint(api.blueprint)
    main()
