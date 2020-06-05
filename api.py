from flask import Flask, Blueprint, jsonify
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)
blueprint = Blueprint('server', __name__,
                      template_folder='templates')


@blueprint.route('/api/tasks')
def get_task(task_id=0):
    # получение задачи
    return jsonify({'id': task_id})



