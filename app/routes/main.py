from .views import *

blueprint = Blueprint('blueprint', __name__)

@blueprint.route('/')
def get_all_posts():
    """Route for home page"""
    page = process_home()
    return page


@blueprint.route("/about")
def about():
    """Route for about page"""
    page = process_about()
    return page


@blueprint.route("/contact", methods=["GET", "POST"])
def contact():
    """Route for contact page"""
    page = process_contact()
    return page


@blueprint.route('/register', methods=["GET", "POST"])
def register():
    """Route for register page"""
    page = process_register()
    return page


@blueprint.route('/login', methods=["GET", "POST"])
def login():
    """Route for login page"""
    page = process_login()
    return page


@blueprint.route("/logout")
@login_required
def logout():
    """Route for logout page"""
    page = process_logout()
    return page


@blueprint.route("/posts/<int:post_id>", 
                 methods=["GET", "POST", "DELETE", "PUT" ])
def posts_id(post_id: int) -> str:
    """Process posts actions on a specific instance"""
    if request.method == "DELETE":
        page = delete_post(post_id)
    elif request.method == "PUT":
        page = update_post(post_id)
    else:
        page = show_post(post_id)
    return page


@blueprint.route("/posts", methods=["GET", "POST"])
def posts() -> str:
    """Process general posts actions"""
    if request.method == "GET": # show all posts
        message = {"error": "The requested feature is not yet implemented."}
        return jsonify(message), 501
    elif request.method == "POST":
        page = create_post()
        return page
    else:
        message = {"error": "The requested feature is not yet implemented."}
        return jsonify(message), 501


