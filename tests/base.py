import unittest
import json
from app import create_app, db
from app.models.models import Post
from config import config_map


class BaseTest(unittest.TestCase):
    def setUp(self):

        self.app = create_app(config_map.get("testing"))
        self.client = self.app.test_client()
        
        with self.app.app_context():

            db.create_all()

            post1: Post
            post2: Post

            posts = [post1,  post2]

            db.session.add_all(posts)
            
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
