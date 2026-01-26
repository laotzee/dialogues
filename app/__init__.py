from flask import Flask, g, url_for
from .extensions import db, migrate, babel, get_locale
from .routes.main import blueprint
from config import app_env

def create_app():
    app = Flask(__name__)
    app.config.from_object(app_env[1])
    app.register_blueprint(blueprint, url_prefix='/', name='blueprint_en')
    app.register_blueprint(blueprint, url_prefix='/es', name='blueprint_es')

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    babel.init_app(app, locale_selector=get_locale)

    @app.before_request
    def before_request():
        g.locale = get_locale()

    @app.context_processor
    def inject_url_helpers():
        def local_url(endpoint, **values):
            return url_for(f'blueprint_{g.locale}.{endpoint}', **values)
    
        return dict(local_url=local_url)

    return app
