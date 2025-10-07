from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.extensions import db
from flask_login import UserMixin

# TODO: change all tables to a singular and sentence case

##CONFIGURE TABLES

class User(db.Model, UserMixin):

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=False, unique=True)
    name =  db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)

    # List of posts made by a particular user
    posts = relationship("BlogPost", back_populates="user")

    # list of comments made by a particualar userwerkzeug.routing.exceptions.BuildError: Could not build url for endpoint 'add_user_confirm' with values
    comments = relationship("Comments", back_populates="user")

class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(250), nullable=False)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    # ID reference to the user who created the post
    user_id = db.Column(db.Integer, ForeignKey("user.id"))
    # Direct reference to the user instance who create the post
    # Like a handle
    user = relationship("User", back_populates="posts")

    # List of comments in a particular post
    comments = relationship("Comments", back_populates="post")

class Comments(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(250), nullable=False)

    # ID reference to the user who created the comment
    user_id = db.Column(db.Integer, ForeignKey("user.id"))

    # ID reference to the blog which holds the comment
    post_id = db.Column(db.Integer, ForeignKey("blog_posts.id"))

    # Direct reference to the post which holds the comment
    post = relationship("BlogPost", back_populates="comments")

    # Direct reference to the user instance who create the comment
    user = relationship("User", back_populates="comments")


#    with app.app_context():
#        db.create_all()

