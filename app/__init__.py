from flask import Flask
from .extensions import db
from .routes.main import blueprint

def create_app(config_class='config.ProductionConfig'):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.register_blueprint(blueprint)
    db.init_app(app)
    return app
