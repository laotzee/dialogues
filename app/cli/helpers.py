import frontmatter
from app.models.models import Post
from app import db


LANG = {
        "en": 1,
        "es": 2,
        }

POST_TYPE = {"post": 1,
             "poem": 2,
             "story": 3,
             }
USER = {
        "laotze":1,
        }

def create_post(file):
    """Creates Post instance from frontmatter file"""
    post = frontmatter.load(file)
    new_post = Post(
            title=post["title"],
            body_raw=post.content,
            user_id=USER["laotze"],
            lang_id=LANG[post["lang"]],
            type_id=POST_TYPE[post["type"]],
            created=post["date"],
            )
    return new_post

