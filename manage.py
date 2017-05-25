#!/usr/bin/env python3
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from pyforum import app
from pyforum import db

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('run', Server(host='127.0.0.1', port=8080))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

