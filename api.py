from flask import Flask
import tasks_resource, users_resource
from flask_restful import Api
import os
from data import db_session


db_session.global_init('db/DataBase.sqlite')
app = Flask(__name__)
api = Api(app)


def main():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


session = db_session.create_session()
api.add_resource(users_resource.UserResource, '/api/users/<user_login>')
api.add_resource(users_resource.UserListResource, '/api/user/')
api.add_resource(tasks_resource.TaskResource, '/api/task/<task_id>')
api.add_resource(tasks_resource.TaskListResource, '/api/tasks/<user_login>')
main()