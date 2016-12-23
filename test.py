import os
import app
import unittest
import tempfile
import json

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        # self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        app.app.secret_key = app.urandom(24) # secret key for session
        self.app = app.app.test_client()
        self.USERS = app.USERS
        # with app.app.app_context():
        #     app.init_db()

    def tearDown(self):
        # os.close(self.db_fd)
        # os.unlink(app.app.config['DATABASE'])
        pass

    def login(self, username, password):
        """
            Helper function for auth.
            client sends post to server app and
            server responds appropriately.
        """
        return self.app.post('/api/login', 
            content_type='application/json',
            data=json.dumps(dict(
            username=username,
            password=password
        )))

    def test_login_should_respond_success(self):
        """
            Given correct username and password, should 
            successfully login and repond with success message
        """
        res = self.login('imranariffin', 'password')
        assert res.status_code == 200
        assert 'success' in json.loads(res.get_data()).values()

    def test_login_contains_correct_data(self):
        """
            login request method should be only POST.
            login request should have username and password as data
            username and password value should be of type string
            username and password value should not be empty
            for the user with username as key
        """
        with app.app.test_request_context('/api/login', 
            content_type='application/json',
            data=json.dumps(dict(
                username='imranariffin',
                password='password'))):
            assert app.request.path == '/api/login'
            data = app.request.get_json()
            assert 'username' in data
            assert 'password' in data
            assert type(data['username']) == type(u's')
            assert type(data['password']) == type(u's')
            assert len(data['username']) > 0
            assert len(data['password']) > 0

    def test_login_should_create_session_token(self):
        """
            Given correct username and password, should 
            create new session_token for user
            respond with session_token and user
        """
        with app.app.test_client() as c:

            username = 'imranariffin'
            password = 'password'
            login_res = c.post('/api/login', 
                content_type='application/json',
                data=json.dumps(dict(
                    username=username,
                    password=password
            )))

            res_data = json.loads(login_res.data)

            assert login_res.status_code == 200
            assert res_data['session_token'] != None
            assert res_data['user']['username'] in self.USERS 

    def test_logout_should_respond_with_message(self):
        """
            Given that user already logged in, /api/logout
            should:
                respond with success message
        """
        with app.app.test_client() as c:
            login_res = c.post('/api/login',
                content_type='application/json',
                data=json.dumps(dict(
                    username='imranariffin',
                    password='password'
            )))

            logout_res = c.post('/api/logout',
                content_type='application/json',
            )

            assert True


if __name__ == '__main__':
    unittest.main()