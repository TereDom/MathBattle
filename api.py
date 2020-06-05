from flask import Flask, Blueprint, jsonify
from flask_restful import Api, Resource, reqparse
from data import db_session
from data.__all_models import *


db_session.global_init('db/DataBase.sqlite')
app = Flask(__name__)
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
    print(params)
    return jsonify(params)





