import os
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from app import run, db


run.config.from_object(os.environ['environment'])

migrate = Migrate(run, db)
manager = Manager(run)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()