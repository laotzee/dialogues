import sys
import frontmatter, markdown
from app.models.models import Post
from app import db, create_app

lang = {
        "en": 1,
        "es": 2,
        }
post_type = {"post": 1,
             "poem": 2,
             "story": 3,
             }
user = {
        "laotze":1,
        }

def process_post(file):

    post = frontmatter.load(file)
    new_post = Post(
            title=post["title"],
            body_raw=post.content,
            user_id=user["laotze"],
            lang_id=lang[post["lang"]],
            type_id=post_type[post["type"]],
            created=post["date"],
            )
    return new_post

def save_posts(posts):
    app = create_app()
    with app.app_context():
        for post in posts:
            post = post.strip()
            new_post = process_post(post)
            db.session.add(new_post)
        db.session.commit()

if __name__ == "__main__":
    posts = sys.stdin
    save_posts(posts)
