import os
from dotenv import load_dotenv

load_dotenv()
env = os.getenv('FLASK_ENV')

db_url = "mysql+pymysql://{}:{}@{}/{}".format(
    os.getenv('DB_USER', 'root'),
    os.getenv('DB_PASSWORD', ''),
    os.getenv('DB_HOST', 'db'),
    os.getenv('DB_NAME', 'my_database'),
)

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_TRANSLATION_DIRECTORIES = os.path.join(BASEDIR, 'translations')


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///./blog.db"
    DEBUG = True


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = db_url
    DEBUG = False


config_map = {
    'development': ('development', 'config.DevelopmentConfig'),
    'testing': ('testing', 'config.TestingConfig'),
    'production': ('production', 'config.ProductionConfig'),
    }

app_env = config_map.get(env, 'production')
