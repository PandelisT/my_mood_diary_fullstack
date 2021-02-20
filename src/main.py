from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 
from flask_wtf import CsrfProtect
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

db = SQLAlchemy()
csrf = CsrfProtect()
migrate = Migrate()
login_manager = LoginManager()
MIGRATION_DIR = os.path.join('.', 'migrations')


def create_app():
    app = Flask(__name__)
    app.config.from_object("default_settings.app_config")

    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db, directory=MIGRATION_DIR)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from models.User import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from commands import db_commands
    app.register_blueprint(db_commands)

    from controllers import registerable_controllers
    for controller in registerable_controllers:
        app.register_blueprint(controller)

    return app