from .helpers import *
from ..extensions import db
from ..models.models import User, Post, Tag, PostType
from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash

def process_index() -> str:
    """Renders the index page passing posts in English"""
    query = request.args.get('type', 'all')
    page = request.args.get('page', 1, type=int)


    if query == 'all':
        stmt = (
                db.select(Post)
                .where(Post.lang_id == 1)
                .order_by(Post.created.desc(), Post.id.desc())
                )
    else:
        stmt = (
                db.select(Post)
                .join(Post.content_type)
                .where(Post.lang_id == 1)
                .where(PostType.name == query)
                .order_by(Post.created.desc(), Post.id.desc())
                )

#    posts = db.session.execute(stmt).scalars().all()
    posts = db.paginate(stmt, page=page, per_page=10, error_out=False)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('partials/index_cards.html', posts=posts)

    return render_template('index.html', posts=posts)

def process_about():
    return render_template('about.html')

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
    return render_template("contact.html",  form=form)

def process_login() -> str:
    form = LogInForm()

    if form.validate_on_submit():
        email, password = process_login_info()
        user = get_user_by_attribute(email=email)

        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for("blueprint.index"))
            else:
                flash("Incorrect password", "error")
        else:
            flash("Such email does not exist. Try to register", "error")
            return redirect(url_for("blueprint.register"))
    return render_template("login.html", form=form)

def process_register() -> str:
    form = RegisterForm()

    if form.validate_on_submit():
        username, password, email = process_register_info()
        email_exist = get_user_by_attribute(email=email)
        username_exist = get_user_by_attribute(username=username)
        print(username_exist)
        print(email_exist)

        if email_exist:
            flash("An account with that email already exist.\nTry logging in", "error")
            return redirect(url_for("blueprint.login"))
        elif username_exist:
            flash("That username is already used", "error)")
        else:
            hashed_password = hash_password(password)
            new_user = create_user(username, password, email)
            login_user(new_user)
            return redirect(url_for("blueprint.index"))

    return render_template("register.html", form=form)


def process_logout() -> str:
    logout_user()
    return redirect(url_for("blueprint.index"))


def show_post(slug: str) -> str:

    stmt = db.select(Post).where(Post.slug == slug)
    post = db.session.execute(stmt).scalar()

    return render_template("post.html", post=post)

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

