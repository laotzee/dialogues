
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_login import LoginManager


login_manager = LoginManager()
db = SQLAlchemy()
ckeditor = CKEditor()
bootstrap = Bootstrap()
    
