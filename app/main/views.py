#!/usr/bin/env python
# -*-coding:utf-8-*-
from flask import render_template
from flask import request, current_app, redirect, g, abort, flash
from flask_login import current_user

from app.models import db, User, Post
from . import main
from .form import PostForm, EditProfileAdminForm


@main.before_request
def before_request():
    g.user = current_user


@main.route("/", methods=["GET", "POST"])
def index():
    form = PostForm()
    page = request.args.get('page', 1, type=int)
    show_followed = False
    show_yours = False

    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
        show_yours = bool(request.cookies.get('show_yours', ''))
    if show_followed:
        query = current_user.followed_posts
    elif show_yours:
        query = Post.query.filter_by(author=current_user)
    else:
        query = Post.query
    pagination = query.order_by(Post.timestamp.desc()).paginate(page,
                                                                per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                                                error_out=False)
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts,user=current_user)


@main.route("/user/<username>", methods=["GET", "POST"])
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    page = request.args.get("page", 1, type=int)
    pagination = user.posts.order_by(Post.publish_date.desc()).paginate(page, per_page=current_app.config[
        'FLASKY_POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    return render_template("user.html", user=user, posts=posts, pagination=pagination)


@main.route('/editProfile/<username>', methods=['GET', 'POST'])
def edit_profile(username):
    user = User.query.filter_by(username=username).first()

    form = EditProfileAdminForm(user=user)

    if form.validate_on_submit():
        _username = form.username.data,
        if _username is None and User.query.filter_by(username=_username).first():
            flash('用户名错误')
        else:
            user = User(username=_username)
            db.session.add(user)
            db.session.commit()
            redirect('main.index')
    return render_template('editProfile.html', form=form)
