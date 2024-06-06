from typing import Optional, Tuple

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from rest_framework.request import Request
from rest_framework_simplejwt.tokens import AccessToken, UntypedToken

from users.authentication import CustomJWTAuthentication


class CustomJWTAuthenticationTestCase(TestCase):
    def setUp(self) -> None:
        self.authentication: CustomJWTAuthentication = CustomJWTAuthentication()
        self.factory: RequestFactory = RequestFactory()

    def test_authenticate_success(self) -> None:
        # Create a user for testing
        CustomUser: User = get_user_model()
        user: User = CustomUser.objects.create_user(
            username='testuser', email='test@example.com', password='password')

        # Create a valid access token for the user
        token: AccessToken = AccessToken.for_user(user)

        # Create a mock request with the token in the header
        request: Request = self.factory.get('/')
        request.META['HTTP_AUTHORIZATION'] = f'Bearer {str(token)}'

        # Authenticate the request
        auth_result: Optional[Tuple[User, UntypedToken]] = self.authentication.authenticate(request)

        # Check if authentication was successful
        if auth_result is not None:
            authenticated_user, authenticated_token = auth_result
            # Verify that authentication is successful
            self.assertIsNotNone(authenticated_user)
            self.assertEqual(authenticated_user.UID, str(user.UID))
            self.assertEqual(str(authenticated_token), str(token))
        else:
            # Handle authentication failure
            self.fail("Authentication failed")

    def test_authenticate_with_wrong_cookies(self) -> None:
        # Create a user for testing
        CustomUser: User = get_user_model()
        user: User = CustomUser.objects.create_user(
            username='testuser', email='test@example.com', password='password')

        # Create a valid access token for the user
        token: AccessToken = AccessToken.for_user(user)
        fake_cookie: str = 'fake_cookies'

        # Create a mock request with the token in the header
        request: Request = self.factory.get('/')
        request.META['HTTP_AUTHORIZATION'] = f'Bearer {fake_cookie}'

        # Authenticate the request
        return_value: Optional[
            Tuple[User, UntypedToken]] = self.authentication.authenticate(request)

        # Verify that authentication is successful
        self.assertIsNone(return_value)

    def test_authenticate_without_cookie(self) -> None:
        # Create a request without a cookie
        request: Request = self.factory.get('/')

        # Authenticate the request
        return_value: Optional[
            Tuple[User, UntypedToken]] = self.authentication.authenticate(request)

        # Assert that authentication fails and returns None for both user and token
        self.assertIsNone(return_value)
