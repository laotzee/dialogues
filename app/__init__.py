from flask import Flask
from .extensions import db, migrate
from .routes.main import blueprint
from config import app_env

def create_app():
    app = Flask(__name__)
    app.config.from_object(app_env[1])
    app.register_blueprint(blueprint)

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    return app
