from .views import *
from ..models.models import Post
from ..extensions import db


blueprint = Blueprint('blueprint', __name__)

@blueprint.route('/')
def index():
    """Route for home page"""
    page = process_index()
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


@blueprint.route("/posts/<string:slug>", methods=["GET"])
def posts(slug) -> str:
    """Process general posts actions"""
    page = process_post(slug)
    return page


@blueprint.route("/subscribe", methods=["POST"])
def subscribe() -> str:
    """Process subscriptions to email listing"""
    response = process_subscription()
    return response
