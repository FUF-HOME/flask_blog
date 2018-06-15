#!/usr/bin/env python
# -*-coding:utf-8-*-
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server

from app import create_app, db
from app.models import User, Post, Role

app = create_app('devconfig')
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('server', Server())
manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(app=app,
                db=db,
                User=User,
                Post=Post,
                Role=Role,
                create_roles=Role.insert_roles()
                )


if __name__ == '__main__':
    manager.run()
