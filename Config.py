#!/usr/bin/env python
# -*-coding:utf-8-*-
import os


class Config(object):
    """Base config class."""
    BOOTSTRAP_SERVE_LOCAL = True
    SECRET_KEY = "Hard to guess string"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = "Flasky Admin <test@gmail.com>"
    FLASKY_ADMIN = "xx@xx.com"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_POSTS_PER_PAGE = os.environ.get("FLASKY_POSTS_PER_PAGE") or 8

    @staticmethod
    def init_app(app):
        pass


class ProdConfig(Config):
    """Production config class."""
    pass


class DevConfig(Config):
    """Development config class."""
    # Open the DEBUG
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    BABEL_DEFAULT_LOCALE = 'zh_CN'

    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@192.168.108.132:3306/blog'


config = {
    'devconfig': DevConfig
}
