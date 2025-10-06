from flask import Flask
from .extensions import db, ckeditor, bootstrap, login_manager
from .routes.main import blueprint

def create_app(config_class='config.ProductionConfig'):

    app = Flask(__name__)
    app.config.from_object(config_class)

    login_manager.init_app(app)
    db.init_app(app)
    ckeditor.init_app(app)
    bootstrap.init_app(app)

    app.register_blueprint(blueprint)

    return app

