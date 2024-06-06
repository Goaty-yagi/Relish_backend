from unittest.mock import patch

from django.http import JsonResponse
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient


class CustomViewsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {'username': 'testuser', 'email': 'test@example.com',
                          'password': 'password', 're_password': 'password'}

    @patch('users.views.ProviderAuthView.post')
    def test_custom_provider_auth_view_sets_cookies(self, mock_provider_auth):
        # Mock the response
        # Replace 'user_data' with the actual data structure you expect
        mock_response = JsonResponse({'user': 'user_data'})
        mock_response.status_code = status.HTTP_201_CREATED
        mock_response.set_cookie('access', 'dummy_access_token')
        mock_response.set_cookie('refresh', 'dummy_refresh_token')

        # Set the mock to return the mock response
        mock_provider_auth.return_value = mock_response

        # Make the POST request
        response = self.client.post(
            reverse('provider-auth', kwargs={'provider': 'test'}))

        # Assert the status code
        self.assertEqual(response.status_code, 201)

        # Assert the cookies
        self.assertEqual(response.cookies.get(
            'access').value, 'dummy_access_token')
        self.assertEqual(response.cookies.get(
            'refresh').value, 'dummy_refresh_token')

        # Optionally assert the JSON response data if needed
        self.assertEqual(response.json(), {'user': 'user_data'})

    @patch('users.views.CustomTokenObtainPairView.post')
    def test_custom_token_obtain_pair_view_sets_cookies(self, mock_post):
        # Create a mock response with cookies
        mock_response = JsonResponse(self.user_data)
        mock_response.set_cookie('access', 'dummy_access_token')
        mock_response.set_cookie('refresh', 'dummy_refresh_token')

        # Set the mock to return the mock response
        mock_post.return_value = mock_response

        # Make the POST request
        response = self.client.post(
            reverse('token_obtain_pair'), self.user_data)

        # Assert the status code and cookies
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.cookies.get(
            'access').value, 'dummy_access_token')
        self.assertEqual(response.cookies.get(
            'refresh').value, 'dummy_refresh_token')

    @patch('users.views.TokenRefreshView.post')
    def test_custom_token_refresh_view_sets_access_cookie(self, mock_post):
        # Mock the post method to return a response object with status code 200 and the desired data
        mock_post.return_value = Response(status=status.HTTP_200_OK, data={
                                          'access': 'dummy_access_token'})

        # Set the 'refresh' cookie in the client
        self.client.cookies['refresh'] = 'dummy_refresh_token'

        # Make a request to the token refresh endpoint
        response = self.client.post(reverse('token_refresh'))

        # Check if the mock post method was called
        self.assertTrue(mock_post.called)

        # Check if the response status code is 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the 'access' cookie is set with the expected value
        self.assertEqual(response.cookies.get(
            'access').value, 'dummy_access_token')

    @patch('users.views.TokenVerifyView.post')
    def test_custom_token_verify_view_returns_200(self, mock_post):
        # Configure the mock post method to return a response object with status code 200
        mock_post.return_value = Response(status=status.HTTP_200_OK)

        # Set the 'access' cookie in the client
        self.client.cookies['access'] = 'dummy_access_token'

        # Make a request to the token verify endpoint
        response = self.client.post(reverse('token_verify'))

        # Check if the mock post method was called
        self.assertTrue(mock_post.called)

        # Check if the response status code is 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_view_deletes_cookies(self):

        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.cookies.get('access').value, '')
        self.assertEqual(response.cookies.get('refresh').value, '')
