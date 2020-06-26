import tasks_resource, users_resource
from flask_restful import Api
from flask import Flask
from data import db_session

app = Flask(__name__)
api = Api(app)
db_session.global_init('db/DataBase.sqlite')


def main():
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    api.add_resource(users_resource.UserResource, '/api/users/<user_login>')
    api.add_resource(users_resource.UserListResource, '/api/user/')
    api.add_resource(tasks_resource.TaskResource, '/api/task/<task_id>')
    api.add_resource(tasks_resource.TaskListResource, '/api/tasks/<user_login>')
    main()