import os
from dotenv import load_dotenv

load_dotenv()
env = os.getenv('FLASK_ENV')

db_url = "mysql+pymysql://{}:{}@{}/{}".format(
    os.getenv('DB_USER', 'root'),
    os.getenv('DB_PASSWORD', ''),
    os.getenv('DB_HOST', 'host.docker.internal'),
    os.getenv('DB_NAME', 'my_database'),
)

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_TRANSLATION_DIRECTORIES = os.path.join(BASEDIR, 'translations')
    SQLALCHEMY_DATABASE_URI = db_url

class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    DEBUG = False


config_map = {
    'development': ('development', 'config.DevelopmentConfig'),
    'testing': ('testing', 'config.TestingConfig'),
    'production': ('production', 'config.ProductionConfig'),
    }

app_env = config_map.get(env, config_map['production'])

