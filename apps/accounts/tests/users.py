"""User tests"""

# Django
from django.db.models import Q
from django.urls import reverse
from rest_framework import status
from django.utils.translation import gettext as _

# Django Rest Framework
from rest_framework.test import APITestCase

# Accounts
from apps.accounts.models import User

# Factory boy
import factory

# Utils
import json


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("company_email")
    phone = factory.Faker("phone_number")
    address = factory.Faker("address")


class UsersTests(APITestCase):
    """Users test case"""

    def setUp(self):
        """Test case setup"""
        UserFactory.create_batch(5)

    def test_createUsers(self):
        """
        Check user registration by anonymous
        """
        url = reverse("users-list")
        input = {
            "data": {
                "type": "users",
                "attributes": {
                    "first_name": factory.Faker("first_name").generate(),
                    "last_name": factory.Faker("last_name").generate(),
                    "email": factory.Faker("email").generate(),
                    "phone": factory.Faker("phone_number").generate(),
                    "address": factory.Faker("address").generate(),
                    "password": factory.Faker("password").generate(),
                },
            }
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(url, json.dumps(input), content_type="application/vnd.api+json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = json.loads(response.content)["data"]
        self.assertEqual(data["type"], "users")
        for key, value in input["data"]["attributes"].items():
            if key != "password":
                self.assertEqual(data["attributes"][key], value)
        self.assertFalse("password" in data["attributes"])  # Sensitive data

    def test_listUsers(self):
        """
        Check user list
        """
        url = reverse("users-list")

        # Super user
        user = User.objects.create_user(email="superuser@example.com", is_superuser=True)
        self.client.force_authenticate(user=user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotContains(response, "password")  # Sensitive data
        self.assertEqual(
            len(json.loads(response.content)["data"]),
            User.objects.all().count(),
        )

        # Standard user
        user = User.objects.create_user(email="standarduser@example.com")
        self.client.force_authenticate(user=user)
        response_trucated = self.client.get(url)
        self.assertEqual(response_trucated.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response_trucated.content)["data"]), 1)
        self.assertNotContains(response_trucated, "password")  # Sensitive data

        # Anonymous user
        self.client.force_authenticate(user=None)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieveUsers(self):
        """
        Check user retrieve
        """
        # Super user
        ## Retrieve another user
        user1 = User.objects.create_user(email="superuser@example.com", is_superuser=True)
        self.client.force_authenticate(user=user1)
        user2 = User.objects.filter(~Q(pk=user1.pk)).order_by("?").first()
        url = reverse("users-detail", kwargs={"pk": user2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)["data"]["type"], "users")
        self.assertEqual(json.loads(response.content)["data"]["id"], str(user2.id))
        self.assertNotContains(response, "password")  # Sensitive data

        # Standard user
        user1 = User.objects.create_user(email="standarduser1@example.com")
        user2 = User.objects.create_user(email="standarduser2@example.com")
        self.client.force_authenticate(user=user1)
        ## Retrieve another user
        url_fail = reverse("users-detail", kwargs={"pk": user2.id})
        response_fail = self.client.get(url_fail)
        self.assertEqual(response_fail.status_code, status.HTTP_404_NOT_FOUND)
        ## Retrieve current user
        url = reverse("users-detail", kwargs={"pk": user1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)["data"]["type"], "users")
        self.assertEqual(json.loads(response.content)["data"]["id"], str(user1.id))
        self.assertNotContains(response, "password")  # Sensitive data

        # Anonymous user
        ## Retrieve any user
        self.client.force_authenticate(user=None)
        user = User.objects.order_by("?").first()
        url = reverse("users-detail", kwargs={"pk": user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_deleteUsers(self):
        """
        Check user deletion
        """
        # Super user
        ## Delete another user
        user1 = User.objects.create_user(email="superuser@example.com", is_superuser=True)
        self.client.force_authenticate(user=user1)
        user2 = User.objects.filter(~Q(pk=user1.pk)).order_by("?").first()
        url = reverse("users-detail", kwargs={"pk": user2.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=user2.id).exists())

        # Standard user
        user1 = User.objects.create_user(email="standarduser1@example.com")
        user2 = User.objects.create_user(email="standarduser2@example.com")
        self.client.force_authenticate(user=user1)
        ## Delete another user
        url_fail = reverse("users-detail", kwargs={"pk": user2.id})
        response_fail = self.client.delete(url_fail)
        self.assertEqual(response_fail.status_code, status.HTTP_404_NOT_FOUND)
        ## Delete current user
        url = reverse("users-detail", kwargs={"pk": user1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=user1.id).exists())

        # Anonymous user
        ## Delete any user
        user = User.objects.order_by("?").first()
        url = reverse("users-detail", kwargs={"pk": user.id})
        self.client.force_authenticate(user=None)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
