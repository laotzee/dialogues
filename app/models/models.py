from datetime import datetime
import re, markdown 
from slugify import slugify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, inspect, String, Text, DateTime, ForeignKey, Table, Column, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from ..extensions import db, Base

excerpt_len = 100

post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)

class User(db.Model):
    """Models a user"""
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    posts: Mapped[list["Post"]] = relationship(back_populates="author")

class Lang(db.Model):
    """Models the language of a post"""
    __tablename__ = "languages"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(2), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(10), unique=True)

class PostType(db.Model):
    """Models the type of a post"""
    __tablename__ = "post_types"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    posts: Mapped[list["Post"]] = relationship(back_populates="content_type")

class Tag(db.Model):
    """Models the tag for posts"""
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    slug: Mapped[str] = mapped_column(String(50), unique=True, index=True)

class Post(db.Model):
    """Models a blog post"""
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    body_raw: Mapped[str] = mapped_column(Text)
    body_html: Mapped[str] = mapped_column(Text)
    excerpt: Mapped[str] = mapped_column(String(excerpt_len))
    is_published: Mapped[bool] = mapped_column(default=False, index=True)
    slug: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    created: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            default=func.now(),
            index=True,
            )
    updated: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            default=func.now(),
            onupdate=func.now(),
            )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    lang_id: Mapped[int] = mapped_column(ForeignKey("languages.id"))
    type_id: Mapped[int] = mapped_column(ForeignKey("post_types.id"), index=True)

    author: Mapped["User"] = relationship(back_populates="posts")
    content_type: Mapped["PostType"] = relationship(back_populates="posts")
    tags: Mapped[list["Tag"]] = relationship(secondary=post_tags, backref="posts")

class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            default=func.now(),
            )
    is_active = db.Column(db.Boolean, default=True)

def generate_unique_slug(target, value, column_name='slug'):
    """Generates a unique slug for any model"""
    if not value:
        return
        
    base_slug = slugify(value)
    slug = base_slug
    counter = 1

    session = db.object_session(target)
    klass = target.__class__

    while session.query(klass).filter(getattr(klass, column_name) == slug).first():
        existing = session.query(klass).filter(getattr(klass, column_name) == slug).first()
        if existing and existing.id == target.id:
            break
            
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug

def generate_html(content):
    """Generates the HTML render of a post"""
    return markdown.markdown(content) if content else ""

@event.listens_for(Tag, 'before_insert')
@event.listens_for(Tag, 'before_update')
def receive_tag_slug(mapper, connection, target):
    target.slug = generate_unique_slug(target, target.name)

@event.listens_for(Post, 'before_insert')
@event.listens_for(Post, 'before_update')
def receive_post_slug(mapper, connection, target):
    target.slug = generate_unique_slug(target, target.title)

@event.listens_for(Post, 'before_insert')
def generate_post_html(mapper, connection, target):
    target.body_html = generate_html(target.body_raw)

@event.listens_for(Post, 'before_update')
def check_body_changes(mapper, connection, target):
    body_history = inspect(target).attrs.body_raw.history
    
    if body_history.has_changes():
        target.body_html = generate_html(target.body_raw)

@event.listens_for(Post, 'before_insert')
def generate_post_excerpt(mapper, connection, target):
    
    if not target.excerpt:
        target.excerpt = target.body_raw[:excerpt_len-1]
