from os import environ
from flask import Flask, render_template, redirect, url_for, flash, request, abort, jsonify
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from functools import wraps
from sqlalchemy import ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from contact import message_template, format_message, send_email
from forms import CreatePostForm, RegisterForm, LogInForm, CommentForm, ContactForm

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = environ.get("api_key")
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CONFIGURE TABLES

class User(db.Model, UserMixin):

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=False, unique=True)
    name =  db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)

    # List of posts made by a particular user
    posts = relationship("BlogPost", back_populates="user")

    # list of comments made by a particualar user
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


with app.app_context():
    db.create_all()

def instance_exist(**kwargs):
    """Helps verify aspects of entity in the db"""

    entity = db.session.query(User).filter_by(**kwargs).first()
    return entity

def only_admin(func):

    @wraps(func)
    def wrapper_func(*args, **kwargs):

        wrapper_func.__name__ = func.__name__
        if not current_user.is_anonymous and current_user.id == 1:
            return func(*args, **kwargs)
        with app.app_context():
            return abort(403)

    return wrapper_func

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts)


@app.route('/register', methods=["GET", "POST"])
def register():

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
            flash("An account with that email already exist.\nTry logging in")
            return redirect(url_for("login"))
        elif name_exist:
            flash("That name is already used")
        else:
            hashed_password = generate_password_hash(
                password=password,
                method="scrypt:32768:8:1",
                salt_length=16,
            )
            new_user = User(
                email=email,
                name=name,
                password=hashed_password,
            )
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)

            return redirect(url_for("get_all_posts"))

    return render_template("register.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():

    form = LogInForm()

    if form.validate_on_submit():

        email = request.form.get("email")
        password = request.form.get("password")

        user = instance_exist(email=email)
        if user:

            if check_password_hash(user.password, password):

                login_user(user)
                #login him in lol
                return redirect(url_for("get_all_posts"))

            else:
                flash("Incorrect password")
        else:
            flash("Such email does not exist. Try to register")
            return redirect("register")

    return render_template("login.html", form=form)



@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):

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

    requested_post = BlogPost.query.get(post_id)
    return render_template(
        "post.html",
        post=requested_post,
        form=form,
        comments=requested_post.comments
    )

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():

    form = ContactForm()
    if form.validate_on_submit():

        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        body = message_template(name, email, message)
        user_email = format_message(body)
        send_email(user_email)

        flash("Email sent. You'll receive a reply as soon as we can!")

    return render_template(
        "contact.html",
        form=form,
    )

@app.route("/new-post", methods=["GET", "POST"])
@only_admin
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():

        new_post = BlogPost(
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
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@only_admin
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
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
        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form)


@app.route("/delete/<int:post_id>")
@only_admin
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("get_all_posts"))

if __name__ == "__main__":
    app.run(debug=True)
