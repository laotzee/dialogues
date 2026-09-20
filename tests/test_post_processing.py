import unittest
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from ..app.models.models import *
#from x import the script itself

class TestPostProcessing(unittest.TestCase):

    def setUp(self):
        # Create an in-memory SQLite database for speed and isolation
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        
        # Create a session factory
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def test_completeness(self):

        self.assertEqual(title, slug)
        pass

        
    def test_slug_char(self):

        title = "My First Post"
        slug = "my-first-post"

        self.assertEqual(title, slug)

    def test_slug_special(self):

        title = "My First Post!%#"
        slug = "my-first-post"

        self.assertEqual(title, slug)

    def test_slug_nums(self):

        title = "My First Post48 8"
        slug = "my-first-post48-8"

        self.assertEqual(title, slug)

    def test_add_floats(self):
        self.assertAlmostEqual(add(0.1, 0.2), 0.3, places=7)

    def test_divide_success(self):
        self.assertEqual(divide(10, 2), 5)

    def test_divide_by_zero(self):
        # Use a context manager to check if a specific error is raised
        with self.assertRaises(ValueError):
            divide(10, 0)


    def tearDown(self):
        # Close the session and drop everything
        self.session.close()
        Base.metadata.drop_all(self.engine)

if __name__ == '__main__':
    unittest.main()
