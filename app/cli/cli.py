import click
from .helpers import create_post
from app import db


def cli_commands(app):
    """Register commands for flask app"""

    @app.cli.command("save_post")
    @click.argument("file")
    def save_post(file):
        """Loads post to the database"""
        new_post = create_post(file)
        db.session.add(new_post)
        db.session.commit()
