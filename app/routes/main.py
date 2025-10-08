from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from functools import wraps
from app.extensions import login_manager, db
from .logic import *

blueprint = Blueprint('blueprint', __name__)

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

@blueprint.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template('index.html', all_posts=posts)
 

@blueprint.route("/about")
def about():
    return render_template("about.html")


@blueprint.route("/contact", methods=["GET", "POST"])
def contact():

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
    return render_template("index.html", all_posts=posts)


@blueprint.route('/register', methods=["GET", "POST"])
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
            flash("An account with that email already exist.\nTry logging in", "error")
            return redirect(url_for("blueprint.login"))
        elif name_exist:
            flash("That name is already used", "error)")
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

            return redirect(url_for("blueprint.get_all_posts"))

    return render_template("register.html", form=form)


@blueprint.route('/login', methods=["GET", "POST"])
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
                return redirect(url_for("blueprint.get_all_posts"))

            else:
                flash("Incorrect password", "error")
        else:
            flash("Such email does not exist. Try to register", "error")
            return redirect("blueprint.register")

    return render_template("login.html", form=form)

@blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("blueprint.get_all_posts"))


@blueprint.route("/posts/<int:post_id>", 
                 methods=["GET", "POST", "DELETE", "PUT" ])
def posts_id(post_id):

    if request.method == "DELETE":
        response = delete_post(post_id)
    elif request.method == "PUT":
        response = update_post(post_id)
    else:
        response = show_post(post_id)

    return response

@blueprint.route("/posts", methods=["GET", "POST"])
def posts():
    if request.method == "GET":
        message = {"error": "The requested feature is not yet implemented."}
        return jsonify(message), 501

    elif request.method == "POST":
        create_post()
    else:
        message = {"error": "The requested feature is not yet implemented."}
        return jsonify(message), 501


