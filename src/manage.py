import os

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import create_app, db


MIGRATION_DIR = os.path.join('src/application', 'migrations')
env_name = os.getenv('FLASK_ENV', 'development')
print(env_name)
app = create_app(env_name)
migrate = Migrate(app, db, directory=MIGRATION_DIR)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manager.run()
