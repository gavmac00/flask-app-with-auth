from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'aofneiufha'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # sqlite is the database type, /// is the relative path to the database
    db.init_app(app)

    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note # importing here to avoid circular import
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' # the login route
    login_manager.init_app(app)

    @login_manager.user_loader # this decorator will reload the user object from the user ID stored in the session
    def load_user(id):
        """Returns the user object."""
        return User.query.get(int(id)) # get() returns the object with the specified primary key

    return app

def create_database(app):
    """Creates the database."""
    with app.app_context():
        if not path.exists('website/' + DB_NAME):
            db.create_all()
            print('\033[92m' + 'Created Database.' + '\033[0m')