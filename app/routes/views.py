from .helpers import *
from ..extensions import db
from ..models.models import User, Post, Tag, PostType, Subscriber
from flask import (Blueprint, render_template, redirect, url_for, request,
                   jsonify, flash, g)
from email_validator import validate_email, EmailNotValidError

def process_index() -> str:
    """Renders the index page passing posts"""
    query = request.args.get('type', 'all')
    page = request.args.get('page', 1, type=int)
    lang_code = 2 if g.locale == 'es' else 1

    if query == 'all':
        stmt = (
    db.select(Post)
                .where(Post.lang_id == lang_code)
                .where(Post.is_published == True)
                .order_by(Post.created.desc(), Post.id.desc())
                )
    else:
        stmt = (
                db.select(Post)
                .join(Post.content_type)
                .where(Post.lang_id == lang_code)
                .where(PostType.name == query)
                .where(Post.is_published == True)
                .order_by(Post.created.desc(), Post.id.desc())
                )

    posts = db.paginate(stmt, page=page, per_page=10, error_out=False)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('partials/index_cards.html', posts=posts)

    return render_template('index.html', posts=posts)

def process_about():
    """Renders the about page"""
    return render_template('about.html')

def process_contact() -> str:
    """Renders the about contact"""
    return render_template("contact.html")

def process_post(slug: str) -> str:
    """Renders the post pages"""
    stmt = db.select(Post).where(Post.slug == slug)
    post = db.session.execute(stmt).scalar()
    return render_template("post.html", post=post)

def process_subscription():
    """Validates and process subscription requests"""
    email: str = request.form.get('email')

    if not email:
        return "Email is required", 400

    try:
        email_info = validate_email(email, check_deliverability=True)
        email = email_info.normalized
    except EmailNotValidError as e:
        return f"Invalid email: {str(e)}", 400

    if Subscriber.query.filter_by(email=email).first():
        return "You're already on the list!", 400
    
    new_sub = Subscriber(email=email)
    db.session.add(new_sub)
    db.session.commit()
    return "Subscribed successfully!"
