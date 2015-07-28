import os
from app import create_app, db
from app.models import Staff
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand


# Initialise
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

def make_shell_context():
    return dict(app=app, db=db, Staff=Staff)
manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()

