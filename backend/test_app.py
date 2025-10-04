import unittest
from app import create_app

class BasicTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()
        self.app.testing = True