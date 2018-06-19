#!/usr/bin/env python
# -*-coding:utf-8-*-
from datetime import datetime
from hashlib import md5

import bleach
from flask_login import UserMixin, AnonymousUserMixin
from markdown import markdown
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login_manager


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(255), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    hash_password = db.Column(db.String(255))
    posts = db.relationship('Post', backref='author', lazy='dynamic',
                            cascade='all, delete-orphan')

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.hash_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.hash_password, password)

    def can(self, permission):
        return self.role is not None and permission == permission

    def is_admin(self):
        return self.can(Permission.ADMIN)

    is_authenticated = True
    is_active = True

    is_anonymous = False

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

        if self.role is None:
            if self.username == 'FUF':
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(permissions=0x07).first()

    def avatar(self,size):
        return 'http://www.gravatar.com/avatar/' + md5(self.email.encode('utf-8')).hexdigest() +'?d=mm&s=' + str(size)
class Comment(db.Model):
    """Represents Proected comments."""

    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    text = db.Column(db.Text())
    date = db.Column(db.DateTime())
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Model Comment `{}`>'.format(self.name)


posts_tags = db.Table('posts_tags',
                      db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
                      db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')))


class Post(db.Model, UserMixin):
    """Represents Proected posts."""

    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    html_body = db.Column(db.Text)

    # Establish contact with Comment's ForeignKey: post_id
    @staticmethod
    def on_body_changed(target, value, oldvalue, initiator):
        allow_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                      'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                      'h1', 'h2', 'h3', 'p', 'span', 'code', 'pre',
                      'img', 'hr', 'div']
        allow_attributes = ['src', 'alt', 'href', 'class']
        target.html_body = bleach.linkify(bleach.clean(markdown(value, output_format='html',
                                                                extensions=['markdown.extensions.extra',
                                                                            'markdown.extensions.codehilite']),
                                                       tags=allow_tags, attributes=allow_attributes, strip=True))
    comments = db.relationship(
        'Comment',
        backref='posts',
        lazy='dynamic')
    # many to many: posts <==> tags
    tags = db.relationship(
        'Tag',
        secondary=posts_tags,
        backref=db.backref('posts', lazy='dynamic'))

    # def __init__(self, title,id):
    #     self.id=id
    #     self.title = title

    def __repr__(self):
        return "<Model Post `{}`>".format(self.title)


class Tag(db.Model):
    """Represents Proected tags."""

    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    # def __init__(self, name,id):
    #     self.id=id
    #     self.name = name

    def __repr__(self):
        return '<tag- %s>' % (self.name)


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), unique=True)
    description = db.Column(db.String(255))
    permissions = db.Column(db.Integer)
    default = db.Column(db.Boolean, default=False, index=True)
    users = db.relationship("User", backref="role", lazy="dynamic")

    def __repr__(self):
        return "<Role %r>" % self.name

    @staticmethod
    def insert_roles():
        roles = {
            "User": (Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES, True),
            "Moderator": (
                Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES | Permission.MODERATE_COMMENTS,
                False),
            "Administrator": (0xff, False)
        }

        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


db.event.listen(Post.body, 'set', Post.on_body_changed)
