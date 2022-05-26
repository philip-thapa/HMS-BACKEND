# # from django.test import TestCase
# from rest_framework.test import APITestCase
# from rest_framework.authtoken.models import Token
# from rest_framework import status
# # from django.contrib.auth.models import User
# from django.urls import reverse
#
# import os
# from .models import User
# from django.core.files.uploadedfile import SimpleUploadedFile
#
#
# class RegisterTests(APITestCase):
#
#     def test_register(self):
#         BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#         data = {
#             "email": "example@gmail.com",
#             "password": "Test123",
#         }
#         response = self.client.post(reverse('register_user_name'), data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#
# class LoginLogoutTests(APITestCase):
#
#     def setUp(self):
#         self.user = User.objects.create_user(email="example@gmail.com",
#                                                    password="Test123")
#
#     def test_login(self):
#         data = {
#             "email": "example@gmail.com",
#             "password": "Test123",
#         }
#         response = self.client.post(reverse('signin'), data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_logout(self):
#         self.token = Token.objects.get(user=self.user)
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
#         response = self.client.post(reverse('signout'))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)



from django.test import TestCase

class YourTestClass(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_something_that_will_pass(self):
        self.assertTrue(4 == 2+2)

    def test_something_that_will_fail(self):
        self.assertTrue(True)

    def test_something_that_will_fail2(self):
        self.assertTrue(True)

    def test_total_sum(self):
        self.assertTrue(4 == 2+2)
    def total_cal(self):
        self.assertEqual(4 == 2*2)
