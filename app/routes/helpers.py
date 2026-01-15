from  ..extensions import login_manager, db
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.models import User, Post, Tag, PostType
from functools import wraps
from sqlalchemy import select
from flask import request


######## DB #######

@login_manager.user_loader
def load_user(user_id: int) -> User | None:
    stmt = select(User).where(User.id==user_id)
    user = db.session.scalars(stmt).first()
    return user


def get_posts() -> list[Post] | None:
    stmt = select(Post)
    posts = db.session.scalars(stmt).all()
    return posts


def get_user_by_attribute(**kwargs) -> User | None: # ???
    """Returns User instance if first kwarg matches one, None otherwise. If 
    more kwargs are given, they will be ignored"""
    if not kwargs:
        return None
    key, val = list(kwargs.items())[0]
    column = getattr(User, key, None)
    print(column)
    if not column:
        raise(f"Key {key} doesn't correspond to any column from User")
    stmt = select(User).where(column == val)
    user = db.session.scalars(stmt).first()
    return user


def only_admin(func):
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        if not current_user.is_anonymous and current_user.id == 1:
            return func(*args, **kwargs)
        with app.app_context():
            return abort(403)
    return wrapper_func


def create_user(username, password, email):
    new_user = User(
        email=email,
        username=username,
        password=hash_password(password),
    )
    db.session.add(new_user)
    db.session.commit()
    return new_user


######## Forms #######

def process_login_info():
    """Gathers info from LogInForm and returns a user if valid"""
    email = request.form.get("email")
    password = request.form.get("password")
    return email, password

def process_register_info():
    """Returns username, password and email from the RegisterForm"""
    username = request.form.get("name")
    password = request.form.get("password")
    email = request.form.get("email")
    return username, password, email


######## Blog #######

def hash_password(password):

    hashed = generate_password_hash(
        password=password,
        method="scrypt:32768:8:1",
        salt_length=16,
        )

    return hashed


