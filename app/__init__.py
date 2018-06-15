from flask import Flask
from flask_admin import Admin
from flask_babelex import Babel
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from  Config import config

db = SQLAlchemy()
admin = Admin()
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()
login_manager = LoginManager()
login_manager.session_protection = 'strong'  # 让session功能更加强壮
login_manager.login_view = 'auth.login'  # 制定系统默认的登录页面
login_manager.login_message = "请登录后再进行访问该页面！"


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    babel.init_app(app)

    moment.init_app(app)
    admin.init_app(app)

    login_manager.init_app(app)
    bootstrap.init_app(app)
    from app.admin import admin as admin_blueprint
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    return app
