from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from smb_quiz_2.config import Config

# initialized outside of app so that they aren't bound to specific app
# (using Blueprints allows me to create multiples instances of app,
# but I can have same db, users, etc., across all instances)
# db = SQLAlchemy()
# bcrypt
# login_manager
# mail


def create_app(): # put in () --> config_class=Config
    app = Flask(__name__)
    # app.config.from_object(config_class)

    # db.init_app(app)

    from smb_quiz_2.errors.handlers import errors
    from smb_quiz_2.main.routes import main
    from smb_quiz_2.users.routes import users
    app.register_blueprint(errors)
    app.register_blueprint(main)
    app.register_blueprint(users)

    return app
