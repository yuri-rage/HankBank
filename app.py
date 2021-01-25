"""
    Children's allowance management via Flask and SQLAlchemy

    Provides a basic web interface for parents and children to manage allowance money using virtual bank accounts

    Templates and basic design based on:
        https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login

    -- Yuri - Jan 2021
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # suppress warnings
    app.config['SECRET_KEY'] = '16cabaf0721e42d27bf86ae5c20ef1224f20acfcb95ac5d4'  # randomly generated characters
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # blueprint for auth routes
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
