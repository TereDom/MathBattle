from flask import Blueprint, jsonify
from flask_restful import Api, Resource, reqparse
from data import db_session
from data.__all_models import *
from app import app


db_session.global_init('db/DataBase.sqlite')
api = Api(app)
blueprint = Blueprint('api', __name__,
                      template_folder='templates')


@blueprint.route('/api/get_task')
def get_task(task_id=1):
    session = db_session.create_session()
    task = session.query(Task).filter(Task.id == task_id).first()

    params = dict()
    params['id'] = task_id
    params['name'] = task.name
    params['user_id'] = task.user_id
    params['content'] = task.content
    params['answer'] = task.answer
    return jsonify(params)


@blueprint.route('/api/post_task')
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
