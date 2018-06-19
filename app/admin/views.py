#!/usr/bin/env python
# -*-coding:utf-8-*-
from flask import request, abort, redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from app import admin
from app.models import User, Post, db
from .form import CKTextAreaField


class MyModelView(ModelView):
    form_overrides = dict(text=CKTextAreaField)
    column_searchable_list = ('body', 'title')

    # Using Add Filter box


    column_filters = ('timestamp',)
    create_template = 'admin/edit_post.html'
    edit_template = 'admin/edit_post.html'

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.role_id:
            return True
        return False


def _handle_view(self, name, **kwargs):
    """
    Override builtin _handle_view in order to redirect users when a view is not accessible.
    """
    if not self.is_accessible():
        if current_user.is_authenticated:
            # permission denied
            abort(403)
        else:
            # login
            return redirect(url_for('auth.login', next=request.url))


admin.add_view(ModelView(User, db.session, name=u'用户管理'))
admin.add_view(MyModelView(Post, db.session, name=u'文章管理'))
