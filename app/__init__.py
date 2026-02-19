from flask import Flask, g, url_for
from .extensions import db, migrate, babel, babel_setup, get_locale
from .routes.main import blueprint
from .cli.cli import cli_commands
from config import app_env

def create_app():
    app = Flask(__name__)
    app.config.from_object(app_env[1])
    app.register_blueprint(blueprint, url_prefix='/', name='blueprint_en')
    app.register_blueprint(blueprint, url_prefix='/es', name='blueprint_es')

    cli_commands(app)
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    babel.init_app(app, locale_selector=get_locale)
    babel_setup(app)

    return app
