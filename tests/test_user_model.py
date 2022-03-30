import time
import unittest
from app import create_app, db
from app.models import User


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_getter(self):
        u = User(password='psw')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_setter(self):
        u = User(password='psw')
        self.assertTrue(u.password_hash is not None)

    def test_password_verification(self):
        u = User(password='psw')
        self.assertTrue(u.verify_password('psw'))
        self.assertFalse(u.verify_password('wsp'))

    def test_invalid_email_confirmation_token(self):
        u1 = User(password='psw')
        u2 = User(password='wsp')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_confirmation_token()
        self.assertFalse(u2.confirm_register_token(token))

    def test_expired_email_confirmation_token(self):
        u = User(password='psw')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token(1)
        time.sleep(2)
        self.assertFalse(u.confirm_register_token(token))

    def test_valid_reset_password_token(self):
        u = User(password='psw')
        db.session.add(u)
        db.session.commit()
        token = u.generate_reset_password_token()
        self.assertTrue(User.reset_password(token, 'bob'))
        self.assertTrue(u.verify_password('bob'))

    def test_invalid_reset_token(self):
        u = User(password='psw')
        db.session.add(u)
        db.session.commit()
        token = u.generate_reset_password_token()
        self.assertFalse(User.reset_password(token + '123', 'wsp'))
        self.assertTrue(u.verify_password('psw'))

    def test_valid_email_change_token(self):
        u = User(email='bob@ex.com', password='psw')
        db.session.add(u)
        db.session.commit()
        token = u.generate_mail_change_token('obo@ex.com')
        self.assertTrue(u.change_email(token))
        self.assertTrue(u.email == 'obo@ex.com')

    def test_invalid_email_change_token(self):
        u1 = User(email='bob@ex.com', password='psw')
        u2 = User(email='john@ex.com', password='wsp')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_mail_change_token('david@example.net')
        self.assertFalse(u2.change_email(token))
        self.assertTrue(u1.email == 'bob@ex.com')
        self.assertTrue(u2.email == 'john@ex.com')


if __name__ == '__main__':
    unittest.main()
