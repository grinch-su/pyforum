#!/usr/bin/env python3
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from pyforum import app
from pyforum import db
from pyforum.user.models import User

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('run', Server(host='0.0.0.0', port=8080))
manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    db.create_all()


@manager.command
def drop_all():
    db.drop_all()


@manager.command
def create_admin():
    user = User(username='admin',
                email='grinchfedorov@gmail.com',
                password='admin'
                )
    user.admin = True
    db.session.add(user)
    db.session.commit()


if __name__ == '__main__':
    manager.run()
