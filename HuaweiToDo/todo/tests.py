from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate, APIRequestFactory
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
    url = reverse("create_todo")
    url_login = reverse("login")

    def setUp(self):
        self.username = "john"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.text = "deneme"
        response = self.client.post(self.url_login, {"username": self.username, "password": self.password}, follow=True)
        self.csrf = response.client.cookies['csrftoken']

    def test_create_todo_with_valid_data(self):
        response = self.client.post(self.url, {"text": "deneme"},
                                    headers={'X-CSRFToken': self.csrf})
        self.assertEqual(201, response.status_code)

    def test_create_todo_with_wrong_data(self):
        response = self.client.post(self.url, {"user": self.username},
                                    headers={'X-CSRFToken': self.csrf})
        self.assertEqual(400, response.status_code)
