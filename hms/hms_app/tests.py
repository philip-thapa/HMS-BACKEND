from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
# from django.contrib.auth.models import User
from django.urls import reverse


# Create your tests here.
from .models import User


class RegisterTestCase(APITestCase):

    def test_register(self):
        data = {
            "email": "Jenkins1@hms.com",
            "password": "12345"
        }
        response = self.client.post(reverse('ek/register_user_name'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginLogoutTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="Jenkins1@hms.com",
                                                   password="12345")

    def test_login(self):
        data = {
            "email": "Jenkins1@hms.com",
            "password": "12345"
        }
        response = self.client.post(reverse('ek/login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        self.token = Token.objects.get(user__email="Jenkins1@hms.com")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('ek/logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)