from flask_admin import Admin, expose, AdminIndexView
from flask_admin.contrib import fileadmin
from flask_admin.contrib.sqlamodel import ModelView

from data.__all_models import *

from app import current_user, redirect


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if current_user:
            if current_user.status == 'developer':
                return super(MyAdminIndexView, self).index()
            else:
                return redirect('/')
        else:
            return redirect('/sign_in')


class MyUserAdmin(ModelView):
    def __init__(self, session):
        self.column_list = ['id', 'name', 'login', 'status', 'points']
        self.can_view_details = True
        super().__init__(User, session)

    def _handle_view(self, name, **kwargs):
        if current_user:
            if not current_user.status == 'developer':
                return redirect('/')
        else:
            return redirect('/sign_in')


class MyTaskAdmin(ModelView):
    def __init__(self, session):
        self.column_list = ['id', 'name', 'content', 'answer', 'user_id']
        self.can_view_details = True
        super().__init__(Task, session)

    def _handle_view(self, name, **kwargs):
        if current_user:
            if not current_user.status == 'developer':
                return redirect('/')
        else:
            return redirect('/sign_in')


class MyAnswerAdmin(ModelView):
    def __init__(self, session):
        self.column_list = ['id', 'content', 'user_id', 'task_id']
        self.can_view_details = True
        super().__init__(Answer, session)

    def _handle_view(self, name, **kwargs):
        if current_user:
            if not current_user.status == 'developer':
                return redirect('/')
        else:
            return redirect('/sign_in')


class MyForumTaskAdmin(ModelView):
    def __init__(self, session):
        self.column_list = ['id', 'str_id', 'title', 'content', 'short_description', 'views', 'answers', 'datetime',
                            'user_id']
        self.can_view_details = True
        super().__init__(ForumTask, session)

    def _handle_view(self, name, **kwargs):
        if current_user:
            if not current_user.status == 'developer':
                return redirect('/')
        else:
            return redirect('/sign_in')


class MyForumAnswerAdmin(ModelView):
    def __init__(self, session):
        self.column_list = ['id', 'content', 'user_id', 'task_id', 'datetime']
        self.can_view_details = True
        super().__init__(ForumAnswer, session)

    def _handle_view(self, name, **kwargs):
        if current_user:
            if not current_user.status == 'developer':
                return redirect('/')
        else:
            return redirect('/sign_in')
