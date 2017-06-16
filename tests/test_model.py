import unittest
import time
# from datetime import datetime
from app import create_app
from app.model import User, Order
from elasticsearch_dsl import Index


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        # drop the whole index
        Index(User._doc_type.index).delete()
        self.app_context.pop()

    def test_password_setter(self):
        u = User()
        u.password = 'cat'
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User()
        u.password = 'cat'
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User()
        u.password = 'cat'
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        u = User()
        u.password = 'cat'
        u2 = User(username='e')
        u2.password = 'cat'
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_user_retrieval(self):
        u = User(email='john@example.com')
        u.password = 'cat'
        if u.save():
            time.sleep(1)  # wait 1s until index is updated
            s = User.search().filter('match', email='john@example.com')
            u2 = s.execute()[0]
            self.assertTrue(u2.verify_password('cat'))
        else:
            print "Can't create object"

    def test_valid_confirmation_token(self):
        u = User()
        u.password = 'cat'
        u.save()
        token = u.generate_token('confirm')
        self.assertTrue(u.apply_token('confirm', token))
        self.assertTrue(u.verified and u.active)
        u.delete()

    def test_invalid_confirmation_token(self):
        u1 = User()
        u1.password = 'cat'
        u2 = User()
        u2.password = 'dog'
        u1.save()
        u2.save()
        token = u1.generate_token('confirm')
        self.assertFalse(u2.apply_token('confirm', token))
        u1.delete()
        u2.delete()

    def test_valid_reset_token(self):
        u = User()
        u.password = 'cat'
        u.save()
        token = u.generate_token('reset_password')
        u.apply_token('reset_password', token, 'dog')
        self.assertTrue(u.verify_password('dog'))
        self.assertFalse(u.verify_password('cat'))
        u.delete()

    def test_wrong_token_option(self):
        u = User()
        u.password = 'cat'
        u.save()
        with self.assertRaises(AttributeError):
            token = u.generate_token('test')
            u.apply_token('test', token)
            u.delete()
