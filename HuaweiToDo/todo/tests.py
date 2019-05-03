from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate, APIRequestFactory, APIClient
from rest_framework.utils import json

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

    def prepare_csrf_token(self, username, password):
        self.client.logout()
        response = self.client.post(self.url_login, {"username": username, "password": password},
                                    follow=True)
        self.csrf = response.client.cookies['csrftoken']

    def setUp(self):
        self.client = APIClient()
        self.username_true = "user1"
        self.email_true = "user1@me.com"
        self.password_true = "pass"
        self.user_true = User.objects.create_user(self.username_true, self.email_true, self.password_true)

        self.username_wrong = "user2"
        self.email_wrong = "user2@me.com"
        self.password_wrong = "pass"
        self.user_wrong = User.objects.create_user(self.username_wrong, self.email_wrong, self.password_wrong)
        self.text = "deneme"

        self.todo = Todo.objects.create(user=self.username_true, text="deneme")

    def test_create_todo_with_valid_data(self):
        self.prepare_csrf_token(self.username_true, self.password_true)
        response = self.client.post(self.url_create, {"text": "deneme"},
                                    headers={'X-CSRFToken': self.csrf})

        self.assertEqual(201, response.status_code)

    def test_create_todo_with_wrong_data(self):
        self.prepare_csrf_token(self.username_true, self.password_true)
        response = self.client.post(self.url_create, {"user": self.username_true},
                                    headers={'X-CSRFToken': self.csrf})
        self.assertEqual(400, response.status_code)

    def test_change_todo_status_with_true_user(self):
        self.prepare_csrf_token(self.username_true, self.password_true)
        todo = Todo.objects.all().get(user=self.username_true)
        current_status = todo.is_completed
        response = self.client.get(self.url_change_status+"?id={}".format(todo.id))
        self.assertEqual(200, response.status_code)
        self.assertNotEqual(current_status, response.data["is_completed"])

    def test_change_todo_status_with_wrong_user(self):
        self.prepare_csrf_token(self.username_wrong, self.password_wrong)
        todo = Todo.objects.all().get(user=self.username_true)
        response = self.client.get(self.url_change_status+"?id={}".format(todo.id))
        self.assertEqual(400, response.status_code)

    def test_delete_todo_with_true_user(self):
        self.prepare_csrf_token(self.username_true, self.password_true)
        todo = Todo.objects.all().get(user=self.username_true)
        response = self.client.get(self.url_delete + "?id={}".format(todo.id))
        self.assertEqual(200, response.status_code)

    def test_delete_todo_with_wrong_user(self):
        self.prepare_csrf_token(self.username_wrong, self.password_wrong)
        todo = Todo.objects.all().get(user=self.username_true)
        response = self.client.get(self.url_delete + "?id={}".format(todo.id))
        self.assertEqual(400, response.status_code)

    def test_get_static_with_authenticated(self):
        self.prepare_csrf_token(self.username_true, self.password_wrong)
        todo_completed_count = Todo.objects.filter(is_completed=True).count()
        todo_not_completed_count = Todo.objects.filter(is_completed=False).count()
        response = self.client.get(self.url_get_statics)

        #First item in response.data is the  number of completed item
        #Second item in response.data is the  number of completed item
        self.assertEqual(todo_completed_count, response.data[0]['Count'])
        self.assertEqual(todo_not_completed_count, response.data[1]['Count'])
        self.assertEqual(200, response.status_code)

    def test_get_static_without_authenticated(self):
        response = self.client.get(self.url_get_statics, follow=True)

        #response.redirect_chain[0] is first adress of redirected url tuple
        #First item in tuple contains the url, second item contains status code
        self.assertTrue(response.redirect_chain[0][0].startswith('/accounts/login/'))

