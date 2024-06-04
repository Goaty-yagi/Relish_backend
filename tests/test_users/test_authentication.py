from django.contrib.auth import get_user_model
from django.test.client import RequestFactory
from django.test import TestCase
from rest_framework_simplejwt.tokens import AccessToken
from users.authentication import CustomJWTAuthentication

class CustomJWTAuthenticationTestCase(TestCase):
    def setUp(self):
        self.authentication = CustomJWTAuthentication()
        self.factory = RequestFactory()

    def test_authenticate_success(self):
        # Create a user for testing
        CustomUser = get_user_model()
        user = CustomUser.objects.create_user(username='testuser', email='test@example.com', password='password')

        # Create a valid access token for the user
        token = AccessToken.for_user(user)

        # Create a mock request with the token in the header
        request = self.factory.get('/')
        request.META['HTTP_AUTHORIZATION'] = f'Bearer {str(token)}'

        # Authenticate the request
        authenticated_user, authenticated_token = self.authentication.authenticate(request)

        # Verify that authentication is successful
        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user.UID, str(user.UID))
        self.assertEqual(str(authenticated_token), str(token))

    def test_authenticate_with_wrong_cookies(self):
        # Create a user for testing
        CustomUser = get_user_model()
        user = CustomUser.objects.create_user(username='testuser', email='test@example.com', password='password')

        # Create a valid access token for the user
        token = AccessToken.for_user(user)
        fake_cookie = 'fake_cookies'

        # Create a mock request with the token in the header
        request = self.factory.get('/')
        request.META['HTTP_AUTHORIZATION'] = f'Bearer {fake_cookie}'

        # Authenticate the request
        return_value = self.authentication.authenticate(request)

        # Verify that authentication is successful
        self.assertIsNone(return_value)

    def test_authenticate_without_cookie(self):
        # Create a request without a cookie
        request = self.factory.get('/')

        # Authenticate the request
        return_value = self.authentication.authenticate(request)

        # Assert that authentication fails and returns None for both user and token
        self.assertIsNone(return_value)

