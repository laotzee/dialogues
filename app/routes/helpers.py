from  ..extensions import login_manager, db
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.models import User, Post, Comment

def hash_password(password):

    hashed = generate_password_hash(
        password=password,
        method="scrypt:32768:8:1",
        salt_length=16,
        )

    return hashed


def create_user(username, password, email):

    new_user = User(
        email=email,
        username=username,
        password=hash_password(password),
    )
    db.session.add(new_user)
    db.session.commit()
    return new_user
