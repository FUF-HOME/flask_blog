#!/usr/bin/env python
# -*-coding:utf-8-*

from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, login_required, logout_user

from app import db
from app.models import User
from . import auth
from .form import LoginForm, RegisterationForm


@auth.route("/login", methods=["GET", "POST"])
def login():
    loginError = None

    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get("next") or url_for("main.index"))
        loginError = "Invalid emial or password"
    return render_template("auth/login.html", form=form, current_user=current_user, loginError=loginError)


@auth.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)

        db.session.add(user)
        db.session.commit()

        # flash("A confirmation email has been sent to your email")
        return redirect(url_for("auth.login"))

    return render_template('auth/register.html', form=form, current_user=current_user)


@auth.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash("You has been logged out.")
    return redirect(url_for("main.index"))
