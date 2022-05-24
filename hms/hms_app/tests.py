# from rest_framework.test import APITestCase
# from rest_framework.authtoken.models import Token
# from rest_framework import status
# from django.urls import reverse
#
# from .models import User
#
#
# class RegisterTestCase(APITestCase):
#
#     def test_register(self):
#         data = {
#             "email": "Jenkins1@hms.com",
#             "password": "12345"
#         }
#         response = self.client.post(reverse('register_user_name'), data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#
# class LoginLogoutTestCase(APITestCase):
#
#     def setUp(self):
#         self.user = User.objects.create_user(email="Jenkins1@hms.com",
#                                                    password="12345")
#
#     def test_login(self):
#         data = {
#             "email": "test1@hms.com",
#             "password": "12345"
#         }
#         response = self.client.post(reverse('signin'), data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_logout(self):
#         self.token = Token.objects.get(user__email="test1@hms.com")
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
