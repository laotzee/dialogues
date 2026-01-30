from app import create_app, db
from app.routes.helpers import *
from .base_db import languages, types, users

app = create_app()

with app.app_context():

    db.create_all()

    db.session.add_all(languages)
    db.session.add_all(types)
    db.session.add_all(users)

    db.session.commit()
    
    print("Database tables created successfully")
