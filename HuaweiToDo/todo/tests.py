from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
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
        #self.assertEqual(200, response.status_code)
        self.assertTrue(response.context['user'].is_authenticated)

