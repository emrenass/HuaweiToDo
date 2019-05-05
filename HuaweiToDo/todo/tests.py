from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient

from .models import Todo



class UserLoginAPIViewTestCase(APITestCase):
    url = reverse("login")

    def setUp(self):
        self.username = "john"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(self.username, self.email, self.password)

    def test_authentication_without_password(self):
        response = self.client.post(self.url, {"username": "snowman"}, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_authentication_with_wrong_password(self):
        response = self.client.post(self.url, {"username": self.username, "password": "I_know"}, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_authentication_with_valid_data(self):
        response = self.client.post(self.url, {"username": self.username, "password": self.password}, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

class TodoAPIViewTestCase(APITestCase):
    url_create = reverse("create_todo")
    url_login = reverse("login")
    url_change_status = reverse("change_status")
    url_logout = reverse("logout")
    url_delete = reverse("delete")
    url_get_statics = reverse("get_statics")
    url_export = reverse("export")

    def prepare_csrf_token(self, username, password):
        self.client.logout()
        response = self.client.post(self.url_login, {"username": username, "password": password},
                                    follow=True)
        self.csrf = response.client.cookies['csrftoken']

    def setUp(self):
        self.client = APIClient()
        self.user1_username = "user1"
        self.user1_email = "user1@me.com"
        self.user1_password = "pass"
        self.user1 = User.objects.create_user(self.user1_username, self.user1_email, self.user1_password)

        self.user2_username = "user2"
        self.user2_email = "user2@me.com"
        self.user2_password = "pass"
        self.user2 = User.objects.create_user(self.user2_username, self.user2_email, self.user2_password)

        self.text = "deneme"
        self.wrong_password ="wrong_password_for_authentication"

        self.todo = Todo.objects.create(user=self.user1_username, text="deneme")

    def test_create_todo_with_valid_data(self):
        self.prepare_csrf_token(self.user1_username, self.user1_password)
        response = self.client.post(self.url_create, {"text": "deneme"},
                                    headers={'X-CSRFToken': self.csrf})

        self.assertEqual(201, response.status_code)

    def test_create_todo_with_wrong_data(self):
        self.prepare_csrf_token(self.user1_username, self.user1_password)
        response = self.client.post(self.url_create, {"user": self.user1_username},
                                    headers={'X-CSRFToken': self.csrf})
        self.assertEqual(400, response.status_code)

    def test_change_todo_status_with_true_user(self):
        self.prepare_csrf_token(self.user1_username, self.user1_password)
        todo = Todo.objects.all().get(user=self.user1_username)
        current_status = todo.is_completed
        response = self.client.get(self.url_change_status+"?id={}".format(todo.id))
        self.assertEqual(200, response.status_code)
        self.assertNotEqual(current_status, response.data["is_completed"])

    def test_change_todo_status_with_wrong_user(self):
        self.prepare_csrf_token(self.user2_username, self.user2_password)
        todo = Todo.objects.all().get(user=self.user1_username)
        response = self.client.get(self.url_change_status+"?id={}".format(todo.id))
        self.assertEqual(400, response.status_code)

    def test_delete_todo_with_true_user(self):
        self.prepare_csrf_token(self.user1_username, self.user1_password)
        todo = Todo.objects.all().get(user=self.user1_username)
        response = self.client.get(self.url_delete + "?id={}".format(todo.id))
        self.assertEqual(200, response.status_code)

    def test_delete_todo_with_wrong_user(self):
        self.prepare_csrf_token(self.user2_username, self.user2_password)
        todo = Todo.objects.all().get(user=self.user1_username)
        response = self.client.get(self.url_delete + "?id={}".format(todo.id))
        self.assertEqual(400, response.status_code)

    def test_get_static_with_authenticated(self):
        self.prepare_csrf_token(self.user1_username, self.user1_password)
        todo_completed_count = Todo.objects.filter(is_completed=True).count()
        todo_not_completed_count = Todo.objects.filter(is_completed=False).count()
        response = self.client.get(self.url_get_statics)

        #First item in response.data is the  number of completed item
        #Second item in response.data is the  number of completed item
        self.assertEqual(todo_completed_count, response.data[0]['Count'])
        self.assertEqual(todo_not_completed_count, response.data[1]['Count'])
        self.assertEqual(200, response.status_code)

    def test_get_static_without_authenticated(self):
        self.prepare_csrf_token(self.user1_username, "deneme")
        response = self.client.get(self.url_get_statics, follow=True)

        #response.redirect_chain[0] is first adress of redirected url tuple
        #First item in tuple contains the url, second item contains status code
        self.assertTrue(response.redirect_chain[0][0].startswith('/accounts/login/'))

    def test_export_with_authenticated(self):
        self.prepare_csrf_token(self.user1_username, self.user1_password)
        response = self.client.get(self.url_export, follow=True)
        self.assertEquals(
            response.get('Content-Disposition'),
            "attachment; filename=todo.csv"
        )

    def test_export_without_authenticated(self):
        self.prepare_csrf_token(self.user1_username, self.wrong_password)
        response = self.client.get(self.url_export, follow=True)
        self.assertTrue(response.redirect_chain[0][0].startswith('/accounts/login/'))

