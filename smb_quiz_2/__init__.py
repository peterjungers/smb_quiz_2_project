from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from smb_quiz_2.config import Config


db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from smb_quiz_2.errors.handlers import errors
    from smb_quiz_2.main.routes import main
    app.register_blueprint(errors)
    app.register_blueprint(main)

    return app
