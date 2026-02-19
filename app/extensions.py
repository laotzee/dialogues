from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
from flask_migrate import Migrate

from flask import Flask, request, g, url_for
from flask_babel import Babel

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(model_class=Base)
migrate = Migrate()
babel = Babel()

def get_locale():
    if request.path.startswith('/es'):
        return 'es'
    return 'en'

def babel_setup(app):
    """Defines babel functions in app context"""
    @app.before_request
    def before_request():
        g.locale = get_locale()

    @app.context_processor
    def inject_url_helpers():
        def local_url(endpoint, **values):
            return url_for(f'blueprint_{g.locale}.{endpoint}', **values)
    
        return dict(local_url=local_url)
