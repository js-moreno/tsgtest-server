"""Auth tests"""

# Django
from django.urls import reverse
from rest_framework import status
from django.utils.translation import gettext as _

# Django Rest Framework
from rest_framework.test import APITestCase

# Oauth2
from oauth2_provider.models import Application, AccessToken

# Accounts
from apps.accounts.models import User

# Utils
import json
from urllib.parse import urlencode
from django.utils.timezone import now, timedelta


class AuthTests(APITestCase):
    """Authentication test case"""

    def setUp(self):
        """Test case setup"""
        self.user = User.objects.create_user(email="user@example.com", password="s3cur3~p4ssw0rd")

        self.application = Application(
            name="Test Application",
            redirect_uris="http://localhost",
            user=self.user,
            client_type="public",
            authorization_grant_type="password",
            algorithm="RS256",
        )
        self.application.save()

        self.token = AccessToken.objects.create(
            user=self.user,
            token="R4ND0MT0K3N",
            application=self.application,
            expires=now() + timedelta(days=365),
            scope="openid read write",
        )

    def test_token(self):
        """
        Check access token generation
        """
        url = reverse("oauth2_provider:token")
        data = urlencode(
            {
                "grant_type": "password",
                "client_id": self.application.client_id,
                "username": self.user.email,
                "password": "s3cur3~p4ssw0rd",
                "scope": "openid read write",
            }
        )
        response = self.client.post(url, data, content_type="application/x-www-form-urlencoded")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = json.loads(response.content)["access_token"]

        self.assertTrue(
            AccessToken.objects.filter(
                token=token, user=self.user, application=self.application
            ).exists()
        )

        url_protected = reverse("oauth2_provider:user-info")

        # Success with token
        auth = "Bearer {0}".format(json.loads(response.content)["access_token"])
        response_authenticated = self.client.get(url_protected, HTTP_AUTHORIZATION=auth)
        self.assertEqual(response_authenticated.status_code, status.HTTP_200_OK)

        # Failure without token
        response_unauthenticated = self.client.get(url_protected)
        self.assertEqual(response_unauthenticated.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_userInfo(self):
        """
        Check user information
        """
        url = reverse("oauth2_provider:user-info")
        bearer = "Bearer {0}".format(self.token.token)
        response = self.client.get(url, HTTP_AUTHORIZATION=bearer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)["sub"], str(self.user.id))
        self.assertEqual(json.loads(response.content)["first_name"], self.user.first_name)
        self.assertEqual(json.loads(response.content)["is_superuser"], self.user.is_superuser)

    def test_revokeToken(self):
        """
        Check access token revocation
        """
        url = reverse("oauth2_provider:revoke-token")
        data = urlencode(
            {
                "client_id": self.application.client_id,
                "token": self.token.token,
            }
        )
        bearer = "Bearer {0}".format(self.token.token)

        response = self.client.post(
            url, data, content_type="application/x-www-form-urlencoded", HTTP_AUTHORIZATION=bearer
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertFalse(
            AccessToken.objects.filter(
                token=self.token.token, user=self.user, application=self.application
            ).exists()
        )