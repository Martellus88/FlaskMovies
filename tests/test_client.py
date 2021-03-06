import unittest
from app import create_app, db
from app.models import User


class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_registration_and_login(self):
        # Registration
        response = self.client.post('/auth/register', data={
            'email': 'bob@ex.com',
            'username': 'bob',
            'password': 'psw',
            'password2': 'psw'
        })
        self.assertEqual(response.status_code, 302)

        # Login
        response = self.client.post('/auth/login', data={
            'email': 'bob@ex.com',
            'password': 'psw'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('You have not confirmed your account yet' in response.get_data(as_text=True))

        # Send confirm token
        user = User.query.filter_by(email='bob@ex.com').first()
        token = user.generate_confirmation_token()
        response = self.client.get(f'/auth/confirm/{token}', follow_redirects=True)
        user.confirm_register_token(token)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('You have confirmed your account' in response.get_data(as_text=True))

        # Logout
        response = self.client.get('/auth/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('You have been logged out' in response.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()
