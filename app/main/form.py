#!/usr/bin/env python
# -*-coding:utf-8-*-


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length, Regexp, ValidationError

from ..models import Role, User


class PostForm(FlaskForm):
    title = StringField(validators=[DataRequired(), Length(1, 64)])
    body = TextAreaField(validators=[DataRequired()], render_kw={"placeholder": "Loading..."})
    submit = SubmitField("Submit")


class NameForm(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired(), Email()],
                       render_kw={"placeholder": "Enter User Name"})
    submit = SubmitField("Submit")


class EditProfileForm(FlaskForm):
    location = StringField("Location", render_kw={"placeholder": "Location"})
    about_me = TextAreaField("About me", render_kw={"placeholder": "Introduce yourself"})
    submit = SubmitField("Save Changes")


class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              'Usernames must have only letters, '
                                              'numbers, dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
