#!/usr/bin/env python3
from flask_script import Manager, Server, prompt_bool
from flask_migrate import Migrate, MigrateCommand
from flask_babel import _

from pyforum import app
from pyforum import db
from pyforum.user.models import User

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('run', Server(host='0.0.0.0', port=8080))
manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    "create database tables fro SQLAlchemy models"
    db.create_all()
    return _'База создана'


@manager.command
def drop_db():
    "drops db tables"
    if prompt_bool(_("Вы действительн хотите потерять все свои данные?")):
        db.drop_all()


@manager.command
def create_admin():
    "create user admin"
    user = User(username='admin',
                email='admin@admin.com',
                password='admin'
                )

    user.admin = True
    db.session.add(user)
    db.session.commit()


if __name__ == '__main__':
    manager.run()
