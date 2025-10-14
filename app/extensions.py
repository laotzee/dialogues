
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

login_manager = LoginManager()
db = SQLAlchemy(model_class=Base)
ckeditor = CKEditor()
bootstrap = Bootstrap()
    
