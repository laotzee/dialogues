from .helpers import *
from ..extensions import login_manager, db
from ..forms import CreatePostForm, RegisterForm, LogInForm, CommentForm, ContactForm
from ..models.models import User, Post, Comment
from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash
from flask_login import login_user, login_required, current_user, logout_user
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


def instance_exist(**kwargs):
    """Helps verify aspects of entity in the db"""

    entity = db.session.query(User).filter_by(**kwargs).first()
    return entity


def only_admin(func):

    @wraps(func)
    def wrapper_func(*args, **kwargs):

        if not current_user.is_anonymous and current_user.id == 1:
            return func(*args, **kwargs)
        with app.app_context():
            return abort(403)

    return wrapper_func

def process_home() -> str:
    posts = Post.query.all()
    return render_template('index.html', all_posts=posts)


def process_about():
    return render_tempalte('about.html')

def process_contact() -> str:
    form = ContactForm()
    if form.validate_on_submit():

        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        body = message_template(name, email, message)
        user_email = format_message(body)
        send_email(user_email)

        flash("Email sent. You'll receive a reply as soon as we can!", "success")

        return render_template(
            "contact.html",
            form=form,
        )
    return render_template("contact.html")

def process_login() -> str:
    form = LogInForm()

    if form.validate_on_submit():

        email = request.form.get("email")
        password = request.form.get("password")

        user = instance_exist(email=email)
        if user:

            if check_password_hash(user.password, password):

                login_user(user)
                #login him in lol
                return redirect(url_for("blueprint.get_all_posts"))

            else:
                flash("Incorrect password", "error")
        else:
            flash("Such email does not exist. Try to register", "error")
            return redirect("blueprint.register")

    return render_template("login.html", form=form)

def process_register() -> str:
    form = RegisterForm()

    if form.validate_on_submit():

        name = request.form.get("name")
        password = request.form.get("password")
        email = request.form.get("email")

        email_exist = instance_exist(email=email)
        name_exist = instance_exist(name=name)
        print(name_exist)
        print(email_exist)

        if email_exist:
            flash("An account with that email already exist.\nTry logging in", "error")
            return redirect(url_for("blueprint.login"))
        elif name_exist:
            flash("That name is already used", "error)")
        else:
            hashed_password = hash_password(password)
            new_user = create_user(username, password, email)
            login_user(new_user)
            return redirect(url_for("blueprint.get_all_posts"))

    return render_template("register.html", form=form)


def process_logout() -> str:
    logout_user()
    return redirect(url_for("blueprint.get_all_posts"))


def show_post(post_id: int) -> str:
    form = CommentForm()

    if form.validate_on_submit():

        # add comment to the appropriate table
        # Verify if the user if logged first

        comment = request.form.get("comment")

        new_comment =  Comments(
            text=comment,
            user_id=current_user.id,
            post_id=post_id,
        )

        db.session.add(new_comment)
        db.session.commit()

    requested_post = Post.query.get(post_id)
    return render_template(
        "post.html",
        post=requested_post,
        form=form,
        comments=requested_post.comments
    )

def delete_post(post_id: int) -> str:
    post_to_delete = Post.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('blueprint.home'))

def update_post(post_id: int) -> str:
    post = Post.query.get(post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("blueprint.show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form)

def create_post() -> str:
    form = CreatePostForm()
    if form.validate_on_submit():

        new_post = Post(
            author=current_user.name,
            title=form.title.data,
            subtitle=form.subtitle.data,
            date=date.today().strftime("%B %d, %Y"),
            body=form.body.data,
            img_url=form.img_url.data,
            user_id=current_user.id,
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("blueprint.home"))
    return render_template("make-post.html", form=form)

