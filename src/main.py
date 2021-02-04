# init.py
from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 
from flask_wtf import CsrfProtect


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
csrf = CsrfProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object("default_settings.app_config")
    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)
    csrf.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from models.User import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from controllers import registerable_controllers
    for controller in registerable_controllers:
        app.register_blueprint(controller)

    return app