
from typing import Optional
from datetime import datetime
from sqlalchemy import ForeignKey, String, DateTime, Text, Boolean, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from ..extensions import db
from flask_login import UserMixin


##CONFIGURE TABLES

class User(db.Model, UserMixin):

    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    username: Mapped[str] =  mapped_column(String(250), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    name: Mapped[str] =  mapped_column(String(250))
    user_role: Mapped[int] =  mapped_column(Integer) #Reference to a different table... or a new class???
    is_active: Mapped[bool] =  mapped_column(Boolean)
    posts: Mapped[list['Post']] = relationship(
            back_populates='author',
            cascade='all, delete-orphan'
            )
    comments: Mapped[list['Comment']] = relationship(
            back_populates='user',
            cascade='all, delete-orphan',
            )
    created_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            default=func.now(),
            )
    updated_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            default=func.now(),
            onupdate=func.now(),
            )

class Post(db.Model):
    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250))
    body: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(Text)
    author: Mapped['User'] = relationship(back_populates='posts')
    comments: Mapped[list['Comment']] = relationship(back_populates='post')
    created_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            default=func.now(),
            )
    updated_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            default=func.now(),
            onupdate=func.now(),
            )

    # Direct reference to the user instance who create the post
    # Like a handle
    # ID reference to the user who created the post
#    user_id: Mapped[int] = mapped_column(teger, ForeignKey('user.id'))
#    user: Mapped[User] = relationship('User', back_populates='posts')

    # List of comments in a particular post

class Comment(db.Model):
    __tablename__ = 'comments'


    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(500), nullable=False)

    # ID reference to the blog which holds the comment
    # Direct reference to the post which holds the comment
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))
    post: Mapped['Post'] = relationship(back_populates='comments')
    # Direct reference to the user instance who create the comment
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='comments')
    created_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            default=func.now(),
            )
    updated_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            default=func.now(),
            onupdate=func.now(),
            )


#    with app.app_context():
#        db.create_all()

