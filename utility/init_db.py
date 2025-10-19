from app import create_app, db
from app.routes.helpers import *

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    
    print("Database tables created successfully")
