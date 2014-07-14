from django.test import TestCase
from models import Question


class LoginTestCase(TestCase):
    def test_index(self):
        self.client.login(username='admin', password='admin')
        # self.assertEqual(self.client.post('/login/', {'username': 'admin',
        #                                               'password': 'admin'}).status_code, 200)


class LogoutTestCase(TestCase):
    def test_index(self):
        self.client.logout()


class NewQuestionTest(TestCase):
    def test_index(self):
        self.assertEqual(self.client.get('/new_question/').status_code, 200)
        self.assertEqual(self.client.post('/new_question/', {'user': 1,
                                                             'subject': 'some subject',
                                                             'body': 'some message'}).status_code, 302)


class QuestionTest(TestCase):
    def test_index(self):
        self.assertEqual(self.client.get('/').status_code, 200)
        self.assertEqual(self.client.get('/?question=1').status_code, 200)


class ResponseTest(TestCase):
    def test_index(self):
        self.assertEqual(self.client.post('/response/', {'question': 1,
                                                         'response': 'some response'}).status_code, 302)


class SignupTest(TestCase):
    def test_index(self):
        self.assertEqual(self.client.get('/signup/').status_code, 200)
        self.assertEqual(self.client.post('/signup/', {'username': 'test',
                                                       'email': 'test@test.com',
                                                       'password1': 'pass',
                                                       'password2': 'pass'}).status_code, 302)


class ActivationView(TestCase):
    def test_index(self):
        self.assertEqual(self.client.get('/activation/?account=YWRtaW5Ac3RhY2tvdmVyZmxvdy5jb20=').status_code, 200)


class RestorePasswordTest(TestCase):
    def test_index(self):
        self.assertEqual(self.client.get('/restore_password/').status_code, 200)
        self.assertEqual(self.client.post('/restore_password', {'email': 'admin@stackoverflow.com'}).status_code, 301)

