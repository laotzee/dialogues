import click
import sys
from .helpers import create_post
from app import db
from app.models.models import Post


def cli_commands(app):
    """Register commands for flask app"""

    @app.cli.command("save_posts")
    @click.argument("file")
    def save_posts(files):
        """Loads posts form stdin to the database"""
        posts = sys.stdin
        for file in files:
            file = file.strip()
            new_post = create_post(file)
            db.session.add(new_post)
        db.session.commit()


    @app.cli.command("publish_post")
    def publish_post():
        """Changes to public the oldest unpublished posts on the database"""
        stmt = db.select(Post).order_by(Post.created).where(
                Post.is_published == False)
        post = db.session.scalars(stmt).first()
        post.is_published = True
        db.session.commit()
