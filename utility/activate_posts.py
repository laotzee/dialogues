from app import create_app, db
from app.routes.helpers import *
from sqlalchemy import update
from app.models.models import Post


if __name__ == "__main__":
    app = create_app()

    with app.app_context():


#        stmt = (
#            update(Post)
#            .values(is_published=True)
#        )
        
#        db.session.execute(stmt)
#        db.session.commit()

