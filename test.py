import os
import app
import dbsetup
import unittest
import tempfile
import json
from pymongo import MongoClient
from seed_data import ls_cities, ls_babysitters, ls_users

"""
SETUP TESTDB
"""
def initTestDB():
    testurl = "mongodb://testuser:password@ds149278.mlab.com:49278/babytest"
    # mongodb://<dbuser>:<dbpassword>@ds149278.mlab.com:49278/babytest
    testclient = MongoClient(testurl) 
    return testclient['babytest']

def setupTestDB():
  handle = initTestDB()

  # clear db of seed data
  for city in ls_cities: 
    handle['city'].delete_many({'city': city['city']})
  for sitter in ls_babysitters: 
    handle['babysitter'].delete_many({'host': sitter['host']})
  for user in ls_users:
    handle['user'].delete_many({'username': user['username']})

  # seed default city data
  handle['city'].insert(ls_cities)

  # seed default babysitter data
  handle['babysitter'].insert(ls_babysitters)
  #add to the host list for each city
  for item in ls_babysitters:
    handle['city'].update({'city': item['city']}, {'$push': {'hoster': item}})

  # seed default user data
  handle['user'].insert(ls_users)

  return handle

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        # self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        # app.app.secret_key = app.urandom(24) # secret key for session
        self.app = app.app.test_client()
        self.handle = setupTestDB()
        self.USERS = self.handle['user'].find()
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
        res = self.login('imran', 'password')
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

    # def test_login_should_create_session_token(self):
    #     """
    #         Given correct username and password, should 
    #         create new session_token for user
    #         respond with session_token and user
    #     """
    #     with app.app.test_client() as c:

    #         username = 'imran'
    #         password = 'password'
    #         login_res = c.post('/api/login', 
    #             content_type='application/json',
    #             data=json.dumps(dict(
    #                 username=username,
    #                 password=password
    #         )))

    #         res_data = json.loads(login_res.data)

    #         assert login_res.status_code == 200
    #         assert res_data['session_token'] != None
    #         assert res_data['user']['username'] in self.USERS 

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

    def test_review_should_respond_success_to_valid_request(self):
        """
            valid request: 
                username: existing parent
                sitter_usrname: existing babysitter
                review: not empty
        """
        with app.app.test_client() as c:
            valid_sitter_usrname = "imran"
            valid_username = "parent1"
            valid_review = "some review"

            res = c.post('/api/babysitter/%s/review'%valid_sitter_usrname, 
                data=json.dumps(dict(
                    username=valid_username,
                    review=valid_review)),
                content_type="application/json")

            assert res.status_code == 200

    def test_review_should_respond_fail_to_invalid_request(self):
        """
            invalid requests:
                username: empty, non existing parent
                sitter_usrname: empty, non existing sitter
                review: empty
        """
        with app.app.test_client() as c:
            non_existing_sitter_usrname = "nonexistingusername"
            existing_username = "parent1"
            valid_review = "Some valid review"

            res = c.post('/api/babysitter/%s/review'%non_existing_sitter_usrname, 
                data=json.dumps(dict(
                    username=existing_username,
                    review=valid_review)),
                content_type="application/json")

            assert res.status_code == 400

        with app.app.test_client() as c:
            existing_sitter_usrname = "imran"
            non_existing_username = "nonexistingparent"
            valid_review = "Some valid review"

            res = c.post('/api/babysitter/%s/review'%existing_sitter_usrname, 
                data=json.dumps(dict(
                    username=non_existing_username,
                    review=valid_review)),
                content_type="application/json")

            assert res.status_code == 400

        with app.app.test_client() as c:
            existing_sitter_usrname = "imran"
            existing_username = "parent1"
            invalid_review = ""

            res = c.post('/api/babysitter/%s/review'%existing_sitter_usrname, 
                data=json.dumps(dict(
                    username=existing_username,
                    review=invalid_review)),
                content_type="application/json")

            assert res.status_code == 400

if __name__ == '__main__':
    unittest.main()