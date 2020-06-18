from flask import Flask, Blueprint, jsonify
from flask_restful import Api
from data import db_session
from data.__all_models import *


db_session.global_init('db/DataBase.sqlite')
app = Flask(__name__)
api = Api(app)
blueprint = Blueprint('api', __name__,
                      template_folder='templates')


@blueprint.route('/api/get_task/<int:task_id>', methods=['GET'])
def get_task(task_id):
    session = db_session.create_session()
    task = session.query(Task).filter(Task.id == task_id).first()

    params = dict()
    params['id'] = task_id
    params['name'] = task.name
    params['user_id'] = task.user_id
    params['content'] = task.content
    params['answer'] = task.answer
    return jsonify(params)


@blueprint.route('/api/post_task', methods=['POST'])
def post_task():
    # Функцию post будем дорабатывать когда, когда уже напишем клиентскую часть
    # Мы подставили конкретные данные для отладки
    session = db_session.create_session()
    last_task = session.query(Task).filter(Task.id).all()[-1]

    task = Task(
        id=last_task.id + 1,
        name='Сложная задачка',
        user_id=1,
        content='Сколько будет 2 + 2 * 2',
        answer='8')

    session.add(task)
    session.commit()


@blueprint.route('/api/get_count_of_task', methods=['GET'])
def get_count():
    session = db_session.create_session()
    count = session.query(Task).count()
    return jsonify(count)


@blueprint.route('/api/change_count_of_decided_tasks/<int:user_id>/<int:task_id>', methods=['PUT'])
def put_decided(user_id, task_id):
    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).first()
    print(user.nickname)
    user.decided_tasks = str(user.decided_tasks) + '%' + str(task_id)
    session.commit()
    return ''


@blueprint.route('/api/user_information/<int:user_id>', methods=['GET'])
def get_user_information(user_id):
    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).first()
    params = dict()
    params['id'] = user.id
    params['name'] = user.nickname
    params['status'] = user.status
    params['decided_tasks'] = user.decided_tasks
    params['login'] = user.login
    return jsonify(params)
